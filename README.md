# 게만아 파이썬 자동매매 기술문서

공식 사이트: https://zacra.github.io/

게만아(퀀트는 게만아)의 공개 기술문서입니다.

## 투자 철학

**수익률보다 MDD · 감정보다 기준 · 예측보다 대응**

높은 수익률 하나보다 큰돈을 넣고도 오래 유지할 수 있는 구조를 먼저 봅니다.
현금, 추세추종, 자산배분, 이동평균, 백테스트를 이용해 투자 기준을 만들고
자동매매는 그 기준을 빠뜨리지 않고 반복하는 도구로 사용합니다.

- 투자 철학: https://zacra.github.io/investment-philosophy.html
- 백테스트: https://zacra.github.io/backtest.html

## 파이썬 자동매매

### 주식·ETF
한국투자증권 · LS증권 · 키움증권 · 토스증권 · KB증권 · NH투자증권 · DB증권

주식은 같은 전략 파일에서 사용할 증권사 Broker를 전환할 수 있는 멀티브로커 구조를 활용합니다.

### 코인
업비트 · 빗썸 · 코인원 · 바이낸스

코인은 주식과 달리 한 파일에서 Adapter를 전환하는 구조가 아니라 거래소별로 따로 구현합니다.
예를 들어 `myBithumb`, `myCoinone`처럼 거래소마다 별도의 공통모듈을 두는 방식입니다.

## 무료 AutobotEx Starter

국내 7개 증권사 중 한 곳을 선택해
자산배분 → 백테스트 → 계좌 조회 → 리밸런싱 → 주문 구조를 경험하는 무료 입문용 Lite 시스템입니다.

https://blog.naver.com/zacra/224382618923

## 공식 채널

- 네이버 블로그: https://blog.naver.com/zacra
- YouTube: https://www.youtube.com/@게만아

> 교육·기술 정보 제공 목적이며 투자 권유 또는 수익 보장이 아닙니다.
