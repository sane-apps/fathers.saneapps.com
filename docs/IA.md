# Information architecture — fathers.saneapps.com

Public library of Fathers reading: **topics** (ante-Nicene dogmatics map) and
**works** (full treatises). Canonical book trees live under
`~/SaneApps/clients/translations/books/`. Extend those books and re-run the site
build — do not invent a second outline.

## Two doors (primary nav)

| Door | Question | Source |
|------|----------|--------|
| **Topics** | What did the Fathers teach about X? | `ante-nicene-topics` |
| **Works** | Read a whole treatise, section by section | `origen-prayer-martyrdom`, `julian-of-eclanum`, … |
| **Explore** | How writers line up on a claim across time | `data/explore/` + library points |

Home presents Topics and Works; Explore is a third nav door (topic river with optional compare ≤3 authors).

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
| `/about/` | Honesty, era notes, GitHub Sponsors |
| `/search/` | Search across topics + works |
| `/authors/` | Author index (both doors) |
| `/authors/{slug}/` | Author hub → works + topical hits + topics |

### Explore door
| Path | Purpose |
|------|---------|
| `/explore/` | Topic river timeline (stance lanes × time) |
| `/explore/?topic=&author=&zoom=` | Deep link filters |

Explore data: `data/explore/{claims,stances,contrast,ruptures}.json` → `dist/data/explore-index.json`.
Primary model: **topic river**. Compare mode: up to 3 authors. Century aggregation by default when crowded; Years on demand. Contrast cards for authors not yet fully in the corpus (e.g. Augustine).

### Topics door
| Path | Purpose |
|------|---------|
| `/topics/` | Locus → topic index with counts |
| `/topics/{topic-id}/` | Excerpts + related works |
| `/e/{excerpt-id}/` | Topical excerpt card |

### Works door
| Path | Purpose |
|------|---------|
| `/works/` | Catalog (status + era labels) |
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
5. **Era honesty** — post-Nicene corpora (Julian, Cyril of Alexandria) carry a banner on work pages and are named on About.
6. **Translation confidence** — short note on each **work** intro (not a Topics filter or badge UI). Collapsed “About this text” also names copy-text, other prints checked, and supplied stretches (`text_history`). The reading column has no apparatus.
7. **No earlier English** — treatises with no earlier complete public-domain English are grouped on `/works/#no-earlier-english` and noted on the work intro and home. Do not invent a slogan button. Do not mark Julian (Victorian English of some of his words already exists inside Augustine). Do not put this on Topics.

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
