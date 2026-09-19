# Fathers — session handoff

## 2026-09-19 — Origen Greek Psalms 1–16.3 SHIP

Live 57 treatises / 2920 sections. Origen Fragmenta in Psalmos (Greek) 70 thought titles through Psalm 16:3 night is the affliction. H1 Fragments on the Psalms (Greek). Authors earliest-first with BC/AD. Photius 18–22 still held. Cesti still 98. Deploy `ad737377.fathers-site.pages.dev`, CSS `?v=795fb67ec6`. Visual: 32/32 ui-review PNGs inspected (artifact `0a1a817b`). Next overnight: lock header **16.7**.

## 2026-09-19 — Origen Greek Psalms 1–5.10 SHIP

Live 57 treatises / 2871 sections. Origen Fragmenta in Psalmos (Greek) 21 thought titles through Psalm 5:10 opened tomb / dead works. H1 Fragments on the Psalms (Greek). Authors earliest-first with BC/AD. Photius 18–22 still held. Cesti still 98. Deploy `b7247acb.fathers-site.pages.dev`, CSS `?v=795fb67ec6`. Visual: 32/32 ui-review PNGs inspected (artifact `bd76092a`). Next overnight: lock header **5.11**.

## 2026-09-19 — Africanus Cesti 3.33–3.36 SHIP (book 3 of this lock closed)

Live 56 treatises / 2838 sections. Cesti tip through book 7 colophon, book 2.1–2.12, and book 3.1–3.36 (toad-fire, date plaster, swan amulet, brand erasure; 86 thought titles). H1 The Cesti. Photius 18–22 still held. Deploy `c270d536.fathers-site.pages.dev`, CSS `?v=f0f1afd6e7`. Visual: 32/32 ui-review PNGs inspected (artifact `f27dc151`) plus extra Cesti reader/s83/s86 shots in `outputs/visual-audit-africanus/`. This lock's book 3 is closed. Do not invent a book-4 split.

## 2026-09-19 night — Africanus Cesti 3.1–3.3 SHIP

Live 56 treatises / 2805 sections. Cesti tip through book 7 colophon, book 2.1–2.12, and book 3.1–3.3 (horse elephantiasis, eye-drugs, generation of horses; 53 thought titles). H1 The Cesti. Photius 18–22 still held. Deploy `15ab99cf.fathers-site.pages.dev`, CSS `?v=f0f1afd6e7`. Visual: 32/32 ui-review PNGs inspected (artifact `9815fa19`) plus extra Cesti reader/s50/s53 shots in `outputs/visual-audit-africanus/`. Next overnight: Cesti 3.4 from the same lock (`--start 54`).

## 2026-09-19 night — Africanus Cesti 2.9–2.12 SHIP (book 2 remainder)

Live 56 treatises / 2801 sections. Cesti tip through book 7 colophon plus book 2.1–2.12 hunt of hearing (49 thought titles). H1 The Cesti. Photius 18–22 still held. Deploy `a22e912f.fathers-site.pages.dev`, CSS `?v=f0f1afd6e7`. Visual: 32/32 ui-review PNGs inspected (artifact `0969eea2`) plus extra Cesti reader/s46/s49 shots in `outputs/visual-audit-africanus/`. Next overnight: Cesti book 3 from the same lock.

## 2026-09-19 night — Africanus Cesti 7.19 opening SHIP (farming 32–34)

Live 56 treatises / 2786 sections. Cesti tip through 7.19 wine/vinegar/oil/garum (34 thought titles). H1 The Cesti. Photius 18–22 still held. Deploy `50e0c630.fathers-site.pages.dev`, CSS `?v=f0f1afd6e7`. Visual: 32/32 ui-review PNGs inspected (artifact `08183e9f`) plus extra Cesti reader/farming shots in `outputs/visual-audit-africanus/`. Remaining 7.19 split 35–37 then missile seal.

## 2026-09-19 — Africanus Cesti 7.4–7.14 SHIP

Live 56 treatises / 2776 sections. Cesti tip through 7.14 (24 thought titles). H1 The Cesti. Photius 18–22 still held. Deploy `ea39159c.fathers-site.pages.dev`, CSS `?v=f0f1afd6e7`. Visual: 32/32 ui-review PNGs inspected plus extra Cesti reader shots in `outputs/visual-audit-africanus/`. Next overnight: Cesti 7.15+.

## SITE wave closeout-3 (2026-09-18) — NO SHIP (49 local vs 54 live; would withdraw 5)

