"""Figures, topic pages, latest.json and the README's 'Latest reading' block, all computed from
the snapshots in data/raw. Runs in seconds and can be rerun after every download."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import networkx as nx
import pandas as pd

from . import analysis as an
from .figstyle import charts, picture

REPO = "github.com/IgnacioMendozaRojas/literature-map"
SOURCE = (
    f"Source: OpenAlex (CC0), journal articles matching the query in config/topics.yaml. {REPO}"
)


def short(text: str, n: int = 90) -> str:
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# --- figures ------------------------------------------------------------------------------------


def fig_trend(name: str, cfg: dict, per_year: pd.Series, g: dict, fig: Path) -> str:
    verb = "rose" if g["recent_avg"] >= g["past_avg"] else "fell"
    title = (
        f"{cfg['label']}: output {verb} from {g['past_avg']:.0f} to "
        f"{g['recent_avg']:.0f} articles a year"
    )
    sub = (
        f"Journal articles per year, {per_year.index.min()}-{per_year.index.max()}; "
        f"averages for {g['past_span']} and {g['recent_span']}"
    )
    x, y = list(per_year.index), list(per_year.values)
    for c in charts(title, sub, SOURCE):
        c.line(x, y, 0, "Articles", end_label=False)
        for yr, label in (cfg.get("events") or {}).items():
            if x[0] <= int(yr) <= x[-1]:
                c.event(int(yr), label)
        c.yaxis("Articles per year")
        c.ax.set_ylim(0, max(y) * 1.15)
        c.save(fig, f"{name}-trend")
    return title


def cluster_layout(g: nx.Graph, comms: list[list[str]]) -> dict:
    """Clusters on a circle, each laid out on its own, so the communities read as groups."""
    import math

    pos = {}
    for i, comm in enumerate(comms):
        angle = 2 * math.pi * i / len(comms) + math.pi / 4
        cx, cy = math.cos(angle), math.sin(angle)
        sub = nx.spring_layout(g.subgraph(comm), weight="weight", seed=7, scale=0.42)
        for k, (x, y) in sub.items():
            pos[k] = (cx + x, cy + y)
    return pos


def fig_map(name: str, cfg: dict, freq, pairs, comms: list[list[str]], fig: Path) -> str:
    """Keyword network with one colour per cluster; the clusters are named in a key on the
    right, and only each cluster's two most frequent keywords are labelled on the map."""
    import textwrap

    comms = [c for c in comms if len(c) >= 2][:6]
    title = f"{cfg['label']}: the literature splits into {len(comms)} clusters of themes"
    sub = (
        f"Co-occurrence of the {len(freq)} most frequent keywords; size = articles, "
        "links = articles that use both"
    )
    g = nx.Graph()
    g.add_nodes_from(k for c in comms for k in c)
    for (a, b), cnt in pairs.items():
        if cnt >= 2 and a in g and b in g:
            g.add_edge(a, b, weight=cnt / (freq[a] * freq[b]))
    pos = cluster_layout(g, comms)
    group = {k: i for i, c in enumerate(comms) for k in c}
    top = max(freq[k] for k in g)
    labelled = {k for c in comms for k in c[:2]}
    for c in charts(title, sub, SOURCE, size=(9, 5.6)):
        c.ax.grid(False)
        c.ax.set_xticks([])
        c.ax.set_yticks([])
        for side in ("left", "bottom"):
            c.ax.spines[side].set_visible(False)
        c.ax.set_position([0.03, 0.12, 0.6, 0.7])
        for a, b in g.edges():
            (x0, y0), (x1, y1) = pos[a], pos[b]
            c.ax.plot([x0, x1], [y0, y1], color=c.t["grid"], linewidth=0.5, alpha=0.7, zorder=1)
        for k, (x, y) in pos.items():
            c.ax.scatter(
                x, y, s=25 + 450 * freq[k] / top, color=c.color(group[k]), zorder=2, linewidths=0
            )
            if k in labelled:
                c.ax.annotate(
                    short(k, 28),
                    (x, y),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha="center",
                    fontsize=7.5,
                    color=c.t["text"],
                    zorder=3,
                )
        y = 0.8
        for i, comm in enumerate(comms):
            c.fig.text(0.665, y, "\u25cf", color=c.color(i), fontsize=12, va="top")
            words = textwrap.wrap(", ".join(comm[:5]), 38)
            c.fig.text(0.69, y - 0.004, "\n".join(words), color=c.t["text"], fontsize=8, va="top")
            y -= 0.035 * len(words) + 0.03
        c.save(fig, f"{name}-map")
    return title


