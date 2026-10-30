"""Command line: `litmap fetch` downloads the snapshots, `litmap report` rebuilds the outputs."""

from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(os.environ.get("LITMAP_ROOT", "."))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="litmap")
    ap.add_argument("command", choices=["fetch", "report"])
    ap.add_argument("--topic", help="only this topic (default: all)")
    args = ap.parse_args(argv)
    topics = yaml.safe_load((ROOT / "config" / "topics.yaml").read_text())
    if args.topic:
        topics = {args.topic: topics[args.topic]}
    if args.command == "report":
        from . import report

        report.main(ROOT, topics)
        return 0
    from . import openalex as oa

    client, today = oa.Client(), date.today()
    for name, cfg in topics.items():
        path = ROOT / "data" / "raw" / f"{name}.json.gz"
        snap = oa.snapshot(client, name, cfg, oa.load(path), today)
        oa.save(path, snap)
        level = "notice" if snap["complete"] else "warning"
        print(
            f"::{level} title={name}::{snap['count']:,} articles in OpenAlex, "
            f"{len(snap['works']):,} kept, {len(snap['new_ids'])} new, {client.calls} calls so far"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
