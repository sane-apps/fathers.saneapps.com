# Via Patrum wrap-up plan (2026-10-14)

Three read-only audits ran on 2026-10-14: the live site (`outputs/wrapup-audit-20261014/site/`, 59 screenshots,
every page link-checked), every published work (`.../content/matrix.json`), and every
background job plus model spend (`.../jobs/`). This plan orders what is left by reader
impact and cost. Spend is capped at $150 a day (`clients/translations/scripts/spend_guard.py`).

## Where things stand

- 332 works live; 284 pass every check a reader would notice. No broken internal
  links in 14,727 pages, no console errors, no sideways scroll on phones.
- Cloudflare grant: about $5,500 left. Spend ran about $388 a day; at the new cap
  it lasts about five weeks instead of two.
- 577 of 841 book folders are not published: 303 held by the pipeline, 175 draft
  scaffolds, 61 never loaded, 38 other.

## Done today

1. Paid shelf: assemble had failed since Oct 9 (a 2.65 GB era zip over the 2 GB
   cap). Cyril of Alexandria now has his own zip; all six fit. The rebuild resumes
   each auto-ship run.
2. Spending cap on every Workers AI job. Lanes stop at 80% of it, between sections.
3. Crash loop stopped: le Blanc's Theses crashed 60 times; repeat crashes now park
   a book, and huge briefs are cut to size.
4. Beliefs job: the broker ran 8-day-old code; restarted, and the watch now
   restarts it on code changes.
5. Held review retries daily after a failed week; Logos names its real fault.
6. Alerts: open alerts repeat on the Air, and a daily email goes out while any
   job has been stuck a day or more.
7. Cyril, On Adoration books 11-16 held: word-for-word Greek was live as English.

## Owner decisions needed

1. **Logos:** allow Accessibility for `/usr/bin/osascript` on the Mini (System
   Settings > Privacy & Security > Accessibility > +). Without it the weekly Logos
   build can never run unattended. 70 books are ready to build.
2. **Le Blanc's Theses:** 412 sections read as notes, not English, and only 16% is
   narrated. Hold it (free), or re-translate those sections and then re-record
   (about $45 for the audio plus the translation run).
3. **The daily cap:** $150 is a starting figure. Raise it to finish faster, lower it
   to stretch the grant.
4. **934 older excerpts** with no reader: keep or hide (open since Oct 7).
5. **Three new works** (Athanasius On the Incarnation, Didache, 1 Clement) already
   exist as held books. Use those, or import the staged public-domain texts.

## Phase 1: free builder and copy pass (one ship, no credits)

Each item is a builder or data edit; the ship's own gates check it.

| # | Fix | Size |
|---|-----|------|
| 1 | Styled 404 for bad `/works/` and `/authors/` URLs (the gate Function serves a bare page) | S |
| 2 | 72 excerpt pages end with `******` and an editor's summary that reads as the Father's words | S |
| 3 | Cyprian has two author hubs (`cyprian`, `cyprian-of-carthage`) | S |
| 4 | Footer has no Privacy link | S |
| 5 | Counts disagree: home says 332 read aloud, 325 audiobooks exist; Downloads gives 319 and 317, 240 and 239 | S |
| 6 | Titles: "Letters (fragments)", "Answers to Questions (a fragment)", two "Fragments on Lamentations", "... by Acts of the Martyrs" | S |
| 7 | Dates: "244 CE" (Origen Notes on Numbers), "AD 180" on Creeds; Diognetus author "Anonymous" on Works but "Mathetes" elsewhere | S |
| 8 | Timeline shows research notes: "Each is queued" (98 pages), "Being searched" (74), OCR and download remarks | M |
| 9 | 16 Wesley sermons: the opening verse is read from the heading, so the audio drain calls the page "not English" | S |
| 10 | 261 works have no topic links (`WORK_TOPICS`) | M |
| 11 | `/explore/churches/` keeps the old crowded design (273 labels under 12 px) | M |
| 12 | Polish: repeated click-a-sentence hint, 9-10 px Timeline labels on phones, "early church", To Florus hub lists its books twice | S |

Worksheet text inside certified English (`[T-ILLEGIBLE ...]` in On Prayer 5,
`[transition to ch. XIV damaged ...]`, `[?]`, "the locked Greek" in Origen's
Psalms excerpts, stray `||` and `***`) cannot be edited in place: changing
certified English breaks its receipt and drops the work. Fix these through the
recert path, a few sections each.

## Phase 2: one cheap model batch (credits, small)

- Reader headings that read as notes, in 60 works (worst: Cyril On Adoration,
  Placeus, le Blanc).
- A real summary line for 93 works whose search snippets read "Fragmenta in
  Jeremiam (Greek)", and the 9 certified books with no blurb.

## Phase 3: audio

- After Spark's 328/328 certification pass: re-voice the 4,482 quotation
  sentences in 157 works in each work's own narrator (about $27).
- Masters cleanup: upload the two .m4b masters, then remove 1.97 GB of local
  copies ($0).
- Le Blanc per decision 2.

## Phase 4: translation backlog, inside the cap

- The weekly held review is the main lever: 341 parked books wait on it, and the
  Oct 4 run released 329 sections. Next run: tomorrow 04:30.
- Lanes keep working within the cap. Cyril On Adoration 11-16 need a
  re-translation before release.
- 216 live works carry "not yet re-checked"; the lanes clear these over weeks.

## Order

1. Decisions 1-3 (minutes for the owner).
2. Phase 1 as one ship, after the paid shelf finishes.
3. Phase 2 batch.
4. Phase 3 after Spark's certification pass.
5. Phase 4 runs on its own under the cap; the daily email reports anything stuck.

