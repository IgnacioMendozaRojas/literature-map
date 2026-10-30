import random
from datetime import date

import pandas as pd
import pytest

from litmap import analysis as an
from litmap import openalex as oa
from litmap import report

RAW = {
    "id": "https://openalex.org/W1",
    "doi": "https://doi.org/10.1/abc",
    "display_name": "Trade  credit and\nSME survival",
    "publication_year": 2020,
    "cited_by_count": 12,
    "type": "article",
    "primary_location": {"source": {"display_name": "Small Business Economics"}},
    "authorships": [{"author": {"display_name": "A. Author"}}, {"author": {}}],
    "keywords": [{"display_name": "Trade Credit"}, {"display_name": "Liquidity"}],
    "primary_topic": {"field": {"display_name": "Economics"}},
    "referenced_works": ["https://openalex.org/W9"],
}


def test_compact_keeps_short_ids_and_clean_text():
    w = oa.compact(RAW)
    assert w["id"] == "W1" and w["doi"] == "10.1/abc"
    assert w["title"] == "Trade credit and SME survival"
    assert w["authors"] == ["A. Author"] and w["keywords"] == ["trade credit", "liquidity"]
    assert w["refs"] == ["W9"] and w["journal"] == "Small Business Economics"


def test_compact_survives_missing_fields():
    w = oa.compact({"id": "https://openalex.org/W2"})
    assert w["id"] == "W2" and w["authors"] == [] and w["cited"] == 0


def test_filter_string_rejects_commas_and_collapses_spaces():
    f = oa.filter_string('"trade credit"\n  AND SME', 1990, 2026)
    assert f.startswith('title_and_abstract.search:"trade credit" AND SME,type:article')
    assert "publication_year:1990-2026" in f
    with pytest.raises(ValueError):
        oa.filter_string("a, b", 1990, 2026)


def synthetic(n=300, seed=1):
    """Two themes that rarely meet (risk vs supply chain) plus a theme that rises late."""
    rng = random.Random(seed)
    works = []
    for i in range(n):
        year = rng.randint(2000, 2025)
        if i % 2:
            kws = ["trade credit", "liquidity", "risk management", "bank credit"]
        else:
            kws = ["trade credit", "supply chain", "inventory", "working capital"]
        if year >= 2021 and rng.random() < 0.7:
            kws.append("fintech")
        works.append(
            {
                "id": f"W{i}",
                "doi": "",
                "title": f"Paper {i}",
                "year": year,
                "cited": rng.randint(0, 100),
                "journal": rng.choice(["J1", "J2", "J3"]),
                "authors": [rng.choice(["Ana", "Ben", "Cai"])],
                "keywords": kws,
                "field": "Economics",
                "refs": ["W900", "W901"] if i % 3 else ["W900"],
            }
        )
    return works


def test_full_years_drops_current_year_and_fills_gaps():
    works = [{"year": 2018}, {"year": 2020}, {"year": 2026}]
    s = an.full_years(works, 2026)
    assert list(s.index) == [2018, 2019, 2020] and list(s) == [1, 0, 1]


def test_growth_compares_windows_ten_years_apart():
    s = pd.Series(range(1, 27), index=range(2000, 2026))
    g = an.growth(s)
    assert g["recent_span"] == "2021-2025" and g["past_span"] == "2011-2015"
    assert g["recent_avg"] == 24 and g["past_avg"] == 14


def test_themes_find_the_rising_keyword():
    th = an.themes(synthetic(), ["trade credit"], split_year=2021)
    assert th.iloc[0]["keyword"] == "fintech" and th.iloc[0]["change"] > 0.3


def test_clusters_separate_the_two_themes():
    sets = an.keyword_sets(synthetic(), ["trade credit"])
    freq, pairs = an.cooccurrence(sets)
    comms = an.clusters(freq, pairs)
    side = {k: i for i, c in enumerate(comms) for k in c}
    assert side["liquidity"] == side["risk management"]
    assert side["liquidity"] != side["supply chain"]


def test_gaps_flag_pairs_that_never_meet():
    works = synthetic()
    sets = an.keyword_sets(works, ["trade credit"])
    freq, pairs = an.cooccurrence(sets)
    gp = an.gaps(freq, pairs, len(works))
    first = {gp.iloc[0]["a"], gp.iloc[0]["b"]}
    assert gp.iloc[0]["observed"] == 0
    assert first & {"liquidity", "risk management", "bank credit"}
    assert first & {"supply chain", "inventory", "working capital"}


def test_foundations_rank_most_cited_references():
    works = synthetic()
    assert an.foundations_ids(works, n=2) == ["W900", "W901"]
    titles = [{"id": "W900", "title": "Old", "year": 1997, "first_author": "P", "cited": 1}]
    f = an.foundations(works, titles)
    assert f.iloc[0]["cited_here"] == len(works)


def test_report_end_to_end(tmp_path):
    (tmp_path / "README.md").write_text("x\n<!-- latest:start -->\nold\n<!-- latest:end -->\n")
    works = synthetic()
    snap = {
        "topic": "tc",
        "fetched": "2026-11-01",
        "count": len(works),
        "complete": True,
        "works": works,
        "foundations": [
            {"id": "W900", "title": "Old", "year": 1997, "first_author": "P", "cited": 1}
        ],
        "new_ids": ["W1", "W2"],
        "previous_fetch": "2026-10-01",
    }
    oa.save(tmp_path / "data" / "raw" / "tc.json.gz", snap)
    cfg = {
        "tc": {
            "label": "Trade credit",
            "query": "q",
            "stop": ["trade credit"],
            "events": {2008: "GFC"},
        }
    }
    out = report.main(tmp_path, cfg, today=date(2026, 11, 1))
    assert len(out) == 1 and len(out[0]["new"]) == 2
    readme = (tmp_path / "README.md").read_text()
    assert "Latest reading: 2026-11-01" in readme and "old" not in readme
    page = (tmp_path / "docs" / "topics" / "tc.md").read_text()
    assert "Under-connected themes" in page and "fintech" in page
    for k in ("trend", "map", "themes"):
        for mode in ("light", "dark"):
            assert (tmp_path / "docs" / "figures" / f"tc-{k}-{mode}.png").exists()
