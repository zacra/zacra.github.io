#!/usr/bin/env python3
"""data/games.json → games.html(목록)와 games/<id>.html(게임별 상세 페이지), OG 이미지, 사이트맵을 생성한다.

games.html의 head·nav·소개·푸터는 그대로 두고 ① 게임 카드 영역 ② ItemList JSON-LD ③ 날짜만 갱신한다.
상세 페이지는 games.html의 head/nav/footer를 바탕으로 게임별 title·meta·OG·JSON-LD를 바꿔 만든다.
게임 추가·스토어 링크 변경은 data/games.json만 고치고 이 스크립트를 실행하면 된다.
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"
LIST_FILE = ROOT / "games.html"
DETAIL_DIR = ROOT / "games"
OG_DIR = ROOT / "assets" / "games" / "og"
SITE = "https://zacra.github.io"
AUTHOR = {"@type": "Person", "name": "게만아", "alternateName": "게임 만드는 아빠", "url": f"{SITE}/about.html"}

STORE_LABEL = {"toss": "Toss", "onestore": "ONE store", "appstore": "iOS", "googleplay": "Android"}


def page_url(g):
    return f"{SITE}/games/{g['id']}.html"


def store_list(g):
    return [STORE_LABEL[k] for k in ("toss", "onestore", "appstore", "googleplay") if k in g["stores"]]


def same_as(g):
    return [g["stores"][k] for k in ("toss", "onestore", "appstore", "googleplay") if k in g["stores"]]


def note(g):
    st = g["stores"]
    phone = [n for k, n in (("toss", "토스"), ("onestore", "원스토어")) if k in st]
    extra = (["App Store는 iPhone·iPad"] if "appstore" in st else []) + (["Google Play는 Android 기기"] if "googleplay" in st else [])
    if extra and phone:
        return f"{'·'.join(phone)}는 해당 앱이 설치된 휴대폰에서, {', '.join(extra)}에서 실행돼요"
    if extra:
        return f"{', '.join(extra)}에서 실행돼요"
    return f"{'·'.join(phone)} 앱이 설치된 휴대폰에서 실행돼요"


def play_button(url, name, label, icon):
    return (
        f'<a class="play-btn" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{name} {label}">'
        f'<img src="/assets/games/brand/{icon}" alt="" width="28" height="28" loading="lazy" decoding="async"/><span>{label}</span></a>'
    )


def ensure_qr(slug, suffix, url):
    """QR 파일이 없으면 만든다(qrcode 모듈이 있을 때)."""
    out = ROOT / "assets" / "games" / f"qr-{slug}{suffix}.svg"
    if out.exists():
        return
    try:
        import qrcode
        import qrcode.image.svg
    except ImportError:
        print(f"[경고] {out.name} 없음: qrcode 모듈이 없어 만들지 못했습니다")
        return
    qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=2).save(out)


def card(g, detail_page=False):
    st, name, gid = g["stores"], g["name"], g["id"]
    im = g["image"]
    badge = '<span class="game-badge" aria-label="대표 게임">BEST</span>' if g["featured"] else ""
    cls = "game-card featured" if g["featured"] else "game-card"
    row1 = []
    if "toss" in st:
        row1.append(play_button(st["toss"], name, "토스에서 플레이", "toss-icon.png"))
    if "onestore" in st:
        row1.append(play_button(st["onestore"], name, "원스토어에서 플레이", "onestore-icon.png"))
    buttons = " ".join(row1)
    row2 = ""
    if "appstore" in st:
        row2 += play_button(st["appstore"], name, "App Store에서 다운로드", "appstore-icon.png")
    if "googleplay" in st:
        row2 += (" " if row2 else "") + play_button(st["googleplay"], name, "Google Play에서 다운로드", "googleplay-icon.png")
    if row2:
        buttons += f'<div class="store-badges">{row2}</div>'
    slug = gid
    qrs = []
    if "toss" in st:
        qrs.append(("", "토스", st["toss"]))
    if "onestore" in st:
        qrs.append(("-onestore", "원스토어", st["onestore"]))
    if "appstore" in st:
        qrs.append(("-appstore", "App Store", st["appstore"]))
    if "googleplay" in st:
        qrs.append(("-googleplay", "Google Play", st["googleplay"]))
    for suf, _, u in qrs:
        ensure_qr(slug, suf, u)
    figs = "".join(
        f'<figure class="game-qr"><img src="/assets/games/qr-{slug}{suf}.svg" alt="{name} {label} 실행 QR 코드" width="104" height="104" loading="lazy"/>'
        f'<figcaption>{label} · 휴대폰 카메라로 스캔</figcaption></figure>'
        for suf, label, _ in qrs
    )
    more = "" if detail_page else f'\n<p class="game-more"><a href="/games/{gid}.html">이 게임만 보기 · 공유 링크 →</a></p>'
    fold = '<details class="fold" open>' if detail_page else '<details class="fold">'
    return (
        f'<article class="{cls}" id="{gid}">\n'
        f'<div class="game-thumb">{badge}'
        f'<img src="{im["src"]}" alt="{im["alt"]}" width="{im["width"]}" height="{im["height"]}" loading="lazy" decoding="async"/></div>\n'
        f'<div class="game-body">\n<p class="game-genre">{g["genre"]}</p>\n<h2>{name}</h2>\n<p class="game-sub">{g["sub"]}</p>\n'
        f'<p>{g["summary"]}</p>\n'
        f'<ul class="game-facts">{"".join(f"<li>{f}</li>" for f in g["facts"])}</ul>\n'
        f'<div class="game-actions"><div>{buttons}<p class="game-note">{note(g)}</p></div>\n'
        f'<div class="game-qrs">{figs}</div></div>\n'
        f'{fold}<summary>자세한 소개 보기</summary>{g["detail"]}</details>{more}\n'
        f'</div></article>'
    )


def list_card(g):
    """games.html용 간단 카드: 이미지·짧은 설명·[게임하러가기] → 상세 페이지."""
    name, gid, im = g["name"], g["id"], g["image"]
    badge = '<span class="game-badge" aria-label="대표 게임">BEST</span>' if g["featured"] else ""
    cls = "game-card featured" if g["featured"] else "game-card"
    url = f"/games/{gid}.html"
    return (
        f'<article class="{cls}" id="{gid}">\n'
        f'<a class="game-thumb" href="{url}" aria-label="{name} 소개 페이지로 이동">{badge}'
        f'<img src="{im["src"]}" alt="{im["alt"]}" width="{im["width"]}" height="{im["height"]}" loading="lazy" decoding="async"/></a>\n'
        f'<div class="game-body">\n<p class="game-genre">{g["genre"]}</p>\n<h2>{name}</h2>\n<p class="game-sub">{g["sub"]}</p>\n'
        f'<p>{g["summary"]}</p>\n'
        f'<ul class="game-facts">{"".join(f"<li>{f}</li>" for f in g["facts"])}</ul>\n'
        f'<p class="game-go"><a class="btn primary" href="{url}" aria-label="{name} 게임하러가기">게임하러가기 →</a></p>\n'
        f'</div></article>'
    )


def video_game(g):
    return {
        "@type": "VideoGame", "name": g["name"], "alternateName": g["sub"], "description": g["ld_description"],
        "url": page_url(g), "image": f"{SITE}{g['image']['src']}", "applicationCategory": "Game",
        "gamePlatform": store_list(g), "inLanguage": "ko-KR", "author": AUTHOR, "sameAs": same_as(g),
    }


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def make_og(g):
    from PIL import Image, ImageEnhance, ImageFilter
    OG_DIR.mkdir(parents=True, exist_ok=True)
    out = OG_DIR / f"{g['id']}.jpg"
    src = Image.open(ROOT / g["image"]["src"].lstrip("/")).convert("RGB")
    W, H = 1200, 630
    scale = max(W / src.width, H / src.height)
    bg = src.resize((int(src.width * scale) + 1, int(src.height * scale) + 1), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(28))).enhance(0.72)
    fg = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
    bg.paste(fg, (0, (H - fg.height) // 2))
    bg.save(out, "JPEG", quality=86, optimize=True)


def head_of(tpl):
    return tpl[: tpl.index("</head>")]


def detail_page(g, tpl, others, updated):
    head = head_of(tpl)
    url = page_url(g)
    title = f"{g['name']} – {g['sub']} | 게임 만드는 아빠 게만아의 게임"
    desc = f"{g['name']}: {g['sub']}. {g['ld_description']}"
    og_title = f"{g['name']} | 게임 만드는 아빠 게만아의 게임"
    og_img = f"{SITE}/assets/games/og/{g['id']}.jpg"
    alt = g["image"]["alt"]

    def sub(pat, repl, s, count=1):
        new, n = re.subn(pat, lambda m: repl, s, count=count, flags=re.S)
        assert n, pat
        return new

    head = sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", head)
    head = sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', head)
    head = sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head)
    head = sub(r'<meta property="og:type" content="website">', '<meta property="og:type" content="website">', head)
    head = sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{escape(og_title)}">', head)
    head = sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{escape(desc)}">', head)
    head = sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', head)
    head = sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_img}">', head)
    head = sub(r'<meta property="og:image:secure_url" content="[^"]*">', f'<meta property="og:image:secure_url" content="{og_img}">', head)
    head = sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{escape(alt)}">', head)
    head = sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{escape(og_title)}">', head)
    head = sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{escape(desc)}">', head)
    head = sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{og_img}">', head)
    head = sub(r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{escape(alt)}">', head)
    # JSON-LD: 첫 WebPage → 상세용 그래프, ItemList 제거
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "headline": title, "name": title, "description": desc, "url": url, "inLanguage": "ko-KR",
             "dateModified": updated, "primaryImageOfPage": og_img, "author": AUTHOR,
             "publisher": {"@type": "Organization", "name": "자밥스튜디오", "url": f"{SITE}/", "brand": {"@type": "Brand", "name": "게만아"}}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "게임", "item": f"{SITE}/games.html"},
                {"@type": "ListItem", "position": 3, "name": g["name"], "item": url}]},
            video_game(g),
        ],
    }
    lds = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', head, re.S))
    assert len(lds) == 2
    head = head[: lds[1].start()] + head[lds[1].end():].lstrip("\n")
    head = head[: lds[0].start()] + f'<script type="application/ld+json">{compact(graph)}</script>' + head[lds[0].end():]
    tail = tpl[tpl.index("</main><footer"):]
    tail = re.sub(r"마지막 업데이트 [0-9-]+", f"마지막 업데이트 {updated}", tail)
    nav = tpl[tpl.index("</head>"): tpl.index('<main id="main">')]
    thumbs = "".join(
        f'<a class="other-card" href="/games/{o["id"]}.html" aria-label="{o["name"]} 소개 페이지로 이동">'
        f'<img src="{o["image"]["src"]}" alt="{o["image"]["alt"]}" width="{o["image"]["width"]}" height="{o["image"]["height"]}" loading="lazy" decoding="async"/>'
        f'<span class="other-name">{o["name"]}</span><span class="other-sub">{o["sub"]}</span></a>'
        for o in others
    )
    main = (
        f'<main id="main"><div class="breadcrumb"><a href="/">홈</a> › <a href="/games.html">게임</a> › {g["name"]}</div>\n'
        f'<div class="game-list single">\n{card(g, True)}\n</div>\n'
        f'<section class="other-games"><h2>다른 게임도 해보세요</h2><div class="other-grid">{thumbs}</div>\n'
        f'<p class="game-back"><a class="btn primary" href="/games.html">다른 게임 보기 →</a></p></section>\n'
        f'<p class="updated">문서 업데이트: {updated} · 게임은 모바일에서 실행돼요.</p>\n'
    )
    return head + nav + main + tail


def update_sitemap(games, updated):
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    for loc in [f"{SITE}/games.html"] + [page_url(g) for g in games]:
        pat = re.compile(r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[0-9-]+(</lastmod>)")
        if pat.search(s):
            s = pat.sub(lambda m: m.group(1) + updated + m.group(2), s)
        else:
            s = s.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{updated}</lastmod>\n  </url>\n</urlset>")
    p.write_text(s, encoding="utf-8")


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    games, updated = data["games"], data["updated_at"]
    s = LIST_FILE.read_text(encoding="utf-8")

    # 목록 페이지: 카드 영역
    a = s.index('<div class="game-list">\n') + len('<div class="game-list">\n')
    b = s.index('\n</div>\n<section class="notice">')
    s = s[:a] + "\n".join(list_card(g) for g in games) + s[b:]
    # ItemList JSON-LD
    m = [x for x in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S) if '"ItemList"' in x.group(1)][0]
    d = json.loads(m.group(1))
    d["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "item": video_game(g)} for i, g in enumerate(games)]
    s = s[: m.start(1)] + compact(d) + s[m.end(1):]
    # 제목·설명에 나열된 게임 이름 순서를 data/games.json 순서에 맞춘다
    alt = "|".join(sorted((re.escape(g["name"]) for g in games), key=len, reverse=True))
    for sep in ("·", ", "):
        pat = re.compile(rf"(?:{alt})(?:{re.escape(sep)}(?:{alt})){{4,}}")
        s = pat.sub(sep.join(g["name"] for g in games), s)
    s = re.sub(r"문서 업데이트: [0-9-]+", f"문서 업데이트: {updated}", s)
    s = re.sub(r"마지막 업데이트 [0-9-]+", f"마지막 업데이트 {updated}", s)
    s = re.sub(r'"dateModified":"[0-9-]+"', f'"dateModified":"{updated}"', s)
    LIST_FILE.write_text(s, encoding="utf-8")

    DETAIL_DIR.mkdir(exist_ok=True)
    for g in games:
        make_og(g)
        # games.html 배치 순서(1순위부터)대로 현재 게임을 제외한 앞의 3개를 보여준다
        others = [o for o in games if o["id"] != g["id"]][:3]
        (DETAIL_DIR / f"{g['id']}.html").write_text(detail_page(g, s, others, updated), encoding="utf-8")
    update_sitemap(games, updated)
    print(f"games.html + {len(games)} detail pages")


if __name__ == "__main__":
    main()
