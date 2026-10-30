#!/usr/bin/env python3
"""Render the strategy catalog page (strategies.html) from data/strategies.json.

새 전략을 추가할 때는 data/strategies.json의 entries에 항목 하나를 더한 뒤
`python3 tools/build_strategies.py`를 실행하면 페이지, 구조화 데이터, sitemap 날짜가 함께 갱신됩니다.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "strategies.json"
PAGE_FILE = ROOT / "strategies.html"
SITEMAP_FILE = ROOT / "sitemap.xml"
URL = "https://zacra.github.io/strategies.html"
TITLE = "게만아 패키지 전략·시스템 카탈로그 | 주식·ETF·코인 자동매매 전략 목록"
DESC = ("게만아 패키지에 포함된 주식·ETF·코인 자동매매 전략과 시스템을 유형별로 정리했습니다. "
        "자산배분, 모멘텀, 분할매매, 변동성 돌파, 코인 현물·선물, 증권사·거래소 공통모듈까지 "
        "전략마다 시장, 대상 자산, 실행 주기와 원본 포스팅 링크를 안내하며, 유형별로 백테스트 Calmar 지수가 높은 순으로 정렬했습니다.")
OG_TITLE = "게만아 패키지 전략·시스템 카탈로그"
OG_DESC = "주식·ETF·코인 자동매매 전략과 시스템을 유형별로 정리한 목록. 시장·자산·주기와 원본 포스팅 링크."

HEAD = """<!doctype html><html lang="ko"><head>
<script defer src="/assets/analytics.js"></script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="{url}"><link rel="stylesheet" href="/assets/style.css">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{ogt}"><meta property="og:description" content="{ogd}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://zacra.github.io/assets/og-default.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{ogt}"><meta name="twitter:description" content="{ogd}"><meta name="twitter:image" content="https://zacra.github.io/assets/og-default.png">
<script type="application/ld+json">{jsonld}</script>
  <link href="/favicon.ico" rel="icon" sizes="any"/>
  <link href="/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
  <link href="/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
  <link href="/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
  <link href="/site.webmanifest" rel="manifest"/>
  <meta content="#0f6a66" name="theme-color"/>