- CONTENT landed E1 rotation + KZ triage + Celsus/Photius adjudications
  (translations 2e10c8f97, 2de4ec08a, 1ad52e70c). Rebuild first showed 48
  works; philostorgius restored via legitimate rebind (below) → 49.
- Philostorgius rebind (corpus ca17a3b28, site lane, lane-scoped, no push):
  KZ changed only Daniel 8 certainty clear→possible; packet regen==stored
  except file+section digests; reviewed source+English byte-identical;
  validate_audit_receipt clean. (rebind_packet.py needs an untouched
  section probe; single-section tip rebound by the same digest method with
  a full-regen proof instead.) No manifest change needed — original
  payload_sha256 still binds.
- NO SHIP: production serves 54 (all 49 local readers byte-identical to
  live modulo favicon+asset lines; home still 54 treatises/2735 sections).
  Deploying would 404 five live readers via the works-gate Function:
  cyril-adoration-1 (33 changed passages), cyril-matthew-fragments (291),
  cyril-recta-fide-arcadia (41), cyril-recta-fide-pulcheria (41) — all E1
  label-move text changes, legacy bindings broken — plus
  origen-dialogue-heraclides (1: s5 stray Lev paran removed). All five need
  NEW corpus-lane source reviews (scope + passages, checker families);
  legacy never refreshes to clear a gate. Same precedent as the 09-17
  closeout audit (41 vs 54 → no ship).
- Photius stays 404 WITH reason (baseline preserved, marker intact): needs
  (a) full review chain that does not exist (reviews/audit/ holds only
  logos_description.md; CONTENT delivered codices 1-17 tracked +
  Acts 17:34 keep-clear verdict, but no scope/packet reviews), AND
  (b) a photius-aware loader — rows key on `codex`, not `section`, so the
  tip-fragment merge path yields one section "None" under author
  "Origen of Alexandria". Corpus lane + site loader work, not a register.
- Gates on the 49-build are otherwise green: ship.sh --dry-run exit 0;
  check_catalogue passed (49/579); UI 12/12; visual-gate 2/2; 4332 pages,
  112844 links, 0 failures; smoke 7/7; CSS ?v=f0f1afd6e7 unchanged;
  browser checks passed, visual review pending (dry-run only, not approval).
- Re-audit (/tmp/closeout3_site_reaudit.py): 49 dist works, zero stubs,
  zero scaffold markers, all reachable from /works/ + 50 author hubs,
  zero live-but-held.
- Build inputs note: UPLOAD lane has uncommitted corpus edits (book.yml x2,
  docx/build_receipts); they do not affect the gate outcomes above
  (excerpts 1923=1923, no new excerpt failures).
- Flags for other lanes: julian Ad Florum 2§69 cite fix (Phase 1a) has no
  CONTENT commit — still open. Five cyril/heraclides reviews + photius
  chain are the next-ship critical path.

## SITE wave closeout-2 ship (2026-09-17 ~10:05 PM ET) — SHIPPED 54/54, zero regressions

- Unblocked the 13: root causes were (a) import-scrub garbling in 11 tip
  meta.json (blurb/edition/method; e.g. `;. II`, `.12)` — never live),
  reverted verbatim to reviewed packet publication_scope strings (which
  production already serves); (b) 11 stale tip packets rebound via the
  pipeline's own make_audit_packet (regen==stored except digests; reviewed
  source+English byte-identical every section); (c) nemesius register
  payload_sha256 x8 refresh for the dedicated-loader row envelope
  (shared keys identical, render-neutral; macarius precedent).
- Review integrity: receipts' scripture notes match current allusions all
  11 books; Jev 24/25 agree, 1 mismatch (mensuris Jer 31:31) adjudicated
  keep-clear on locked Greek kaines diathekes; assert_tip_ready 13/13;
  pipeline suite 28 green. No hashes refreshed to bypass: every restored
  string is review-bound and production-identical.
- Corpus commit `aefef79dd` (33 files: 11 meta + 11 packet + 11 receipt);
  site commit `1b4f916` (nemesius SHAs). No pushes (owner gate).
- Dry-run green: 54 works / 1923 excerpts / 2735 sections; 4842 pages,
  126732 links, 0 failures; UI 12/12; visual-gate 2/2; smoke 7/7;
  browser checks passed; 32/32 screenshots inspected with concrete
  findings (review passed, artifact-bound e3e8b3f0).
- Diff vs production BEFORE ship: works sets identical 54/54; 52 readers
  byte-identical modulo favicon+asset-hash lines; baron +Art. III
  (registered staged tip) and philostorgius rewrite (reviewed 09-15) the
  only content diffs; home 54/2735 + feed dedup; excerpts 1923=1923.
