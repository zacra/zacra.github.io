# zacra.github.io 저장소 관리 가이드

이 저장소는 **게만아 시스템 투자 공식 가이드** `https://zacra.github.io/`를 배포합니다.

## 배포 구조

GitHub Pages는 `main` 브랜치의 `/(root)`에서 배포합니다. 수정 파일은 별도 하위 폴더를 만들지 말고 저장소의 기존 경로에 그대로 덮어씁니다.

예:

```text
zacra.github.io/
├── index.html
├── about.html
├── faq.html
├── assets/
├── brokers/
├── robots.txt
├── sitemap.xml
├── llms.txt
└── ...
```

## 수정할 때 기억할 것

- 새 페이지를 만들면 `sitemap.xml`에도 URL을 추가합니다.
- 기존 페이지의 내용만 수정했다면 URL은 그대로 유지합니다.
- `README.md`, `llms.txt`, `robots.txt`에도 오래된 브랜드명·지원 범위가 남지 않았는지 함께 확인합니다.
- 발급받은 API Key, Secret, 접근토큰, 계좌 인증정보는 비밀번호와 같은 정보이므로 공개 파일에 실제 값을 넣지 않습니다.
- 큰 수정은 하나의 커밋으로 남겨두면 필요할 때 이전 커밋으로 되돌리기 쉽습니다.

## 주요 진입점

- 공식 가이드: https://zacra.github.io/
- 시작 가이드: https://zacra.github.io/system-guide.html
- 무료 Starter: https://zacra.github.io/starter.html
- 패키지: https://zacra.github.io/package.html
- 슈퍼 이동평균: https://zacra.github.io/super-moving-average.html
- 주식·증권사 API: https://zacra.github.io/broker-openapi.html
- 코인 자동매매: https://zacra.github.io/crypto-auto-trading.html
- FAQ: https://zacra.github.io/faq.html

이 파일은 저장소 관리용 메모이며 사이트 방문자를 위한 본문 페이지는 아닙니다.
