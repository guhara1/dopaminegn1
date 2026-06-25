# 강남 가라오케 도파민

`dopamine-karaoke.com` 메인 페이지 및 지역 랜딩 페이지 정적 사이트.

## SEO 핵심 설정

- **검색결과 사이트 이름(빨간 원 영역)** → 모든 페이지에 `og:site_name` + `WebSite` 스키마의 `name`을 `강남 가라오케 도파민`으로 설정
- **타이틀** → `강남 가라오케 도파민 | 24시 연중무휴`
- **디스크립션** → `강남 선릉 삼성동 위치. 도파민, 감성 들만 모아놓은 신선한 가라오케. 24시 연중무휴 전화하면 실시간 추천과 특가 혜택까지!`

## 구조

- `index.html` — 메인 페이지
- `regions/*.html` — 지역(롱테일) 페이지: 강남 · 선릉 · 삼성동 · 역삼 · 논현 · 신논현 · 청담 · 압구정
- `assets/style.css` — 공통 스타일
- `sitemap.xml`, `robots.txt` — 색인용

## 스키마(JSON-LD)

모든 페이지에 적용:

- `LocalBusiness` + `AggregateRating`(점수) + `Review`(후기/리뷰)
- 메인: `WebSite` / 지역: `BreadcrumbList`

## 내부링크 강화

상단 네비, 본문 "주변 지역" 링크, 푸터에서 메인 ↔ 모든 지역 페이지를 롱테일 키워드로 상호 연결.

## 빌드

```bash
python3 generate.py
```

`generate.py`의 `REGIONS` 데이터를 수정하면 지역 페이지 / 스키마 / 내부링크가 일괄 갱신된다.
