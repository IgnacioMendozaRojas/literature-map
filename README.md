# literature-map

[![CI](https://github.com/IgnacioMendozaRojas/literature-map/actions/workflows/ci.yml/badge.svg)](https://github.com/IgnacioMendozaRojas/literature-map/actions/workflows/ci.yml)
[![Monthly update](https://github.com/IgnacioMendozaRojas/literature-map/actions/workflows/update.yml/badge.svg)](https://github.com/IgnacioMendozaRojas/literature-map/actions/workflows/update.yml)

**Research tool: a bibliometric review that rebuilds itself every month.** For each research field it maps growth, themes, clusters, foundational works and under-connected themes, from open data (OpenAlex), so any reader can rerun it.

> I started with a bibliometric review of trade credit in SMEs built by hand from Scopus and VOSviewer. This repository makes the same review reproducible and keeps it current. It runs on open data and covers the three fields of my research: trade credit in SMEs, ownership and boards, and AI and labour costs.

## Results

_Filled in after the first run._

## Latest reading

<!-- latest:start -->
**Latest reading: 2026-10-31.** 10 new articles since the last update. The fastest-growing field is AI, automation and labour costs: 56 articles a year in 2021-2025, against 5 in 2011-2015.

| Field | Articles | A year, recent | A year, ten years earlier | New | Under-connected |
|---|---:|---:|---:|---:|---|
| [Trade credit and SMEs](docs/topics/trade-credit-smes.md) | 440 | 29 (2021-2025) | 15 (2011-2015) | 0 | sme financing / accounts receivable |
| [Ownership and boards](docs/topics/ownership-and-boards.md) | 2,906 | 177 (2021-2025) | 108 (2011-2015) | 10 | ceo duality / indonesia stock exchange |
| [AI, automation and labour costs](docs/topics/ai-and-labour-costs.md) | 510 | 56 (2021-2025) | 5 (2011-2015) | 0 | labor share / digital transformation |

*New: articles that were not in the previous monthly snapshot. Under-connected: the pair of frequent themes that appear together least often relative to chance.*
<!-- latest:end -->

## License

MIT. OpenAlex metadata is CC0.