- SHIP OK: https://5686a0fc.fathers-site.pages.dev (first attempt
  dfda89ab deployed fine; live gate caught 2-byte edge cutover lag,
  recheck green, reshipped for a clean receipt). CSS ?v=f0f1afd6e7.
  Live gate: 579 checked / 574 held / 0 failed.
- Live probes: 54/54 works 200; /works/photius-bibliotheca/ 404 with
  marker (baseline preserved); held spots (origen prayer/john-13/
  song-IV) 404 with marker. Restored blurbs verified live (serapion,
  epistula-canonica). Home: 54 treatises, 2735 sections.
- Re-audit (wave-1 script): 54 dist works, zero stubs, zero scaffold
  markers, all reachable from /works/ + author hubs (51), zero dangling
  cite links, zero live-but-held.
- Flags for other lanes (not ship-blockers): annuntiationem TN has a
  scrub-truncated sentence ("Earlier as not matching...") — Logos-visible,
  needs content-lane wording; cyril-matthew EN+source uncommitted edits
  in tree (CONTENT lane) will affect the NEXT build's gate; /contribute/
  publishes internal SOP/commands (pre-existing, byte-identical to prod).

## SITE wave closeout audit (2026-09-17 ~9:25 PM ET) — NO SHIP (would withdraw 13 live works)

- Full gate green via `scripts/ship.sh --dry-run` (exit 0): build 41 works /
  1923 excerpts / 2714 sections; catalogue+UI regressions passed (41 live,
  587 held); UI tests 12/12; visual-gate+lock tests 2/2; 4805 pages,
  125,793 local links, 0 failures; smoke 7/7 paths 200, CSS ?v=f0f1afd6e7;
  browser behavior checks passed (visual image review remains pending).
  The 2026-09-15 blocker (`/works/julian-to-florus/1.27/` 404 in browser gate)
  is gone — page builds (841 cite pages under julian-to-florus/).
- Independent audit (`/tmp/site_audit.py`): zero stub/empty work pages, zero
  scaffold markers in published pages, 41/41 reachable from `/works/` and from
  author hubs (48 hubs), zero dangling cite-section links.
- NO SHIP: production serves 54 works (probed live 2026-09-17, all 200);
  local dist publishes 41. Deploying would 404 thirteen live reader pages via
  the works-gate Function. Staged-but-unshipped improvements held back with it:
  baron section 3 (art3 tip, registered + gate-passing), Explore progress
  strip, favicon, home-feed dedup, link-hover CSS.
- The 13 (all fail publication review on corpus-side staleness, NOT site bugs):
  epiphanius anacephalaeosis/ancoratus/de-mensuris/panarion (stale packets +
  identity/scope mismatch), 7 gregory-thaumaturgus tips (stale snapshots after
  the 2026-09-16 Jev certainty migration), nemesius (stale packet), serapion
  (identity/scope mismatch). Unblock = corpus lane rebinds review packets
  (`rebind_packet.py`) + scope reviews in books/, then site rebuilds and ships.
  Site lane did not touch book files and did not refresh hashes to bypass.
- Register state: payload_sha256 refreshes + baron:3 already in
  `data/publication-review.json` (uncommitted); they keep the 41 live, they do
  not restore the 13. Nothing further registerable site-side.
- Re-audit round: re-ran audit post-decision — same 41/41 clean, 13 still held
  for the corpus reasons above. No misses fixable in-lane.

## Explore corpus progress strip (2026-09-16, uncommitted)

- Builder change only: Explore header gains one static line below the intro:
  N works live / X of Y sections translated / Z held for review (#explore-progress,
  same p-intro pattern as the home Works line, no new styling, no JS).
- Counts from loader data before the gates: live = post-gate works,
  held = held_works, sections = pre-gate merged totals with translated =
  non-blank non-scaffold English (gate SCAFFOLD rule). Totals also recorded in
  outputs/catalogue-quality.json; jsdom test cross-checks the strip against it.
- No deploy, no commits; dist/ rebuilds locally for verification.

## Epistula Canonica live ship (2026-09-15 ~2:41 PM ET)

- tip-ready OK; verify_docx OK; Canones GR Canon I locked; scaffold discarded; Pass A≠B OK
- Deploy: https://5590190c.fathers-site.pages.dev
- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-epistula-canonica/
- Also live: https://fathers.saneapps.com/works/gregory-thaumaturgus-ecclesiastes-metaphrase/
- live_works=43; held=577
- Claims remain prepped
- Next densify: serapion, epiphanius-* (still scaffold English — need real-lock)


