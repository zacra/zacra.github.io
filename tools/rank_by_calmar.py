#!/usr/bin/env python3
"""패키지 백테스트 마스터 표(.md)로 전략 카탈로그의 분류별 Calmar 순위를 계산해 data/strategies.json 에 저장합니다.

사용법:  python3 tools/rank_by_calmar.py <마스터표.md> [--agg max|median] [--min-years 2.0] [--show]

- 분류 안의 순위(rank)만 data/strategies.json 에 저장합니다.
- 번호마다 하나의 대표값을 쓰며, 아래 조건을 모두 만족하는 행만 비교 대상입니다.
    · 구분이 '백테스트'이고 상태가 '성공'이며 Calmar가 숫자
    · 포트폴리오가 TOTAL / 기본 / 포트폴리오 종합 (개별 종목·고정 모드 행은 제외)
    · 기간이 --min-years 이상 (기본 2년)
  번호에 여러 버전이 있으면 --agg 기준(기본 max)으로 하나를 고릅니다.
- categories 에서 "ranked": true 인 분류만 순위를 매기고, 순위가 없는 전략(백테스트 없음·비교 제외)은
  페이지에서 번호순으로 뒤에 놓입니다. 특별 항목(S)은 항상 맨 앞입니다.
- 실행 후 `python3 tools/build_strategies.py` 로 페이지를 다시 만드세요.
"""
import argparse
import datetime as dt
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "strategies.json"
COLS = ["num", "pkg", "kind", "script", "new", "portfolio", "period", "bars", "cagr", "mdd", "calmar", "status", "note"]
OK_PORTFOLIOS = {"TOTAL", "기본", "포트폴리오 종합"}


def parse_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 12 or not cells[0].isdigit():
            continue
        cells = cells[:12] + [" | ".join(cells[12:])]
        rows.append(dict(zip(COLS, cells)))
    return rows


def years(period: str) -> float | None:
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})", period)
    if not m:
        return None
    a, b = (dt.date.fromisoformat(x) for x in m.groups())
    return (b - a).days / 365.25


def representative(rows: list[dict], agg: str, min_years: float) -> dict[int, float]:
    by: dict[int, list[float]] = {}
    for r in rows:
        if r["kind"] != "백테스트" or r["status"] != "성공" or r["portfolio"] not in OK_PORTFOLIOS:
            continue
        try:
            cal = float(r["calmar"])
        except ValueError:
            continue
        y = years(r["period"])
        if y is None or y < min_years:
            continue
        by.setdefault(int(r["num"]), []).append(cal)
    fn = max if agg == "max" else statistics.median
    return {k: fn(v) for k, v in by.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("master")
    ap.add_argument("--agg", choices=["max", "median"], default="max")
    ap.add_argument("--min-years", type=float, default=2.0)
    ap.add_argument("--show", action="store_true", help="로컬 확인용: 순서와 수치를 화면에 출력(저장하지 않음)")
    a = ap.parse_args()

    rep = representative(parse_rows(Path(a.master)), a.agg, a.min_years)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ranked_cats = {c["name"] for c in data["categories"] if c.get("ranked")}
    for name in [c["name"] for c in data["categories"] if c["name"] in ranked_cats]:
        members = [e for e in data["entries"] if e["category"] == name and not e.get("special")]
        have = sorted((e for e in members if e["code"] in rep), key=lambda e: (-rep[e["code"]], e["code"]))
        for i, e in enumerate(have, 1):
            e["rank"] = i
        for e in members:
            if e["code"] not in rep:
                e.pop("rank", None)
        if a.show:
            print(f"\n[{name}] 순위 {len(have)} / 전체 {len(members)}")
            for e in have:
                print(f"  {e['rank']:>2}. #{e['code']:<3} {rep[e['code']]:>6.2f}  {e['title'][:34]}")
            print("  번호순(비교 없음):", [e["code"] for e in sorted(members, key=lambda e: e["code"]) if e["code"] not in rep])
    for e in data["entries"]:
        if e["category"] not in ranked_cats:
            e.pop("rank", None)
    if not a.show:
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        n = sum(1 for e in data["entries"] if "rank" in e)
        print(f"순위 저장: {n}개 전략 (수치는 저장하지 않음)")


if __name__ == "__main__":
    main()
