#!/usr/bin/env python3
"""Build fathers.saneapps.com static site from translations books."""
from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from html import escape
from pathlib import Path

try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML required") from e

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ASSETS = ROOT / "assets"


def _asset_version() -> str:
    import hashlib

    h = hashlib.md5()
    for p in sorted(ASSETS.glob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()[:10]


ASSET_VER = _asset_version()
BOOKS = Path.home() / "SaneApps/clients/translations/books"
TOPICS_BOOK = BOOKS / "ante-nicene-topics"
ORIGEN_BOOK = BOOKS / "origen-prayer-martyrdom"
ORIGEN_BOOK2 = BOOKS / "origen-heraclides-pascha"
ORIGEN_BOOK3 = BOOKS / "origen-jeremiah-samuel"
CYRIL_BOOK = BOOKS / "cyril-alexandria"
CYRIL_BOOKS = sorted(BOOKS.glob("cyril-alexandria*"))
JULIAN_BOOK = BOOKS / "julian-of-eclanum"
EXPLORE_DATA = ROOT / "data" / "explore"
SPONSORS = "https://github.com/sponsors/MrSaneApps"
SITE_NAME = "Fathers"
SITE_TAG = "Fathers reading — topics and whole works"
BASE = ""

# Work ↔ topic cross-refs (topic ids from ante-nicene-topics/topics.yml).
WORK_TOPICS: dict[str, list[str]] = {
    "origen-on-prayer": ["liturgy-prayer"],
    "origen-exhortation-to-martyrdom": ["martyrdom-witness"],
    "origen-dialogue-heraclides": [
        "father-son-spirit",
        "incarnation-word-flesh",
        "two-natures-seed",
    ],
    "origen-on-pascha": [
        "old-and-new",
        "hermeneutics-types",
        "passion-resurrection",
        "eucharist-thanksgiving",
    ],
    "origen-homilies-jeremiah": [
        "gifts-and-order",
        "hermeneutics-types",
        "old-and-new",
        "discipline-penance",
        "sin-and-death",
        "incarnation-word-flesh",
    ],
    "julian-to-florus": [
        "free-will",
        "sin-and-death",
        "grace-and-assistance",
        "image-likeness",
        "faith-and-obedience",
    ],
    "julian-turbantius-fragments": [
        "free-will",
        "sin-and-death",
        "grace-and-assistance",
    ],
    "julian-marriage-extracts": ["sin-and-death", "image-likeness"],
    "julian-letter-to-rome": ["free-will", "grace-and-assistance"],
    "julian-collective-letter": ["free-will", "grace-and-assistance", "sin-and-death"],
}


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "x"


def eng_list(val) -> list[str]:
    if val is None:
        return []
    if isinstance(val, str):
        return [val]
    if isinstance(val, list):
        out = []
        for x in val:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, list):
                out.extend(str(y) for y in x)
        return out
    return [str(val)]


def soft_snippet(text: str, limit: int = 280) -> str:
    """Trim for preview cards: prefer sentence, else word boundary + ellipsis."""
    t = re.sub(r"\s+", " ", (text or "").strip())
    if len(t) <= limit:
        return t
    cut = t[: limit + 1]
    # Prefer ending on a sentence if one fits in the window
    for sep in (". ", "; ", "? ", "! "):
        i = cut.rfind(sep)
        if i >= int(limit * 0.45):
            return cut[: i + 1].rstrip()
    i = cut.rfind(" ")
    if i >= int(limit * 0.55):
        return cut[:i].rstrip(" ,;:—-") + "…"
    return t[:limit].rstrip() + "…"


def period_key(p: str | None) -> str:
    if not p:
        return "9999"
    m = re.search(r"(\d{3,4})", p)
    return m.group(1) if m else "9999"


def year_from_period(p: str | None) -> int | None:
    if not p:
        return None
    m = re.search(r"(\d{3,4})", p)
    return int(m.group(1)) if m else None


def era_band(year: int | None) -> str:
    if year is None:
        return "Unknown"
    if year < 150:
        return "Apostolic"
    if year < 325:
        return "Ante-Nicene"
    if year < 451:
        return "Nicene"
    return "Post-Nicene"


def _json_load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_explore_raw() -> dict:
    """Merge core Explore files with optional *_expansion.json drafts."""
    claims = _json_load(EXPLORE_DATA / "claims.json", [])
    stances = _json_load(EXPLORE_DATA / "stances.json", [])
    contrast = _json_load(EXPLORE_DATA / "contrast.json", [])
    ruptures = _json_load(EXPLORE_DATA / "ruptures.json", [])

    seen_topics = {c.get("topic") for c in claims if isinstance(c, dict)}
    for block in _json_load(EXPLORE_DATA / "claims_expansion.json", []):
        if isinstance(block, dict) and block.get("topic") and block["topic"] not in seen_topics:
            claims.append(block)
            seen_topics.add(block["topic"])

    seen_stance = {
        (s.get("ref"), s.get("topic"), s.get("claim_id"))
        for s in stances
        if isinstance(s, dict)
    }
    for row in _json_load(EXPLORE_DATA / "stances_expansion.json", []):
        if not isinstance(row, dict):
            continue
        key = (row.get("ref"), row.get("topic"), row.get("claim_id"))
        if key in seen_stance:
            continue
        stances.append(row)
        seen_stance.add(key)

    seen_rupture = {r.get("topic") for r in ruptures if isinstance(r, dict)}
    for row in _json_load(EXPLORE_DATA / "ruptures_expansion.json", []):
        if isinstance(row, dict) and row.get("topic") and row["topic"] not in seen_rupture:
            ruptures.append(row)
            seen_rupture.add(row["topic"])

    seen_contrast = {c.get("author_slug") for c in contrast if isinstance(c, dict)}
    for card in _json_load(EXPLORE_DATA / "contrast_expansion.json", []):
        if not isinstance(card, dict):
            continue
        slug = card.get("author_slug")
        if slug and slug in seen_contrast:
            # Append only new point ids onto the existing author card.
            host = next(c for c in contrast if c.get("author_slug") == slug)
            have = {p.get("id") for p in host.get("points") or []}
            for p in card.get("points") or []:
                if p.get("id") not in have:
                    host.setdefault("points", []).append(p)
                    have.add(p.get("id"))
            continue
        contrast.append(card)
        if slug:
            seen_contrast.add(slug)

    return {
        "claims": claims,
        "stances": stances,
        "contrast": contrast,
        "ruptures": ruptures,
    }


def load_authors() -> dict[str, dict]:
    data = _json_load(TOPICS_BOOK / "authors.json", {})
    return data.get("authors") or {}


AUTHORS = load_authors()


def author_sort_year(name: str | None, period: str | None = None) -> int:
    rec = AUTHORS.get(name or "") or {}
    if rec.get("sort_year"):
        return int(rec["sort_year"])
    y = year_from_period(period)
    return y if y is not None else 9999


def _plain_tag(s: str) -> str:
    return (s or "").replace("-", " ").replace("_", " ").strip().title()