</head><body><a class="skip" href="#main">본문 바로가기</a><header class="site-header"><nav class="nav" aria-label="주요 메뉴">
<a class="brand" href="/"><img src="/favicon-32x32.png" alt="" aria-hidden="true" style="width:28px;height:28px;border-radius:7px;vertical-align:middle;margin-right:8px;box-shadow:0 1px 4px rgba(0,0,0,.18);"/>게만아 <small>공식 가이드</small></a>
<div class="nav-links">
<a href="/investment-philosophy.html">투자 철학</a>
<a href="/python-auto-trading.html">자동매매 시작</a>
<a href="/system-guide.html">시작 가이드</a>
<a href="/investment-lab.html">투자 실험실</a><a href="/super-moving-average.html">슈퍼 이동평균</a>
<a href="/coin-double-ma.html">코인 더블 이평</a>
<a href="/package.html">패키지</a>
<a class="nav-cta" href="/strategies.html" aria-current="page">전략 카탈로그</a>
<a href="/broker-openapi.html">멀티 증권사 API</a>
<a href="/starter.html">무료 Starter</a>
</div></nav></header>"""

FOOT = """</main><footer class="site-footer"><div class="footer-inner">
<p><strong>게만아</strong> · 주식·ETF·코인 파이썬 자동매매·백테스트·API 공식 가이드</p>
<p>교육·기술 정보 제공 목적이며 특정 금융상품의 추천 또는 수익 보장이 아닙니다. 증권사·거래소 API 사양은 변경될 수 있으므로 실제 구현 전 최신 공식 문서를 확인하세요.</p>
<p><a href="https://blog.naver.com/zacra" target="_blank" rel="noopener noreferrer">네이버 블로그</a> · <a href="/games.html">게임 만드는 아빠</a> · <a href="/glossary.html">용어 풀이</a> · <a href="/sources.html">공식 출처</a> · 마지막 업데이트 {date}</p>
</div></footer>
<script>
(function(){{
  var h=document.querySelector('.site-header'),b=document.getElementById('cta-bar'),r=document.documentElement;
  function set(){{r.style.setProperty('--hdr',(h?h.offsetHeight:0)+'px');r.style.setProperty('--cta',(b?b.offsetHeight:0)+'px');}}
  set();window.addEventListener('resize',set);window.addEventListener('load',set);
}})();
(function(){{
  var q=document.getElementById('strat-q');if(!q)return;
  var cards=[].slice.call(document.querySelectorAll('.strat'));
  var sections=[].slice.call(document.querySelectorAll('.strat-section'));
  var status=document.getElementById('strat-status');
  q.addEventListener('input',function(){{
    var v=q.value.trim().toLowerCase(),n=0;
    cards.forEach(function(c){{var hit=!v||c.textContent.toLowerCase().indexOf(v)>-1;c.hidden=!hit;if(hit)n++;}});
    sections.forEach(function(s){{s.hidden=!s.querySelector('.strat:not([hidden])');}});
    if(status)status.textContent=v?('검색 결과 '+n+'개'):'';
  }});
}})();
</script></body></html>"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def fmt_date(d: str | None) -> str:
    if d and re.fullmatch(r"\d{8}", d):
        return f"{d[:4]}.{d[4:6]}"
    return ""


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    cats = data["categories"]
    # 정렬: 특별 항목(S) 먼저 → 분류 안에서 Calmar 순위가 있는 전략(rank 오름차순) → 순위 없는 전략은 번호순
    # (rank 는 tools/rank_by_calmar.py 가 저장하며 수치는 저장하지 않습니다)
    entries = sorted(data["entries"], key=lambda e: (not e.get("special"), e.get("rank") is None, e.get("rank", 0),
                                                       e["code"] if isinstance(e["code"], int) else 0))
    numbered = [e for e in entries if not e.get("special")]
    updated = data["updated_at"]
    by_cat: dict[str, list[dict]] = {c["name"]: [] for c in cats}
    for e in entries:
        if e["category"] not in by_cat:
            raise SystemExit(f"알 수 없는 분류: {e['category']} (번호 {e['code']})")
        by_cat[e["category"]].append(e)

    # structured data
    items = []
    shown = [e for c in cats for e in by_cat[c["name"]]]
    for pos, e in enumerate(shown, 1):
        items.append({"@type": "ListItem", "position": pos, "name": f"[{e['code']}] {e['title']}",
                      "url": f"{URL}#s-{e['code']}", "description": e["summary"]})
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": OG_TITLE, "url": URL, "inLanguage": "ko-KR",
         "description": DESC, "dateModified": updated,
         "author": {"@type": "Person", "name": "게만아", "url": "https://zacra.github.io/about.html"},
         "publisher": {"@type": "Organization", "name": "자밥스튜디오", "url": "https://zacra.github.io/"},
         "isPartOf": {"@type": "WebPage", "url": "https://zacra.github.io/package.html"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://zacra.github.io/"},
            {"@type": "ListItem", "position": 2, "name": "패키지", "item": "https://zacra.github.io/package.html"},
            {"@type": "ListItem", "position": 3, "name": "전략·시스템 카탈로그", "item": URL}]},
        {"@type": "ItemList", "name": OG_TITLE, "numberOfItems": len(entries), "itemListElement": items},
    ]}
    jsonld = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))

    pillar_cards = []
    for e in sorted((x for x in data["entries"] if x.get("pillar")), key=lambda x: x["pillar"].get("order", 9)):
        pl = e["pillar"]
        btns = []
        if e.get("internal"):
            btns.append(f'<a class="btn primary" href="{esc(e["internal"]["url"])}">전략 자세히 보기 →</a>')
        if e.get("urls"):
            btns.append(f'<a class="btn" href="{esc(e["urls"][0])}" target="_blank" rel="noopener noreferrer">백테스트 결과 보기 (네이버) →</a>')
        if pl.get("buy"):
            btns.append(f'<a class="btn accent" href="{esc(pl["buy"])}" target="_blank" rel="noopener noreferrer">단독 20만원 시작하기</a>')
        price = f'<p class="pillar-price">{esc(pl["price"])}</p>' if pl.get("price") else ""
        pillar_cards.append(
            f'<article class="pillar"><p class="pillar-tag">{esc(pl["tag"])}</p><h3>{esc(e["title"])}</h3>{price}'
            f'<p>{esc(pl["blurb"])}</p><p class="strat-links">{" ".join(btns)}</p></article>')
    pillars = ("" if not pillar_cards else
               '<section class="pillars"><h2>장기투자 대표 전략 · 주식 1개, 코인 1개</h2>'
               '<p>하나씩만 꼽는다면 이 두 가지입니다. 둘 다 게만아 패키지에 포함되어 있고, 각각 200,000원 단독 상품으로도 이용할 수 있습니다.</p>'
               f'<div class="pillar-grid">{"".join(pillar_cards)}</div></section>')

    chips = "".join(
        f'<a href="#c-{c["id"]}">{esc(c["name"])} <span>{len(by_cat[c["name"]])}</span></a>' for c in cats)

    sections = []
    for c in cats:
        lst = by_cat[c["name"]]
        if not lst:
            continue
        cards = []
        for e in lst:
            meta = []
            if e.get("market"):
                meta.append(f'<li><b>시장</b> {esc(e["market"])}</li>')
            if e.get("assets") and e["assets"] != "-":
                meta.append(f'<li><b>대상</b> {esc(e["assets"])}</li>')
            if e.get("cycle") and not e["cycle"].startswith("-"):
                meta.append(f'<li><b>실행</b> {esc(e["cycle"])}</li>')
            if e.get("broker"):
                meta.append(f'<li><b>Broker 코드</b> {esc(e["broker"])}</li>')
            links = []
            for i, u in enumerate(e["urls"], 1):
                label = "원본 포스팅(네이버)" if len(e["urls"]) == 1 else f"원본 포스팅 {i}(네이버)"
                links.append(f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{label} →</a>')
            if e.get("internal"):
                links.append(f'<a href="{esc(e["internal"]["url"])}">{esc(e["internal"]["label"])} →</a>')
            date = fmt_date(e.get("post_date"))
            if date:
                links.append(f'<span class="strat-date">게시 {date}</span>')
            special = bool(e.get("special"))
            cards.append(
                f'<article class="strat{" strat-special" if special else ""}" id="s-{e["code"]}">'
                f'<h3><span class="strat-no{" special" if special else ""}">{e["code"]}</span> {esc(e["title"])}</h3>'
                f'<ul class="strat-meta">{"".join(meta)}</ul>'
                f'<p>{esc(e["summary"])}</p>'
                f'<p class="strat-links">{" ".join(links)}</p></article>')
        sections.append(
            f'<section class="strat-section" id="c-{c["id"]}"><h2>{esc(c["name"])} '
            f'<small>{len(lst)}</small></h2><p class="strat-desc">{esc(c["desc"])}</p>'
            f'<div class="strat-list">{"".join(cards)}</div></section>')

    body = f"""<main id="main"><div class="breadcrumb"><a href="/">홈</a> › <a href="/package.html">패키지</a> › 전략·시스템 카탈로그</div>
<h1>게만아 패키지 전략·시스템 카탈로그</h1>
<div class="cta-bar" id="cta-bar"><span class="cta-text"><strong>이 전략·시스템 전부가 게만아 패키지에 포함됩니다</strong> · 500,000원</span><a class="cta-btn" href="https://www.latpeed.com/products/Wxjik" target="_blank" rel="noopener noreferrer"><span class="long">네이버페이·카카오페이·카드로 시작하기</span><span class="short">시작하기</span></a></div>
<p class="lead">게만아 패키지의 주식·ETF·코인 자동매매 <strong>전략과 시스템 {len(numbered)}개</strong>를 유형별로 정리했습니다. 시장·대상·실행 주기를 한눈에 보고, 자세한 설명은 원본 포스팅에서 확인하세요.</p>
<figure class="intro-anim"><a href="/package.html" aria-label="게만아 파이썬 자동매매 패키지 소개 보기"><img src="/assets/intro/package.webp" alt="게만아 파이썬 자동매매 패키지 소개 이미지: AI로 자동매매 코드, 이제 금방 만듭니다. 그런데 그 코드, 내 계좌에 바로 연결해도 될까요?" width="640" height="640" decoding="async"/></a></figure>
<div class="notice"><ul>
<li>번호는 <a href="/package-content-guide.html">패키지 콘텐츠 번호</a>와 같고, <b>S</b>는 번호 없는 스페셜(대표) 전략입니다.</li>
<li>각 유형은 백테스트 <a href="/glossary.html#calmar">Calmar 지수</a>(수익률÷최대낙폭)가 높은 순이며, 백테스트가 없는 전략은 뒤에 번호순입니다. 결과는 포트폴리오·기간에 따라 달라지니 <strong>직접 백테스트로 확인</strong>해 보세요.</li>
<li>교육·기술 정보 제공 목적이며 종목 추천이나 수익 보장이 아닙니다.</li>
</ul></div>
{pillars}
<p class="strat-nav">{chips}</p>
<p class="strat-search"><label for="strat-q">전략 검색</label> <input id="strat-q" type="search" placeholder="예: 올웨더, 업비트, 트레일링, TQQQ" autocomplete="off"/> <span id="strat-status" role="status"></span></p>
{"".join(sections)}
<section class="callout"><h2>전략을 직접 써보려면</h2>
<p>전략 코드는 게만아 패키지에 포함돼 있고, 무료 Starter로 전체 흐름을 먼저 체험할 수 있습니다. 주식·ETF 장기 전략 하나만 원한다면 <a href="/super-moving-average.html">슈퍼 이동평균 V2 단독 20만원</a>, 코인 장기 전략 하나만 원한다면 <a href="/coin-double-ma.html">코인 더블 이동평균 New 단독 20만원</a>도 있습니다.</p>
<div class="actions"><a class="btn primary" href="https://www.latpeed.com/products/Wxjik" target="_blank" rel="noopener noreferrer">패키지 시작하기 · 500,000원</a><a class="btn" href="/starter.html">무료 Starter</a><a class="btn" href="/system-guide.html">시작 가이드</a></div></section>
<p class="updated">문서 업데이트: {updated} · 교육·기술 정보 제공 목적이며 투자 권유가 아닙니다.</p>
"""
    page = HEAD.format(title=esc(TITLE), desc=esc(DESC), url=URL, ogt=esc(OG_TITLE), ogd=esc(OG_DESC),
                       jsonld=jsonld) + body + FOOT.format(date=updated)
    PAGE_FILE.write_text(page, encoding="utf-8")

    if SITEMAP_FILE.exists():
        sm = SITEMAP_FILE.read_text(encoding="utf-8")
        entry = f"  <url>\n    <loc>{URL}</loc>\n    <lastmod>{updated}</lastmod>\n  </url>\n"
        if f"<loc>{URL}</loc>" in sm:
            sm = re.sub(r"(<loc>" + re.escape(URL) + r"</loc>\s*<lastmod>)[^<]*", r"\g<1>" + updated, sm)
        else:
            sm = sm.replace("</urlset>", entry + "</urlset>")
        SITEMAP_FILE.write_text(sm, encoding="utf-8")
    print(f"{PAGE_FILE.name}: {len(entries)} strategies, {len(cats)} categories")


if __name__ == "__main__":
    main()
