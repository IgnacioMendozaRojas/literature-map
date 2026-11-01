# Ownership and boards

*Rebuilt from OpenAlex on 2026-11-01. Do not edit by hand: see
[`report.py`](../../src/litmap/report.py).*

**Query** (title and abstract, journal articles since 1990):
`("ownership structure" OR "ownership concentration" OR "family ownership" OR blockholder OR blockholders OR "controlling shareholder" OR "large shareholders" OR "owner identity") AND ("board of directors" OR "board composition" OR "board independence" OR "independent directors" OR "board structure" OR "director appointment")`

**Coverage.** 2,908 articles; 36% of them published in
2021-2025.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/ownership-and-boards-trend-dark.png">
  <img alt="Ownership and boards: output rose from 108 to 177 articles a year" src="../figures/ownership-and-boards-trend-light.png">
</picture>

## Focus: Combinations of large owners

Combinations of large owners: 10 of 2,739 articles, all published since 2009 (0% of the field's output in those years). Pattern on titles and keywords: `multiple (large )?(shareholders|blockholders|owners)|second (largest )?(shareholder|blockholder)|ownership constellation|coalition|contestab`.

| First author | Year | Title | Journal |
|---|---|---|---|
| Andrés Fernando Mejía Amaya | 2026 | [CEO–COB separation as a governance outcome: ownership structure, contestability, and inst…](https://openalex.org/W7223174058) | Review of Managerial Science |
| Caiyu Yan | 2023 | [Multiple Large Shareholders and Firm Performance: Evidence from China*](https://openalex.org/W4381053845) | Asia-Pacific Journal of Financial Studies |
| Samridhi Suman | 2022 | [The Role of Multiple Large Shareholders in Dividend Payouts: Evidence from India](https://openalex.org/W4229053702) | American Business Review |
| Shanzhong Du | 2022 | [Non-actual controllers and corporate innovation: Evidence from China](https://openalex.org/W4286781298) | China Journal of Accounting Research |
| Ibrahim Rufai | 2018 | [The impacts of multiple large ownership structure on board independence](https://openalex.org/W4229672610) | International Journal of Accounting Auditing and Performance Evaluation |
| Jin‐hui Luo | 2014 | [Family-Concentrated Ownership in Chinese PLCs: Does Ownership Concentration Always Enhanc…](https://openalex.org/W2158442514) | International Journal of Financial Studies |
| Wan Di-fang | 2011 | [Private benefits of control of incumbent shareholders:Theoretical model and empirical fin…](https://openalex.org/W2365028540) | Systems Engineering - Theory & Practice |
| Jin‐hui Luo | 2010 | [The private benefits of control in Chinese listed firms: Do cash flow rights always reduc…](https://openalex.org/W1999997164) | Asia Pacific Journal of Management |
| Wan Di-fang | 2010 | [Large Shareholdings and Firm Value:An Empirical Analysis](https://openalex.org/W2371699905) | Application of Statistics and Management |
| 廖振盛 | 2009 | [三篇有關台灣金融機構效率的論文:銀行、產險與證券業](https://openalex.org/W2340571536) |  |

## Strands of the field

Articles whose title or keywords match each strand's pattern in [`topics.yaml`](../../config/topics.yaml); an article can be in several.

| Strand | Articles | Share |
|---|---|---|
| Institutional investors | 573 | 21% |
| Family owners | 455 | 17% |
| The State | 282 | 10% |
| Foreign owners | 238 | 9% |
| Combinations of large owners | 10 | 0% |

## Themes and clusters

Keyword communities found by modularity on the co-occurrence network (the method behind
VOSviewer's clustering), largest first:

1. board independence, board size, institutional ownership, managerial ownership, foreign ownership, emerging markets, state ownership, board gender diversity
2. independent directors, ceo duality, board composition, listed companies, family ownership, agency theory, board structure, family business
3. firm size, leverage, audit committee, indonesia stock exchange, earnings management, manufacturing companies, audit quality, audit committee independence
4. firm performance, return on assets, financial performance, tobin's q, return on equity, firm value

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/ownership-and-boards-map-dark.png">
  <img alt="Ownership and boards: the literature splits into 4 clusters of themes" src="../figures/ownership-and-boards-map-light.png">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../figures/ownership-and-boards-themes-dark.png">
  <img alt="Ownership and boards: since 2021, the rising themes are board independence and board gender diversity" src="../figures/ownership-and-boards-themes-light.png">
</picture>

## Under-connected themes

Pairs of frequent keywords that appear together far less often than chance would predict. They
are candidates for research gaps, to be read against the literature, not conclusions.

- **state ownership** and **family business**: 3 articles together, 12 expected if unrelated
- **foreign ownership** and **family business**: 4 articles together, 14 expected if unrelated
- **firm performance** and **earnings management**: 10 articles together, 29 expected if unrelated
- **managerial ownership** and **family business**: 8 articles together, 23 expected if unrelated
- **institutional ownership** and **family business**: 10 articles together, 26 expected if unrelated
- **audit committee** and **family business**: 5 articles together, 13 expected if unrelated

## Foundations: the works this field cites most

| First author | Year | Title | Cited by articles here | Share |
|---|---|---|---|---|
| Michael C. Jensen | 1976 | [Theory of the firm: Managerial behavior, agency costs and ownership structure](https://openalex.org/W2752617332) | 829 | 30% |
| Eugene F. Fama | 1983 | [Separation of Ownership and Control](https://openalex.org/W3122859634) | 579 | 21% |
| Andrei Shleifer | 1997 | [A Survey of Corporate Governance](https://openalex.org/W3121693921) | 469 | 17% |
| Michael C. Jensen | 1993 | [The Modern Industrial Revolution, Exit, and the Failure of Internal Control Systems](https://openalex.org/W3021889044) | 328 | 12% |
| David Yermack | 1996 | [Higher market valuation of companies with a small board of directors](https://openalex.org/W2074132263) | 308 | 11% |
| Rafael La Porta | 1999 | [Corporate Ownership Around the World](https://openalex.org/W3123091495) | 266 | 10% |
| Andrei Shleifer | 1986 | [Large Shareholders and Corporate Control](https://openalex.org/W2135241016) | 258 | 9% |
| Randall Mørck | 1988 | [Management ownership and market valuation](https://openalex.org/W1606272114) | 233 | 9% |
| Eugene F. Fama | 1980 | [Agency Problems and the Theory of the Firm](https://openalex.org/W2160184254) | 228 | 8% |
| Harold Demsetz | 1985 | [The Structure of Corporate Ownership: Causes and Consequences](https://openalex.org/W1991795148) | 200 | 7% |

## Most cited articles

| First author | Year | Title | Journal | Citations |
|---|---|---|---|---|
| Benjamin E. Hermalin | 1991 | [The Effects of Board Composition and Direct Incentives on Firm Performance](https://openalex.org/W1977528366) | Financial Management | 2313 |
| Li Li Eng | 2003 | [Corporate governance and voluntary disclosure](https://openalex.org/W2069712330) | Journal of Accounting and Public Policy | 1967 |
| Sanjai Bhagat | 2007 | [Corporate Governance and Firm Performance](https://openalex.org/W4237866076) | Journal of Corporate Finance | 1750 |
| Hoje Jo | 2011 | [Corporate Governance and Firm Value: The Impact of Corporate Social Responsibility](https://openalex.org/W2036829732) | Journal of Business Ethics | 1604 |
| Hollis Ashbaugh Skaife | 2006 | [The effects of corporate governance on firms’ credit ratings](https://openalex.org/W3121156620) | Journal of Accounting and Economics | 1321 |
| Ronald C. Anderson | 2004 | [Board Composition: Balancing Family Influence in S&P 500 Firms](https://openalex.org/W3124866554) | Administrative Science Quarterly | 1154 |
| Robert M. Bushman | 2003 | [Financial accounting information, organizational complexity and corporate governance syst…](https://openalex.org/W3124681717) | Journal of Accounting and Economics | 1059 |
| Barry D. Baysinger | 1991 | [EFFECTS OF BOARD AND OWNERSHIP STRUCTURE ON CORPORATE R&D STRATEGY.](https://openalex.org/W1987715081) | Academy of Management Journal | 949 |
| Anil Shivdasani | 1993 | [Board composition, ownership structure, and hostile takeovers](https://openalex.org/W2014524200) | Journal of Accounting and Economics | 906 |
| Stuart Gillan | 2006 | [Recent Developments in Corporate Governance: An Overview](https://openalex.org/W2035551893) | Journal of Corporate Finance | 877 |

## Rising: recent articles with the most citations per year

| First author | Year | Title | Journal | Citations a year |
|---|---|---|---|---|
| Bruno Buchetti | 2024 | [A literature review on corporate governance and ESG research: Emerging trends and future…](https://openalex.org/W4404202412) | International Review of Financial Analysis | 32.3 |
| Fuxiu Jiang | 2024 | [Understanding corporate governance in China](https://openalex.org/W4401354569) | The British Accounting Review | 21.3 |
| Waseem Akhter | 2023 | [Does corporate social responsibility mediate the relationship between corporate governanc…](https://openalex.org/W4385837895) | Corporate Social Responsibility and Environmental Management | 16.0 |
| Subhas Mondal | 2024 | [Unveiling the moderating role of governance mechanism on the nexus between CSR and firm p…](https://openalex.org/W4402499120) | Corporate Social Responsibility and Environmental Management | 14.0 |
| Asuman Erben Yavuz | 2024 | [The Impact of Corporate Governance on Sustainability Disclosures: A Comparison from the P…](https://openalex.org/W4402929122) | Sustainability | 13.7 |
| Pei-Gi Shu | 2024 | [Board network and ESG performance: Evidence from China](https://openalex.org/W4399920157) | Corporate Social Responsibility and Environmental Management | 13.3 |
| Shms Alduha Abualhassan | 2024 | [Does corporate governance moderate the impact of earnings management on capital structure…](https://openalex.org/W4396691807) | Discover Sustainability | 13.3 |
| Arshad Hasan | 2023 | [Corporate governance and tax avoidance: evidence from an emerging market](https://openalex.org/W4362695657) | Applied Economics | 13.0 |

## Journals and authors

| Journal | Articles |
|---|---|
| Zenodo (CERN European Organization for Nuclear Research) | 68 |
| Corporate Ownership and Control | 61 |
| Corporate Governance | 51 |
| DOAJ (DOAJ: Directory of Open Access Journals) | 46 |
| RePEc: Research Papers in Economics | 44 |
| Corporate Governance An International Review | 34 |
| DJA (Diponegoro Journal of Accounting) | 23 |
| Corporate Board role duties and composition | 19 |
| Journals & Books Hosting (International Knowledge Sharing Platform) | 18 |
| International Journal of Business and Management | 17 |

| Author | Articles |
|---|---|
| Onipe Adabenege Yahaya | 34 |
| Khaled Hussainey | 10 |
| Hafiza Aishah Hashim | 9 |
| Yuan George Shan | 9 |
| Juan Manuel San Martín Reyna | 7 |
| Azhar Abdul Rahman | 6 |
| Nejla Ould Daoud Ellili | 6 |
| Félix J. López‐Iturriaga | 6 |
| Shamsul Nahar Abdullah | 6 |
| Balwinder Singh | 6 |

## New since the last update (2026-10-31)

| First author | Year | Title | Journal |
|---|---|---|---|
| Ramsey Prince Osere | 2025 | [Corporate Governance and Organisational Health in Selected Deposit Money Banks in Lagos S…](https://openalex.org/W4413082352) |  |
| Faten Ben Bouheni | 2017 | [Analyzing the governance structure of French banking groups](https://openalex.org/W2619017680) | Research in International Business and Finance |
| Widijaya Widijaya | 2022 | [KARAKTERISTIK DEWAN DIREKSI, KOMITE AUDIT, DAN KEPEMILIKAN TERHADAP KINERJA PERUSAHAAN](https://openalex.org/W4310542380) | Jurnal Ekonomi Pembangunan STIE Muhammadiyah Palopo |
| Nguyễn Thị Thu Thảo | 2026 | [THE MEDIATING ROLE OF CASH HOLDINGS IN THE RELATIONSHIP BETWEEN CORPORATE GOVERNANCE AND…](https://openalex.org/W7225002020) | Financial and credit activity problems of theory and practice |
| Shikha Chauhan | 2010 | [Corporate Governance Structure and Performance of Indian Companies](https://openalex.org/W2735137444) | Indian Journal of Corporate Governance |
| علی رحمانی | 2017 | [محرکهای افشای اختیاری در بازار سرمایه ایران](https://openalex.org/W3119344588) | DOAJ (DOAJ: Directory of Open Access Journals) |
| Mengkai Wang | 2025 | [Data-Driven Disclosure Governance in Blockchain-Adopting Firms: Evidence from Supply Chai…](https://openalex.org/W7224993398) | Journal of Business and Data Analytics |
| Paul Olojede | 2020 | [Corporate Governance and Creative Accounting Practices in The Listed Companies in Nigeria](https://openalex.org/W3081347010) | Academy of Accounting and Financial Studies journal |
