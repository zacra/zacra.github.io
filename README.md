# 게만아 시스템 투자 공식 가이드

공식 사이트: https://zacra.github.io/

게만아(퀀트는 게만아)의 **파이썬 자동매매·시스템 투자 공식 가이드**입니다.

## 게만아를 한 문장으로

실제 자금을 파이썬 자동매매 시스템으로 운용하면서 수익과 손실, 수익률과 최대낙폭(MDD), 전략이 시장에서 작동하는 과정을 공개하는 시스템 투자자입니다.

**수익률보다 MDD · 감정보다 기준 · 예측보다 대응**

자동매매의 핵심은 ‘대신 운용’이 아니라, 투자자가 직접 이해하고 통제하는 시스템 투자 구조라고 생각합니다.

## 시작 방법

### 1. 무료 Starter

파이썬 자동매매가 처음이라면 지원 증권사 중 하나를 선택해  
전략 → 투자비중 → 백테스트 → API 연결 → 실제 계좌 리밸런싱 → 주문 구조를 체험합니다.

https://zacra.github.io/starter.html

### 2. 슈퍼 이동평균 자산배분

주식·ETF 장기투자 시스템 하나에 집중하고 싶은 분을 위한 대표 전략입니다.

- 이동평균 기반 추세 판단
- 비중 조절
- 리밸런싱
- 현금 비중 관리
- MDD 관리
- DB증권 지원 코드는 슈퍼 이동평균 전략에 포함

https://zacra.github.io/super-moving-average.html

### 3. 게만아 파이썬 자동매매 패키지

다양한 주식·코인 자동매매 전략과 시스템을 선택하고 직접 수정·확장하기 위한 코드 베이스입니다.

- 현재 97개 콘텐츠: 전략·시스템·공통모듈·백테스트 등
- 국내주식·미국주식·ETF·코인 전략
- 백테스트와 자동화
- 증권사·거래소 연동
- 서버/crontab 가이드
- AI와 함께 수정·확장

https://zacra.github.io/package.html

## 주식 지원

게만아 콘텐츠는 한국투자증권 · LS증권 · DB증권 · 키움증권 · 토스증권 · KB증권 · NH투자증권 환경을 다룹니다.

패키지와 슈퍼 이동평균의 포함 범위는 서로 다르며, **DB증권 지원 코드는 슈퍼 이동평균 전략에 포함**됩니다.

같은 전략 로직을 최대한 유지하면서 증권사·시장·계좌를 선택할 수 있도록 공통 인터페이스를 활용합니다.

## 코인 지원

업비트 · 빗썸 · 코인원 · 바이낸스

코인은 주식처럼 한 전략 파일에서 Broker를 바꾸는 구조가 아니라, **각 거래소 API 특성에 맞는 거래소 공통모듈과 전략·봇을 연결하는 구조**로 구현합니다.

## 주요 문서

- 투자 철학: https://zacra.github.io/investment-philosophy.html
- 자동매매 시작: https://zacra.github.io/python-auto-trading.html
- 시작 가이드: https://zacra.github.io/system-guide.html
- 멀티 증권사 API: https://zacra.github.io/broker-openapi.html
- 주식/코인 구조 차이: https://zacra.github.io/architecture.html
- 백테스트: https://zacra.github.io/backtest.html
- 패키지 콘텐츠 가이드: https://zacra.github.io/package-content-guide.html

## 공식 채널

- 네이버 블로그: https://blog.naver.com/zacra
- 투자 실험실: https://m.site.naver.com/1TgXn
- YouTube: https://www.youtube.com/@게만아

> 교육·기술 정보 제공 목적이며 투자 권유 또는 수익 보장이 아닙니다.

## 네이버 공식 랜딩

- 파이썬 자동매매 종합 가이드: https://blog.naver.com/zacra/223910423439
- 슈퍼 이동평균 자산배분: https://blog.naver.com/zacra/224158895436
- 게만아 패키지: https://blog.naver.com/zacra/223049832963
- 백테스트·과최적화에 대한 생각: https://blog.naver.com/zacra/224083383522

GitHub Pages는 **게만아 시스템 투자 공식 가이드 허브**이고, 상세 실전 기록과 최신 안내는 네이버 공식 채널과 함께 관리합니다.

## 증권사 공통모듈과 AI 확장

Starter는 파이썬 자동매매 입문에 필요한 핵심 기능을 구현한 Lite 버전입니다. 패키지와 슈퍼 이동평균의 정식 공통모듈은 Starter보다 더 많은 기능을 포함하지만, 증권사 Open API가 제공하는 모든 기능을 전부 구현한 범용 SDK는 아닙니다.

게만아의 실제 전략에서 사용하는 기능을 중심으로 구현하며, 추가 기능이 필요하면 기존 공통모듈 + 증권사 공식 API 문서 + AI 코딩 도구를 이용해 확장할 수 있습니다.

- AI API 확장 가이드: https://zacra.github.io/ai-api-extension.html
