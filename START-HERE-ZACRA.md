# zacra.github.io 첫 배포 가이드

지금 `https://zacra.github.io/`에서 404가 보이는 것은 정상입니다.
현재는 Repository 주소만 만들어졌고 사이트 파일과 GitHub Pages 배포가 아직 없기 때문입니다.

이번 첫 배포는 가장 단순하게:

**main 브랜치의 /(root)에서 바로 배포**

방식을 사용합니다.

## 1. 이 파일을 사용하세요

`zacra_github_io_UPLOAD_ONLY.zip`

압축을 풀면 다음처럼 보입니다.

```text
index.html
about.html
python-auto-trading.html
stock-auto-trading.html
crypto-auto-trading.html
broker-openapi.html
starter.html
assets/
brokers/
robots.txt
sitemap.xml
llms.txt
README.md
```

중요: 압축을 푼 상위 폴더를 통째로 한 단계 아래에 넣는 것이 아니라,
**그 안의 파일과 폴더가 Repository 최상단에 바로 올라가야 합니다.**

정상 구조:

```text
zacra.github.io/
├── index.html
├── assets/
├── brokers/
├── robots.txt
├── sitemap.xml
└── ...
```

잘못된 구조:

```text
zacra.github.io/
└── zacra_github_io_UPLOAD_ONLY/
    └── index.html
```

## 2. GitHub에 업로드

현재 Repository:

`zacra / zacra.github.io`

의 Code 화면에서

- `uploading an existing file`

또는

- `Add file` → `Upload files`

를 선택합니다.

압축을 푼 폴더 **안쪽의 내용물 전체**를 업로드 영역에 드래그합니다.

Commit message는:

`Launch 게만아 파이썬 자동매매 기술문서`

정도로 입력하고 `Commit changes`를 누릅니다.

업로드 완료 후 Code 화면 최상단에 `index.html`이 보이면 정상입니다.

## 3. GitHub Pages 켜기

Repository 상단:

`Settings`
→ 왼쪽 `Pages`
→ `Build and deployment`

다음처럼 설정합니다.

```text
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

`Save`

이번 배포용 파일은 root에 바로 올리므로 `/docs`가 아니라 **/(root)** 입니다.

## 4. 몇 분 기다린 뒤 확인

Pages 화면에:

`Your site is live at https://zacra.github.io/`

와 비슷한 문구가 나오면 성공입니다.

확인:
https://zacra.github.io/

계속 404라면:
- 5~10분 기다리기
- 강력 새로고침
- 시크릿 창에서 확인

을 해보세요.

## 5. 공개 후 확인할 주소

메인:
https://zacra.github.io/

파이썬 자동매매:
https://zacra.github.io/python-auto-trading.html

주식·ETF:
https://zacra.github.io/stock-auto-trading.html

코인:
https://zacra.github.io/crypto-auto-trading.html

7개 증권사 API:
https://zacra.github.io/broker-openapi.html

무료 Starter:
https://zacra.github.io/starter.html

robots:
https://zacra.github.io/robots.txt

sitemap:
https://zacra.github.io/sitemap.xml

llms:
https://zacra.github.io/llms.txt

## 6. 주소는 이미 전부 반영되어 있습니다

이번 배포본에는 다음이 모두 `https://zacra.github.io/` 기준으로 생성되어 있습니다.

- canonical URL
- Open Graph URL
- Open Graph 이미지 URL
- JSON-LD
- sitemap.xml
- robots.txt
- llms.txt

따라서 사이트 주소를 직접 수정할 필요가 없습니다.

## 7. 사이트가 실제로 뜬 다음

그 다음 단계에서:
1. Google Search Console
2. Bing Webmaster Tools
3. 네이버 서치어드바이저

를 차례로 등록하면 됩니다.

오늘은 우선:
**파일 업로드 → main/(root) Pages 활성화 → 홈페이지 확인**
까지만 성공시키면 됩니다.