def fig_themes(name: str, cfg: dict, th: pd.DataFrame, split: int, fig: Path) -> str:
    up = th[th["change"] > 0].head(6)
    down = th[th["change"] < 0].tail(4)
    rise = up["keyword"].head(2).tolist()
    if len(rise) == 2:
        title = f"{cfg['label']}: since {split}, the rising themes are {rise[0]} and {rise[1]}"
    else:
        title = f"{cfg['label']}: since {split}, the rising theme is {rise[0]}"
    sub = (
        f"Change in the share of articles that use each keyword, before {split} against since; "
        "the largest rises in colour, the largest falls in grey"
    )
    shown = pd.concat([up, down])
    labels = [short(k, 40) for k in shown["keyword"]]
    for c in charts(title, sub, SOURCE):
        c.hbars(
            labels,
            list(shown["change"] * 100),
            fmt="{:+.1f} pp",
            highlight={short(k, 40) for k in up["keyword"]},
            sort=False,
        )
        c.ax.axvline(0, color=c.t["muted"], linewidth=0.8)
        c.xlabel("Percentage points")
        c.fig.subplots_adjust(left=0.36, right=0.92)
        c.save(fig, f"{name}-themes")
    return title


# --- one topic ----------------------------------------------------------------------------------


def analyse(name: str, cfg: dict, snap: dict, fig: Path) -> dict:
    works = snap["works"]
    year = date.fromisoformat(snap["fetched"]).year
    per_year = an.full_years(works, year)
    g = an.growth(per_year)
    sets = an.keyword_sets(works, cfg.get("stop", []))
    freq, pairs = an.cooccurrence(sets, top=40)
    comms = an.clusters(freq, pairs)
    split = year - 5
    th = an.themes(works, cfg.get("stop", []), split)
    gp = an.gaps(freq, pairs, len(works))
    titles = {
        "trend": fig_trend(name, cfg, per_year, g, fig),
        "map": fig_map(name, cfg, freq, pairs, comms, fig),
        "themes": fig_themes(name, cfg, th, split, fig) if (th["change"] > 0).any() else "",
    }
    return {
        "name": name,
        "cfg": cfg,
        "snap": snap,
        "per_year": per_year,
        "growth": g,
        "clusters": comms,
        "themes": th,
        "gaps": gp,
        "split": split,
        "top_cited": an.top_cited(works),
        "rising": an.rising(works, year),
        "journals": an.counts(works, "journal"),
        "authors": an.counts(works, "authors"),
        "foundations": an.foundations(works, snap.get("foundations", [])),
        "new": [w for w in works if w["id"] in set(snap.get("new_ids", []))],
        "titles": titles,
    }


