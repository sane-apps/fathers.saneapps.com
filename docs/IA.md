# Information architecture — fathers.saneapps.com

Public library of Fathers reading: **topics** (ante-Nicene dogmatics map) and
**works** (full treatises). Canonical book trees live under
`~/SaneApps/clients/translations/books/`. Extend those books and re-run the site
build — do not invent a second outline.

## Two doors (primary nav)

| Door | Question | Source |
|------|----------|--------|
| **Topics** | What did the Fathers teach about X? | `ante-nicene-topics` |
| **Works** | Read a whole treatise; find / sort / filter the catalog | `origen-prayer-martyrdom`, `julian-of-eclanum`, … |
| **Explore** | Curated doctrinal paths + how writers line up on a claim across time | `data/explore/` + library points |

Home presents Topics and Works; Explore is a third nav door (path cards + topic river with optional compare ≤3 authors). Authors is the A–Z index. **Search is not a separate tab** — find lives on Works (`/works/?q=`). Old `/search/` redirects to `/works/`.

## Browse rules (2026-09-12)

1. **Alphabetical** for topics (within each locus/area), loci/areas, authors, and Explore topic lists — case-insensitive Latin sort. No load/DB insertion order.
2. **Works default sort:** chronology by author era / floruit (`author_sort_year`), earliest first. Alternates: author name, work title. Controls are visible on `/works/`.
3. **Works find** filters the catalog and surfaces passage/topic hits from `search-index.json` so a separate Search tab is unnecessary.
4. **Explore paths** come from `data/explore/paths.json` (doctrine, controversy, scripture, era, rupture, reading). Stub/partial statuses are honest when the corpus is thin.

## Cross-references (required)

Every public surface should point to the other door when a link exists:

| From | To |
|------|-----|
| Work home / section | Related **topics** + author hub |
| Topic page | Related **works** (see `WORK_TOPICS` in `scripts/build_site.py`) |
| Excerpt card | Topic, author, related works |
| Author hub | Their works + topical excerpts + related topics |

Update `WORK_TOPICS` when a new treatise lands. Topic ids must match
`ante-nicene-topics/topics.yml`.

## URL map (stable)

### Shared
| Path | Purpose |
|------|---------|
| `/` | Brand + enter Topics / Works + donate |
| `/about/` | Evergreen mission, how to read, badge meaning, Sponsors (no work inventory) |
| `/methodology/` | How English is made: sources, two passes, OET meaning, apparatus vs reader |
| `/search/` | **Redirect** → `/works/` (find/filter lives on Works) |
| `/authors/` | Author index A–Z (both doors) |
| `/authors/{slug}/` | Author hub → works + topical hits + topics |

### Explore door
| Path | Purpose |
|------|---------|
| `/explore/` | Curated paths + topic river timeline (stance lanes × time) |
| `/explore/?topic=&author=&zoom=&compare=` | Deep link filters |

Explore data: `data/explore/{claims,stances,contrast,ruptures,paths}.json` (+ `*_expansion.json`) → `dist/data/explore-index.json`.
Primary model: **path cards** then **topic river**. Compare mode: up to 3 authors. Century aggregation by default when crowded; Years on demand. Contrast cards for authors not yet fully in the corpus (e.g. Augustine).

### Topics door
| Path | Purpose |
|------|---------|
| `/topics/` | Locus → topic index with counts (**A–Z** within each area) |
| `/topics/{topic-id}/` | Excerpts + related works |
| `/e/{excerpt-id}/` | Topical excerpt card |

### Works door
| Path | Purpose |
|------|---------|
| `/works/` | Catalog with find, chronology default, author/title sorts, era + OET filters |
| `/works/?q=&sort=&filter=` | Deep links into the catalog |
| `/works/{work-slug}/` | Continuous reader (text-first rail). Multi-book works: short hub |
| `/works/{work-slug}/book-N/` | One book as a continuous reader |
| `/works/{work-slug}/{section}/` | Cite page; “Read continuously” jumps to the reader `#s…` |

Presentation: `AGENTS.md` → Works reader SOP. Contents is one line per thought, not one line per edition slice.

### Current works (2026-09-10)

| Slug | Author | Notes |
|------|--------|-------|
| `origen-on-prayer` | Origen | Complete (34) |
| `origen-exhortation-to-martyrdom` | Origen | Complete (proem + 51) |
| `origen-dialogue-heraclides` | Origen | Book 2 — ships when English JSON exists |
| `origen-on-pascha` | Origen | Book 2 — ships when English JSON exists |
| `cyril-adoration-1` | Cyril of Alexandria | *De adoratione* Book 1 — **post-Nicene**; not Cyril of Jerusalem |
| `origen-homilies-jeremiah` | Origen | Homilies 1–2 of 20 Greek Jeremiah homilies (GCS III). In progress. |
| `julian-to-florus` | Julian of Eclanum | 834 sections; **not ante-Nicene** (early 5th c.) |
| `julian-turbantius-fragments` | Julian | Excerpts in Against Julian |
| `julian-marriage-extracts` | Julian | Marriage & Concupiscence II |
| `julian-letter-to-rome` | Julian | Fragments |
| `julian-collective-letter` | Julian | Collective letter |

## Navigation that scales

1. **Persistent dual rail** — Topics loci OR Works TOC; mobile drawer.
2. **Breadcrumbs** always: Home → Door → … → page.
3. **Chronological** within topics; **edition order** within works (Koetschau / Florus book.section).
4. **Prev / next** on every work section; grouped TOC for multi-book works.
5. **Era honesty** — post-Nicene corpora carry a banner on their work pages. About stays evergreen and does not name a rotating title list.
6. **Translation confidence** — short note on each **work** intro (not a Topics filter or badge UI). Collapsed “About this text” also names copy-text, other prints checked, and supplied stretches (`text_history`). The reading column has no apparatus.
7. **Original English Translation** — treatises with **no previous English translation** (no complete prior English of the work) are grouped on `/works/#original-english` (aliases `#no-prior-english` and `#no-earlier-english` still resolve) and marked on the work mast, cards, and About-this-text banner with the full phrase `Original English Translation` (tooltip: `Original English Translation — no previous English translation`). Do **not** say “free English” / “previous free English” / “complete free English” in public copy. Do not use a bare `English` badge (that reads as language-only). Prefer the full phrase over a shortened chip unless space truly cannot fit. Do not invent a slogan button. Do not mark Julian (Victorian English of some of his words already exists inside Augustine). Do not put this on Topics. Keep true language metadata (`lang`, witness `language: Greek|Latin`) unchanged. Deep essay: `/methodology/`.

## Public copy

No GTG jargon. No “complete critical edition” claims. Do not surface internal verification stamps as reader toggles.

## Donate

GitHub Sponsors: https://github.com/sponsors/MrSaneApps  
Quiet Support in header/footer and `/about/`. No paywall.

## Build / deploy

```bash
cd ~/SaneApps/websites/fathers.saneapps.com
~/SaneApps/clients/translations/.venv/bin/python scripts/build_site.py
npx wrangler pages deploy dist --project-name fathers-site
```

Hostname: `fathers.saneapps.com`. Mini-first for visual proof after deploy.
