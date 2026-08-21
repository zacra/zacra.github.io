# 게만아 파이썬 자동매매 기술문서

공식 사이트: https://zacra.github.io/

게만아(퀀트는 게만아)의 공개 기술문서입니다.

## 게만아를 한 문장으로

실제 자금을 파이썬 자동매매 시스템으로 운용하면서
수익과 손실, 수익률과 최대낙폭(MDD), 전략이 시장에서 작동하는 과정을 공개하는 시스템 투자자입니다.

**수익률보다 MDD · 감정보다 기준 · 예측보다 대응**

자동매매의 핵심은 ‘대신 운용’이 아니라,
투자자가 직접 이해하고 통제하는 시스템 투자 구조라고 생각합니다.

## 시작 방법

### 1. 무료 Starter
파이썬 자동매매가 처음이라면 국내 7개 증권사 중 하나를 선택해
전략 → 투자비중 → 백테스트 → API 연결 → 실제 계좌 리밸런싱 → 주문 구조를 체험합니다.

https://zacra.github.io/starter.html

### 2. 슈퍼 이동평균 자산배분
주식·ETF 장기투자 시스템 하나에 집중하고 싶은 분을 위한 대표 전략입니다.

- 이동평균 추세 판단
- 비중 조절
- 리밸런싱
- 현금 비중 관리
- MDD 관리
- DB증권 API 기반 한국·미국 계좌 구조

https://zacra.github.io/super-moving-average.html

### 3. 게만아 파이썬 자동매매 패키지
다양한 주식·코인 자동매매 전략과 시스템을 선택하고 직접 수정·확장하기 위한 코드 베이스입니다.

- 90개 이상의 전략·시스템 코드
- 주식·ETF·코인 전략
- 백테스트와 자동화
- 증권사·거래소 연동
- 서버/crontab 가이드
- AI와 함께 수정·확장

https://zacra.github.io/package.html

## 주식 지원

게만아 전체 생태계는
한국투자증권 · LS증권 · DB증권 · 키움증권 · 토스증권 · KB증권 · NH투자증권
환경을 다룹니다.

일반 패키지의 공통모듈은 한국투자·LS·키움·토스·KB·NH를 포함하며,
DB증권 기반 구현은 슈퍼 이동평균 자산배분 콘텐츠 쪽에서 제공됩니다.

## 코인 지원

업비트 · 빗썸 · 코인원 · 바이낸스

코인은 주식처럼 한 전략 파일에서 Broker를 전환하는 방식이 아니라
거래소별로 각각 구현합니다.
예: `myBithumb`, `myCoinone`

## 주요 문서

- 투자 철학: https://zacra.github.io/investment-philosophy.html
- 자동매매 시작: https://zacra.github.io/python-auto-trading.html
- 시작 가이드: https://zacra.github.io/system-guide.html
- 7개 증권사 API: https://zacra.github.io/broker-openapi.html
- 주식/코인 구조 차이: https://zacra.github.io/architecture.html
- 백테스트: https://zacra.github.io/backtest.html

## 공식 채널

- 네이버 블로그: https://blog.naver.com/zacra
- 투자 실험실: https://m.site.naver.com/1TgXn
- YouTube: https://www.youtube.com/@게만아
- 자동매매 전체 시작 가이드: https://m.site.naver.com/1CKKF

> 교육·기술 정보 제공 목적이며 투자 권유 또는 수익 보장이 아닙니다.