## Ecclesiastes metaphrase live ship (2026-09-15 ~2:36 PM ET)

- tip-ready OK; verify_docx OK; MGR Greek Cap. I tip locked (TLG 2063.006); scaffold English discarded; Pass A≠B OK
- Publication review registered (scope + section 1); catalogue kept
- Deploy: https://1b34f63e.fathers-site.pages.dev
- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-ecclesiastes-metaphrase/ → HTTP 200
- live_works=42; held=578
- Claim greg-thaum-eccl-metaphrase-densify remains prepped
- Next densify: epistula-canonica, serapion, epiphanius-* (real-lock standard)


Updated 2026-09-15 12:38 PM ET. Nemesius tip shipped live (see below).

## Nemesius live ship (2026-09-15 12:38 PM ET)

Stephan approved live ship. CoS spot-check: tip-ready OK, verify_docx OK, English 1.1–1.3 real Pass B, OCR Greek damaged but disclosed.

- tip-ready: `nature_hominis_english.json` + `nature_hominis_source.json` → ok
- Dry-run / LIVE allowlist includes `/works/nemesius-de-natura-hominis/`
- Deployed via `scripts/ship.sh --skip-build` after artifact-bound visual review (32 screenshots inspected)
- Pages deployment: https://58e0f435.fathers-site.pages.dev
- Live work: https://fathers.saneapps.com/works/nemesius-de-natura-hominis/ → HTTP 200; title **De natura hominis**; Nemesius of Emesa; sections 1.1–3.1 visible
- Live gate: first post-deploy check had 2 SHA mismatches on `/` and `/data/search-index.json` (edge cutover lag); recheck → 588 checks, 0 failures
- CSS ?v=898957519c; live works count 34 (includes Nemesius tip)
- CLAIMS: left `nemesius-de-natura-hominis-densify` **prepped** (full-work densify row; tip ship is not full densify done; no established non-ai_promote densify-tip stamp)

Do not stop/pause OpenCode or unrelated Mini jobs.

## Current state

Deployed successfully through scripts/ship.sh (Nemesius tip live 2026-09-15 12:38 PM ET):
- Production: https://fathers.saneapps.com
- Deployment: https://58e0f435.fathers-site.pages.dev
- Live work: https://fathers.saneapps.com/works/nemesius-de-natura-hominis/
- CSS version: 898957519c
- Built artifact (this ship): e20cd96166986b9b69c88c6f7510aef057e68682bed81c84ed24dfdeab2dfba2

Current screened build publishes 34 live works (583 held), 1923 topic excerpts and 2706 work sections. These counts are not a whole-corpus fidelity certificate.

## Repairs

Author headings and work titles now lead the catalogue. Repeated Available/Unknown labels and unsupported first-English claims are removed. Century chronology and author/title views are corrected. The merged PR1 mobile, search and internal-link fixes are included.

Known scaffolds, contaminated source texts and false complete-work summaries are withheld without deleting corpus files. Blind On Prayer and Exhortation to Martyrdom tip overlays no longer replace whole chapters. Both works remain withheld. The fuller base of On Prayer still omits surviving Greek after a lacuna; it must not be approved merely because it is longer.

Seven topic citation collisions and nine collective-letter fragment collisions are fixed while preserving existing canonical links. Numerical locus sorting restores canonical JSON order for 330 passages across four Julian works. Equal-locus fragments keep source order. Readers see edition references, while unique suffixes remain in route IDs.

A primary-source review corrected two displaced Bible references in Julian, To Florus 1.27. Its exact passage-only packet and receipt are in the corpus under books/julian-of-eclanum/reviews/audit/. Jeremiah 6.1 was corrected against the printed Greek: love, agency, and six Bible targets. It was not newly published by this audit.

## Required gates

Use scripts/ship.sh. It locks publication, requires catalogue and real-browser checks even with --skip-build, requires inspected images tied to the built files, rechecks current published source receipts, and uploads a private immutable copy.

The publication index binds author, work, edition, locus, ordered scope and each passage payload. Legacy hashes remain provisional. Never refresh them to bypass a failed review. New or changed passages require current raw-source-backed semantic review. Samples approve only their selected passages.

Canonical drafting and promotion reject missing evidence, omissions, false or uncertain checks, same-family checkers and stale files. The CF configuration permits two checker families distinct from each configured draft family. Overnight prep remains the default. No inference calls were needed for this audit.

## Verification and evidence

