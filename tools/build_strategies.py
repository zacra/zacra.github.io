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
        if c.get("ranked"):
            lead_special = any(x.get("special") for x in lst)
            sort_note = ("슈퍼 이동평균 V2 먼저 · 이어서 " if lead_special else "") + \
                '<a href="#calmar">백테스트 Calmar 높은 순</a> · 백테스트가 없거나 비교하기 어려운 전략은 맨 뒤에 번호순'
        else:
            sort_note = "번호순 (전략이 아닌 보조 목록이라 순위 없음)"
        sections.append(
            f'<section class="strat-section" id="c-{c["id"]}"><h2>{esc(c["name"])} '
            f'<small>{len(lst)}</small></h2><p class="strat-desc">{esc(c["desc"])}</p>'
            f'<p class="strat-sort">정렬: {sort_note}</p>'
            f'<div class="strat-list">{"".join(cards)}</div></section>')

    body = f"""<main id="main"><div class="breadcrumb"><a href="/">홈</a> › <a href="/package.html">패키지</a> › 전략·시스템 카탈로그</div>
<h1>게만아 패키지 전략·시스템 카탈로그</h1>
<p class="lead">게만아 패키지에 들어 있는 주식·ETF·코인 자동매매 <strong>전략과 시스템 {len(numbered)}개</strong>를 유형별로 정리한 목록입니다. 전략마다 어떤 시장에서 무엇을 대상으로 어떤 주기로 실행되는지 한눈에 보고, 자세한 설명은 원본 포스팅에서 이어서 확인하세요.</p>
<div class="notice"><p><strong>이 목록을 읽는 법</strong></p>
<ul>
<li>앞의 번호는 <a href="/package-content-guide.html">패키지 콘텐츠 번호</a>와 같습니다. 번호별 필독 포스팅과 crontab 예시는 그 페이지에 있습니다. 번호 대신 <b>S</b>가 붙은 것은 번호 없이 맨 앞에 둔 스페셜(대표) 전략입니다.</li>
<li>교육·기술 정보 제공 목적이며 종목 추천이나 수익 보장이 아닙니다. <strong>과거 성과 수치는 일부러 싣지 않았습니다.</strong> 원본 포스팅의 수치는 당시 조건의 과거 결과입니다.</li>
<li>백테스트 코드는 별도 도구(<a href="#c-tools">백테스트·도구</a>)로만 들어 있는 것이 아니라 다른 번호의 전략에 함께 포함된 경우도 있습니다. 전략마다 다르니 원본 포스팅에서 확인하세요.</li>
<li>같은 전략도 시장·기간·비용 가정에 따라 결과가 달라지고, 일부 전략은 이후 개선판이나 다른 전략으로 대체됐다고 포스팅에 밝혀 두었습니다.</li>
<li>주식 전략은 증권사 공통모듈로 증권사를 바꿔 쓰는 구조를 지향하며, 지원 범위는 콘텐츠마다 다릅니다. <a href="/broker-openapi.html">멀티 증권사 API 구조 보기 →</a></li>
</ul></div>
<div class="easy-box" id="calmar"><p><strong>정렬 기준: Calmar(칼마) 지수</strong></p>
<p>각 유형 안의 전략은 <strong>백테스트의 Calmar 지수가 높은 순</strong>으로 나열했습니다. Calmar는 <strong>연평균 수익률(CAGR)을 최대낙폭(<a href="/mdd.html">MDD</a>)의 크기로 나눈 값</strong>입니다. “가장 크게 떨어졌던 구간에 비해 얼마나 벌었는지”를 한 숫자로 보여주며, 값이 클수록 같은 낙폭 대비 수익 효율이 좋았다는 뜻입니다. 1.0이면 연평균 수익률이 최대낙폭과 같은 크기라는 뜻이고, 수익이 마이너스면 값도 마이너스입니다.</p>
<ul>
<li>기준은 2026년 10월에 패키지의 백테스트 코드를 실행한 결과입니다. 한 번호에 백테스트 버전이 여러 개면 가장 높은 값을 기준으로 했습니다.</li>
<li>기간이 짧거나 분봉처럼 서로 비교하기 어려운 결과, 백테스트가 없는 전략은 순위에서 빼고 <strong>각 유형의 맨 뒤에 번호순</strong>으로 두었습니다. 보조 시스템·백테스트 도구·공통모듈은 순위 없이 번호순입니다.</li>
<li>슈퍼 이동평균 V2는 대표 전략이라 순위와 상관없이 <strong>자산배분 맨 앞</strong>에 둡니다.</li>
<li><strong>세부 수치는 공개하지 않습니다.</strong> 백테스트 결과는 <strong>포트폴리오·종목·기간·설정에 따라 크게 달라지고</strong> 과거 결과가 미래를 보장하지 않으며, Calmar가 높다고 안전하거나 수익이 난다는 뜻이 아닙니다. 관심 있는 전략은 내 포트폴리오와 기간으로 <strong>직접 백테스트해 확인</strong>하세요. <a href="/backtest.html">백테스트 체크리스트 →</a></li>
</ul></div>
<p class="strat-nav">{chips}</p>
<p class="strat-search"><label for="strat-q">전략 검색</label> <input id="strat-q" type="search" placeholder="예: 올웨더, 업비트, 트레일링, TQQQ" autocomplete="off"/> <span id="strat-status" role="status"></span></p>
{"".join(sections)}
<section class="callout"><h2>전략을 직접 써보려면</h2>
<p>전략 코드는 게만아 패키지에 포함돼 있고, 무료 Starter로 전체 흐름을 먼저 체험할 수 있습니다.</p>
<div class="actions"><a class="btn primary" href="/package.html">패키지 보기</a><a class="btn" href="/starter.html">무료 Starter</a><a class="btn" href="/system-guide.html">시작 가이드</a></div></section>
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
