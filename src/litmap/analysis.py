"""Bibliometric measures from a list of compact works: growth, influential works, journals,
authors, themes, keyword clusters, under-connected themes and the field's foundations."""

from __future__ import annotations

import re
from collections import Counter
from itertools import combinations

import networkx as nx
import pandas as pd


def full_years(works: list[dict], fetched_year: int) -> pd.Series:
    """Publications per year, without the current (incomplete) year and with empty years as 0."""
    years = [w["year"] for w in works if w.get("year") and w["year"] < fetched_year]
    if not years:
        return pd.Series(dtype=int)
    s = pd.Series(Counter(years)).sort_index()
    return s.reindex(range(s.index.min(), s.index.max() + 1), fill_value=0)


def growth(per_year: pd.Series, window: int = 5) -> dict:
    """Average output in the last window against the window ten years earlier."""
    y1 = int(per_year.index.max())
    recent = per_year.loc[y1 - window + 1 : y1].mean()
    past = per_year.loc[y1 - window - 9 : y1 - 10].mean()
    total = per_year.sum()
    return {
        "last_year": y1,
        "recent_avg": float(recent),
        "past_avg": float(past),
        "past_span": f"{y1 - window - 9}-{y1 - 10}",
        "recent_span": f"{y1 - window + 1}-{y1}",
        "share_recent": float(per_year.loc[y1 - window + 1 : y1].sum() / total) if total else 0.0,
    }


def dedupe(works: list[dict]) -> list[dict]:
    """OpenAlex sometimes holds one article twice (preprint and version of record, or two
    records of one DOI): keep the most cited record of each title."""
    best: dict[str, dict] = {}
    for w in works:
        key = re.sub(r"[^a-z0-9]", "", w["title"].lower())[:80] or w["id"]
        if key not in best or w["cited"] > best[key]["cited"]:
            best[key] = w
    return list(best.values())


def focus(works: list[dict], pattern: str) -> pd.DataFrame:
    """Works whose title or keywords match a pattern: a strand of the field to follow."""
    rx = re.compile(pattern, re.IGNORECASE)
    rows = [
        {
            "id": w["id"],
            "first_author": w["authors"][0] if w["authors"] else "",
            "year": w["year"],
            "title": w["title"],
            "journal": w["journal"],
            "cited": w["cited"],
        }
        for w in works
        if rx.search(w["title"]) or any(rx.search(k) for k in w["keywords"])
    ]
    df = pd.DataFrame(rows, columns=["id", "first_author", "year", "title", "journal", "cited"])
    return df.sort_values(["year", "cited"], ascending=False).reset_index(drop=True)


def strands(works: list[dict], patterns: dict[str, str]) -> pd.DataFrame:
    """Articles in each strand of a field (pattern on titles and keywords), largest first."""
    rows = [{"strand": k, "works": len(focus(works, p))} for k, p in patterns.items()]
    df = pd.DataFrame(rows, columns=["strand", "works"])
    df["share"] = df["works"] / max(len(works), 1)
    return df.sort_values("works", ascending=False).reset_index(drop=True)


def top_cited(works: list[dict], n: int = 10) -> pd.DataFrame:
    df = pd.DataFrame(works)
    df["first_author"] = df["authors"].map(lambda a: a[0] if a else "")
    cols = ["id", "first_author", "year", "title", "journal", "cited"]
    return df.sort_values("cited", ascending=False)[cols].head(n).reset_index(drop=True)


def rising(works: list[dict], fetched_year: int, years: int = 3, n: int = 8) -> pd.DataFrame:
    """Recent works with the most citations per year since publication."""
    df = pd.DataFrame(works)
    df = df[df["year"] >= fetched_year - years].copy()
    if df.empty:
        return df
    df["per_year"] = df["cited"] / (fetched_year - df["year"] + 1)
    df["first_author"] = df["authors"].map(lambda a: a[0] if a else "")
    cols = ["id", "first_author", "year", "title", "journal", "cited", "per_year"]
    return df.sort_values("per_year", ascending=False)[cols].head(n).reset_index(drop=True)


def counts(works: list[dict], key: str, n: int = 10) -> pd.DataFrame:
    c = Counter()
    for w in works:
        vals = w[key] if isinstance(w[key], list) else [w[key]]
        c.update(v for v in set(vals) if v)
    return pd.DataFrame(c.most_common(n), columns=[key.rstrip("s"), "works"])


def keyword_sets(works: list[dict], stop: list[str]) -> list[set[str]]:
    stop_l = {s.lower() for s in stop}
    return [{k for k in w["keywords"] if k not in stop_l} for w in works]


