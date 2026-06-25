# 강남 가라오케 도파민

`dopamine-karaoke.com` 프리미엄 가라오케 정적 사이트 (모바일 퍼스트, SEO 최적화).

## 구성

- `index.html` — 메인 페이지
  - 드롭다운 상단 메뉴(도파민 소개 / 룸 & 시설 / 서비스 안내 / 이용 안내 / 예약 문의) + 모바일 햄버거
  - 히어로 → 본문(SEO 약 2,300자) → 핵심가치 5 → 룸투어(L/M/S) → 요금배너 → 실시간 예약폼 → 후기 → FAQ → 오시는 길(지도) → 지역 링크 → 푸터
- `regions/*.html` — 지역(롱테일) 페이지: 강남 · 선릉 · 삼성동 · 역삼 · 논현 · 신논현 · 청담 · 압구정
- `assets/style.css` — 디자인 시스템(반응형, 드롭다운, 다크 럭셔리 테마)
- `assets/app.js` — 모바일 메뉴 / 드롭다운 / 스크롤 등장 / 예약 폼
- `sitemap.xml`, `robots.txt`

## SEO

- **검색결과 사이트 이름** → 모든 페이지 `og:site_name` + `WebSite` 스키마 `name` = `강남 가라오케 도파민`
- **타이틀** → `강남 가라오케 도파민 | 24시 연중무휴 프리미엄 파티 공간`
- **메타 설명** → 선릉·삼성동 위치, 24시 연중무휴, 시설·DJ·프라이빗·특가 강조
- **스키마(JSON-LD)** → `NightClub`(LocalBusiness) + `AggregateRating`(점수) + `Review`(후기) + `WebSite` + `FAQPage` + (지역)`BreadcrumbList`
- 로컬 키워드(강남/선릉/삼성동 가라오케·노래방)를 타이틀·설명·본문에 배치
- 메인 ↔ 지역 내부링크: 상단 네비 / 푸터 / "강남 지역별 가라오케" 섹션

## 빌드

```bash
python3 generate.py
```

`REGIONS`, `FEATURES`, `ROOMS`, `FAQ` 등 데이터만 수정하면 전 페이지·스키마·내부링크가 일괄 갱신됩니다.

## 배포 전 교체 필요 (generate.py 상단)

- `CONTACT_TEL` — 실제 전화번호 (예: `tel:010-1234-5678`)
- `KAKAO_URL` — 카카오톡 채널 링크
- 후기/평점 수치(`MAIN_REVIEWS`, 각 지역 `reviews`/`rating`/`count`)는 예시 샘플 → 실제 후기로 교체 권장
- `og-image.jpg` — 대표 공유 이미지 추가 권장
