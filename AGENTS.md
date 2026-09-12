# AGENTS — fathers.saneapps.com

- Dual product: **Topics** + **Works** + **Explore** timeline. Do not collapse into a topics-only site.
- Canonical data: `~/SaneApps/clients/translations/books/*` — extend books, then rebuild.
- Explore editorial layer: `data/explore/` (claims, stances, contrast, ruptures). Schema in `clients/translations/docs/SCHEMAS.md`.
- Cross-refs: keep `WORK_TOPICS` in `scripts/build_site.py` in sync with `docs/IA.md` and `topics.yml`. Every new work needs topic links + author hub.
- No “Verified only” filter or confidence badges on Topics. Put a short translation-confidence note on each **work** intro.
- Julian (and any post-Nicene corpus) must show an era banner — do not silently call the whole site ante-Nicene only.
- Donate: GitHub Sponsors `MrSaneApps`. No paywall.
- Deploy to Cloudflare Pages `fathers-site`; hostname `fathers.saneapps.com`.
- Prefer `./scripts/ship.sh` (build → smoke → deploy → print CSS `?v=`).
- Never hand-edit `dist/`; only `scripts/build_site.py` + `assets/` (+ data/books), then rebuild. See `docs/DIST.md`.
- Mini-first for live visual verification after deploy.
- Read `docs/IA.md` before changing URL structure.
- Build with the translations venv (PyYAML): `~/SaneApps/clients/translations/.venv/bin/python scripts/build_site.py`.

## Works reader SOP (permanent)

How every whole work is presented on the site. Do not invent a second reading pattern.

1. **Continuous page.** `/works/<slug>/` is a reader, not a TOC that forces a click per section. Multi-book works get one reader per book (`/works/<slug>/book-N/`) plus a short overview hub.
2. **Thought-chunks, not slices.** Consecutive sections that share a real title merge into one passage (heading + range). Locus-only heads (`Against Julian 1.5.16`, `To Florus 1.3`, `Marriage 2.2.3`, etc.) count as untitled and size-group. Edition §numbers stay as small gold inline marks and deep-link targets (`#s…`). Biblical locus titles on gospel fragments (`Matthew 1:16`) stay visible in Contents but do **not** merge distinct fragments that share a verse.
3. **Contents = plain English, logical order.** One line per thought. Never list the same title once per micro-section. Summary meta is `N passages · M sections` when they differ. Jump links land on the first § of the chunk. Labels are reader-facing only (e.g. `Matthew 1:16`) — never lead with `CPG … fr.N`. Gospel-fragment Contents (and default reading order) follow chapter then verse, then fragment id as tiebreaker — not raw edition fragment-number order.
4. **Reading headings stay clean.** Section H1/H2 text names the thought or biblical locus. No technical bibliography in titles (`CPG 5206 fr.N …`, witness sigla, edition sigla). Put CPG / fragment / edition / witness detail in **About this text** and/or bottom scholar metadata under the passage.
5. **Text first.** Slim mast (title + one meta line). Sticky left rail holds Contents, Author, Related topics, and a collapsed “About this text” (banners, blurb, confidence, witnesses, and joins). The reading column starts at the first passage with no scroll-past intro stack. On narrow screens the text column comes first; rail follows.
6. **Cite pages remain.** `/works/<slug>/<section>/` stays for citations; its middle nav is “Read continuously” into the reader at that §anchor.
7. **Source panels.** One Greek/Latin `<details>` per thought-chunk (not per slice), labeled with the § range.
8. **New works** must ship through this builder path (`chunk_sections` / `reader_page` in `scripts/build_site.py`). Do not add a one-section-per-page browsing UX.
9. **Witnesses.** “About this text” names the copy-text, other prints checked, and every stretch supplied from another witness. The reading column has no apparatus. A one-line italic cue is used only when a whole stretch is supplied from another witness. Do not call the reading text a manuscript. Do not claim a combination that was not actually done.