def themes(
    works: list[dict], stop: list[str], split_year: int, min_works: int = 5, n: int | None = None
) -> pd.DataFrame:
    """Change in each keyword's share of works, from before split_year to split_year onwards,
    largest rise first."""
    sets = keyword_sets(works, stop)
    early = [s for s, w in zip(sets, works, strict=True) if w["year"] and w["year"] < split_year]
    late = [s for s, w in zip(sets, works, strict=True) if w["year"] and w["year"] >= split_year]
    if not early or not late:
        return pd.DataFrame(columns=["keyword", "early", "late", "change", "works"])
    ce, cl = Counter(k for s in early for k in s), Counter(k for s in late for k in s)
    rows = []
    for k in set(ce) | set(cl):
        if ce[k] + cl[k] < min_works:
            continue
        e, lt = ce[k] / len(early), cl[k] / len(late)
        rows.append(
            {"keyword": k, "early": e, "late": lt, "change": lt - e, "works": ce[k] + cl[k]}
        )
    df = pd.DataFrame(rows, columns=["keyword", "early", "late", "change", "works"])
    df = df.sort_values("change", ascending=False)
    return (df.head(n) if n else df).reset_index(drop=True)


def cooccurrence(sets: list[set[str]], top: int = 40) -> tuple[Counter, Counter]:
    """Frequencies of the 'top' keywords and the number of works in which each pair appears."""
    freq = Counter(k for s in sets for k in s)
    keep = {k for k, _ in freq.most_common(top)}
    pairs = Counter()
    for s in sets:
        pairs.update(combinations(sorted(s & keep), 2))
    return Counter({k: freq[k] for k in keep}), pairs


def clusters(freq: Counter, pairs: Counter, min_pair: int = 2) -> list[list[str]]:
    """Keyword communities (greedy modularity on association strength), largest first."""
    g = nx.Graph()
    g.add_nodes_from(freq)
    for (a, b), c in pairs.items():
        if c >= min_pair:
            g.add_edge(a, b, weight=c / (freq[a] * freq[b]))
    if g.number_of_edges() == 0:
        return [sorted(freq, key=freq.get, reverse=True)]
    comms = nx.community.greedy_modularity_communities(g, weight="weight", resolution=1.0)
    out = [sorted(c, key=lambda k: -freq[k]) for c in comms]
    return sorted(out, key=lambda c: -sum(freq[k] for k in c))


def tokens(keyword: str) -> set[str]:
    """Content words of a keyword, with British and American spellings merged and cut to six
    letters, so that 'independence' and 'independent' count as the same word."""
    words = re.findall(r"[a-z0-9]+", keyword.lower().replace("labour", "labor"))
    return {w[:6] for w in words if w not in {"and", "of", "the", "in", "for", "to", "a"}}


# Keywords that describe the sample (a country, a market) rather than a theme; a gap between a
# theme and a country says where studies were done, not what is missing.
CONTEXT = re.compile(
    r"stock exchange|listed (companies|firms)|emerging (markets|economies)|developing countries|"
    r"\b(china|chinese|indonesia\w*|malaysia\w*|nigeria\w*|india\w*|pakistan\w*|vietnam\w*|"
    r"ghana\w*|kenya\w*|bangladesh\w*|jordan\w*|saudi|gcc|spain|spanish|italy|italian|"
    r"europe\w*|africa\w*|asia\w*|latin america\w*|united states|u\.s\.|uk)\b"
)


def gaps(freq: Counter, pairs: Counter, n_works: int, n: int = 6, top: int = 20) -> pd.DataFrame:
    """Under-connected themes: pairs of frequent keywords that appear together far less often
    than if they were independent (observed / expected co-occurrence, VOSviewer's association
    strength scaled by the number of works). A low ratio flags a possible research gap. Pairs
    that share a word (board composition, board structure) are alternative labels for one theme,
    not a gap, and are skipped."""
    common = [k for k, _ in freq.most_common() if not CONTEXT.search(k)][:top]
    rows = []
    for a, b in combinations(common, 2):
        expected = freq[a] * freq[b] / n_works
        if expected < 3 or tokens(a) & tokens(b):  # too rare to say anything
            continue
        observed = pairs.get(tuple(sorted((a, b))), 0)
        rows.append({"a": a, "b": b, "observed": observed, "expected": expected})
    df = pd.DataFrame(rows, columns=["a", "b", "observed", "expected"])
    if df.empty:
        return df
    df["ratio"] = df["observed"] / df["expected"]
    return df.sort_values(["ratio", "expected"], ascending=[True, False]).head(n)


def foundations_ids(works: list[dict], n: int = 40) -> list[str]:
    """The works most often cited by the field: its intellectual base."""
    c = Counter(r for w in works for r in set(w.get("refs", [])))
    return [k for k, _ in c.most_common(n)]


def foundations(works: list[dict], titles: list[dict], n: int = 10) -> pd.DataFrame:
    c = Counter(r for w in works for r in set(w.get("refs", [])))
    df = pd.DataFrame(titles)
    if df.empty:
        return df
    df["cited_here"] = df["id"].map(c).fillna(0).astype(int)
    df["share"] = df["cited_here"] / len(works)
    return df.sort_values("cited_here", ascending=False).head(n).reset_index(drop=True)