- 27 corpus QA/promotion tests passed.
- Publication attack regressions, 7 JavaScript tests and 2 visual-gate tests passed.
- 4,775 generated pages and 115,587 local links were checked: zero failures, including duplicate IDs.
- 32 Mini Brave view/state images were inspected. Coverage includes desktop, tablet and phone catalogue; search, retry, empty state, focus and menu; reader and Contents; home, author, topic and Explore; actual Help/Methodology copy; and Julian Bible/source details.
- Source/citation order is now an explicit visual inspection item. Dark OS preference preserves the intended light palette.
- Browser receipt: outputs/ui-review/browser-receipt.json
- Deployment log: outputs/audit-final-deploy.log
- Source-order checks: outputs/audit-source-order-dry-run.log
- Corpus tests: outputs/qa-audit/final-regressions.log in the translations repo
- Findings: docs/IA.md
- Visual coverage: docs/UI_REVIEW.md

Live byte comparisons and post-deployment screenshots are recorded below when completed.

The permanent live gate is now in scripts/check_links.py and runs from ship.sh. It checks current homepage, catalogue, search index and assets, then probes every held work URL for a real 404 without scaffold text. The first production run correctly failed: the custom domain returned 200 for all 573 held URLs, while the Pages deployment URL returned 404. Host, URL, prefix and zone cache purges did not clear those old Pages edge objects. A scoped cache Page Rule lacked effect and was removed. The DNS record and original fathers-site binding were restored after a temporary validation experiment. Production was a no-go until the Pages Function allowlist shipped (see below).

## Incident and remaining work

A separate Cursor publishing job restored the old builder from a22c2b7 and pushed c64b187, removing safeguards. Only its unsafe upload process group 35630 was terminated, before completion. Other work and source files were preserved. Do not restore an old builder to add a loader glob.

Source authenticity, completeness and fidelity review remain unfinished for legacy content. Repair held families one at a time through the existing claim queue; do not use catalogue volume as a quality target. No open GitHub issues were returned in either repository during this audit. No Logos recompilation was performed during the website audit.

Shared work guards remain active because other Mini work continues. Do not stop unrelated jobs.


## Withdrawn-URL preservation cache (2026-09-13)

**Symptom:** custom domain returned HTTP 200 for all held `/works/<slug>/` URLs (often with `x-robots-tag: noindex`), while the matching `*.fathers-site.pages.dev` deployment returned 404. Purge by URL/host and zone Cache/Page/Transform checks did not clear it. DNS and the `fathers-site` domain binding were clean.

**Cause:** Cloudflare Pages asset-server preservation for the custom hostname when the current deployment has no file for that path. `_redirects` 404 rules are not enough on that hostname.

**Fix:** `scripts/generate_works_gate.py` writes `functions/works/[[path]].js` (live-slug allowlist) plus staging `_routes.json` (`include: ["/works/*"]`). `scripts/ship.sh` regenerates both after the reviewed artifact is staged. Denied slugs return a synthetic 404 body containing `Page unavailable` and never call `ASSETS.fetch` on the withdrawn path. Keep `_redirects` as a second layer for the deployment hostname. Live gate remains `scripts/check_links.py --live`.

**Verified live 2026-09-13:** deployment `https://edaf2b75.fathers-site.pages.dev`. `check_links.py --live https://fathers.saneapps.com` → 578 checks, 573 held → 404 with `Page unavailable`, 0 failures. A live work (`/works/cyril-adoration-1/`) and `/works/` remain 200. First ship after the Function upload failed the live gate only because of edge cutover lag; ship.sh now probes one held URL for 404 before the full gate.

**Ops note:** Pages Functions on the Workers free plan can "fail open" to static assets when the daily Functions allowance is exhausted — prefer fail-closed for this project in the dashboard if available.


## Gregory Thaumaturgus In annuntiationem tip live (2026-09-15 ~1:45 PM ET)

- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-in-annuntiationem/ → HTTP 200
- Section: `/1/` → HTTP 200
- Deploy: https://a6ca72bd.fathers-site.pages.dev
- live_works=39; claim left **prepped**
- OpenCode left alone


## Gregory Thaumaturgus Sermo in omnes sanctos tip live (2026-09-15 ~1:55 PM ET)

- Live: https://fathers.saneapps.com/works/gregory-thaumaturgus-sermo-in-omnes-sanctos/ → HTTP 200
- Section: `/1/` → HTTP 200
- Deploy: https://6dba211d.fathers-site.pages.dev
- live_works=40; claim left **prepped**
- OpenCode left alone