def build_explore_index(
    excerpts: list[dict],
    works: list[dict],
    topic_meta: dict[str, dict],
) -> dict:
    """Merge stance tags with library points for /explore/."""
    raw = load_explore_raw()
    by_excerpt = {x["id"]: x for x in excerpts if x.get("id")}
    works_by_slug = {w["slug"]: w for w in works}
    section_lookup: dict[str, dict] = {}
    for w in works:
        for s in w["sections"]:
            section_lookup[f"{w['slug']}/{s['section']}"] = {
                "work": w,
                "section": s,
            }

    points: list[dict] = []
    authors: dict[str, str] = {}

    for row in raw["stances"]:
        ref = row["ref"]
        topic = row["topic"]
        year = row.get("year")
        if ref.startswith("excerpt:"):
            eid = ref.split(":", 1)[1]
            x = by_excerpt.get(eid)
            if not x:
                continue
            author = x.get("author") or "Unknown"
            slug = slugify(author)
            if "origen" in author.lower():
                slug = "origen"
            if "julian" in author.lower():
                slug = "julian-of-eclanum"
            year = year or year_from_period(x.get("period"))
            authors[slug] = author
            points.append(
                {
                    "id": ref,
                    "kind": "excerpt",
                    "ref": ref,
                    "topic": topic,
                    "claim_id": row["claim_id"],
                    "stance": row["stance"],
                    "year": year,
                    "century": (year // 100) * 100 if year else None,
                    "era_band": era_band(year),
                    "author": author,
                    "author_slug": slug,
                    "period": x.get("period"),
                    "title": x.get("citation") or eid,
                    "citation": x.get("citation"),
                    "href": f"/e/{eid}/",
                    "snippet": soft_snippet(" ".join(eng_list(x.get("english")))),
                    "note": row.get("note"),
                }
            )
        elif ref.startswith("work:"):
            key = ref.split(":", 1)[1]
            hit = section_lookup.get(key)
            if not hit:
                continue
            w, s = hit["work"], hit["section"]
            year = year or year_from_period(w.get("period"))
            authors[w["author_slug"]] = w["author"]
            points.append(
                {
                    "id": ref,
                    "kind": "work",
                    "ref": ref,
                    "topic": topic,
                    "claim_id": row["claim_id"],
                    "stance": row["stance"],
                    "year": year,
                    "century": (year // 100) * 100 if year else None,
                    "era_band": era_band(year),
                    "author": w["author"],
                    "author_slug": w["author_slug"],
                    "period": w.get("period"),
                    "title": s.get("head") or key,
                    "citation": s.get("head"),
                    "href": f"/works/{w['slug']}/{s['section']}/",
                    "snippet": soft_snippet(" ".join(eng_list(s.get("english")))),
                    "note": row.get("note"),
                }
            )

    for card in raw["contrast"]:
        authors[card["author_slug"]] = card["author"]
        for p in card.get("points") or []:
            year = p.get("year") or card.get("year")
            points.append(
                {
                    "id": f"contrast:{p['id']}",
                    "kind": "contrast",
                    "ref": f"contrast:{p['id']}",
                    "topic": p["topic"],
                    "claim_id": p["claim_id"],
                    "stance": p["stance"],
                    "year": year,
                    "century": (year // 100) * 100 if year else None,
                    "era_band": card.get("era_band") or era_band(year),
                    "author": card["author"],
                    "author_slug": card["author_slug"],
                    "period": card.get("period"),
                    "title": p.get("citation") or p["id"],
                    "citation": p.get("citation"),
                    "href": None,
                    "summary": p.get("summary"),
                    "disclaimer": card.get("disclaimer"),
                    "note": p.get("note"),
                }
            )

    topics_out = []
    for block in raw["claims"]:
        tid = block["topic"]
        title = block.get("title") or (topic_meta.get(tid) or {}).get("title") or tid
        topics_out.append(
            {
                "id": tid,
                "title": title,
                "claims": block.get("claims") or [],
            }
        )

    eras = []
    for band in ("Apostolic", "Ante-Nicene", "Nicene", "Post-Nicene", "Unknown"):
        if any(p.get("era_band") == band for p in points):
            eras.append(band)

    author_list = [{"slug": s, "name": n} for s, n in sorted(authors.items(), key=lambda kv: kv[1].lower())]

    return {
        "version": 1,
        "model": "topic-river",
        "disclaimer": (
            "Stance tags are editorial readings of the English and sources for study — "
            "not an orthodoxy score. Contrast cards mark writers not yet fully in the library."
        ),
        "topics": topics_out,
        "ruptures": raw["ruptures"],
        "eras": eras,
        "authors": author_list,
        "points": points,
    }


def load_topics_taxonomy() -> dict:
    return yaml.safe_load((TOPICS_BOOK / "topics.yml").read_text())


def load_topic_excerpts() -> list[dict]:
    items = []
    tdir = TOPICS_BOOK / "translations" / "topics"
    for path in sorted(tdir.glob("*.json")):
        data = json.loads(path.read_text())
        rows = data if isinstance(data, list) else data.get("excerpts", [])
        for x in rows:
            if not isinstance(x, dict) or not x.get("id"):
                continue
            x = dict(x)
            x["_source_file"] = path.name
            items.append(x)
    return items


def _section_sort_key(sec: str):
    if sec == "proem":
        return (0, 0, 0)
    parts = sec.split(".")
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            return (2, sec, 0)
    while len(nums) < 3:
        nums.append(0)
    return (1, nums[0], nums[1], nums[2])


def _source_rows(raw) -> list[dict]:
    """Accept a bare section list or a {sections: [...]} wrapper."""
    if isinstance(raw, list):
        return [s for s in raw if isinstance(s, dict)]
    if isinstance(raw, dict):
        for key in ("sections", "fragments", "rows"):
            rows = raw.get(key)
            if isinstance(rows, list):
                return [s for s in rows if isinstance(s, dict)]
    return []


def _text_history_from_meta(meta: dict) -> dict:
    """Prefer nested text_history; else lift method/witnesses/joins from meta root."""
    th = meta.get("text_history")
    if isinstance(th, dict) and th:
        return th
    lifted = {
        k: meta[k]
        for k in ("method", "witnesses", "joins")
        if k in meta and meta.get(k) not in (None, "", [])
    }
    return lifted


_BIBLE_LOCUS_TITLE = re.compile(
    r"^(On )?(Matthew|Mark|Luke|John|Acts|Romans|Genesis|Exodus)\s+\d+",
    re.I,
)
_CPG_TITLE = re.compile(r"^CPG\s+\d+", re.I)


def _matthew_ref_sort_key(matthew, fragment, section) -> tuple:
    nums = [int(x) for x in re.findall(r"\d+", str(matthew or ""))]
    ch = nums[0] if nums else 999
    vs = nums[1] if len(nums) > 1 else 0
    try:
        sec = int(section)
    except (TypeError, ValueError):
        sec = 0
    fr = int(fragment) if fragment is not None else sec
    return (0, ch, vs, fr, sec)


def _reader_title_from_matthew(matthew: str | None) -> str:
    raw = (matthew or "").strip()
    if not raw:
        return ""
    ref = re.sub(r"(?<=\d)-(?=\d)", "–", raw)
    return f"Matthew {ref}"


# Treatises with no earlier complete English a reader could freely use.
# Julian is omitted: some of his words already sit in Victorian Augustine translations.
FIRST_ENGLISH_NOTES: dict[str, str] = {
    "origen-on-prayer": (
        "This treatise had no earlier complete English a reader could freely use. "
        "The English here is new."
    ),
    "origen-exhortation-to-martyrdom": (
        "This treatise had no earlier complete English a reader could freely use. "
        "The English here is new."
    ),
    "origen-dialogue-heraclides": (
        "This dialogue had no earlier complete English a reader could freely use. "
        "The Greek was recovered in the 1940s. The English here is new."
    ),
    "origen-on-pascha": (
        "This treatise had no earlier complete English a reader could freely use. "
        "The Greek was recovered in the twentieth century. The English here is new."
    ),
    "cyril-adoration-1": (
        "Cyril’s long work On Adoration (seventeen books) has never had a complete English. "
        "This is Book 1 only. The English here is new."
    ),
    "origen-homilies-jeremiah": (
        "These Greek homilies had no earlier complete English a reader could freely use. "
        "This page is Homilies 1–2 only. The English here is new."
    ),
}

WITNESS_ROLE_LABEL = {
    "copy-text": "Copy-text",
    "check": "Checked print",
    "version": "Ancient version",
    "fragments": "Fragments",
}


def text_history_html(th: dict | None) -> str:
    """Collapsed About block: copy-text, checks, and real joins only."""
    if not isinstance(th, dict) or not th:
        return ""
    bits: list[str] = []
    method = str(th.get("method") or "").strip()
    if method:
        bits.append(f'<p class="intro">{escape(method)}</p>')
    witnesses = th.get("witnesses") or []
    if isinstance(witnesses, list) and witnesses:
        items = []
        for wtn in witnesses:
            if not isinstance(wtn, dict):
                continue
            role_key = str(wtn.get("role") or "").strip()
            role = WITNESS_ROLE_LABEL.get(role_key, role_key.replace("-", " ").title())
            name = str(wtn.get("name") or "").strip()
            if not name:
                continue
            cov = str(wtn.get("coverage") or "").strip()
            lang = str(wtn.get("language") or "").strip()
            url = str(wtn.get("url") or "").strip()
            label = escape(name)
            if url:
                label = f'<a href="{escape(url)}" rel="noopener">{label}</a>'
            extra = " · ".join(x for x in (lang, cov) if x)
            extra_h = f' <span class="wit-extra">({escape(extra)})</span>' if extra else ""
            items.append(
                f'<li><span class="role">{escape(role)}</span> {label}{extra_h}</li>'
            )
        if items:
            bits.append(
                '<p class="intro fine">Witnesses</p>'
                f'<ul class="witness-list">{"".join(items)}</ul>'
            )
    joins = th.get("joins") or []
    if isinstance(joins, list) and joins:
        items = []
        for j in joins:
            if not isinstance(j, dict):
                continue
            note = str(j.get("note") or "").strip()
            if not note:
                continue
            where = str(j.get("where") or "").strip()
            loc = f'<span class="where">{escape(where)}</span> — ' if where else ""
            items.append(f"<li>{loc}{escape(note)}</li>")
        if items:
            bits.append(
                '<p class="intro fine">Where the prints differ</p>'
                f'<ul class="join-list">{"".join(items)}</ul>'
            )
    if not bits:
        return ""
    return f'<div class="text-history">{"".join(bits)}</div>'


def _pack_work(
    *,
    slug: str,
    title: str,
    author: str,
    author_slug: str,
    period: str,
    status: str,
    edition: str,
    sections: list[dict],
    blurb: str = "",
    era_note: str = "",
    groups: list[dict] | None = None,
    first_english: bool | None = None,
    first_english_note: str = "",
    text_history: dict | None = None,
) -> dict:
    if sections and any(s.get("sort_key") is not None for s in sections):
        sections = sorted(
            sections,
            key=lambda s: s.get("sort_key") or _section_sort_key(str(s["section"])),
        )
    else:
        sections = sorted(sections, key=lambda s: _section_sort_key(str(s["section"])))
    is_first = bool(first_english) if first_english is not None else slug in FIRST_ENGLISH_NOTES
    note = (first_english_note or FIRST_ENGLISH_NOTES.get(slug) or "").strip()
    return {
        "slug": slug,
        "title": title,
        "author": author,
        "author_slug": author_slug,
        "period": period,
        "status": status,
        "edition": edition,
        "sections": sections,
        "section_count": len(sections),
        "blurb": blurb,
        "era_note": era_note,
        "groups": groups or [],
        "related_topics": list(WORK_TOPICS.get(slug, [])),
        "first_english": is_first,
        "first_english_note": note,
        "text_history": text_history or {},
    }


def work_card_html(w: dict) -> str:
    st = "In progress" if w["status"] == "in_progress" else "Available"
    return (
        f'<li><a href="/works/{escape(w["slug"])}/"><strong>{escape(w["title"])}</strong>'
        f"<span>{escape(w['author'])} · {w['section_count']} sections · {st}</span></a></li>"
    )


def load_origen_works() -> list[dict]:
    gebet_en = json.loads((ORIGEN_BOOK / "translations/gebet_english.json").read_text())
    gebet_src = {
        str(s.get("section")): s
        for s in json.loads((ORIGEN_BOOK / "translations/gebet_source.json").read_text())
    }
    mart_en = json.loads((ORIGEN_BOOK / "translations/martyrium_english.json").read_text())
    mart_src = {
        str(s.get("section")): s
        for s in json.loads((ORIGEN_BOOK / "translations/martyrium_source.json").read_text())
    }

    def _nav_title(row: dict, src: dict, sec: str) -> str:
        """Prefer editorial title; never show OCR apparatus as the TOC label."""
        titled = (row.get("title") or "").strip()
        if titled:
            return titled
        raw = (src.get("head") or "").strip()
        # Bare "1." / "proem." / OCR "printed '…'" junk → plain chapter label
        if (
            not raw
            or re.fullmatch(r"(proem\.?|\d+\.?|[IVXLC]+\.?)", raw, re.I)
            or "printed" in raw.lower()
            or "read as" in raw.lower()
            or "head survives" in raw.lower()
        ):
            if sec.lower() == "proem":
                return "Proem"
            return f"Chapter {sec}"
        return raw

    def rows(english_rows, source_map) -> list[dict]:
        out = []
        for row in english_rows:
            sec = str(row.get("section"))
            src = source_map.get(sec, {})
            out.append(
                {
                    "section": sec,
                    "head": _nav_title(row, src, sec),
                    "english": eng_list(row.get("english")),
                    "greek": eng_list(src.get("greek")),
                    "latin": eng_list(src.get("latin")),
                    "source_url": None,
                }
            )
        return out

    return [
        _pack_work(
            slug="origen-on-prayer",
            title="On Prayer",
            author="Origen of Alexandria",
            author_slug="origen",
            period="c. 233–235",
            status="available",
            edition="Koetschau GCS (1899)",
            sections=rows(gebet_en, gebet_src),
            blurb="Origen’s treatise on prayer. Open the Greek under each section.",
            text_history={
                "method": (
                    "English follows Paul Koetschau, Origenes Werke II (GCS, 1899). "
                    "The Archive OCR of that same print was checked. This is a reading "
                    "translation for study, not a new critical edition."
                ),
                "witnesses": [
                    {
                        "name": "Koetschau, Origenes Werke II (GCS 3, 1899)",
                        "language": "Greek",
                        "role": "copy-text",
                        "coverage": "On Prayer",
                    },
                    {
                        "name": "Archive.org OCR of GCS 3",
                        "language": "Greek",
                        "role": "check",
                        "coverage": "Same print",
                    },
                ],
                "joins": [],
            },
        ),
        _pack_work(
            slug="origen-exhortation-to-martyrdom",
            title="Exhortation to Martyrdom",
            author="Origen of Alexandria",
            author_slug="origen",
            period="c. 235",
            status="available",
            edition="Koetschau GCS (1899)",
            sections=rows(mart_en, mart_src),
            blurb="Written for Ambrose and Protoctetus. Open the Greek under each section.",
            text_history={
                "method": (
                    "English follows Paul Koetschau, Origenes Werke I (GCS, 1899). "
                    "The Archive OCR of that same print was checked. This is a reading "
                    "translation for study, not a new critical edition."
                ),
                "witnesses": [
                    {
                        "name": "Koetschau, Origenes Werke I (GCS 2, 1899)",
                        "language": "Greek",
                        "role": "copy-text",
                        "coverage": "Exhortation to Martyrdom",
                    },
                    {
                        "name": "Archive.org OCR of GCS 2",
                        "language": "Greek",
                        "role": "check",
                        "coverage": "Same print",
                    },
                ],
                "joins": [],
            },
        ),
    ]


def _origen_rows(english_rows, source_map) -> list[dict]:
    out = []
    for row in english_rows:
        sec = str(row.get("section"))
        src = source_map.get(sec, {})
        titled = (row.get("title") or "").strip()
        raw = (src.get("head") or "").strip()
        matthew = str(row.get("matthew") or src.get("matthew") or "").strip()
        # Gospel-fragment works: never let CPG/edition heads be the reader title.
        if matthew and (_CPG_TITLE.match(titled) or _CPG_TITLE.match(raw) or not titled):
            head = _reader_title_from_matthew(matthew)
        elif titled:
            head = titled
        elif (
            not raw
            or re.fullmatch(r"(proem\.?|\d+\.?|[IVXLC]+\.?)", raw, re.I)
            or "printed" in raw.lower()
            or "read as" in raw.lower()
            or "head survives" in raw.lower()
            or _CPG_TITLE.match(raw)
        ):
            head = "Proem" if sec.lower() == "proem" else f"Chapter {sec}"
        else:
            head = raw
        supplied = str(row.get("supplied_from") or src.get("supplied_from") or "").strip()
        scholar = str(
            row.get("scholar_label")
            or row.get("edition_head")
            or (raw if _CPG_TITLE.match(raw) else "")
            or ""
        ).strip()
        fragment = row.get("fragment", src.get("fragment"))
        sort_key = None
        if matthew:
            sort_key = _matthew_ref_sort_key(matthew, fragment, sec)
        out.append(
            {
                "section": sec,
                "head": head,
                "english": eng_list(row.get("english")),
                "greek": eng_list(src.get("greek")),
                "latin": eng_list(src.get("latin")),
                "source_url": None,
                "supplied_from": supplied,
                "scholar_label": scholar,
                "sort_key": sort_key,
            }
        )
    return out


def load_origen_book2() -> list[dict]:
    """Dialogue with Heraclides + On Pascha — skip a work until English exists."""
    trans = ORIGEN_BOOK2 / "translations"
    works: list[dict] = []

    her_en_path = trans / "heraclides_english.json"
    if her_en_path.exists():
        her_en = json.loads(her_en_path.read_text(encoding="utf-8"))
        her_src_rows = _json_load(trans / "heraclides_source.json", [])
        her_src = {str(s.get("section")): s for s in her_src_rows}
        works.append(
            _pack_work(
                slug="origen-dialogue-heraclides",
                title="Dialogue with Heraclides",
                author="Origen of Alexandria",
                author_slug="origen",
                period="c. 245",
                status="available",
                edition="Scherer (Toura papyrus) via DCO Greek",
                sections=_origen_rows(her_en, her_src),
                blurb=(
                    "Bishops examine Heraclides on the Father, the Son, and the soul. "
                    "Gaps in the Greek are marked, not filled."
                ),
                text_history={
                    "method": (
                        "English follows the Greek of the Toura dialogue in the Scherer "
                        "tradition, from Documenta Catholica Omnia. Gaps in the papyrus "
                        "are marked, not filled. Sources Chrétiennes 67 was not used as copy-text."
                    ),
                    "witnesses": [
                        {
                            "name": "Scherer tradition via Documenta Catholica Omnia",
                            "language": "Greek",
                            "role": "copy-text",
                            "coverage": "Dialogue with Heraclides",
                            "url": "https://documentacatholicaomnia.eu/1004/1001/0185-0254,_Origenes,_Dialogus_cum_Heraclide,_MGR.html",
                        }
                    ],
                    "joins": [],
                },
            )
        )

    pas_en_path = trans / "pascha_english.json"
    if pas_en_path.exists():
        pas_en = json.loads(pas_en_path.read_text(encoding="utf-8"))
        pas_src_rows = _json_load(trans / "pascha_source.json", [])
        pas_src = {str(s.get("section")): s for s in pas_src_rows}
        works.append(
            _pack_work(
                slug="origen-on-pascha",
                title="On Pascha",
                author="Origen of Alexandria",
                author_slug="origen",
                period="c. 245",
                status="available",
                edition="Witte’s 1993 edition of the Greek",
                sections=_origen_rows(pas_en, pas_src),
                blurb=(
                    "Origen on the Passover. Damaged lines are marked as gaps, not filled in."
                ),
                text_history={
                    "method": (
                        "English follows the Greek as printed in Witte (1993), from the page "
                        "images. OCR of those pages was checked. Damaged lines are marked as "
                        "gaps, not filled from another edition. This is a reading translation "
                        "for study, not a new critical edition."
                    ),
                    "witnesses": [
                        {
                            "name": "Witte, Die Schrift des Origenes „Über das Passa“ (1993)",
                            "language": "Greek",
                            "role": "copy-text",
                            "coverage": "On Pascha, from the page images",
                        },
                        {
                            "name": "OCR of the Witte page images",
                            "language": "Greek",
                            "role": "check",
                            "coverage": "Same print",
                        },
                    ],
                    "joins": [],
                },
            )
        )
    return works


def load_origen_book3() -> list[dict]:
    """Jeremiah homilies + 1 Samuel 28 — skip a work until English exists."""
    works: list[dict] = []
    trans = ORIGEN_BOOK3 / "translations"
    if not trans.is_dir():
        return works
    for en_path in sorted(trans.glob("*_english.json")):
        stem = en_path.name[: -len("_english.json")]
        if stem.startswith("_"):
            continue
        rows = json.loads(en_path.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            continue
        src_rows = _json_load(trans / f"{stem}_source.json", [])
        src_map = {str(s.get("section")): s for s in src_rows if isinstance(s, dict)}
        meta = _json_load(trans / f"{stem}_meta.json", {})
        publish_homilies = meta.get("publish_homilies")
        if publish_homilies:
            allow = {int(x) for x in publish_homilies}
            rows = [
                r
                for r in rows
                if isinstance(r, dict) and int(r.get("homily") or 0) in allow
            ]
            if not rows:
                continue
        slug = meta.get("slug") or f"origen-{stem.replace('_', '-')}"
        works.append(
            _pack_work(
                slug=slug,
                title=meta.get("title") or stem.replace("_", " ").title(),
                author="Origen of Alexandria",
                author_slug="origen",
                period=meta.get("period") or "c. 240–250",
                status=meta.get("status") or "in_progress",
                edition=meta.get("edition") or "Klostermann, Origenes Werke III (GCS 6, 1901)",
                sections=_origen_rows(rows, src_map),
                blurb=meta.get("blurb") or "English from the Greek, for study.",
                first_english=bool(meta.get("first_english", True)),
                first_english_note=meta.get("first_english_note") or "",
                text_history=meta.get("text_history") or {},
            )
        )
        if slug not in WORK_TOPICS and meta.get("topics"):
            WORK_TOPICS[slug] = list(meta["topics"])
    return works


def load_cyril_works() -> list[dict]:
    """Cyril of Alexandria whole works — only when English JSON is present."""
    works: list[dict] = []
    era = (
        "Cyril of Alexandria died in 444 — later than the first three centuries of the church."
    )
    folders = CYRIL_BOOKS or ([CYRIL_BOOK] if CYRIL_BOOK.exists() else [])
    for folder in folders:
        trans = folder / "translations"
        if not trans.is_dir():
            continue
        for en_path in sorted(trans.glob("*_english.json")):
            stem = en_path.name[: -len("_english.json")]
            if stem.startswith("_"):
                continue
            rows = json.loads(en_path.read_text(encoding="utf-8"))
            if not isinstance(rows, list) or not rows:
                continue
            src_rows = _source_rows(_json_load(trans / f"{stem}_source.json", []))
            src_map = {str(s.get("section")): s for s in src_rows}
            meta = _json_load(trans / f"{stem}_meta.json", {})
            slug = meta.get("slug") or f"cyril-{stem.replace('_', '-')}"
            title = meta.get("title") or stem.replace("_", " ").title()
            works.append(
                _pack_work(
                    slug=slug,
                    title=title,
                    author="Cyril of Alexandria",
                    author_slug="cyril-of-alexandria",
                    period=meta.get("period") or "c. 412–423",
                    status=meta.get("status") or "available",
                    edition=meta.get("edition") or "Migne PG 68",
                    sections=_origen_rows(rows, src_map),
                    blurb=meta.get("blurb") or "English from the Greek, for study.",
                    era_note=era,
                    first_english=bool(meta.get("first_english", True)),
                    first_english_note=meta.get("first_english_note") or "",
                    text_history=_text_history_from_meta(meta),
                )
            )
            if slug not in WORK_TOPICS and meta.get("topics"):
                WORK_TOPICS[slug] = list(meta["topics"])
    return works


def load_julian_works() -> list[dict]:
    """Early fifth-century Julian — disclosed as not ante-Nicene."""
    era = (
        "Julian wrote in the early 400s, in the fight over Pelagius. "
        "This is later than the first three centuries of the church."
    )

    def _latin_from_candidates(row: dict) -> list[str]:
        cands = row.get("candidate_quotations") or []
        if cands:
            return [str(c).strip() for c in cands if str(c).strip()]
        # Prefer Julian’s words when present; otherwise keep a short context window.
        if row.get("julian"):
            return eng_list(row.get("julian"))
        ctx = (row.get("latin_context") or "").strip()
        return [ctx] if ctx else []

    def _index_by_bcs(path: Path) -> dict[str, dict]:
        rows = json.loads(path.read_text())
        out: dict[str, dict] = {}
        for r in rows:
            key = f"{r.get('book')}.{r.get('chapter')}.{r.get('section')}"
            out[key] = r
        return out

    florus_latin = {
        b: {
            str(r["section"]): eng_list(r.get("julian"))
            for r in json.loads((JULIAN_BOOK / "sources" / f"ad_florum_{b}.json").read_text())
        }
        for b in range(1, 7)
    }

    sequence = (141, 236, 216, 136, 64, 41)
    florus_sections: list[dict] = []
    groups = []
    for b, total in enumerate(sequence, 1):
        rows = json.loads((JULIAN_BOOK / "translations" / f"ad_florum_{b}_english.json").read_text())
        assert [x["section"] for x in rows] == list(range(1, total + 1)), f"Incomplete Book {b}"
        book_secs = []
        for x in rows:
            s = x["section"]
            sec_id = f"{b}.{s}"
            url = (
                f"https://www.augustinus.it/latino/incompiuta_giuliano/"
                f"incompiuta_giuliano_{b}_libro.htm#JL_{b:03}_{s:03}_{s:03}"
            )
            item = {
                "section": sec_id,
                "head": f"To Florus {b}.{s}",
                "english": eng_list(x.get("english")),
                "greek": [],
                "latin": florus_latin[b].get(str(s), []),
                "source_url": url,
                "group": f"Book {b}",
            }
            florus_sections.append(item)
            book_secs.append(sec_id)
        groups.append({"title": f"Book {b}", "sections": book_secs})

    works = [
        _pack_work(
            slug="julian-to-florus",
            title="To Florus",
            author="Julian of Eclanum",
            author_slug="julian-of-eclanum",
            period="c. 419–430",
            status="available",
            edition="Preserved in Augustine, Unfinished Work Against Julian",
            sections=florus_sections,
            blurb=(
                "Julian’s six preserved books to Florus, quoted section by section "
                "in Augustine’s unfinished reply. Augustine’s refutations are omitted. "
                "Latin of Julian’s words is on each section."
            ),
            era_note=era,
            groups=groups,
            text_history={
                "method": (
                    "Julian’s own books do not survive as a separate manuscript. English "
                    "follows his words as Augustine quotes them in the Unfinished Work "
                    "Against Julian. Augustine’s replies are omitted. We do not restore a "
                    "Julian text independent of Augustine."
                ),
                "witnesses": [
                    {
                        "name": "Augustine, Unfinished Work Against Julian",
                        "language": "Latin",
                        "role": "copy-text",
                        "coverage": "Julian’s words as quoted, Books 1–6",
                    },
                    {
                        "name": "Augustinus.it Latin of the Unfinished Work",
                        "language": "Latin",
                        "role": "check",
                        "coverage": "Same work",
                        "url": "https://www.augustinus.it/latino/incompiuta_giuliano/index2.htm",
                    },
                    {
                        "name": "Migne PL 45",
                        "language": "Latin",
                        "role": "check",
                        "coverage": "Hard cases",
                    },
                ],
                "joins": [],
            },
        )
    ]

    turb_src = {}
    for b in range(1, 7):
        turb_src.update(_index_by_bcs(JULIAN_BOOK / "sources" / f"contra_julianum_{b}.json"))

    turb: list[dict] = []
    turb_groups: list[dict] = []
    for b in range(1, 7):
        book_secs: list[str] = []
        for x in json.loads((JULIAN_BOOK / "translations" / f"contra_julianum_{b}_english.json").read_text()):
            loc = x["location"]
            src = turb_src.get(loc, {})
            sec_id = loc.replace(".", "-")
            turb.append(
                {
                    "section": sec_id,
                    "head": f"Against Julian {loc}",
                    "english": eng_list(x.get("english")),
                    "greek": [],
                    "latin": _latin_from_candidates(src),
                    "source_url": x.get("source") or src.get("source"),
                    "kind": x.get("kind"),
                }
            )
            book_secs.append(sec_id)
        if book_secs:
            turb_groups.append({"title": f"Book {b}", "sections": book_secs})
    works.append(
        _pack_work(
            slug="julian-turbantius-fragments",
            title="To Turbantius — fragments in Against Julian",
            author="Julian of Eclanum",
            author_slug="julian-of-eclanum",
            period="c. 418–430",
            status="available",
            edition="Excerpts in Augustine, Against Julian",
            sections=turb,
            blurb=(
                "Earlier four-book work to Turbantius, surviving as excerpts arranged by "
                "Augustine’s witness. Latin source text is on each section when recovered."
            ),
            era_note=era,
            groups=turb_groups,
            text_history={
                "method": (
                    "English follows Julian’s words as Augustine excerpts them in Against "
                    "Julian. This is not a recovered complete To Turbantius."
                ),
                "witnesses": [
                    {
                        "name": "Augustine, Against Julian",
                        "language": "Latin",
                        "role": "copy-text",
                        "coverage": "Excerpts arranged by Augustine’s books",
                    }
                ],
                "joins": [],
            },
        )
    )

    marriage_src = _index_by_bcs(JULIAN_BOOK / "sources" / "marriage2_sections.json")
    marriage = []
    for x in json.loads((JULIAN_BOOK / "translations/marriage2_english.json").read_text()):
        loc = x["location"]
        src = marriage_src.get(loc, {})
        marriage.append(
            {
                "section": loc.replace(".", "-"),
                "head": f"Marriage {loc}",
                "english": eng_list(x.get("english")),
                "greek": [],
                "latin": _latin_from_candidates(src),
                "source_url": x.get("source"),
                "kind": x.get("kind"),
            }
        )
    works.append(
        _pack_work(
            slug="julian-marriage-extracts",
            title="Extracts in On Marriage and Concupiscence",
            author="Julian of Eclanum",
            author_slug="julian-of-eclanum",
            period="c. 418–420",
            status="available",
            edition="Witness in Augustine, On Marriage and Concupiscence II",
            sections=marriage,
            blurb=(
                "Intermediary extracts Augustine answered in Book Two — compiler framing "
                "labeled where needed. Latin context is on each section when recovered."
            ),
            era_note=era,
            text_history={
                "method": (
                    "English follows the extracts Augustine answered in On Marriage and "
                    "Concupiscence II. Compiler framing is labeled where needed."
                ),
                "witnesses": [
                    {
                        "name": "Augustine, On Marriage and Concupiscence II",
                        "language": "Latin",
                        "role": "copy-text",
                        "coverage": "Extracts of Julian",
                    }
                ],
                "joins": [],
            },
        )
    )

    rome = []
    for x in json.loads((JULIAN_BOOK / "translations/letter_to_rome_english.json").read_text()):
        loc = x["location"]
        rome.append(
            {
                "section": loc.replace(".", "-"),
                "head": f"Rome {loc}",
                "english": eng_list(x.get("english")),
                "greek": [],
                "latin": eng_list(x.get("latin")),
                "source_url": x.get("source"),
                "kind": x.get("kind"),
            }
        )
    works.append(
        _pack_work(
            slug="julian-letter-to-rome",
            title="Letter to Rome (fragments)",
            author="Julian of Eclanum",
            author_slug="julian-of-eclanum",
            period="c. 418–420",
            status="available",
            edition="Against Two Letters of the Pelagians I",
            sections=rome,
            blurb=(
                "Fragments attributed to Julian; descriptions of opponents’ teaching are not "
                "his positive creed. Open the Latin source witness on each section."
            ),
            era_note=era,
            text_history={
                "method": (
                    "Fragments attributed to Julian in Against Two Letters of the Pelagians I. "
                    "Descriptions of opponents’ teaching are not his positive creed."
                ),
                "witnesses": [
                    {
                        "name": "Augustine, Against Two Letters of the Pelagians I",
                        "language": "Latin",
                        "role": "fragments",
                        "coverage": "Letter to Rome fragments",
                    }
                ],
                "joins": [],
            },
        )
    )

    coll = []
    for x in json.loads((JULIAN_BOOK / "translations/collective_letter_english.json").read_text()):
        loc = x["location"]
        coll.append(
            {
                "section": loc.replace(".", "-"),
                "head": f"Collective letter {loc}",
                "english": eng_list(x.get("english")),
                "greek": [],
                "latin": eng_list(x.get("latin")),
                "source_url": x.get("source"),
                "kind": x.get("kind"),
            }
        )
    works.append(
        _pack_work(
            slug="julian-collective-letter",
            title="Collective letter to Thessalonica",
            author="Julian of Eclanum",
            author_slug="julian-of-eclanum",
            period="c. 418–420",
            status="available",
            edition="Against Two Letters of the Pelagians II–IV",
            sections=coll,
            blurb=(
                "Surviving material from the bishops’ letter; not a recovered complete text. "
                "Open the Latin source witness on each section."
            ),
            era_note=era,
            text_history={
                "method": (
                    "Surviving material from the bishops’ letter as Augustine quotes it in "
                    "Against Two Letters of the Pelagians II–IV. Not a recovered complete letter."
                ),
                "witnesses": [
                    {
                        "name": "Augustine, Against Two Letters of the Pelagians II–IV",
                        "language": "Latin",
                        "role": "fragments",
                        "coverage": "Collective letter",
                    }
                ],
                "joins": [],
            },
        )
    )
    return works


CONFIDENCE_NOTE = (
    "English is newly prepared for study from the stated edition. "
    "It is not a complete critical edition."
)

CONFIDENCE_NOTE_WITH_GREEK = (
    "English is newly prepared for study from the stated edition. "
    "Open Greek on each section for the source text. "
    "This is not a complete critical edition."
)

CONFIDENCE_NOTE_WITH_LATIN = (
    "English is newly prepared for study from the stated edition. "
    "Open Latin on each section (or the Latin source witness link) for the source text. "
    "This is not a complete critical edition."
)


def related_panel(title: str, links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    items = "".join(
        f'<li><a href="{escape(href)}">{escape(label)}</a></li>' for label, href in links
    )
    return f'<aside class="related"><h2>{escape(title)}</h2><ul>{items}</ul></aside>'


def prev_next_nav(
    work_slug: str, sections: list[dict], idx: int, contents_href: str | None = None
) -> str:
    parts = []
    if idx > 0:
        prev = sections[idx - 1]
        parts.append(
            f'<a class="pn prev" href="/works/{escape(work_slug)}/{escape(str(prev["section"]))}/">'
            f'← §{escape(str(prev["section"]))}</a>'
        )
    else:
        parts.append('<span class="pn prev"></span>')
    parts.append(
        f'<a class="pn toc" href="{escape(contents_href or f"/works/{work_slug}/")}">Read continuously</a>'
    )
    if idx + 1 < len(sections):
        nxt = sections[idx + 1]
        parts.append(
            f'<a class="pn next" href="/works/{escape(work_slug)}/{escape(str(nxt["section"]))}/">'
            f'§{escape(str(nxt["section"]))} →</a>'
        )
    else:
        parts.append('<span class="pn next"></span>')
    return '<nav class="section-nav" aria-label="Chapter">' + "".join(parts) + "</nav>"


def layout(
    title: str,
    body: str,
    *,
    crumb: list[tuple[str, str]] | None = None,
    active: str = "",
    description: str = SITE_TAG,
    styles: list[str] | None = None,
    scripts: list[str] | None = None,
    body_class: str = "",
) -> str:
    crumbs = ""
    if crumb:
        parts = []
        for label, href in crumb:
            if href:
                parts.append(f'<a href="{escape(href)}">{escape(label)}</a>')
            else:
                parts.append(f"<span>{escape(label)}</span>")
        crumbs = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"

    def nav_cls(name: str) -> str:
        return ' class="is-active"' if active == name else ""

    extra_css = "".join(f'<link rel="stylesheet" href="{escape(h)}?v={ASSET_VER}">\n' for h in styles or [])
    extra_js = "".join(f'<script src="{escape(h)}?v={ASSET_VER}" defer></script>\n' for h in scripts or [])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light">
<meta name="theme-color" content="#f7f3ea">
<title>{escape(title)} · {SITE_NAME}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="https://fathers.saneapps.com/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;550;650&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_VER}">
{extra_css}</head>
<body class="{escape(body_class)}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="/">{SITE_NAME}</a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav">
      <a href="/topics/"{nav_cls("topics")}>Topics</a>
      <a href="/works/"{nav_cls("works")}>Works</a>
      <a href="/explore/"{nav_cls("explore")}>Explore</a>
      <a href="/authors/"{nav_cls("authors")}>Authors</a>
      <a href="/search/"{nav_cls("search")}>Search</a>
      <a href="/contribute/"{nav_cls("contribute")}>Help</a>
      <a href="/about/"{nav_cls("about")}>About</a>
      <a class="support" href="{SPONSORS}" rel="noopener">Support</a>
    </nav>
  </div>
</header>
{crumbs}
<main id="main" class="main">
{body}
</main>
<footer class="site-footer">
  <p>Free public library · <a href="{SPONSORS}">Support on GitHub Sponsors</a></p>
  <p class="fine">Ancient texts · new English for study · not a complete critical edition</p>
</footer>
<script src="/assets/site.js?v={ASSET_VER}" defer></script>
{extra_js}</body>
</html>
"""


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(ASSETS, DIST / "assets")

    explore_topic_ids = {c["topic"] for c in load_explore_raw()["claims"] if c.get("topic")}

    tax = load_topics_taxonomy()
    excerpts = load_topic_excerpts()
    works = (
        load_origen_works()
        + load_origen_book2()
        + load_origen_book3()
        + load_cyril_works()
        + load_julian_works()
    )
    works_by_slug = {w["slug"]: w for w in works}

    by_topic: dict[str, list[dict]] = defaultdict(list)
    by_author: dict[str, list[dict]] = defaultdict(list)
    topic_meta: dict[str, dict] = {}

    for locus in tax.get("loci", []):
        for t in locus.get("topics", []):
            topic_meta[t["id"]] = {
                "id": t["id"],
                "title": t["title"],
                "locus_id": locus["id"],
                "locus_title": locus["title"],
                "development": t.get("development") or "",
                "heresies": t.get("heresies") or [],
                "modern_relevance": t.get("modern_relevance") or "",
            }

    topic_to_works: dict[str, list[str]] = defaultdict(list)
    for w in works:
        for tid in w.get("related_topics") or []:
            topic_to_works[tid].append(w["slug"])

    for x in excerpts:
        tid = x.get("topic") or "unknown"
        by_topic[tid].append(x)
        author = x.get("author") or "Unknown"
        by_author[author].append(x)

    for tid, rows in by_topic.items():
        rows.sort(
            key=lambda r: (
                author_sort_year(r.get("author"), r.get("period")),
                r.get("author") or "",
                period_key(r.get("period")),
                r.get("locus") or "",
                r.get("id") or "",
            )
        )

    search_index: list[dict] = []

    # --- Home ---
    sample_cards = []
    for x in excerpts[:8]:
        sample_cards.append(
            f"""<li><a href="/e/{escape(x['id'])}/"><strong>{escape(x.get('author') or '')}</strong>
            <span>{escape(x.get('citation') or x['id'])}</span></a></li>"""
        )
    first_works = [w for w in works if w.get("first_english")]
    other_works = [w for w in works if not w.get("first_english")]
    first_cards = "".join(work_card_html(w) for w in first_works)
    other_cards = "".join(work_card_html(w) for w in other_works)

    home = f"""
<section class="hero">
  <p class="eyebrow">Public library · donation supported</p>
  <h1>The Fathers, readable</h1>
  <p class="lede">Teaching by topic, and whole treatises chapter by chapter. Ante-Nicene voices first; later writers are labeled when they appear. Several treatises here had no earlier complete English.</p>
  <div class="hero-actions">
    <a class="btn primary" href="/topics/">Browse topics</a>
    <a class="btn" href="/works/">Browse works</a>
    <a class="btn" href="/explore/?topic=free-will">Explore over time</a>
  </div>
</section>
<section>
  <h2>Treatises with no earlier English</h2>
  <p class="intro">These had no earlier complete English a reader could freely use. The English here is new.</p>
  <ul class="card-list">{first_cards}</ul>
  <p><a href="/works/#no-earlier-english">All of them on the works page →</a></p>
</section>
<section class="split">
  <div>
    <h2>Topics</h2>
    <p>What did they teach about God, Christ, will, church, last things? {len(excerpts)} excerpts across the map.</p>
    <a href="/topics/">Open the map →</a>
  </div>
  <div>
    <h2>Works</h2>
    <p>{len(works)} treatises online · {sum(w['section_count'] for w in works)} sections. Cross-linked to related topics.</p>
    <ul class="card-list">{other_cards}</ul>
    <p><a href="/works/">All works →</a></p>
  </div>
</section>
<section>
  <h2>From the topics</h2>
  <ul class="card-list">{''.join(sample_cards)}</ul>
  <p><a href="/topics/">Browse all topics →</a></p>
</section>
"""
    write(DIST / "index.html", layout("Home", home, active=""))

    # --- Topics index ---
    locus_blocks = []
    for locus in tax.get("loci", []):
        rows = []
        for t in locus.get("topics", []):
            n = len(by_topic.get(t["id"], []))
            if n == 0 and t["id"] not in topic_to_works:
                continue
            extra = ""
            if t["id"] in topic_to_works:
                extra = f" · {len(topic_to_works[t['id']])} related work{'s' if len(topic_to_works[t['id']])!=1 else ''}"
            rows.append(
                f'<li data-count="{n}"><a href="/topics/{escape(t["id"])}/">'
                f'<span class="t">{escape(t["title"])}</span>'
                f'<span class="c">{n} excerpts{extra}</span></a></li>'
            )
        if not rows:
            continue
        locus_blocks.append(
            f'<section class="locus" id="{escape(locus["id"])}">'
            f'<h2>{escape(locus["title"])}</h2><ul class="topic-list">{"".join(rows)}</ul></section>'
        )

    topics_body = f"""
<h1>Topics</h1>
<p class="intro">Map of teaching from the books in this library. Related whole works appear on each topic page. Later writers are labeled where they enter. English is newly prepared for study — not a complete critical edition. <a href="/explore/">See how positions line up over time →</a></p>
{''.join(locus_blocks)}
"""
    write(
        DIST / "topics" / "index.html",
        layout("Topics", topics_body, crumb=[("Home", "/"), ("Topics", "")], active="topics"),
    )

    # --- Topic pages + excerpt pages ---
    for tid, rows in by_topic.items():
        meta = topic_meta.get(tid, {"title": tid, "locus_title": "Topics", "locus_id": ""})
        related_works = [
            (works_by_slug[s]["title"], f"/works/{s}/")
            for s in topic_to_works.get(tid, [])
            if s in works_by_slug
        ]
        rel_html = related_panel("Related works", related_works)
        items_html = []
        current_author = None
        for x in rows:
            paras = "".join(f"<p>{escape(p)}</p>" for p in eng_list(x.get("english")))
            author = x.get("author") or "Unknown"
            if author != current_author:
                if current_author is not None:
                    items_html.append("</section>")
                rec = AUTHORS.get(author) or {}
                dates = rec.get("dates_display") or (x.get("period") or "")
                items_html.append(
                    f'<section class="author-group" id="{escape(slugify(author))}">'
                    f"<h2>{escape(author)}"
                    f'<span class="meta">{escape(dates)}</span></h2>'
                )
                current_author = author
            items_html.append(
                f"""<article class="excerpt" id="{escape(x['id'])}">
                <header><a href="/e/{escape(x['id'])}/"><h2>{escape(x.get('citation') or x['id'])}</h2></a>
                <p class="meta">{escape(author)} · {escape(x.get('period') or '')} · {escape(x.get('work') or '')}</p></header>
                <div class="body">{paras}</div>
                </article>"""
            )
            src_block = ""
            if x.get("greek"):
                g = eng_list(x["greek"])
                src_block += "<details><summary>Greek</summary>" + "".join(
                    f"<p class='src'>{escape(p)}</p>" for p in g
                ) + "</details>"
            if x.get("latin"):
                la = eng_list(x["latin"])
                src_block += "<details><summary>Latin</summary>" + "".join(
                    f"<p class='src'>{escape(p)}</p>" for p in la
                ) + "</details>"
            al = (x.get("author") or "").lower()
            author_slug = slugify(x.get("author") or "unknown")
            if "origen" in al:
                author_slug = "origen"
            elif "julian" in al:
                author_slug = "julian-of-eclanum"
            elif "cyril of alexandria" in al:
                author_slug = "cyril-of-alexandria"
            cross = related_panel(
                "Also see",
                [
                    (meta["title"] + " (topic)", f"/topics/{tid}/"),
                    (x.get("author") or "Author", f"/authors/{author_slug}/"),
                ]
                + related_works[:4],
            )
            ebody = f"""
<article class="excerpt-page">
  <h1>{escape(x.get('citation') or x['id'])}</h1>
  <p class="meta">{escape(x.get('author') or '')} · {escape(x.get('work') or '')} · {escape(x.get('period') or '')}</p>
  <div class="body">{paras}</div>
  {src_block}
  {cross}
  <p class="back"><a href="/topics/{escape(tid)}/">← {escape(meta['title'])}</a></p>
</article>
"""
            write(
                DIST / "e" / x["id"] / "index.html",
                layout(
                    x.get("citation") or x["id"],
                    ebody,
                    crumb=[
                        ("Home", "/"),
                        ("Topics", "/topics/"),
                        (meta["title"], f"/topics/{tid}/"),
                        ("Excerpt", ""),
                    ],
                    active="topics",
                    description=(eng_list(x.get("english")) or [""])[0][:160],
                ),
            )
            search_index.append(
                {
                    "kind": "excerpt",
                    "id": x["id"],
                    "title": x.get("citation") or x["id"],
                    "author": x.get("author"),
                    "href": f"/e/{x['id']}/",
                    "topic": tid,
                    "verified": x.get("confidence") == "source_verified",
                    "text": " ".join(eng_list(x.get("english")))[:400],
                }
            )
        if current_author is not None:
            items_html.append("</section>")

        explore_link = ""
        if tid in explore_topic_ids:
            explore_link = (
                f'<p class="intro"><a href="/explore/?topic={escape(tid)}">'
                f"See how this topic lines up over time →</a></p>"
            )
        lead = next((str(x.get("topic_lead")).strip() for x in rows if x.get("topic_lead")), "")
        relevance = (meta.get("modern_relevance") or "").strip()
        intro = lead or relevance
        intro_html = f'<p class="intro">{escape(intro)}</p>' if intro else ""
        meta_bits = [escape(meta.get("locus_title") or ""), f"{len(rows)} excerpts"]
        dev = meta.get("development") or ""
        if dev == "consensus":
            meta_bits.append("Broad agreement in this library")
        elif dev == "debate":
            meta_bits.append("Marked debate — read the differences")
        heresies = [_plain_tag(h) for h in (meta.get("heresies") or []) if h]
        if heresies:
            meta_bits.append("Against: " + ", ".join(heresies))
        years = [year_from_period(x.get("period")) for x in rows]
        years = [y for y in years if y is not None]
        era_html = ""
        if any(y >= 325 for y in years):
            era_html = (
                '<p class="banner">This topic includes Nicene and later writers '
                "alongside earlier voices. Dates sit on each excerpt.</p>"
            )
        tbody = f"""
<h1>{escape(meta['title'])}</h1>
<p class="meta">{" · ".join(meta_bits)}</p>
{era_html}{intro_html}
{explore_link}
{rel_html}
{''.join(items_html)}
"""
        write(
            DIST / "topics" / tid / "index.html",
            layout(
                meta["title"],
                tbody,
                crumb=[("Home", "/"), ("Topics", "/topics/"), (meta["title"], "")],
                active="topics",
            ),
        )

    # Topics that only have related works (no excerpts yet)
    for tid, slugs in topic_to_works.items():
        if tid in by_topic:
            continue
        meta = topic_meta.get(tid)
        if not meta:
            continue
        related_works = [(works_by_slug[s]["title"], f"/works/{s}/") for s in slugs if s in works_by_slug]
        write(
            DIST / "topics" / tid / "index.html",
            layout(
                meta["title"],
                f"""<h1>{escape(meta['title'])}</h1>
                <p class="intro">{escape(meta.get('locus_title') or '')} · topical excerpts still growing.</p>
                {related_panel("Related works", related_works)}""",
                crumb=[("Home", "/"), ("Topics", "/topics/"), (meta["title"], "")],
                active="topics",
            ),
        )

    # --- Works ---
    first_list = "".join(work_card_html(w) for w in works if w.get("first_english"))
    other_list = "".join(work_card_html(w) for w in works if not w.get("first_english"))
    write(
        DIST / "works" / "index.html",
        layout(
            "Works",
            f"""<h1>Works</h1>
<p class="intro">Whole treatises, section by section. Later writers are labeled on their pages. Each work links to related topics.</p>
<section id="no-earlier-english">
<h2>Treatises with no earlier English</h2>
<p class="intro">These had no earlier complete English a reader could freely use. The English here is new.</p>
<ul class="card-list">{first_list}</ul>
</section>
<section>
<h2>Also in this library</h2>
<p class="intro">Some English of this material already exists in older books, often inside another author’s reply. It is here so the arguments can be read in one place.</p>
<ul class="card-list">{other_list}</ul>
</section>""",
            crumb=[("Home", "/"), ("Works", "")],
            active="works",
        ),
    )

    for w in works:
        topic_links = []
        for tid in w.get("related_topics") or []:
            meta = topic_meta.get(tid)
            if meta:
                topic_links.append((meta["title"], f"/topics/{tid}/"))
        rel_topics = related_panel("Related topics", topic_links)
        author_link = related_panel(
            "Author",
            [(w["author"], f"/authors/{w['author_slug']}/")],
        )

        note = ""
        if w["status"] == "in_progress":
            note = f"<p class='banner'>Translation in progress — {w['section_count']} sections online.</p>"
        era = f"<p class='banner'>{escape(w['era_note'])}</p>" if w.get("era_note") else ""
        first_banner = ""
        if w.get("first_english"):
            first_banner = (
                f'<p class="banner first-english">{escape(w.get("first_english_note") or FIRST_ENGLISH_NOTES.get(w["slug"]) or "")}</p>'
            )
        blurb = f"<p class='intro'>{escape(w['blurb'])}</p>" if w.get("blurb") else ""
        has_greek = any(s.get("greek") for s in w["sections"])
        has_latin = any(s.get("latin") for s in w["sections"])
        has_latin_link = any(s.get("source_url") for s in w["sections"])
        if has_greek:
            conf = CONFIDENCE_NOTE_WITH_GREEK
        elif has_latin or has_latin_link:
            conf = CONFIDENCE_NOTE_WITH_LATIN
        else:
            conf = CONFIDENCE_NOTE
        confidence = f"<p class='intro fine'>{escape(conf)}</p>"
        work_mast = (
            f"<header class=\"reader-mast\">"
            f"<h1>{escape(w['title'])}</h1>"
            f"<p class=\"meta\">{escape(w['author'])} · {escape(w['period'])} · {escape(w['edition'])}</p>"
            f"</header>"
        )
        history_html = text_history_html(w.get("text_history"))
        about_bits = "".join(
            x for x in (first_banner, era, note, blurb, history_html, confidence) if x
        )
        rail_about = (
            f'<details class="reader-about"><summary>About this text</summary>{about_bits}</details>'
            if about_bits
            else ""
        )
        hub_about = (
            f'<details class="reader-about"><summary>About this text</summary>{history_html}{confidence}</details>'
            if history_html
            else confidence
        )
        # Overview / hub pages that still want the full stack above the fold.
        work_header = (
            f"<h1>{escape(w['title'])}</h1>"
            f"<p class=\"meta\">{escape(w['author'])} · {escape(w['period'])} · {escape(w['edition'])}</p>"
            f"{first_banner}{era}{note}{blurb}{hub_about}"
        )

        # --- continuous reader: whole work (or one book) on a single page ---
        def display_head(s: dict) -> str:
            """Editorial thought title, or '' if the head is only a locus label."""
            sid = str(s["section"])
            head = str(s.get("head") or "").strip()
            if not head:
                return ""
            low = head.lower()
            sid_dot = sid.replace("-", ".")
            sid_dash = sid.replace(".", "-")
            echoes = {
                sid.lower(),
                sid_dot.lower(),
                sid_dash.lower(),
                f"chapter {sid}".lower(),
                f"§{sid}".lower(),
                f"section {sid}".lower(),
                f"{w['title']} {sid}".lower(),
                f"{w['title']} {sid_dot}".lower(),
                f"to florus {sid}".lower(),
                f"to florus {sid_dot}".lower(),
                f"against julian {sid}".lower(),
                f"against julian {sid_dot}".lower(),
                f"marriage {sid}".lower(),
                f"marriage {sid_dot}".lower(),
                f"rome {sid}".lower(),
                f"rome {sid_dot}".lower(),
                f"collective letter {sid}".lower(),
                f"collective letter {sid_dot}".lower(),
            }
            if low in echoes:
                return ""
            # "Against Julian 1.5.16" / "Marriage 2.2.3" when section is 1-5-16 / 2-2-3
            if re.fullmatch(
                r"(against julian|marriage|rome|collective letter|to florus)\s+[\d.]+",
                low,
            ):
                return ""
            # Edition apparatus must never be the reader heading.
            if _CPG_TITLE.match(head):
                return ""
            return head

        def chunk_sections(secs: list[dict]) -> list[dict]:
            """Group consecutive sections that carry one thought.

            Same cleaned title → one editorial thought (edition slices mid-stream).
            Untitled / locus-only runs (fragment works) group by size so a source
            panel never covers an unreasonable stretch.
            Biblical locus titles (e.g. Matthew 1:16) stay visible in Contents but
            do not merge distinct fragments that share a verse.
            """
            chunks: list[dict] = []
            cur: dict | None = None
            for s in secs:
                h = display_head(s)
                n = sum(len(p) for p in s["english"])
                bible_locus = bool(h and _BIBLE_LOCUS_TITLE.match(h))
                same_title = (
                    cur is not None
                    and h
                    and cur["head"] == h
                    and cur["chars"] < 9000
                    and not bible_locus
                )
                untitled_run = (
                    cur is not None and not h and not cur["head"]
                    and cur["chars"] < 3500 and len(cur["secs"]) < 8
                )
                if same_title or untitled_run:
                    cur["secs"].append(s)
                    cur["chars"] += n
                else:
                    cur = {"head": h, "secs": [s], "chars": n}
                    chunks.append(cur)
            return chunks

        def untitled_snip(ch: dict, *, limit: int = 72) -> str:
            """First-line English for untitled chunks — Contents and H2 share this."""
            snip = " ".join(ch["secs"][0].get("english") or []).strip()
            snip = re.sub(r"\s+", " ", snip)
            if limit and len(snip) > limit:
                snip = snip[: limit - 3].rsplit(" ", 1)[0] + "…"
            return snip

        def chunk_label(ch: dict) -> str:
            secs = ch["secs"]
            first, last = str(secs[0]["section"]), str(secs[-1]["section"])
            rng = first if len(secs) == 1 else f"{first}–{last}"
            if ch["head"]:
                return f"{rng}  {ch['head']}"
            # Untitled chunk: soft first-line summary so Contents is not empty.
            snip = untitled_snip(ch)
            return f"{rng}  {snip}" if snip else rng

        def chunk_block(ch: dict) -> str:
            secs = ch["secs"]
            first, last = str(secs[0]["section"]), str(secs[-1]["section"])
            rng = f"§{first}" if len(secs) == 1 else f"§§{first}–{last}"
            if ch["head"]:
                heading = (
                    f'<h2 class="reader-head"><span class="reader-title">{escape(ch["head"])}</span>'
                    f'<span class="range">{escape(rng)}</span></h2>'
                )
            else:
                # Same rule as titled chunks: plain-English thought first; § stays a mark.
                snip = untitled_snip(ch, limit=110)
                if snip:
                    heading = (
                        f'<h2 class="reader-head"><span class="reader-title">{escape(snip)}</span>'
                        f'<span class="range">{escape(rng)}</span></h2>'
                    )
                else:
                    heading = (
                        f'<h2 class="reader-head"><span class="reader-title range-title">'
                        f'{escape(rng)}</span></h2>'
                    )
            cues = [(s.get("supplied_from") or "").strip() for s in secs]
            unique_cues = {c for c in cues if c}
            chunk_cue = ""
            if len(unique_cues) == 1:
                chunk_cue = f'<p class="reader-supplied">{escape(next(iter(unique_cues)))}</p>'
            paras = []
            for s in secs:
                sid = str(s["section"])
                supplied = (s.get("supplied_from") or "").strip()
                if supplied and len(unique_cues) != 1:
                    paras.append(f'<p class="reader-supplied">{escape(supplied)}</p>')
                for i, p in enumerate(s["english"]):
                    marker = ""
                    if i == 0:
                        marker = (
                            f'<a class="vnum" id="s{escape(sid)}" href="/works/{escape(w["slug"])}/{escape(sid)}/" '
                            f'title="Section {escape(sid)} — page for citing and sharing">{escape(sid)}</a>'
                        )
                    paras.append(f"<p>{marker}{escape(p)}</p>")
                scholar = (s.get("scholar_label") or "").strip()
                if scholar:
                    paras.append(f'<p class="meta scholar">{escape(scholar)}</p>')
            gk, la, wit = [], [], []
            for s in secs:
                sid = str(s["section"])
                if s.get("greek"):
                    if len(secs) > 1:
                        gk.append(f'<p class="src-sec">§{escape(sid)}</p>')
                    gk += [f"<p class='src'>{escape(p)}</p>" for p in s["greek"]]
                if s.get("latin"):
                    if len(secs) > 1:
                        la.append(f'<p class="src-sec">§{escape(sid)}</p>')
                    la += [f"<p class='src'>{escape(p)}</p>" for p in s["latin"]]
                if s.get("source_url"):
                    wit.append(f'<a href="{escape(s["source_url"])}" rel="noopener">§{escape(sid)}</a>')
            src_block = ""
            if gk:
                src_block += f'<details><summary>Greek · {escape(rng)}</summary>{"".join(gk)}</details>'
            if la:
                src_block += f'<details><summary>Latin · {escape(rng)}</summary>{"".join(la)}</details>'
            witness = (
                f'<p class="meta">Latin source witness: {" · ".join(wit)}</p>' if wit else ""
            )
            return f'<section class="reader-sec">{heading}{chunk_cue}{"".join(paras)}{src_block}{witness}</section>'

        def reader_body(secs: list[dict]) -> str:
            return "".join(chunk_block(ch) for ch in chunk_sections(secs))

        def toc_items_from_chunks(chunks: list[dict], href_prefix: str = "") -> str:
            """One Contents line per thought-chunk — never repeat the same title N times."""
            out = []
            for ch in chunks:
                first = str(ch["secs"][0]["section"])
                last = str(ch["secs"][-1]["section"])
                num = first if len(ch["secs"]) == 1 else f"{first}–{last}"
                label = ch["head"] or chunk_label(ch).split("  ", 1)[-1]
                out.append(
                    f'<li><a href="{href_prefix}#s{escape(first)}">'
                    f'<span class="num">{escape(num)}</span> {escape(label[:90])}</a></li>'
                )
            return "".join(out)

        def contents_details(secs: list[dict], label: str = "Contents", *, open_default: bool = True) -> str:
            chunks = chunk_sections(secs)
            n_sec = len(secs)
            n_ch = len(chunks)
            meta = (
                f"{n_ch} passages · {n_sec} sections"
                if n_ch != n_sec
                else f"{n_ch} passages"
            )
            open_attr = " open" if open_default else ""
            return (
                f'<details class="toc-group reader-contents" id="contents"{open_attr}>'
                f'<summary><span class="toc-summary-title">{escape(label)}</span>'
                f'<span class="toc-summary-meta">{escape(meta)}</span></summary>'
                f'<ol class="toc">{toc_items_from_chunks(chunks)}</ol></details>'
            )

        back_to_top = '<a class="reader-top" href="#contents">Contents ↑</a>'

        def reader_page(main: str, *, contents_html: str, mast_extra: str = "", mast: str | None = None) -> str:
            """Slim title; rail holds Contents + meta; reading column starts at once."""
            return (
                f"{mast if mast is not None else work_mast}{mast_extra}"
                f'<div class="reader-layout">'
                f'<aside class="reader-rail">'
                f"{contents_html}"
                f"{author_link}{rel_topics}{rail_about}"
                f"</aside>"
                f'<div class="reader-main">{main}</div>'
                f"</div>"
                f"{back_to_top}"
            )

        sec_contents_href: dict[str, str] = {}

        if w.get("groups"):
            # One reader page per book; the work page is a short overview.
            sec_map = {str(s["section"]): s for s in w["sections"]}
            book_slugs = [slugify(g["title"]) for g in w["groups"]]
            for g, bslug in zip(w["groups"], book_slugs):
                for sid in g["sections"]:
                    sec_contents_href[str(sid)] = f"/works/{w['slug']}/{bslug}/#s{sid}"

            jump = "".join(
                f'<a class="book-chip" href="/works/{escape(w["slug"])}/{escape(b)}/">'
                f'{escape(g["title"])} · {len(g["sections"])}</a>'
                for g, b in zip(w["groups"], book_slugs)
            )
            overview_toc = []
            for g, bslug in zip(w["groups"], book_slugs):
                secs = [sec_map[str(sid)] for sid in g["sections"] if str(sid) in sec_map]
                chunks = chunk_sections(secs)
                lis = toc_items_from_chunks(chunks, href_prefix=f"/works/{w['slug']}/{bslug}/")
                overview_toc.append(
                    f'<details class="toc-group">'
                    f'<summary><span class="toc-summary-title">{escape(g["title"])}</span>'
                    f'<span class="toc-summary-meta">{len(chunks)} passages · {len(secs)} sections · '
                    f'<a href="/works/{escape(w["slug"])}/{escape(bslug)}/" onclick="event.stopPropagation()">read</a></span></summary>'
                    f'<ol class="toc">{lis}</ol></details>'
                )
            write(
                DIST / "works" / w["slug"] / "index.html",
                layout(
                    w["title"],
                    f"""{work_header}
                    {author_link}{rel_topics}
                    <p class="intro">Each book reads on one continuous page:</p>
                    <nav class="book-jump" aria-label="Books">{jump}</nav>
                    {''.join(overview_toc)}""",
                    crumb=[("Home", "/"), ("Works", "/works/"), (w["title"], "")],
                    active="works",
                    description=w.get("blurb") or SITE_TAG,
                ),
            )
            for i, (g, bslug) in enumerate(zip(w["groups"], book_slugs)):
                secs = [sec_map[str(sid)] for sid in g["sections"] if str(sid) in sec_map]
                blocks = reader_body(secs)
                bnav_bits = []
                if i > 0:
                    bnav_bits.append(
                        f'<a class="pn prev" href="/works/{escape(w["slug"])}/{escape(book_slugs[i-1])}/">← {escape(w["groups"][i-1]["title"])}</a>'
                    )
                else:
                    bnav_bits.append('<span class="pn prev"></span>')
                bnav_bits.append(f'<a class="pn toc" href="/works/{escape(w["slug"])}/">All books</a>')
                if i + 1 < len(w["groups"]):
                    bnav_bits.append(
                        f'<a class="pn next" href="/works/{escape(w["slug"])}/{escape(book_slugs[i+1])}/">{escape(w["groups"][i+1]["title"])} →</a>'
                    )
                else:
                    bnav_bits.append('<span class="pn next"></span>')
                bnav = '<nav class="section-nav" aria-label="Books">' + "".join(bnav_bits) + "</nav>"
                book_mast = (
                    f"<header class=\"reader-mast\">"
                    f"<h1>{escape(w['title'])} <span class=\"h1-book\">— {escape(g['title'])}</span></h1>"
                    f"<p class=\"meta\">{escape(w['author'])} · {escape(w['period'])} · {escape(w['edition'])}</p>"
                    f"</header>"
                )
                write(
                    DIST / "works" / w["slug"] / bslug / "index.html",
                    layout(
                        f"{w['title']} — {g['title']}",
                        reader_page(
                            f"{bnav}<div class=\"reader\">{blocks}</div>{bnav}",
                            contents_html=contents_details(secs, label=f"{g['title']} contents"),
                            mast=book_mast,
                        ),
                        crumb=[
                            ("Home", "/"),
                            ("Works", "/works/"),
                            (w["title"], f"/works/{w['slug']}/"),
                            (g["title"], ""),
                        ],
                        active="works",
                        description=w.get("blurb") or SITE_TAG,
                    ),
                )
        else:
            for s in w["sections"]:
                sec_contents_href[str(s["section"])] = f"/works/{w['slug']}/#s{s['section']}"
            blocks = reader_body(w["sections"])
            write(
                DIST / "works" / w["slug"] / "index.html",
                layout(
                    w["title"],
                    reader_page(
                        f'<div class="reader">{blocks}</div>',
                        contents_html=contents_details(w["sections"]),
                    ),
                    crumb=[("Home", "/"), ("Works", "/works/"), (w["title"], "")],
                    active="works",
                    description=w.get("blurb") or SITE_TAG,
                ),
            )

        for idx, s in enumerate(w["sections"]):
            paras = "".join(f"<p>{escape(p)}</p>" for p in s["english"])
            # Same pattern as excerpt pages: English body, then language panels at the bottom.
            src_block = ""
            if s.get("greek"):
                src_block += "<details><summary>Greek</summary>" + "".join(
                    f"<p class='src'>{escape(p)}</p>" for p in s["greek"]
                ) + "</details>"
            if s.get("latin"):
                src_block += "<details><summary>Latin</summary>" + "".join(
                    f"<p class='src'>{escape(p)}</p>" for p in s["latin"]
                ) + "</details>"
            if not src_block and not s.get("source_url"):
                # Only when we truly have no source text online.
                src_block = (
                    "<p class='intro fine'>Source language for this section is not "
                    "loaded on the page yet.</p>"
                )
            source = ""
            if s.get("source_url"):
                source = (
                    f'<p class="meta"><a href="{escape(s["source_url"])}" rel="noopener">Latin source witness</a></p>'
                )
            kind = ""
            if s.get("kind"):
                kind = f'<p class="badge">{escape(str(s["kind"]).capitalize())}</p>'
            supplied = (s.get("supplied_from") or "").strip()
            supplied_html = (
                f'<p class="reader-supplied">{escape(supplied)}</p>' if supplied else ""
            )
            nav = prev_next_nav(
                w["slug"], w["sections"], idx,
                contents_href=sec_contents_href.get(str(s["section"])),
            )
            cross = related_panel(
                "Cross-references",
                [(w["author"], f"/authors/{w['author_slug']}/")] + topic_links[:5],
            )
            write(
                DIST / "works" / w["slug"] / str(s["section"]) / "index.html",
                layout(
                    f"{w['title']} §{s['section']}",
                    f"""<article class="work-section">
                    {nav}
                    <p class="meta"><a href="/works/{escape(w['slug'])}/">{escape(w['title'])}</a> · §{escape(str(s['section']))}</p>
                    {kind}
                    <h1>{escape(str(s['head']))}</h1>
                    {supplied_html}
                    <div class="body">{paras}</div>
                    {source}{src_block}
                    {rail_about}
                    {cross}
                    {nav}
                    </article>""",
                    crumb=[
                        ("Home", "/"),
                        ("Works", "/works/"),
                        (w["title"], f"/works/{w['slug']}/"),
                        (f"§{s['section']}", ""),
                    ],
                    active="works",
                    description=(s["english"] or [""])[0][:160],
                ),
            )
            search_index.append(
                {
                    "kind": "work",
                    "id": f"{w['slug']}-{s['section']}",
                    "title": f"{w['title']} §{s['section']}: {s['head']}",
                    "author": w["author"],
                    "href": f"/works/{w['slug']}/{s['section']}/",
                    "verified": False,
                    "text": " ".join(s["english"])[:400],
                }
            )

    # --- Authors ---
    author_links = []
    hubs_done = set()

    def write_author_hub(slug: str, display: str, work_author_slug: str | None = None):
        hubs_done.add(slug)
        ww = [w for w in works if w["author_slug"] == (work_author_slug or slug)]
        ow = "".join(
            f'<li><a href="/works/{escape(w["slug"])}/">{escape(w["title"])} ({w["section_count"]})</a></li>'
            for w in ww
        )
        ot = []
        for a, rows in by_author.items():
            al = a.lower()
            if slug == "origen" and "origen" in al:
                ot.extend(rows)
            elif slug == "julian-of-eclanum" and "julian" in al:
                ot.extend(rows)
            elif slug == "cyril-of-alexandria" and "cyril of alexandria" in al:
                ot.extend(rows)
        ot_by_topic: dict[str, list] = defaultdict(list)
        for x in ot:
            ot_by_topic[x.get("topic") or "unknown"].append(x)
        ot_blocks = []
        for tkey, xs in sorted(
            ot_by_topic.items(),
            key=lambda kv: (topic_meta.get(kv[0], {}) or {}).get("title") or kv[0],
        ):
            ttitle = (topic_meta.get(tkey) or {}).get("title") or tkey
            lis = "".join(
                f'<li><a href="/e/{escape(x["id"])}/">{escape(x.get("citation") or x["id"])}</a></li>'
                for x in xs[:80]
            )
            ot_blocks.append(f"<h3>{escape(ttitle)}</h3><ul class='card-list'>{lis}</ul>")
        ot_lis = "".join(ot_blocks)
        topic_set = []
        for w in ww:
            for tid in w.get("related_topics") or []:
                meta = topic_meta.get(tid)
                if meta and (meta["title"], tid) not in topic_set:
                    topic_set.append((meta["title"], tid))
        topics_ul = related_panel(
            "Related topics",
            [(t, f"/topics/{tid}/") for t, tid in topic_set],
        )
        explore_bits = []
        for t, tid in topic_set[:5]:
            explore_bits.append((f"Explore: {t}", f"/explore/?topic={tid}&author={slug}"))
        if slug == "julian-of-eclanum":
            explore_bits.insert(
                0,
                ("Where Julian meets earlier writers", "/explore/?topic=free-will&author=julian-of-eclanum"),
            )
        explore_ul = related_panel("Over time", explore_bits)
        write(
            DIST / "authors" / slug / "index.html",
            layout(
                display,
                f"""<h1>{escape(display)}</h1>
                <h2>Works</h2><ul class="card-list">{ow or "<li>None yet.</li>"}</ul>
                {topics_ul}{explore_ul}
                <h2>Topical excerpts</h2>{ot_lis or "<p>None linked yet.</p>"}""",
                crumb=[("Home", "/"), ("Authors", "/authors/"), (display, "")],
                active="authors",
            ),
        )
        author_links.append(
            f'<li><a href="/authors/{escape(slug)}/"><strong>{escape(display)}</strong>'
            f'<span>{len(ww)} work{"s" if len(ww)!=1 else ""} · {len(ot)} topical</span></a></li>'
        )

    write_author_hub("origen", "Origen of Alexandria", "origen")
    write_author_hub("julian-of-eclanum", "Julian of Eclanum", "julian-of-eclanum")
    if any(w.get("author_slug") == "cyril-of-alexandria" for w in works):
        write_author_hub("cyril-of-alexandria", "Cyril of Alexandria", "cyril-of-alexandria")

    # Augustine hub (topical excerpts + contrast cards; full works forthcoming)
    aug_rows = by_author.get("Augustine of Hippo", [])
    aug_lis = "".join(
        f'<li><a href="/e/{escape(x["id"])}/">{escape(x.get("citation") or x["id"])}</a></li>' for x in aug_rows[:200]
    )
    write(
        DIST / "authors" / "augustine-of-hippo" / "index.html",
        layout(
            "Augustine of Hippo",
            f"""<h1>Augustine of Hippo</h1>
            <p class="banner">Topical excerpts and contrast cards for now — full Augustine works are not yet in this library. Use Explore to place his late teaching beside earlier writers.</p>
            <aside class="related"><h2>Over time</h2><ul>
            <li><a href="/explore/?topic=free-will&amp;author=augustine-of-hippo">Free will</a></li>
            <li><a href="/explore/?topic=sin-and-death&amp;author=augustine-of-hippo">Sin and death</a></li>
            <li><a href="/explore/?topic=grace-and-assistance&amp;author=augustine-of-hippo">Grace</a></li>
            <li><a href="/explore/?topic=gifts-and-order&amp;author=augustine-of-hippo">Gifts and order</a></li>
            </ul></aside>
            <h2>Topical excerpts</h2><ul class="card-list">{aug_lis or "<li>None linked yet.</li>"}</ul>
            <p class="intro">Compare with <a href="/authors/julian-of-eclanum/">Julian of Eclanum</a> and the ante-Nicene topic map.</p>""",
            crumb=[("Home", "/"), ("Authors", "/authors/"), ("Augustine", "")],
            active="authors",
        ),
    )
    hubs_done.add("augustine-of-hippo")
    author_links.insert(
        0,
        f'<li><a href="/authors/augustine-of-hippo/"><strong>Augustine of Hippo</strong><span>{len(aug_rows)} topical · contrast cards</span></a></li>',
    )
    # Old slug kept as a redirect so existing links don't break.
    write(
        DIST / "authors" / "augustine" / "index.html",
        '<!DOCTYPE html><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0; url=/authors/augustine-of-hippo/">'
        '<link rel="canonical" href="https://fathers.saneapps.com/authors/augustine-of-hippo/">'
        '<title>Augustine of Hippo</title>'
        '<p><a href="/authors/augustine-of-hippo/">Augustine of Hippo has moved.</a></p>',
    )

    for author in sorted(by_author.keys(), key=lambda a: a.lower()):
        al = author.lower()
        if "origen" in al or "julian of eclanum" in al or al == "cyril of alexandria":
            continue
        sl = slugify(author)
        if sl in hubs_done:
            continue
        n = len(by_author[author])
        author_links.append(
            f'<li><a href="/authors/{escape(sl)}/"><strong>{escape(author)}</strong><span>{n} topical excerpts</span></a></li>'
        )
        rows = by_author[author]
        rec = AUTHORS.get(author) or {}
        dates = rec.get("dates_display") or ""
        grouped: dict[str, list] = defaultdict(list)
        for x in rows:
            grouped[x.get("topic") or "unknown"].append(x)
        blocks = []
        if dates:
            blocks.append(f'<p class="meta">{escape(dates)}</p>')
        for tkey, xs in sorted(
            grouped.items(),
            key=lambda kv: (topic_meta.get(kv[0], {}) or {}).get("title") or kv[0],
        ):
            ttitle = (topic_meta.get(tkey) or {}).get("title") or tkey
            lis = "".join(
                f'<li><a href="/e/{escape(x["id"])}/">{escape(x.get("citation") or x["id"])}</a></li>'
                for x in xs[:80]
            )
            explore = ""
            if tkey in explore_topic_ids:
                explore = f' <a href="/explore/?topic={escape(tkey)}">Explore</a>'
            blocks.append(
                f"<h2>{escape(ttitle)}{explore}</h2><ul class='card-list'>{lis}</ul>"
            )
        write(
            DIST / "authors" / sl / "index.html",
            layout(
                author,
                f"<h1>{escape(author)}</h1>{''.join(blocks)}",
                crumb=[("Home", "/"), ("Authors", "/authors/"), (author, "")],
                active="authors",
            ),
        )

    write(
        DIST / "authors" / "index.html",
        layout(
            "Authors",
            f"<h1>Authors</h1><ul class='card-list'>{''.join(author_links)}</ul>",
            crumb=[("Home", "/"), ("Authors", "")],
            active="authors",
        ),
    )

    # --- Search / Explore / About ---
    (DIST / "data").mkdir(exist_ok=True)
    (DIST / "data" / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    explore_index = build_explore_index(excerpts, works, topic_meta)
    (DIST / "data" / "explore-index.json").write_text(
        json.dumps(explore_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    explore_body = """
<div class="explore" data-explore>
  <div class="explore-chrome">
    <h1>Explore</h1>
    <a class="explore-home" href="/">← Library</a>
    <label class="field field-topic"><span>Topic</span><select id="explore-topic"></select></label>
    <button type="button" class="explore-filters-toggle" id="explore-filters-toggle" aria-expanded="false">Filters</button>
    <label class="field field-extra"><span>Era</span><select id="explore-era"></select></label>
    <label class="field field-extra"><span>Author</span><select id="explore-author"></select></label>
    <label class="field field-extra"><span>Compare</span><select id="explore-compare-add"></select></label>
    <div class="explore-chips" id="explore-chips"></div>
    <div class="explore-seg" role="group" aria-label="Scale">
      <button type="button" id="zoom-century">Centuries</button>
      <button type="button" id="zoom-year">Years</button>
    </div>
  </div>
  <aside id="explore-tip" class="explore-tip" data-open="0" hidden>
    <strong class="tip-title"></strong>
    <span class="tip-body" id="explore-tip-body"></span>
    <button type="button" id="explore-tip-toggle">Show note</button>
  </aside>
  <div class="explore-stage">
    <div class="explore-canvas" id="explore-canvas">
      <div class="explore-tooltip" id="explore-tooltip"></div>
    </div>
    <aside class="explore-drawer" id="explore-drawer">
      <p class="empty">Loading…</p>
    </aside>
  </div>
</div>
"""
    write(
        DIST / "explore" / "index.html",
        layout(
            "Explore",
            explore_body,
            active="explore",
            description="See how Fathers line up on a topic across time",
            styles=["/assets/explore.css"],
            scripts=["/assets/explore.js"],
            body_class="explore-mode",
        ),
    )

    write(
        DIST / "search" / "index.html",
        layout(
            "Search",
            """<h1>Search</h1>
            <input type="search" id="q" class="search-input" placeholder="Author, topic, words…" autofocus>
            <ul id="results" class="card-list"></ul>""",
            crumb=[("Home", "/"), ("Search", "")],
            active="search",
        ),
    )
    write(
        DIST / "contribute" / "index.html",
        layout(
            "Help us",
            """<h1>Help us</h1>
            <p class="intro">This library is free. If you want to help it keep growing, pick one of these. None of them is required to read.</p>

            <ol class="help-list">
              <li class="help-option" id="donate">
                <p class="n">1</p>
                <h2>Donate</h2>
                <p>A gift on GitHub Sponsors goes straight to keeping this work going.</p>
                <p><a class="btn primary" href="https://github.com/sponsors/MrSaneApps" rel="noopener">GitHub Sponsors</a></p>
              </li>
              <li class="help-option" id="mac-app">
                <p class="n">2</p>
                <h2>Buy a Mac app</h2>
                <p>If you use a Mac, the SaneApps utilities are a one-time purchase with no subscription. They run on your machine. Buying one also supports this library.</p>
                <p><a class="btn" href="https://saneapps.com" rel="noopener">SaneApps</a></p>
              </li>
              <li class="help-option" id="ai">
                <p class="n">3</p>
                <h2>Point an AI at a slice</h2>
                <p>Copy this into your AI. Change YourName to your name.</p>
                <p><button type="button" class="btn primary" data-copy="#ai-prompt">Copy prompt</button></p>
                <pre id="ai-prompt"><code># Start here

Copy this whole file into your AI.

You are helping finish public-domain Fathers texts in new English for https://fathers.saneapps.com.

Do not copy FOTC, ACW, ANF, NPNF, blogs, or other English. Translate from the locked Greek or Latin in https://github.com/sane-apps/translations

Clone that repo if you do not already have it. Then run:

```bash
python3 scripts/claims.py start --agent YourName
```

Replace YourName with a real name. That takes the next free slice and prints what to do. One slice only.

Then:

- Read the book’s `books/&lt;slug&gt;/SESSION_HANDOFF.md`.
- Translate only the sections on that claim.
- **Pass A:** literal gloss + lemmas in `reviews/justifications/&lt;id&gt;.json` (`pass_a_gloss`). Copy an existing file in that folder for the shape.
- **Pass B:** reading English in `translations/*_english.json` → `english[]`. Same meaning as A, in the author’s voice. Do not paste A as B.
- Title the thought, not the section number.
- Finish with `python3 scripts/ai_promote.py --claim &lt;id&gt; --agent YourName`
- Stop. Do not take a second slice. Do not deploy the website. Do not run Logos.

If there is no free slice, stop and say so.

More detail: `docs/SOP.md`.</code></pre>
              </li>
              <li class="help-option" id="corrections">
                <p class="n">4</p>
                <h2>Spot-check the Greek or Latin</h2>
                <p>If you read the original language and a line of English looks wrong, send a short note. Name the work, the section, and what you think it should say.</p>
                <p><a class="btn" href="https://github.com/sane-apps/translations/issues/new?template=correction.yml">Submit a correction</a></p>
              </li>
            </ol>""",
            crumb=[("Home", "/"), ("Help us", "")],
            active="contribute",
            description="Donate, buy a Mac app, point an AI at a slice, or submit a Greek or Latin correction",
        ),
    )

    write(
        DIST / "about" / "index.html",
        layout(
            "About",
            f"""<h1>About</h1>
            <p>Fathers is a free public library: a <strong>topic map</strong> of ante-Nicene teaching, <strong>whole works</strong> in edition order, and an <strong>Explore</strong> timeline that shows how writers line up on a claim across time.</p>
            <p>Works online today include Origen’s treatises as they are finished, Cyril of Alexandria, and Julian of Eclanum’s surviving arguments. Later writers are labeled on those pages. Augustine appears first as contrast cards on Explore until his works are loaded.</p>
            <p>Some treatises here had no earlier complete English a reader could freely use. They are listed together on the <a href="/works/#no-earlier-english">works page</a>, and each one says so at the start. The English here is new.</p>
            <p>This is not a complete scholarly edition. Where Greek or Latin is loaded, open it under the reading text.</p>
            <p>Each whole work names the print it follows. Other public-domain Greek or Latin prints of the same work are checked when they exist. The reading English follows that copy-text. Where a stretch is missing there and is supplied from another witness, it is marked. Open <strong>About this text</strong> on a work for the list.</p>
            <p>Explore stance tags are editorial readings for study — not rankings of who was right. Start with <a href="/explore/?topic=free-will">Free will over time</a>.</p>
            <p>Want to help finish a text? See <a href="/contribute/">Help</a>.</p>
            <p>If it helps you, you can <a href="{SPONSORS}">support the work on GitHub Sponsors</a>.</p>""",
            crumb=[("Home", "/"), ("About", "")],
            active="about",
        ),
    )

    (DIST / "_headers").write_text(
        """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
""",
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "excerpts": len(excerpts),
                "works": len(works),
                "work_sections": sum(w["section_count"] for w in works),
                "search_docs": len(search_index),
                "explore_points": len(explore_index["points"]),
                "dist": str(DIST),
            }
        )
    )


if __name__ == "__main__":
    build()
