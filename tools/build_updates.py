#!/usr/bin/env python3
"""data/updates.json 으로 updates.html(업데이트 노트)을 생성합니다.

새 업데이트를 추가하려면 data/updates.json 의 entries 맨 앞에 항목을 추가하고
`python3 tools/build_updates.py` 를 실행하세요. 페이지·사이트맵(lastmod)이 함께 갱신됩니다.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "updates.json"
PAGE = ROOT / "updates.html"
SEED = ROOT / "brokers" / "mr.html"      # 페이지가 없을 때 머리글·메뉴·바닥글을 가져올 기존 페이지
SITEMAP = ROOT / "sitemap.xml"
URL = "https://zacra.github.io/updates.html"
TITLE = "게만아 업데이트 노트 | 패키지·전략·무료 Starter·공식 가이드 최신 변경"
OGT = "게만아 업데이트 노트"
DESC = "게만아 패키지에 추가된 콘텐츠, 슈퍼 이동평균 업데이트, 무료 Starter 지원 증권사, 공식 가이드의 최신 변경 내용을 날짜별로 정리합니다."


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def plain(h: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = sorted(data["entries"], key=lambda e: e["date"], reverse=True)
    latest = entries[0]["date"]
    base = (PAGE if PAGE.exists() else SEED).read_text(encoding="utf-8")
    base = base.replace("https://zacra.github.io/brokers/mr.html", URL)

    s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(TITLE)}</title>", base, count=1)
    for pat, val in [
        (r'(<meta name="description" content=")[^"]*(")', DESC),
        (r'(<meta property="og:title" content=")[^"]*(")', OGT),
        (r'(<meta property="og:description" content=")[^"]*(")', DESC),
        (r'(<meta name="twitter:title" content=")[^"]*(")', OGT),
        (r'(<meta name="twitter:description" content=")[^"]*(")', DESC),
    ]:
        s = re.sub(pat, lambda m, v=val: m.group(1) + esc(v) + m.group(2), s, count=1)

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": OGT, "description": DESC, "url": URL, "inLanguage": "ko-KR",
         "dateModified": latest, "publisher": {"@id": "https://zacra.github.io/#organization"},
         "hasPart": [{"@type": "WebPageElement", "name": e["title"], "datePublished": e["date"]} for e in entries]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://zacra.github.io/"},
            {"@type": "ListItem", "position": 2, "name": OGT, "item": URL}]},
    ]}
    ldj = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">' + ldj + "</script>", s, count=1, flags=re.S)

    blocks = []
    for e in entries:
        lis = []
        for it in e["items"]:
            links = " · ".join(f'<a href="{u}">{n} →</a>' for n, u in it.get("links", []))
            lis.append(f'<li><span class="upd-type">{it["type"]}</span> {it["text"]}' + (f" <span class=\"upd-links\">{links}</span>" if links else "") + "</li>")
        blocks.append(f'<section class="upd" id="u-{e["date"]}"><h2><time datetime="{e["date"]}">{e["date"]}</time> · {e["title"]}</h2><ul class="upd-list">{"".join(lis)}</ul></section>')

    main_html = f'''<main id="main"><div class="breadcrumb"><a href="/">홈</a> › {OGT}</div><p class="eyebrow">UPDATES</p><h1>게만아 업데이트 노트</h1>
<p class="lead">게만아 패키지에 <strong>추가된 콘텐츠</strong>, 슈퍼 이동평균 <strong>업데이트</strong>, 무료 Starter <strong>지원 증권사</strong>, 공식 가이드의 <strong>최신 변경</strong>을 날짜별로 정리합니다. 날짜는 이 사이트에 반영한 날 기준입니다.</p>
<div class="easy-box"><p><strong>이 페이지는 이렇게 쓰세요</strong> · 새로 들어온 패키지 번호와 바뀐 규칙을 한눈에 보고, 자세한 설명은 각 링크와 네이버 공식 포스팅에서 확인하세요. 전체 목록은 <a href="/strategies.html">전략·시스템 카탈로그</a>와 <a href="/package-content-guide.html">패키지 콘텐츠 전체 가이드</a>에 있습니다.</p></div>
{"".join(blocks)}
<section class="notice"><h2>확인할 때 참고하세요</h2><p>각 항목의 상세 사양과 최신 안내는 네이버 블로그의 공식 포스팅이 가장 정확합니다. 증권사·거래소의 정책과 API 사양은 바뀔 수 있으므로 실제 사용 전에 공식 문서를 확인하세요. 이 사이트는 교육·기술 정보 제공 목적이며 투자 권유나 수익 보장이 아닙니다.</p></section>
<p class="updated">문서 업데이트: {latest}</p></main>'''
    s = re.sub(r'<main id="main">.*?</main>', lambda m: main_html, s, count=1, flags=re.S)
    PAGE.write_text(s, encoding="utf-8")

    sm = SITEMAP.read_text(encoding="utf-8")
    if URL not in sm:
        anchor = "  <url>\n    <loc>https://zacra.github.io/package-content-guide.html</loc>"
        entry = f"  <url>\n    <loc>{URL}</loc>\n    <lastmod>{latest}</lastmod>\n  </url>\n"
        sm = sm.replace(anchor, entry + anchor, 1) if anchor in sm else sm.replace("</urlset>", entry + "</urlset>")
    sm = re.sub(r"(<loc>" + re.escape(URL) + r"</loc>\s*<lastmod>)[^<]+", r"\g<1>" + latest, sm)
    SITEMAP.write_text(sm, encoding="utf-8")
    print(f"{PAGE.name}: {len(entries)} updates")


if __name__ == "__main__":
    main()
