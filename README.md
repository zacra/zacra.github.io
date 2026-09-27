# 게만아 시스템 투자 공식 가이드

공식 사이트: https://zacra.github.io/

게만아(퀀트는 게만아)의 **파이썬 자동매매·시스템 투자 공식 가이드**입니다.

게만아는 콘텐츠 크리에이터 이름이며, 이 공식 사이트와 관련 콘텐츠는 **자밥스튜디오**가 운영합니다.

## 게만아를 한 문장으로

실제 자금을 파이썬 자동매매 시스템으로 운용하면서 수익과 손실, 수익률과 최대낙폭(MDD), 전략이 시장에서 작동하는 과정을 공개하는 시스템 투자자입니다.

**수익률보다 MDD · 감정보다 기준 · 예측보다 대응**

자동매매의 핵심은 ‘대신 운용’이 아니라, 투자자가 직접 이해하고 통제하는 시스템 투자 구조라고 생각합니다.

## 시작 방법

### 1. 무료 Starter

파이썬 자동매매가 처음이라면 지원 증권사 중 하나를 선택해  
전략 → 투자비중 → 백테스트 → API 연결 → 실제 계좌 리밸런싱 → 주문 구조를 체험합니다.

https://zacra.github.io/starter.html

### 2. 실행 환경 — GMA Runner 또는 AWS

자동매매를 시작하기 위해 AWS 서버가 항상 필수인 것은 아닙니다.

- **GMA Runner**: Windows·Mac PC에서 Python 파일 수동 실행, 예약 실행, 로그 확인
- **AWS 등 서버**: 24시간 안정 운용, 고정 IP, PC 종료·절전의 영향을 피하고 싶을 때 권장
- GMA Runner는 현재 신규 통합 패키지에 포함되며, 기존 이용자는 기존 제공 범위에 따라 계속 사용

https://zacra.github.io/gma-runner.html

### 3. 게만아 통합 패키지

현재 신규 유료 구매는 **게만아 패키지 500,000원** 하나로 운영합니다.

포함 범위:

- 기존 게만아 패키지 전체 콘텐츠
- 슈퍼 이동평균 자산배분 V2
- 국내주식·미국주식·ETF·코인 전략
- 백테스트와 자동화
- 증권사·거래소 연동
- GMA Runner 또는 서버/crontab 자동 실행
- AI와 함께 수정·확장

슈퍼 이동평균 V2는 효율적 투자선과 CORE·FIXED·FAST·SLOW 구조, 현금 비중 관리, Rolling / Walk-Forward 백테스트를 결합한 대표 주식·ETF 장기 시스템입니다.

https://zacra.github.io/package.html
https://zacra.github.io/super-moving-average.html

새로운 콘텐츠는 **패키지 멤버십 월 15,000원**으로 먼저 제공되며, 멤버십을 이용하지 않아도 **출시 후 120일이 지나면 통합 패키지에 순차 편입**됩니다.

기존에 패키지만 구매했거나 슈퍼 이동평균만 구매한 분에게 통합 구성이 자동으로 소급 적용되지는 않습니다. 추가 이용은 zacra007@gmail.com 문의 후 별도 구매 안내를 받습니다.

## 주식 지원

게만아 콘텐츠는 한국투자증권 · LS증권 · DB증권 · 키움증권 · 토스증권 · KB증권 · NH투자증권 환경을 다룹니다.

통합 패키지에는 기존 패키지 콘텐츠와 슈퍼 이동평균 V2가 함께 포함됩니다. **DB증권 지원 코드는 슈퍼 이동평균 전략 구성 안에 포함**되어 있으며, 다른 6개 증권사의 범용 공통모듈과는 제공 형태가 다릅니다.

같은 전략 로직을 최대한 유지하면서 증권사·시장·계좌를 선택할 수 있도록 공통 인터페이스를 활용합니다.

## 코인 지원

업비트 · 빗썸 · 코인원 · 바이낸스

코인은 주식처럼 한 전략 파일에서 Broker를 바꾸는 구조가 아니라, **각 거래소 API 특성에 맞는 거래소 공통모듈과 전략·봇을 연결하는 구조**로 구현합니다.

## 주요 문서

- 핵심 투자 개념 모음: https://zacra.github.io/concepts.html
- 시스템 투자란?: https://zacra.github.io/system-investing.html
- MDD란?: https://zacra.github.io/mdd.html
- 추세추종이란?: https://zacra.github.io/trend-following.html
- 투자 철학: https://zacra.github.io/investment-philosophy.html
- 파이썬 자동매매: https://zacra.github.io/python-auto-trading.html
- 시작 가이드: https://zacra.github.io/system-guide.html
- GMA Runner: https://zacra.github.io/gma-runner.html
- 멀티 증권사 API: https://zacra.github.io/broker-openapi.html
- 주식/코인 구조 차이: https://zacra.github.io/architecture.html
- 백테스트: https://zacra.github.io/backtest.html
- 효율적 투자선: https://zacra.github.io/efficient-frontier.html
- 패키지 콘텐츠 전체 가이드: https://zacra.github.io/package-content-guide.html

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

## 게만아 코드와 AI 확장

AI 확장은 증권사 공통모듈에만 한정되지 않습니다. 주식·코인 전략, 백테스트, 자동매매 봇, 증권사·거래소 공통모듈, 알림·모니터링 같은 보조시스템까지 기존 파이썬 코드를 AI와 함께 이해하고 수정·확장할 수 있습니다.

통합 패키지와 그 안에 포함된 슈퍼 이동평균 V2를 실제로 운용하는 데 필요한 핵심 API 기능은 이미 구현되어 있으므로, 일반 사용자가 증권사 공식 API 문서를 보고 처음부터 추가 개발할 필요는 없습니다. 현재 코드에 없는 새로운 API 기능을 개인적으로 추가할 때만 공식 문서를 기준으로 확장하면 됩니다.

- 전체 코드 AI 확장 가이드: https://zacra.github.io/ai-api-extension.html