def table(df: pd.DataFrame, cols: dict) -> str:
    if df is None or df.empty:
        return "_None yet._"
    head = "| " + " | ".join(cols.values()) + " |\n|" + "---|" * len(cols) + "\n"
    rows = []
    for _, r in df.iterrows():
        cells = []
        for k in cols:
            v = r[k]
            if k == "title":
                v = f"[{short(str(v))}](https://openalex.org/{r['id']})"
            elif k in ("share", "change", "early", "late"):
                v = f"{v:.0%}" if k in ("share", "early", "late") else f"{v * 100:+.1f} pp"
            elif k in ("per_year", "expected"):
                v = f"{v:.1f}"
            cells.append(str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return head + "\n".join(rows)


def page(t: dict) -> str:
    """docs/topics/<name>.md: everything about one field, rebuilt on every run."""
    name, cfg, snap, g = t["name"], t["cfg"], t["snap"], t["growth"]
    fig = "../figures"
    clusters = "\n".join(
        f"{i + 1}. {', '.join(c[:8])}" for i, c in enumerate(t["clusters"]) if len(c) >= 2
    )
    bench = cfg.get("scopus_benchmark")
    bench_line = (
        f" The original review found {bench} articles in Scopus with a narrower query "
        "(articles with both terms in title, abstract or keywords)."
        if bench
        else ""
    )
    gaps = t["gaps"]
    gap_lines = (
        "\n".join(
            f"- **{r.a}** and **{r.b}**: {r.observed} articles together, "
            f"{r.expected:.0f} expected if unrelated"
            for r in gaps.itertuples()
        )
        or "_None at this threshold._"
    )
    new = pd.DataFrame(t["new"])
    if not new.empty:
        new["first_author"] = new["authors"].map(lambda a: a[0] if a else "")
    return f"""# {cfg["label"]}

*Rebuilt from OpenAlex on {snap["fetched"]}. Do not edit by hand: see
[`report.py`](../../src/litmap/report.py).*

**Query** (title and abstract, journal articles since {cfg.get("since", 1990)}):
`{" ".join(cfg["query"].split())}`

**Coverage.** {snap["count"]:,} articles; {g["share_recent"]:.0%} of them published in
{g["recent_span"]}.{bench_line}

{picture(f"{fig}/{name}-trend-light.png", t["titles"]["trend"])}

## Themes and clusters

Keyword communities found by modularity on the co-occurrence network (the method behind
VOSviewer's clustering), largest first:

{clusters}

{picture(f"{fig}/{name}-map-light.png", t["titles"]["map"])}

{picture(f"{fig}/{name}-themes-light.png", t["titles"]["themes"]) if t["titles"]["themes"] else ""}

## Under-connected themes

Pairs of frequent keywords that appear together far less often than chance would predict. They
are candidates for research gaps, to be read against the literature, not conclusions.

{gap_lines}

## Foundations: the works this field cites most

{
        table(
            t["foundations"],
            {
                "first_author": "First author",
                "year": "Year",
                "title": "Title",
                "cited_here": "Cited by articles here",
                "share": "Share",
            },
        )
    }

## Most cited articles

{
        table(
            t["top_cited"],
            {
                "first_author": "First author",
                "year": "Year",
                "title": "Title",
                "journal": "Journal",
                "cited": "Citations",
            },
        )
    }

## Rising: recent articles with the most citations per year

{
        table(
            t["rising"],
            {
                "first_author": "First author",
                "year": "Year",
                "title": "Title",
                "journal": "Journal",
                "per_year": "Citations a year",
            },
        )
    }

## Journals and authors

{table(t["journals"], {"journal": "Journal", "works": "Articles"})}

{table(t["authors"], {"author": "Author", "works": "Articles"})}

## New since the last update ({snap.get("previous_fetch") or "first run"})

{
        table(
            new,
            {
                "first_author": "First author",
                "year": "Year",
                "title": "Title",
                "journal": "Journal",
            },
        )
        if not new.empty
        else "_No new articles._"
    }
"""


# --- latest.json and README ---------------------------------------------------------------------


def latest(topics: list[dict], today: date) -> dict:
    metrics = []
    for t in topics:
        g, label = t["growth"], t["cfg"]["label"]
        metrics.append(
            {
                "id": f"{t['name']}_per_year",
                "label": f"{label}: articles a year",
                "value": round(g["recent_avg"], 1),
                "unit": "articles",
                "period": g["recent_span"],
                "previous": round(g["past_avg"], 1),
                "change": round(g["recent_avg"] - g["past_avg"], 1),
                "change_type": "absolute",
            }
        )
        metrics.append(
            {
                "id": f"{t['name']}_new",
                "label": f"{label}: new articles since the last update",
                "value": len(t["new"]),
                "unit": "articles",
                "period": t["snap"]["fetched"],
            }
        )
    return {
        "schema": 1,
        "id": "literature-map",
        "repo": "literature-map",
        "title": "Bibliometric maps of three research fields",
        "question": "How are these fields growing, what are their themes and where are the gaps?",
        "as_of": today.isoformat(),
        "frequency": "monthly",
        "updated": today.isoformat(),
        "source": "OpenAlex",
        "headline": headline(topics),
        "metrics": metrics,
    }


def headline(topics: list[dict]) -> str:
    fastest = max(topics, key=lambda t: t["growth"]["recent_avg"] / max(t["growth"]["past_avg"], 1))
    g = fastest["growth"]
    total = sum(len(t["new"]) for t in topics)
    new = f"{total} new articles since the last update" if total else "No new articles this month"
    return (
        f"{new}. The fastest-growing field is {fastest['cfg']['label']}: "
        f"{g['recent_avg']:.0f} articles a year in {g['recent_span']}, against "
        f"{g['past_avg']:.0f} in {g['past_span']}."
    )


def readme_block(topics: list[dict], today: date) -> str:
    rows = [
        "| Field | Articles | A year, recent | A year, ten years earlier | New | Under-connected |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for t in topics:
        g, gp = t["growth"], t["gaps"]
        gap = f"{gp.iloc[0]['a']} / {gp.iloc[0]['b']}" if not gp.empty else ""
        rows.append(
            f"| [{t['cfg']['label']}](docs/topics/{t['name']}.md) | {t['snap']['count']:,} | "
            f"{g['recent_avg']:.0f} ({g['recent_span']}) | {g['past_avg']:.0f} ({g['past_span']}) "
            f"| {len(t['new'])} | {gap} |"
        )
    return (
        f"**Latest reading: {today.isoformat()}.** {headline(topics)}"
        + "\n\n"
        + "\n".join(rows)
        + "\n\n*New: articles that were not in the previous monthly snapshot. Under-connected: the "
        + "pair of frequent themes that appear together least often relative to chance.*"
    )


def write_readme(block: str, path: Path) -> None:
    text = path.read_text()
    new = f"<!-- latest:start -->\n{block}\n<!-- latest:end -->"
    text = re.sub(r"<!-- latest:start -->.*?<!-- latest:end -->", new, text, flags=re.S)
    path.write_text(text)


def main(root: Path, topics_cfg: dict, today: date | None = None) -> list[dict]:
    from .openalex import load

    today = today or date.today()
    fig = root / "docs" / "figures"
    out = []
    for name, cfg in topics_cfg.items():
        snap = load(root / "data" / "raw" / f"{name}.json.gz")
        if not snap or not snap["works"]:
            print(f"::warning title={name}::no snapshot yet")
            continue
        t = analyse(name, cfg, snap, fig)
        pages = root / "docs" / "topics"
        pages.mkdir(parents=True, exist_ok=True)
        (pages / f"{name}.md").write_text(page(t))
        proc = root / "data" / "processed" / name
        proc.mkdir(parents=True, exist_ok=True)
        t["per_year"].rename("articles").to_csv(proc / "per_year.csv", index_label="year")
        for key in ("themes", "gaps", "top_cited", "rising", "foundations", "journals", "authors"):
            t[key].to_csv(proc / f"{key}.csv", index=False)
        for k, title in t["titles"].items():
            if title:
                print(f"::notice title={name} {k}::{title}")
        gp = t["gaps"]
        gl = "; ".join(f"{r.a} / {r.b} ({r.observed} vs {r.expected:.0f})" for r in gp.itertuples())
        print(f"::notice title={name} gaps::{gl}")
        cl = " | ".join(", ".join(c[:5]) for c in t["clusters"][:5])
        print(f"::notice title={name} clusters::{cl}")
        out.append(t)
    if out:
        doc = latest(out, today)
        (root / "latest.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        write_readme(readme_block(out, today), root / "README.md")
        print(f"::notice title=latest::{doc['headline']}")
    return out
