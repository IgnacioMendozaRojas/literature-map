"""Download works from OpenAlex (open, CC0 metadata) and keep a compact record of each."""

from __future__ import annotations

import gzip
import json
import os
import time
from datetime import date
from pathlib import Path

import requests

API = "https://api.openalex.org/works"
FIELDS = [
    "id",
    "doi",
    "display_name",
    "publication_year",
    "cited_by_count",
    "type",
    "primary_location",
    "authorships",
    "keywords",
    "primary_topic",
    "referenced_works",
]


def short_id(url: str | None) -> str:
    """'https://openalex.org/W123' -> 'W123'."""
    return (url or "").rsplit("/", 1)[-1]


def filter_string(query: str, since: int, until: int) -> str:
    q = " ".join(query.split())
    if "," in q:
        raise ValueError("OpenAlex filters are separated by commas; remove them from the query")
    return (
        f"title_and_abstract.search:{q},type:article,"
        f"publication_year:{since}-{until},is_retracted:false"
    )


def compact(work: dict) -> dict:
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    topic = work.get("primary_topic") or {}
    return {
        "id": short_id(work.get("id")),
        "doi": (work.get("doi") or "").replace("https://doi.org/", ""),
        "title": " ".join((work.get("display_name") or "").split()),
        "year": work.get("publication_year"),
        "cited": work.get("cited_by_count") or 0,
        "journal": source.get("display_name") or "",
        "authors": [
            a["author"]["display_name"]
            for a in work.get("authorships") or []
            if (a.get("author") or {}).get("display_name")
        ],
        "keywords": [k["display_name"].lower() for k in work.get("keywords") or []],
        "field": ((topic.get("field") or {}).get("display_name")) or "",
        "refs": [short_id(r) for r in work.get("referenced_works") or []],
    }


class Client:
    def __init__(self, pause: float = 0.2, session: requests.Session | None = None):
        self.s = session or requests.Session()
        self.s.headers["User-Agent"] = "literature-map (github.com/IgnacioMendozaRojas)"
        self.key = os.environ.get("OPENALEX_API_KEY", "")
        self.pause = pause
        self.calls = 0

    def get(self, params: dict) -> dict:
        if self.key:
            params = {**params, "api_key": self.key}
        for attempt in range(5):
            r = self.s.get(API, params=params, timeout=60)
            self.calls += 1
            if r.status_code == 200:
                time.sleep(self.pause)
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** (attempt + 1))
                continue
            break
        # surface the reason in the run's annotations (logs need a login to read)
        msg = f"{r.url[:300]} -> {r.text[:500]}"
        print(f"::error title=OpenAlex {r.status_code}::{msg}", flush=True)
        r.raise_for_status()
        return {}

    def works(self, flt: str, limit: int) -> tuple[int, list[dict]]:
        """All works matching the filter (cursor paging), up to 'limit'."""
        out, cursor, count = [], "*", 0
        while cursor and len(out) < limit:
            page = self.get(
                {"filter": flt, "select": ",".join(FIELDS), "per-page": 100, "cursor": cursor}
            )
            count = page["meta"]["count"]
            out += [compact(w) for w in page["results"]]
            cursor = page["meta"].get("next_cursor") if page["results"] else None
        return count, out[:limit]

    def titles(self, ids: list[str]) -> list[dict]:
        """Title, year, first author and citations for a list of work ids (50 per request)."""
        out = []
        for i in range(0, len(ids), 50):
            chunk = ids[i : i + 50]
            page = self.get(
                {
                    "filter": "openalex:" + "|".join(chunk),
                    "select": "id,display_name,publication_year,authorships,cited_by_count",
                    "per-page": 50,
                }
            )
            for w in page["results"]:
                names = [a["author"]["display_name"] for a in w.get("authorships") or []]
                out.append(
                    {
                        "id": short_id(w["id"]),
                        "title": " ".join((w.get("display_name") or "").split()),
                        "year": w.get("publication_year"),
                        "first_author": names[0] if names else "",
                        "cited": w.get("cited_by_count") or 0,
                    }
                )
        return out


def load(path: Path) -> dict | None:
    if not path.exists():
        return None
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def save(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))


def snapshot(
    client: Client, name: str, cfg: dict, previous: dict | None, today: date, limit: int = 6000
) -> dict:
    """Download one topic. Works not in the previous snapshot are listed as new."""
    flt = filter_string(cfg["query"], cfg.get("since", 1990), today.year)
    count, works = client.works(flt, limit)
    from .analysis import foundations_ids  # local import keeps the download module light

    found = client.titles(foundations_ids(works, n=40))
    old = {w["id"] for w in (previous or {}).get("works", [])}
    new = [w["id"] for w in works if old and w["id"] not in old]
    return {
        "topic": name,
        "fetched": today.isoformat(),
        "filter": flt,
        "count": count,
        "complete": count <= limit,
        "works": works,
        "foundations": found,
        "new_ids": new,
        "previous_fetch": (previous or {}).get("fetched"),
    }
