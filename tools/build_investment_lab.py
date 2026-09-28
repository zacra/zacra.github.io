#!/usr/bin/env python3
"""Render the static investment-lab archive from data/investment-lab.json."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "investment-lab.json"
PAGE_FILE = ROOT / "investment-lab.html"
SITEMAP_FILE = ROOT / "sitemap.xml"
TAG_ORDER = (
    "미국주식", "국내주식", "코인", "ETF", "연금", "ISA",
    "스마트스플릿", "자산배분", "전략대결", "단타", "중장기",
    "추세추종", "결산", "백테스트", "실계좌", "파이썬자동매매",
)
FILTERS = (
    ("전체", "all"), ("미국주식", "미국주식"), ("국내주식", "국내주식"),
    ("코인", "코인"), ("자산배분", "자산배분"), ("전략대결", "전략대결"),
)
START_MARKER = "<!-- GMA_INVESTMENT_LAB_GENERATED_START -->"
END_MARKER = "<!-- GMA_INVESTMENT_LAB_GENERATED_END -->"
JSONLD_START = "<!-- GMA_INVESTMENT_LAB_JSONLD_START -->"
JSONLD_END = "<!-- GMA_INVESTMENT_LAB_JSONLD_END -->"
FILTERS_START = "<!-- GMA_INVESTMENT_LAB_FILTERS_START -->"
FILTERS_END = "<!-- GMA_INVESTMENT_LAB_FILTERS_END -->"
UPDATED_START = "<!-- GMA_INVESTMENT_LAB_UPDATED_START -->"
UPDATED_END = "<!-- GMA_INVESTMENT_LAB_UPDATED_END -->"


def fail(message: str) -> None:
    raise SystemExit(f"투자 실험실 데이터 오류: {message}")


def normalized_naver_url(value: str) -> str:
    parts = urlsplit(value.strip())
    host = (parts.hostname or "").lower()
    if parts.scheme != "https" or host not in {"blog.naver.com", "m.blog.naver.com"}:
        fail(f"네이버 블로그 HTTPS 원문 URL이어야 합니다: {value}")
    if not parts.path.strip("/"):
        fail(f"원문 게시물 경로가 없습니다: {value}")
    path = re.sub(r"/+", "/", parts.path).rstrip("/")
    return urlunsplit(("https", "blog.naver.com", path, "", ""))


def load_entries() -> tuple[dict, list[dict]]:
    try:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"JSON을 읽을 수 없습니다 ({exc})")
    if not isinstance(payload, dict) or payload.get("version") != 1:
        fail("최상위 객체의 version은 1이어야 합니다")
    try:
        date.fromisoformat(payload["updated_at"])
    except (KeyError, TypeError, ValueError):
        fail("updated_at은 YYYY-MM-DD 날짜여야 합니다")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        fail("entries는 배열이어야 합니다")

    seen_urls: dict[str, str] = {}
    seen_ids: set[str] = set()
    clean_entries: list[dict] = []
    for index, entry in enumerate(entries, start=1):
        where = f"entries[{index - 1}]"
        if not isinstance(entry, dict):
            fail(f"{where}는 객체여야 합니다")
        for key in ("id", "date", "title", "summary", "threads_text", "tags", "url"):
            if key not in entry:
                fail(f"{where}.{key}가 필요합니다")
        if not isinstance(entry["id"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
            fail(f"{where}.id는 소문자 영문·숫자·하이픈 slug여야 합니다")
        if entry["id"] in seen_ids:
            fail(f"중복 id: {entry['id']}")
        seen_ids.add(entry["id"])
        try:
            published_date = date.fromisoformat(entry["date"])
        except (TypeError, ValueError):
            fail(f"{where}.date는 YYYY-MM-DD 날짜여야 합니다")
        for key in ("title", "summary", "threads_text"):
            if not isinstance(entry[key], str) or not entry[key].strip():
                fail(f"{where}.{key}는 비어 있지 않은 문자열이어야 합니다")
        tags = entry["tags"]
        if not isinstance(tags, list) or not 2 <= len(tags) <= 4 or any(not isinstance(tag, str) for tag in tags):
            fail(f"{where}.tags는 2~4개여야 합니다")
        if len(set(tags)) != len(tags) or any(tag not in TAG_ORDER for tag in tags):
            fail(f"{where}.tags에 중복 또는 미등록 태그가 있습니다")
        if "파이썬자동매매" not in tags:
            fail(f"{where}.tags에는 파이썬자동매매가 필요합니다")
        url = normalized_naver_url(entry["url"] if isinstance(entry["url"], str) else "")
        if url in seen_urls:
            fail(f"네이버 원문 URL 중복: {url} ({seen_urls[url]} / {entry['id']})")
        seen_urls[url] = entry["id"]
        thumbnail = entry.get("thumbnail")
        if thumbnail is not None:
            if not isinstance(thumbnail, str) or urlsplit(thumbnail).scheme != "https":
                fail(f"{where}.thumbnail은 null 또는 HTTPS URL이어야 합니다")
        clean_entries.append({**entry, "url": url, "thumbnail": thumbnail})
    return payload, sorted(clean_entries, key=lambda item: (item["date"], item["id"]), reverse=True)


def render_entry(entry: dict) -> str:
    tags = " ".join(entry["tags"])
    escaped_tags = html.escape(tags, quote=True)
    tag_markup = " ".join(f'<span class="lab-tag">{html.escape(tag)}</span>' for tag in entry["tags"])
    thumbnail = ""
    card_class = "lab-card"
    if entry["thumbnail"]:
        card_class += " has-thumbnail"
        thumbnail = (
            f'<a class="lab-link-card-image" href="{html.escape(entry["url"], quote=True)}" '
            f'rel="noopener noreferrer" target="_blank" aria-label="네이버 원문 열기: {html.escape(entry["title"], quote=True)}">'
            f'<img class="lab-thumbnail" src="{html.escape(entry["thumbnail"], quote=True)}" '
            f'alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer"></a>'
        )
    threads_lines = "\n".join(html.escape(line) for line in entry["threads_text"].splitlines())
    return (
        f'<article class="{card_class}" data-tags="{escaped_tags}" id="{html.escape(entry["id"], quote=True)}">'
        f'{thumbnail}<div class="lab-card-content">'
        f'<p class="lab-card-date"><time datetime="{html.escape(entry["date"], quote=True)}">'
        f'{html.escape(entry["date"].replace("-", "."))}</time></p>'
        f'<h3>{html.escape(entry["title"])}</h3>'
        f'<p class="lab-summary">{html.escape(entry["summary"])}</p>'
        f'<details class="lab-threads"><summary>요약 내용 보기</summary>'
        f'<div class="lab-threads-text">{threads_lines}</div></details>'
        f'<div class="lab-tags" aria-label="태그">{tag_markup}</div>'
        f'<p class="lab-original"><a href="{html.escape(entry["url"], quote=True)}" '
        f'rel="noopener noreferrer" target="_blank">네이버 원문 보기 <span aria-hidden="true">→</span></a></p>'
        "</div></article>"
    )


def render_cards(entries: list[dict]) -> str:
    if not entries:
        return (
            '<section class="lab-empty notice" aria-labelledby="lab-empty-title">'
            '<h2 id="lab-empty-title">아직 등록된 기록이 없습니다</h2>'
            '<p>게만아가 실제 자금을 시스템으로 운용하며 남긴 투자 실험을 요약해 소개합니다. '
            '이전 기록은 네이버 투자 실험실에서 확인할 수 있습니다.</p>'
            '<p><a class="btn primary" href="https://m.site.naver.com/1TgXn" '
            'rel="noopener noreferrer" target="_blank">투자 실험실 결산 →</a></p>'
            '</section>'
        )
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["date"]].append(entry)
    sections: list[str] = []
    for day in sorted(grouped, reverse=True):
        label = day.replace("-", ".")
        articles = "\n".join(render_entry(entry) for entry in grouped[day])
        sections.append(
            f'<section class="lab-day" aria-labelledby="lab-day-{day}">'
            f'<h2 id="lab-day-{day}"><time datetime="{day}">{label}</time></h2>'
            f'<div class="lab-day-cards">{articles}</div></section>'
        )
    return "\n".join(sections)


def render_filters(entries: list[dict]) -> str:
    if not entries:
        return ""
    buttons = []
    for index, (label, tag) in enumerate(FILTERS):
        selected = " aria-pressed=\"true\"" if index == 0 else " aria-pressed=\"false\""
        buttons.append(
            f'<button class="lab-filter" type="button" data-filter="{html.escape(tag, quote=True)}"{selected}>'
            f'{html.escape(label)}</button>'
        )
    return (
        '<div class="lab-filters" role="group" aria-label="투자 기록 분류">'
        + "".join(buttons)
        + '</div><p class="lab-filter-status" aria-live="polite"></p>'
    )


def render_jsonld(entries: list[dict], updated_at: str) -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://zacra.github.io/investment-lab.html#collection",
                "url": "https://zacra.github.io/investment-lab.html",
                "name": "게만아 투자 실험실 | 파이썬 자동매매 실계좌 기록 아카이브",
                "description": "게만아가 실제 계좌로 운용하는 주식·ETF·코인 시스템 투자 기록을 날짜별로 요약하고 네이버 상세 기록으로 연결하는 공식 아카이브입니다.",
                "inLanguage": "ko-KR",
                "dateModified": updated_at,
                "mainEntity": {"@id": "https://zacra.github.io/investment-lab.html#itemlist"},
            },
            {
                "@type": "ItemList",
                "@id": "https://zacra.github.io/investment-lab.html#itemlist",
                "itemListOrder": "https://schema.org/ItemListOrderDescending",
                "numberOfItems": len(entries),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": position,
                        "name": entry["title"],
                        "url": entry["url"],
                    }
                    for position, entry in enumerate(entries, start=1)
                ],
            },
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>"


def update_sitemap(sitemap: str, updated_at: str) -> str:
    pattern = re.compile(
        r"(<url>\s*<loc>https://zacra\.github\.io/investment-lab\.html</loc>\s*<lastmod>)[^<]*(</lastmod>\s*</url>)",
        re.IGNORECASE,
    )
    sitemap, count = pattern.subn(rf"\g<1>{updated_at}\g<2>", sitemap)
    if count != 1:
        fail("sitemap.xml에 investment-lab.html URL이 정확히 한 개 있어야 합니다")
    return sitemap


def replace_region(document: str, start: str, end: str, value: str) -> str:
    if document.count(start) != 1 or document.count(end) != 1:
        fail(f"템플릿 marker가 정확히 한 쌍이어야 합니다: {start}")
    before, remainder = document.split(start, 1)
    _, after = remainder.split(end, 1)
    return before + start + "\n" + value + "\n" + end + after


def main() -> None:
    payload, entries = load_entries()
    try:
        document = PAGE_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"페이지 템플릿을 읽을 수 없습니다 ({exc})")
    document = replace_region(document, START_MARKER, END_MARKER, render_cards(entries))
    document = replace_region(document, JSONLD_START, JSONLD_END, render_jsonld(entries, payload["updated_at"]))
    document = replace_region(document, FILTERS_START, FILTERS_END, render_filters(entries))
    document = replace_region(
        document, UPDATED_START, UPDATED_END,
        f'<time datetime="{html.escape(payload["updated_at"], quote=True)}">{html.escape(payload["updated_at"].replace("-", "."))}</time>',
    )
    try:
        sitemap = SITEMAP_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"sitemap.xml을 읽을 수 없습니다 ({exc})")
    sitemap = update_sitemap(sitemap, payload["updated_at"])
    PAGE_FILE.write_text(document, encoding="utf-8")
    SITEMAP_FILE.write_text(sitemap, encoding="utf-8")
    print(f"정적 카드 생성 완료: {len(entries)}건 · {PAGE_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