## Status, 2026-10-14 midday (Claude)

Phase 1 is built on branch `cleanup-20261014` and merged as one ship. Done:
styled 404 and working author redirects on the gate; editor glosses off 74
excerpts; one Cyprian page; Privacy in the footer and the app linked; zip
counts rebuilt when a kept zip lacks books; text authors are not bylines; the
two fragment titles; AD/BC in intros and on Creeds; Mathetes on Works;
Timeline gap notes reader-facing, labels 11 px or more; Wesley verse pages
get Play; builder notes off era banners; reader hint once per page; "early
Church"; Listen gives the real audiobook count; Nicaea label no longer on the
300 tick; translator gap notes in source panels show as a lacuna; repeated
scrap sections dropped. Topic links for 241 works (`data/work-topics.json`),
summary lines for 103 (`data/work-blurbs.json`), plain headings for 337
sections (`data/section-titles.json`), all written by reading each work.

Held (FORCED_WITHHOLD): Cyril On Adoration 11-16 (word-for-word Greek);
origen-lamentationes-fragments (second copy of Lamentations);
diodorus-fragmenta (Dionysius of Corinth's letters under Diodorus's name);
origen-apocalypse-scholia-scrap (Origen's letter from Eusebius 6.19, not
Apocalypse notes); olympiodorus-contra-severum (a heading, no text).

Still open, found on the way:
- Placeus: section 628 has no translation (only a note); cut-off first words
  ("Ince", "eny", "nswer") and repeats ("and heart." x3 in 22, "blood" x3 in
  691); about 14 more shorthand headings (153, 155, 168, 171, 193 ...).
- hesychius-homilia-i-lazarum: the text (Bethlehem and Zion, James at the
  council) does not match the title; check the source.
- origen-lamentations-fragments: "About this text" is the Jeremiah/1 Samuel
  book's intro (shared book folder).
- theophilus-alex-fragmenta-joannem cites John 3 for words from John 9.
- About 1,600 compact semicolon headings remain ("Lift hands by good works;
  infants faint without the Word"); readable, left as they are.
- /explore/churches/ restyle needs an owner-approved sketch (UI gate).
- Audiobook masters: upload to private `backup/` through the admin route after
  this ship, then free about 4 GB of local copies (AUDIO_CLEANUP_HANDOFF).


## Resume note (Claude restart, 2026-10-14 afternoon)
- The two background waiters (cleanup-live watcher, ship-failure watcher) died with the session. On resume, check by hand:
  https://viapatrum.org/about/ shows the Privacy footer link (= cleanup + churches redesign live), and the tail of
  ~/Library/Logs/SaneApps/fathers-ship-auto.log for SHIP OK / failures. Then do the "After the cleanup is live" list.
- SaneCite marketing work from the same session: outputs/sanecite-phase2-full-20261013/outreach/PLAN.md.

## Owner decisions, 2026-10-15
Owner: "wrap things up as cleanly as possible. I dont want to do new work until we see some sales. Just polish
and finish anything thats pending that could use it."
- Logos Accessibility: no longer needed; the job runs through Terminal (logos-build-automation memory).
- Le Blanc's Theses: HOLD. No re-translation or re-recording. SUPERSEDED same day: finish it (see below).
- Daily cap: keep $150.
- 934 (now 914) older excerpts: KEEP as they are. Hiding them would remove 914 public pages and their links;
  that is a site change, not polish. Revisit after sales.
- Three new works: DEFERRED (new work). SUPERSEDED same day: they exist as held books, so finish them.
- Orphan R2 key bundles/via-patrum-audiobooks-5-after-chalcedon.zip: leave it (no cost to speak of).
- Still to do as polish: Placeus s628, hesychius-homilia-i-lazarum title/text, origen-lamentations-fragments
  About text, theophilus John 3 vs John 9; Logos queue finishes on its own (9 builds, 24 uploads at 04:00).

## Finish list, worked 2026-10-15 (owner: "improve, fill in, polish, finish ... nothing wasted")
Done today:
- Davenant 671/673/709 and Strimesius 622 fixed against the Latin (translations 17def664b): the 4 sections that held
  both works (about 1,540 sections) now pass check_pass_ab --tip-ready. Verify both live after the next ship.
- 8 Logos covers painted; the painter now compiles to outputs/bin on demand, catch-up paints missing covers
  (3ac1c4e74, 58ef470ee; 38 Logos tests pass). The 8 upload in the 04:00 run.
- 14 summaries (work_blurb) for certified works that had none (73b92a99e).
- Lamentations About text, Hesychius James/David title (cdc007e), Theophilus John 9:3 note (1af751462).
- The 2 title-rule works were already fixed in an earlier ship.
Runs on its own (check results, do not re-queue by hand):
- Placeus 32 held sections, Marcellus 4, Didymus Romans, Evagrius, Origen Philocalia/Romans/Letters: held for
  "confirmed problems after 3 repairs"; the daily held review judges them. Origen De Principiis needs source.
- Macarius homilies, Origen Ezekiel, pseudo-Cyprian: FORCED_WITHHOLD _RECERT; unpublished lanes C/E re-run them.
- Logos: 9 builds (incl. the 2 Gregory books that failed on row-finding) and 24 uploads at 04:00 (aa903a7df fix).
Owner, later 2026-10-15: "think of via patrum as improve, fill in, polish finish. so what we have is useable and
complete. nothing wasted", then "good do all in order". So these get finished inside the $150/day cap: le Blanc 412 note sections (~$45 audio after translation),
Cyril On Adoration 10-16 re-translation, the three new works (held books exist), quote re-voicing (~$27).
