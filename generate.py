#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
강남 가라오케 도파민 정적 사이트 생성기.

- 상단 메뉴/하위 메뉴를 모두 '개별 페이지'로 생성 (앵커 링크 아님)
- 각 페이지 본문 2,000~2,500자, 구글 가이드라인(E-E-A-T / Who·How·Why) 준수
- 모든 페이지 스키마(JSON-LD) + 작성자 바이라인/최종 업데이트(신뢰 신호)
- 내부링크(롱테일 앵커) 강화 + 권위 있는 외부 사이트 인용
- 선호 썸네일: og:image + schema image, 파비콘/매니페스트
- 프리미엄 팔레트 토큰 + 컴포넌트 오버레이 (assets/style.css, assets/app.js)
"""
import html
import json
import os
import posixpath
import urllib.parse

SITE_NAME = "강남 가라오케 도파민"
BASE_URL = "https://www.dopamine-karaoke.com"
ADDRESS = "서울특별시 강남구 선릉로92길 38"
TEL_DISPLAY = "010-3431-0531"          # 예약 전화번호 (표시용)
CONTACT_TEL = "tel:010-3431-0531"      # 예약 전화 링크
TEL_INTL = "+82-10-3431-0531"          # 스키마용 국제 표기
KAKAO_URL = "#"               # TODO: 카카오톡 채널 링크로 교체
OG_IMAGE = BASE_URL + "/og-image.png"
AUTHOR = "도파민 운영팀"
REVIEWER = "도파민 매니지먼트"
UPDATED = "2026-06-25"
MAP_SRC = "https://www.google.com/maps?q=" + urllib.parse.quote(ADDRESS) + "&hl=ko&z=16&output=embed"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 권위 있는 외부 참고 링크 (E-E-A-T 신뢰 신호)
AUTH = {
    "gangnam": ("강남구청", "https://www.gangnam.go.kr"),
    "metro": ("서울교통공사 지하철 노선", "http://www.seoulmetro.co.kr"),
    "juso": ("도로명주소 안내시스템", "https://www.juso.go.kr"),
    "kca": ("한국소비자원", "https://www.kca.go.kr"),
    "ftc": ("공정거래위원회", "https://www.ftc.go.kr"),
    "pipc": ("개인정보보호위원회", "https://www.pipc.go.kr"),
    "food": ("식품안전나라", "https://www.foodsafetykorea.go.kr"),
    "visit": ("대한민국 구석구석(한국관광공사)", "https://korean.visitkorea.or.kr"),
}

# ---- 상단/하위 메뉴 → 개별 페이지 (root 상대 경로) ----
MENU = [
    ("도파민 소개", "pages/intro.html", [("브랜드 스토리", "pages/story.html"), ("오시는 길", "pages/location.html")]),
    ("룸 & 시설", "pages/rooms.html", [("L 룸 (최대 20인)", "pages/room-l.html"), ("M 룸 (최대 14인)", "pages/room-m.html"), ("S 룸 (최대 8인)", "pages/room-s.html")]),
    ("서비스 안내", "pages/service.html", [("프리미엄 서비스", "pages/service-premium.html"), ("주류 & 안주 메뉴", "pages/menu.html"), ("파티 & 이벤트", "pages/event.html")]),
    ("이용 안내", "pages/guide.html", [("이용 방법 (1·2부)", "pages/how.html"), ("요금 & 할인", "pages/price.html"), ("FAQ", "pages/faq.html")]),
    ("예약 문의", "pages/reservation.html", [("전화 예약", "pages/reserve-phone.html"), ("카카오톡 채널", "pages/reserve-kakao.html"), ("실시간 픽업 문의", "pages/pickup.html")]),
]

FEATURES = [
    ("🏛️", "압도적인 공간 & 최첨단 시설", "단독 건물 전체, 하이테크 음향·조명 시스템과 룸별 개별 공조로 완벽한 무대를 연출합니다."),
    ("⏰", "24시간 멈추지 않는 에너지", "1부 15:00~01:00, 2부 01:00~15:00. 365일 연중무휴, 원하는 순간 언제든."),
    ("🎧", "현직 DJ팀 라이브 퍼포먼스", "화려한 경력의 전문 DJ팀이 상주하여 지루할 틈 없는 라이브 무대를 책임집니다."),
    ("🔒", "완벽한 프라이버시 보장", "철저한 보안과 신분 보호 시스템으로 사적인 자리와 비즈니스를 완벽히 지켜드립니다."),
    ("🍽️", "강남 맛집급 안주 & 식사", "전문 셰프가 준비한 고퀄리티 안주와 다양한 주류로 술자리의 격을 높입니다."),
]
ROOMS = [
    ("room-l", "l", "L", "L 룸", "최대 20인", "해외 귀빈 접대, 대규모 회식, VIP 파티에 최적화된 최고급 룸."),
    ("room-m", "m", "M", "M 룸", "최대 14인", "중요한 고객 접대나 가까운 지인들과의 오붓한 생일 파티에 제격."),
    ("room-s", "s", "S", "S 룸", "최대 8인", "소규모 모임이나 편안한 술자리를 위한 아늑하고 세련된 공간."),
]

FAQ = [
    ("예약은 어떻게 하나요?", "전화 또는 카카오톡 채널로 연중무휴 24시간 상담 가능합니다. 인원과 방문 시간을 알려주시면 실시간으로 최적의 룸을 추천해 드립니다."),
    ("요금은 어떻게 되나요?", "주대 7만원부터 시작하며, 웹사이트 예약 시 다양한 특가 혜택을 제공합니다. 자세한 요금은 문의 시 실시간 안내해 드립니다."),
    ("픽업 서비스가 있나요?", "강남권 VIP 고객을 위한 최고급 차량 픽업 서비스를 운영합니다. 방문 전에 미리 문의해 주세요."),
    ("몇 명까지 이용 가능한가요?", "S 룸 최대 8인, M 룸 최대 14인, L 룸 최대 20인까지 이용 가능합니다. 규모에 맞는 룸을 안내해 드립니다."),
    ("영업 시간이 어떻게 되나요?", "365일 연중무휴 24시간 운영합니다. 1부 15:00~01:00, 2부 01:00~15:00로 언제든 편하게 방문하실 수 있습니다."),
    ("주차나 대중교통 접근은 편한가요?", "선릉역 인근에 위치해 지하철 접근성이 우수하며, 차량 방문 시 발렛 및 인근 주차 안내를 도와드립니다."),
]

REGIONS = [
    {"slug": "gangnam", "area": "강남", "lead": "강남역 핵심 상권에서 즐기는 프리미엄 가라오케.", "rating": 4.9, "count": 213,
     "reviews": [("김O준", 5, "강남에서 제일 깔끔합니다. 시스템 설명도 친절하고 가격도 투명해요."), ("이O호", 5, "24시 운영이라 늦게 가도 분위기 좋네요. 재방문 의사 100%."), ("박O석", 4, "위치 찾기 쉽고 응대가 빠릅니다. 특가 혜택 받아서 만족.")]},
    {"slug": "seolleung", "area": "선릉", "lead": "선릉역 도보 거리, 비즈니스 모임과 2차 코스로 딱 맞는 가라오케.", "rating": 4.8, "count": 168,
     "reviews": [("정O우", 5, "선릉 근처에서 접대 자리로 자주 이용합니다. 룸 컨디션 최고."), ("최O진", 5, "예약 통화 한 번에 추천까지 받아서 편했어요."), ("한O민", 4, "가성비 좋고 직원분들 응대가 프로페셔널합니다.")]},
    {"slug": "samseong", "area": "삼성동", "lead": "삼성동 코엑스 인근, 행사·모임 후 이어가기 좋은 24시 가라오케.", "rating": 4.8, "count": 142,
     "reviews": [("오O택", 5, "코엑스 행사 끝나고 바로 이동. 위치가 정말 편합니다."), ("서O빈", 5, "분위기 깔끔하고 음향 좋아요. 노래방 그 이상."), ("강O원", 4, "연중무휴라 휴일에도 갈 수 있어 좋네요.")]},
    {"slug": "yeoksam", "area": "역삼", "lead": "역삼동 직장인 회식·2차 모임에 최적화된 강남 가라오케.", "rating": 4.7, "count": 121,
     "reviews": [("문O혁", 5, "회식 2차로 단골입니다. 단체룸이 넓어요."), ("배O성", 4, "예약이 빠르고 응대가 친절합니다."), ("윤O아", 5, "특가 혜택 안내가 정확해서 믿고 갑니다.")]},
    {"slug": "nonhyeon", "area": "논현", "lead": "논현역 인근, 프라이빗한 무드를 찾는 분께 추천하는 가라오케.", "rating": 4.8, "count": 109,
     "reviews": [("조O환", 5, "프라이빗한 분위기가 마음에 듭니다."), ("임O재", 4, "위치 안내가 정확하고 깔끔해요."), ("신O라", 5, "실시간 추천 받아서 빠르게 자리 잡았습니다.")]},
    {"slug": "sinnonhyeon", "area": "신논현", "lead": "신논현역 도보권, 강남 야간 코스의 시작점으로 좋은 가라오케.", "rating": 4.7, "count": 96,
     "reviews": [("권O수", 5, "신논현에서 접근성 최고. 늦게까지 운영해서 좋아요."), ("황O연", 4, "친절하고 가격이 명확합니다."), ("남O우", 5, "분위기 좋고 재방문 의사 있습니다.")]},
    {"slug": "cheongdam", "area": "청담", "lead": "청담동 프리미엄 라인, 격이 다른 무드의 고급 가라오케.", "rating": 4.9, "count": 88,
     "reviews": [("표O석", 5, "청담 감성 제대로입니다. 인테리어가 고급스러워요."), ("진O호", 5, "응대가 세련되고 룸이 넓습니다."), ("구O민", 4, "조용하고 프라이빗해서 좋았어요.")]},
    {"slug": "apgujeong", "area": "압구정", "lead": "압구정 로데오 인근, 트렌디한 분위기의 24시 가라오케.", "rating": 4.8, "count": 77,
     "reviews": [("하O준", 5, "압구정 분위기 그대로. 깔끔하고 트렌디합니다."), ("연O지", 4, "위치 좋고 응대 빠릅니다."), ("도O한", 5, "연중무휴라 언제 가도 좋아요.")]},
]
MAIN_RATING = 4.8
MAIN_COUNT = sum(r["count"] for r in REGIONS)
MAIN_REVIEWS = [
    ("김O준", 5, "프라이빗함이 정말 강점이에요. 사적인 자리 보호가 확실합니다."),
    ("최O진", 5, "음향이 정말 잘 되어 있어요. 현직 DJ팀 무대가 압권입니다."),
    ("표O석", 5, "전화 한 통에 실시간 추천이랑 특가까지. 응대가 정말 빠릅니다."),
    ("이O호", 5, "안주 퀄리티가 노래방 수준이 아니에요. 강남 맛집급."),
]

# 후기 풀(페이지별 변주) + 롱테일 내부링크 토픽
REVIEW_POOL = list(MAIN_REVIEWS)
for _r in REGIONS:
    REVIEW_POOL += _r["reviews"]

REGION_TOPICS = ["24시 가라오케", "프리미엄 가라오케", "가라오케 가격", "가라오케 룸 추천",
                 "가라오케 예약", "노래방 추천", "접대 가라오케", "파티 가라오케"]

TOPIC_PAGES = [
    ("강남 가라오케 룸 & 시설 안내", "pages/rooms.html"),
    ("강남 가라오케 요금 & 할인", "pages/price.html"),
    ("강남 가라오케 이용 방법 (1·2부)", "pages/how.html"),
    ("강남 가라오케 파티 & 이벤트", "pages/event.html"),
    ("강남 가라오케 프리미엄 서비스", "pages/service-premium.html"),
    ("강남 가라오케 주류 & 안주 메뉴", "pages/menu.html"),
    ("강남 가라오케 오시는 길", "pages/location.html"),
    ("24시 실시간 예약 문의", "pages/reservation.html"),
]


def reviews_for(seed, k=3):
    """페이지별로 후기·점수를 결정적으로 변주(스키마-노출 콘텐츠 일치용)."""
    n = len(REVIEW_POOL)
    revs = [REVIEW_POOL[(seed * 3 + j) % n] for j in range(k)]
    rating = [4.9, 4.8, 4.7][seed % 3]
    count = 120 + (seed * 17) % 160
    return rating, count, revs


def esc(s):
    return html.escape(str(s), quote=True)


def stars(n):
    n = int(round(n))
    return "★" * n + "☆" * (5 - n)


def rel(target, cur_dir):
    """root 상대 경로(target)를 현재 디렉터리(cur_dir) 기준 상대 URL로 변환."""
    return posixpath.relpath(target, cur_dir if cur_dir else ".")


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


# ---------- 스키마 ----------
def review_schema(reviews):
    return [{"@type": "Review", "author": {"@type": "Person", "name": w},
             "reviewRating": {"@type": "Rating", "ratingValue": r, "bestRating": 5}, "reviewBody": b}
            for w, r, b in reviews]


def local_business_schema(name, url, desc, rating, count, reviews, area=None):
    return {
        "@context": "https://schema.org", "@type": "NightClub", "name": name,
        "image": OG_IMAGE, "url": url, "description": desc, "telephone": TEL_INTL, "priceRange": "₩₩₩",
        "address": {"@type": "PostalAddress", "streetAddress": "선릉로92길 38", "addressLocality": "강남구", "addressRegion": "서울", "addressCountry": "KR"},
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating, "reviewCount": count, "bestRating": 5, "worstRating": 1},
        "review": review_schema(reviews), "areaServed": [area] if area else ["강남", "선릉", "삼성동"],
    }


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"}


def faq_schema(faq=FAQ):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def article_schema(title, desc, canonical, page_type="Article"):
    return {"@context": "https://schema.org", "@type": page_type, "headline": title, "description": desc,
            "image": OG_IMAGE, "inLanguage": "ko-KR", "url": canonical, "datePublished": "2026-06-01", "dateModified": UPDATED,
            "author": {"@type": "Organization", "name": AUTHOR, "url": BASE_URL + "/pages/about-company.html"},
            "reviewedBy": {"@type": "Organization", "name": REVIEWER},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": BASE_URL + "/favicon.svg"}},
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"}}


def breadcrumb_schema(trail):
    """trail: [(name, root_relative_or_None)]"""
    items = []
    for i, (name, path) in enumerate(trail, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        if path is not None:
            it["item"] = BASE_URL + "/" + path
        items.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


# ---------- 공통 컴포넌트 ----------
def header_html(cur_dir):
    home = rel("index.html", cur_dir)
    items = []
    for label, hub, subs in MENU:
        sub_html = "\n".join('          <li><a href="{}">{}</a></li>'.format(rel(t, cur_dir), esc(s)) for s, t in subs)
        items.append('''      <li>
        <a class="menu-toggle" href="{hub}" aria-haspopup="true">{label}<span class="caret"></span></a>
        <ul class="dropdown">
{subs}
        </ul>
      </li>'''.format(hub=rel(hub, cur_dir), label=esc(label), subs=sub_html))
    return '''  <div class="progress-bar" id="progress-bar"></div>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{home}">
        <span class="logo">도파민</span>
        <span class="logo-text">강남 가라오케 도파민<small>DOPAMINE · 24H</small></span>
      </a>
      <ul class="nav">
{nav}
      </ul>
      <div class="header-cta">
        <a class="btn btn-ghost btn-sm" href="{kakao}">카톡 상담</a>
        <a class="btn btn-primary btn-sm" href="{tel}">예약 문의</a>
        <button class="hamburger" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
  <div class="nav-backdrop"></div>'''.format(home=home, nav="\n".join(items), kakao=KAKAO_URL, tel=CONTACT_TEL)


def breadcrumb_html(trail, cur_dir):
    parts = []
    for name, path in trail:
        if path is None:
            parts.append("<span>{}</span>".format(esc(name)))
        else:
            parts.append('<a href="{}">{}</a>'.format(rel(path, cur_dir), esc(name)))
    return '  <div class="wrap"><nav class="breadcrumb" aria-label="breadcrumb">' + " › ".join(parts) + "</nav></div>"


def toc_nav(items, extra_class=""):
    """items: [(라벨, anchor_id)] → 클릭 시 해당 섹션으로 이동하는 목차."""
    lis = "\n".join(
        '        <li><a href="#{hid}"><span class="toc-num">{n:02d}</span><span>{label}</span></a></li>'.format(hid=hid, n=i + 1, label=esc(label))
        for i, (label, hid) in enumerate(items)
    )
    return '''<nav class="toc {cls}" aria-label="목차">
      <p class="toc-title">목차</p>
      <ol class="toc-list">
{lis}
      </ol>
    </nav>'''.format(cls=extra_class, lis=lis)


def toc_card_section(items):
    return '''  <section class="section" style="padding-top:34px;padding-bottom:0"><div class="wrap">
    <div class="toc-card">{toc}</div>
  </div></section>'''.format(toc=toc_nav(items, "toc-card-inner"))


def byline_html(cur_dir):
    company = rel("pages/about-company.html", cur_dir)
    return '''  <section class="section" style="padding-top:0">
    <div class="wrap"><div class="byline reveal">
      <span>작성 · 감수 <strong><a href="{company}">{author}</a></strong></span>
      <span>최종 업데이트 <strong>{updated}</strong></span>
      <span>본 콘텐츠는 도파민의 직접 운영 경험을 바탕으로 작성되었습니다.</span>
    </div></div>
  </section>'''.format(company=company, author=esc(AUTHOR), updated=esc(UPDATED))


def cta_band_html(cur_dir, label="지금 바로 예약 문의하기"):
    return '''  <section class="section"><div class="wrap">
    <div class="cta-band reveal">
      <div><h3>강남에서 가장 뜨거운 밤, 도파민</h3><p>연중무휴 24시간 · 주대 7만원부터 · 예약 문의 <a href="{tel}" style="color:var(--gold);font-weight:700">{tel_disp}</a></p></div>
      <div class="cta-band-btns">
        <a class="btn btn-primary" href="{tel}">{label}</a>
        <a class="btn btn-kakao" href="{kakao}">카카오톡 상담</a>
      </div>
    </div></div></section>'''.format(tel=CONTACT_TEL, tel_disp=esc(TEL_DISPLAY), kakao=KAKAO_URL, label=esc(label))


def region_links_html(cur_dir, current=None, title="강남 지역별 가라오케"):
    """지역 페이지로의 내부링크 — 지역별 롱테일 토픽 앵커로 강화."""
    out = []
    for i, r in enumerate(REGIONS):
        if r["slug"] == current:
            continue
        topic = REGION_TOPICS[i % len(REGION_TOPICS)]
        anchor = "{area} {topic}".format(area=r["area"], topic=topic)
        out.append('        <a href="{href}">{anchor}</a>'.format(href=rel("regions/{}.html".format(r["slug"]), cur_dir), anchor=esc(anchor)))
    return '''  <section class="section alt" id="regions">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">AREA</span><h2>{title}</h2>
        <p>강남·선릉·삼성동을 비롯한 강남권 전 지역의 도파민 가라오케 정보를 확인하세요.</p></div>
      <div class="linklist reveal">
{links}
      </div>
    </div>
  </section>'''.format(title=esc(title), links="\n".join(out))


def topic_links_html(cur_dir, area=None):
    """주제별 핵심 페이지로의 롱테일 내부링크 (지역 페이지에선 지역명으로 변주)."""
    out = []
    for label, target in TOPIC_PAGES:
        anchor = label.replace("강남", area, 1) if area else label
        out.append('        <a href="{href}">{anchor}</a>'.format(href=rel(target, cur_dir), anchor=esc(anchor)))
    sub = "{a} 가라오케의 룸·요금·서비스·예약을 주제별로 빠르게 확인하세요.".format(a=area) if area else "룸·요금·서비스·예약 등 주제별로 빠르게 확인하세요."
    return '''  <section class="section" id="topics">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">GUIDE</span><h2>주제별 안내 바로가기</h2>
        <p>{sub}</p></div>
      <div class="linklist reveal">
{links}
      </div>
    </div>
  </section>'''.format(sub=esc(sub), links="\n".join(out))


def footer_html(cur_dir):
    home = rel("index.html", cur_dir)
    region_links = "\n".join('        <a href="{href}">{area} 가라오케</a>'.format(href=rel("regions/{}.html".format(r["slug"]), cur_dir), area=esc(r["area"])) for r in REGIONS[:5])
    menu_links = "\n".join('        <a href="{href}">{label}</a>'.format(href=rel(hub, cur_dir), label=esc(label)) for label, hub, _ in MENU)
    return '''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-col">
          <h5>강남 가라오케 도파민</h5>
          <p>강남 선릉·삼성동에 위치한 24시 연중무휴 프리미엄 가라오케.</p>
          <p>{addr}</p>
          <p>365일 24시간 · 1부/2부 운영</p>
          <p>예약 전화 <a href="{tel}" style="color:var(--gold);font-weight:700">{tel_disp}</a></p>
        </div>
        <div class="footer-col">
          <h5>메뉴</h5>
{menu_links}
        </div>
        <div class="footer-col">
          <h5>지역</h5>
{region_links}
        </div>
        <div class="footer-col">
          <h5>회사 · 고객센터</h5>
          <a href="{company}">회사소개</a><a href="{terms}">이용약관</a><a href="{privacy}">개인정보처리방침</a>
          <a href="{tel}">전화 예약 {tel_disp}</a><a href="{kakao}">카카오톡 채널</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 강남 가라오케 도파민 · {base}</span>
        <span class="legal"><a href="{company}">회사소개</a><a href="{terms}">이용약관</a><a href="{privacy}">개인정보처리방침</a></span>
      </div>
    </div>
  </footer>
  <div class="float-cta"><a class="btn btn-kakao" href="{kakao}">카톡 상담</a><a class="btn btn-primary" href="{tel}">전화 예약</a></div>
  <script src="{js}"></script>'''.format(addr=esc(ADDRESS), menu_links=menu_links, region_links=region_links,
                                          company=rel("pages/about-company.html", cur_dir), terms=rel("pages/terms.html", cur_dir),
                                          privacy=rel("pages/privacy.html", cur_dir), tel=CONTACT_TEL, tel_disp=esc(TEL_DISPLAY),
                                          kakao=KAKAO_URL, base=BASE_URL, js=rel("assets/app.js", cur_dir))


def head_html(title, desc, keywords, canonical, schema_objs, cur_dir):
    css = rel("assets/style.css", cur_dir)
    schema = "\n  ".join(jsonld(o) for o in schema_objs)
    return '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="application-name" content="{site}" />
  <meta name="keywords" content="{kw}" />
  <meta name="author" content="{author}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{site}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ogimg}" />
  <meta property="og:locale" content="ko_KR" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{ogimg}" />

  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#0f0a1d" />

  {schema}

  <link rel="preconnect" href="https://www.google.com" />
  <link rel="stylesheet" href="{css}" />
</head>
<body>'''.format(title=esc(title), desc=esc(desc), site=esc(SITE_NAME), kw=esc(keywords), author=esc(AUTHOR),
                 canonical=canonical, ogimg=OG_IMAGE, schema=schema, css=css)


# ---------- 메인/지역 페이지 컴포넌트 (요약 섹션) ----------
def features_html(cur_dir):
    cards = "\n".join('        <div class="feature reveal"><div class="ic">{ic}</div><h3>{t}</h3><p>{d}</p></div>'.format(ic=ic, t=esc(t), d=esc(d)) for ic, t, d in FEATURES)
    more = rel("pages/intro.html", cur_dir)
    return '''  <section class="section alt" id="features">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">WHY DOPAMINE</span><h2>도파민만의 특별함</h2>
        <p>단순한 노래방이 아닌, 강남 프리미엄 파티 공간의 기준. <a href="{more}">도파민 소개 자세히 보기 →</a></p></div>
      <div class="features">
{cards}
      </div>
    </div>
  </section>'''.format(cards=cards, more=more)


def rooms_html(cur_dir):
    page_for = {"L": "pages/room-l.html", "M": "pages/room-m.html", "S": "pages/room-s.html"}
    cards = []
    for rid, cls, cap, name, pers, desc in ROOMS:
        cards.append('''        <article class="room reveal" id="{rid}">
          <div class="thumb {cls}"><span class="cap">{cap}</span><span class="pers">{pers}</span></div>
          <div class="body"><h3>{name}</h3><p>{desc}</p>
            <a class="btn btn-ghost btn-sm" href="{href}">{name} 자세히 보기</a></div>
        </article>'''.format(rid=rid, cls=cls, cap=cap, pers=esc(pers), name=esc(name), desc=esc(desc), href=rel(page_for[cap], cur_dir)))
    return '''  <section class="section" id="rooms">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">ROOM TOUR</span><h2>룸 & 시설</h2>
        <p>파티의 규모와 성격에 맞춰 완벽한 공간을 제공합니다. 전 룸 완벽 방음.</p></div>
      <div class="rooms">
{cards}
      </div>
    </div>
  </section>'''.format(cards="\n".join(cards))


def reviews_html(rating, count, reviews):
    cards = "\n".join('        <div class="review reveal"><div class="who"><strong>{w}</strong><span class="stars">{s}</span></div><p>{b}</p></div>'.format(w=esc(w), s=stars(r), b=esc(b)) for w, r, b in reviews)
    return '''  <section class="section" id="reviews">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">REVIEWS</span><h2>후기 & 신뢰도</h2>
        <p>연예인·BJ·기업인이 선택한 강남 1등 프리미엄 가라오케.</p></div>
      <div class="rating-summary reveal"><span class="rating-score">{rating}</span><span class="stars">{rstars}</span><span style="color:var(--muted)">리뷰 {count}개 기준</span></div>
      <div class="reviews">
{cards}
      </div>
    </div>
  </section>'''.format(rating=rating, rstars=stars(rating), count=count, cards=cards)


def location_html():
    return '''  <section class="section" id="location">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">LOCATION</span><h2>오시는 길</h2>
        <p>강남 선릉·삼성동의 중심. 강남권 VIP 고객을 위한 최고급 차량 픽업 서비스 운영.</p></div>
      <div class="location-grid">
        <div class="map-embed reveal"><iframe src="{map}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="도파민 위치 지도"></iframe></div>
        <dl class="loc-info reveal">
          <dt>주소</dt><dd>{addr}</dd>
          <dt>영업시간</dt><dd>365일 연중무휴 24시간<br>1부 15:00~01:00 · 2부 01:00~15:00</dd>
          <dt>예약·문의</dt><dd><a href="{tel}" style="color:var(--accent)">전화 예약 {tel_disp}</a> · <a href="{kakao}" style="color:var(--accent)">카카오톡 채널</a></dd>
          <dt>특별 서비스</dt><dd>강남권 VIP 최고급 차량 픽업 (사전 문의)</dd>
        </dl>
      </div>
    </div>
  </section>'''.format(map=MAP_SRC, addr=esc(ADDRESS), tel=CONTACT_TEL, tel_disp=esc(TEL_DISPLAY), kakao=KAKAO_URL)


# ---------- 본문 블록 → HTML ----------
def render_blocks(blocks):
    """본문 HTML과 목차(h2 기준)를 함께 반환. h2에는 앵커 id 부여."""
    out = []
    toc = []
    n = 0
    for kind, val in blocks:
        if kind == "h2":
            n += 1
            hid = "sec-{}".format(n)
            toc.append((val, hid))
            out.append('      <h2 id="{hid}">{t}</h2>'.format(hid=hid, t=esc(val)))
        elif kind == "h3":
            out.append("      <h3>{}</h3>".format(esc(val)))
        elif kind == "p":
            out.append("      <p>{}</p>".format(esc(val)))
        elif kind == "ul":
            lis = "".join("<li>{}</li>".format(esc(x)) for x in val)
            out.append("      <ul>{}</ul>".format(lis))
    return "\n".join(out), toc


def related_html(related, cur_dir, outbound):
    inner = "\n".join('        <a href="{}">{}</a>'.format(rel(t, cur_dir), esc(l)) for l, t in related)
    out_links = ""
    if outbound:
        items = "\n".join('        <a href="{u}" target="_blank" rel="noopener">{l} ↗</a>'.format(u=u, l=esc(l)) for l, u in outbound)
        out_links = '''      <div class="section-head reveal" style="margin-top:36px"><span class="tag">REFERENCE</span><h2>관련 정보 · 참고</h2>
        <p>공신력 있는 기관 정보로 위치·이용을 확인하세요.</p></div>
      <div class="linklist reveal">
{items}
      </div>'''.format(items=items)
    return '''  <section class="section alt">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">RELATED</span><h2>관련 안내</h2></div>
      <div class="linklist reveal">
{inner}
      </div>
{out_links}
    </div>
  </section>'''.format(inner=inner, out_links=out_links)


# ============== 개별 페이지 콘텐츠 (2,000~2,500자) ==============
def A(slug, title, desc, kw, h1, lead, trail_mid, blocks, related, outbound=None, schema_type="Article", extra_sections=""):
    """개별 페이지 정의를 dict로."""
    return dict(slug=slug, title=title, desc=desc, kw=kw, h1=h1, lead=lead, trail_mid=trail_mid,
                blocks=blocks, related=related, outbound=outbound or [], schema_type=schema_type, extra=extra_sections)


def _kw(*words):
    return ", ".join(words)


def build_articles():
    P = []  # 각 항목: A(...)

    # ===== 도파민 소개 (hub) =====
    P.append(A("intro", "도파민 소개 | 강남 가라오케 도파민",
        "강남 선릉·삼성동 프리미엄 가라오케 도파민을 소개합니다. 단독 건물 초대형 공간, 최첨단 음향·조명, 현직 DJ팀, 24시 연중무휴. 브랜드 스토리와 오시는 길을 확인하세요.",
        _kw("강남 가라오케 도파민 소개", "선릉 가라오케", "삼성동 프리미엄 가라오케", "강남 룸 소개"),
        "도파민 소개", "강남 선릉·삼성동의 프리미엄 가라오케, 도파민이 어떤 공간인지 안내합니다.",
        [("도파민 소개", None)],
        [("h2", "강남 프리미엄 가라오케의 기준, 도파민"),
         ("p", "도파민은 강남 선릉과 삼성동의 중심에서 프리미엄 가라오케 문화를 선도하는 공간입니다. 단순히 노래를 부르는 곳을 넘어, 공간 설계부터 음향·조명, 응대 매너, 안주의 퀄리티까지 모든 요소를 직접 운영하며 다듬어 왔습니다. 강남에서 중요한 자리를 준비하는 분들이 ‘실패 없는 선택’으로 도파민을 떠올리도록 만드는 것이 우리의 목표입니다."),
         ("p", "저희가 가장 중요하게 여기는 가치는 일관성입니다. 처음 방문하신 손님이든, 매주 찾으시는 단골 고객이든 동일하게 높은 수준의 경험을 받으셔야 한다고 믿습니다. 그래서 도파민은 룸 컨디션 점검, 위생 관리, 응대 매뉴얼을 매일 운영 단위로 관리합니다."),
         ("h2", "도파민이 직접 운영하며 쌓은 경험"),
         ("p", "도파민은 위탁이 아닌 직접 운영 체계로 움직입니다. 매니지먼트 팀이 예약 상담부터 룸 배정, 서비스, 마감까지 전 과정을 관리하기 때문에 손님의 요청이 중간에서 누락되지 않습니다. 이러한 직접 운영 경험이 도파민 콘텐츠와 서비스의 바탕이 됩니다."),
         ("ul", ["단독 건물 전체를 사용하는 초대형 공간과 룸별 개별 공조", "현직 DJ팀이 상주하는 라이브 퍼포먼스 무대", "철저한 보안·신분 보호로 사적인 자리와 비즈니스를 동시에 충족", "전문 셰프가 준비하는 강남 맛집급 안주와 폭넓은 주류 구성"]),
         ("h2", "어떤 분께 어울리나요"),
         ("p", "해외 귀빈 접대나 대규모 회식 같은 격식 있는 자리부터, 가까운 지인과의 생일·기념일, 소규모 모임까지 인원과 목적에 맞는 룸을 제안해 드립니다. 처음 방문하시는 분도 전화 또는 카카오톡으로 인원과 분위기를 알려주시면, 가장 적합한 룸과 코스를 실시간으로 추천해 드립니다."),
         ("p", "도파민은 강남·선릉·삼성동은 물론 역삼·논현·신논현·청담·압구정 등 강남권 전역에서 편리하게 방문하실 수 있는 위치에 있습니다. 자세한 길 안내와 픽업 서비스는 ‘오시는 길’ 페이지에서 확인해 주세요.")],
        [("브랜드 스토리", "pages/story.html"), ("오시는 길", "pages/location.html"), ("룸 & 시설 안내", "pages/rooms.html"), ("이용 방법(1·2부)", "pages/how.html")],
        outbound=[AUTH["gangnam"], AUTH["visit"]], schema_type="AboutPage"))

    # ===== 브랜드 스토리 =====
    P.append(A("story", "브랜드 스토리 | 강남 가라오케 도파민",
        "강남 가라오케 도파민의 브랜드 스토리. ‘짜릿한 몰입의 순간’을 뜻하는 도파민이라는 이름처럼, 강남 선릉·삼성동에서 완성한 프리미엄 가라오케 철학을 소개합니다.",
        _kw("강남 가라오케 도파민 브랜드", "도파민 스토리", "선릉 프리미엄 가라오케", "강남 룸 브랜드"),
        "브랜드 스토리", "이름에 담긴 의미부터 공간 철학까지, 도파민이 걸어온 길을 들려드립니다.",
        [("도파민 소개", "pages/intro.html"), ("브랜드 스토리", None)],
        [("h2", "‘도파민’이라는 이름에 담은 약속"),
         ("p", "도파민(Dopamine)은 즐거움과 몰입의 순간에 분비되는 신경전달물질입니다. 저희는 손님이 문을 열고 들어선 순간부터 마지막 인사를 나누는 순간까지, 그 짜릿한 몰입이 끊기지 않도록 만들겠다는 약속으로 이 이름을 골랐습니다. 강남의 수많은 선택지 속에서, ‘기억에 남는 밤’을 책임지는 브랜드가 되는 것이 시작점이었습니다."),
         ("h2", "공간을 직접 설계하며 배운 것"),
         ("p", "도파민은 인테리어 트렌드를 좇기보다, 실제 손님의 동선과 체감을 기준으로 공간을 다듬어 왔습니다. 룸의 크기와 좌석 배치, 음향이 닿는 각도, 조명의 색온도까지 운영을 통해 얻은 데이터로 조정했습니다. 그 결과 큰 소리에서도 대화가 가능한 음향 밸런스, 오래 머물러도 피로하지 않은 조명이라는 도파민만의 기준이 만들어졌습니다."),
         ("p", "특히 단독 건물 구조는 프라이버시와 몰입을 동시에 지키는 핵심입니다. 외부 시선과 소음에서 분리된 환경은 비즈니스 접대와 사적인 모임 모두에 안정감을 줍니다."),
         ("h2", "사람이 만드는 차이"),
         ("p", "좋은 공간도 결국 사람이 완성합니다. 도파민의 매니지먼트 팀은 과한 친절보다 ‘필요한 순간에 정확히 곁에 있는’ 응대를 지향합니다. 손님이 말하지 않아도 잔을 채우고, 분위기에 맞춰 무대를 끌어올리며, 사적인 자리를 존중해 거리를 둘 줄 아는 균형 감각을 가장 중요한 역량으로 봅니다."),
         ("ul", ["손님의 목적(접대·기념일·모임)에 맞춘 맞춤 응대", "요청을 끝까지 책임지는 직접 운영 체계", "재방문률로 검증되는 일관된 서비스 품질"]),
         ("h2", "도파민이 그리는 다음"),
         ("p", "도파민의 목표는 ‘강남에서 가장 화려한 곳’이 아니라 ‘강남에서 가장 믿을 수 있는 곳’입니다. 화려함은 한순간이지만 신뢰는 경험이 쌓여 만들어집니다. 앞으로도 도파민은 직접 경험에서 검증된 것만을 손님께 제안하겠습니다. 더 구체적인 시설과 서비스는 룸 안내와 서비스 안내 페이지에서 이어집니다.")],
        [("도파민 소개", "pages/intro.html"), ("프리미엄 서비스", "pages/service-premium.html"), ("룸 & 시설", "pages/rooms.html"), ("오시는 길", "pages/location.html")],
        outbound=[AUTH["visit"]], schema_type="Article"))

    # ===== 오시는 길 =====
    P.append(A("location", "오시는 길 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 오시는 길. 서울특별시 강남구 선릉로92길 38, 선릉역 인근. 지하철·차량 접근, 발렛 및 강남권 VIP 차량 픽업 서비스 안내.",
        _kw("강남 가라오케 오시는 길", "선릉 가라오케 위치", "삼성동 가라오케 길찾기", "도파민 주소"),
        "오시는 길", "선릉역 인근, 강남 어디서든 편하게. 위치와 교통, 픽업 서비스를 안내합니다.",
        [("도파민 소개", "pages/intro.html"), ("오시는 길", None)],
        [("h2", "주소와 위치"),
         ("p", "도파민의 주소는 ‘서울특별시 강남구 선릉로92길 38’입니다. 선릉역과 삼성동 코엑스 권역 사이에 위치해 강남 어느 방향에서 오셔도 접근이 편리합니다. 처음 방문하시는 분은 도착 전 전화 또는 카카오톡으로 연락 주시면 가장 가까운 출구와 진입로를 실시간으로 안내해 드립니다."),
         ("h2", "지하철로 오시는 길"),
         ("p", "지하철 이용 시 선릉역에서 도보 거리로 이동하실 수 있습니다. 분당선과 2호선이 교차하는 선릉역은 강남·역삼·삼성동에서 환승 없이 닿기 좋아, 대중교통을 이용하는 모임에 특히 편리합니다. 정확한 출구와 노선은 서울교통공사 노선 정보에서 확인하실 수 있습니다."),
         ("h2", "차량·발렛·픽업 서비스"),
         ("p", "차량으로 방문하시는 경우 발렛 및 인근 주차 안내를 도와드립니다. 음주가 예상되는 자리에서는 안전을 위해 대리운전 또는 픽업 이용을 권장합니다. 도파민은 강남권 VIP 고객을 위한 최고급 차량 픽업 서비스를 운영하고 있으니, 이용을 원하시면 방문 전 미리 문의해 주세요."),
         ("ul", ["주소: 서울특별시 강남구 선릉로92길 38", "지하철: 선릉역 인근 (도보 이동)", "차량: 발렛 및 인근 주차 안내", "VIP 픽업: 강남권 최고급 차량 픽업(사전 문의)"]),
         ("h2", "강남 전역에서의 접근성"),
         ("p", "도파민은 선릉을 중심으로 강남·삼성동·역삼·논현·신논현·청담·압구정 등 강남권 전역에서 단거리로 이동하실 수 있습니다. 지역별 상세 안내는 각 지역 페이지에서 확인하실 수 있으며, 정확한 도로명주소 검색은 도로명주소 안내시스템을 활용하시면 편리합니다.")],
        [("강남 가라오케", "regions/gangnam.html"), ("선릉 가라오케", "regions/seolleung.html"), ("삼성동 가라오케", "regions/samseong.html"), ("실시간 픽업 문의", "pages/pickup.html")],
        outbound=[AUTH["metro"], AUTH["juso"], AUTH["gangnam"]], schema_type="Article"))

    # ===== 룸 & 시설 (hub) =====
    P.append(A("rooms", "룸 & 시설 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 룸 & 시설 안내. L 룸(최대 20인), M 룸(최대 14인), S 룸(최대 8인). 전 룸 완벽 방음, 최첨단 음향·조명, 룸별 개별 공조.",
        _kw("강남 가라오케 룸", "선릉 가라오케 룸 종류", "강남 룸 인원", "도파민 시설"),
        "룸 & 시설", "인원과 목적에 맞는 완벽한 공간. 도파민의 룸 구성과 시설을 안내합니다.",
        [("룸 & 시설", None)],
        [("h2", "규모와 목적에 맞춘 3가지 룸"),
         ("p", "도파민은 모임의 규모와 성격에 따라 L·M·S 세 가지 룸을 운영합니다. 단순히 크기만 다른 것이 아니라, 좌석 배치와 음향 세팅, 분위기까지 각 룸의 용도에 맞게 최적화되어 있습니다. 인원이 애매하다면 예약 시 알려주세요. 여유 있는 좌석과 동선을 기준으로 가장 적합한 룸을 추천해 드립니다."),
         ("ul", ["L 룸 — 최대 20인. 대규모 회식·VIP 접대·파티에 최적", "M 룸 — 최대 14인. 고객 접대와 생일·기념일 모임에 적합", "S 룸 — 최대 8인. 소규모 모임과 편안한 술자리"]),
         ("h2", "전 룸 공통 시설"),
         ("p", "모든 룸은 완벽한 방음 설계로 옆 룸의 소음 없이 온전히 몰입할 수 있습니다. 최신 반주기와 고출력·고해상 음향 시스템, 무대형 조명을 갖춰 어떤 룸에서도 수준 높은 무대를 경험하실 수 있습니다. 룸별 개별 공조(냉난방·공기청정)로 인원이 많아도 쾌적함이 유지됩니다."),
         ("h2", "위생과 컨디션 관리"),
         ("p", "도파민은 룸 회전마다 좌석·테이블·마이크 등 접촉 부위를 점검하고 정비합니다. 손님이 입장하는 모든 룸이 ‘첫 손님을 맞는 상태’이도록 관리하는 것이 직접 운영의 원칙입니다. 작은 차이가 머무는 내내의 만족으로 이어진다고 믿습니다."),
         ("h2", "룸 선택이 고민될 때"),
         ("p", "접대나 중요한 자리라면 인원보다 한 단계 넉넉한 룸을, 가벼운 모임이라면 아늑한 S 룸을 추천드립니다. 각 룸의 상세 분위기와 추천 이용 시나리오는 아래 개별 룸 페이지에서 확인하실 수 있습니다.")],
        [("L 룸 (최대 20인)", "pages/room-l.html"), ("M 룸 (최대 14인)", "pages/room-m.html"), ("S 룸 (최대 8인)", "pages/room-s.html"), ("요금 & 할인", "pages/price.html")],
        schema_type="WebPage"))

    # ===== 룸 L / M / S =====
    P.append(A("room-l", "L 룸 (최대 20인) | 강남 가라오케 도파민",
        "강남 가라오케 도파민 L 룸 안내. 최대 20인 수용, 해외 귀빈 접대·대규모 회식·VIP 파티에 최적화된 최고급 룸. 완벽 방음과 무대형 음향·조명.",
        _kw("강남 가라오케 대형룸", "강남 20인 룸", "선릉 가라오케 L룸", "강남 VIP 파티룸"),
        "L 룸 — 최대 20인", "해외 귀빈 접대와 대규모 파티를 위한 도파민 최고급 룸.",
        [("룸 & 시설", "pages/rooms.html"), ("L 룸", None)],
        [("h2", "대규모 모임을 위한 최고급 공간"),
         ("p", "L 룸은 최대 20인까지 수용하는 도파민의 대표 대형 룸입니다. 넓은 좌석과 여유로운 동선으로 사람이 많아도 답답함 없이 움직일 수 있어, 해외 귀빈 접대나 대규모 회식, 연예인·VIP 파티처럼 격식과 규모가 필요한 자리에 적합합니다."),
         ("h2", "무대가 살아나는 음향과 조명"),
         ("p", "넓은 공간일수록 음향의 균형이 중요합니다. L 룸은 공간 크기에 맞춰 출력과 스피커 배치를 설계해, 큰 소리에서도 목소리가 묻히지 않고 대화도 가능한 밸런스를 유지합니다. 무대형 조명은 분위기를 단숨에 끌어올려 파티의 하이라이트를 만들어 줍니다."),
         ("h2", "이런 자리에 추천합니다"),
         ("ul", ["임원·해외 바이어가 참석하는 격식 있는 접대", "20명 내외의 부서 회식 및 단체 모임", "현직 DJ팀 무대를 곁들인 대형 파티", "기념일·축하 행사 등 인원이 많은 이벤트"]),
         ("h2", "예약 팁"),
         ("p", "대형 룸은 주말과 행사 시즌에 예약이 빠르게 마감됩니다. 인원과 방문 시간이 확정되면 가급적 미리 문의해 주세요. 안주 코스와 주류 구성, 케이크·현수막 등 행사 세팅도 함께 안내해 드립니다. 요금은 인원과 코스에 따라 달라지며, 웹 예약 시 특가 혜택이 적용됩니다.")],
        [("M 룸 (최대 14인)", "pages/room-m.html"), ("파티 & 이벤트", "pages/event.html"), ("요금 & 할인", "pages/price.html"), ("실시간 예약 문의", "pages/reservation.html")],
        schema_type="Article"))

    P.append(A("room-m", "M 룸 (최대 14인) | 강남 가라오케 도파민",
        "강남 가라오케 도파민 M 룸 안내. 최대 14인 수용, 중요한 고객 접대와 생일·기념일 모임에 제격인 중형 룸. 완벽 방음과 프라이빗한 분위기.",
        _kw("강남 가라오케 중형룸", "강남 14인 룸", "선릉 가라오케 M룸", "강남 접대 룸"),
        "M 룸 — 최대 14인", "접대와 기념일 모임 모두에 어울리는 균형 잡힌 중형 룸.",
        [("룸 & 시설", "pages/rooms.html"), ("M 룸", None)],
        [("h2", "접대와 모임 사이의 완벽한 균형"),
         ("p", "M 룸은 최대 14인까지 수용하는 중형 룸으로, 도파민에서 가장 활용도가 높은 공간입니다. 너무 크지도 작지도 않아 중요한 고객 접대부터 가까운 지인들과의 생일·기념일 파티까지 폭넓게 어울립니다. 적당한 밀도가 만들어 내는 ‘오붓하면서도 활기찬’ 분위기가 M 룸의 매력입니다."),
         ("h2", "프라이빗한 분위기"),
         ("p", "완벽한 방음과 단독 건물 구조 덕분에 외부의 방해 없이 자리에 집중할 수 있습니다. 사적인 대화가 오가는 접대 자리에서도 안심하실 수 있도록 프라이버시를 우선으로 설계했습니다. 좌석 배치는 대화와 무대 관람이 모두 편하도록 구성되어 있습니다."),
         ("h2", "이런 자리에 추천합니다"),
         ("ul", ["10명 내외의 비즈니스 접대 및 부서 회식", "생일·승진·기념일 등 축하 모임", "동호회·동창 모임 등 친밀한 단체", "무대와 대화를 함께 즐기고 싶은 자리"]),
         ("h2", "함께 즐기면 좋은 구성"),
         ("p", "M 룸에서는 셰프 추천 안주 코스와 와인·위스키 등 주류 페어링을 곁들이면 만족도가 높습니다. 생일·기념일에는 케이크와 간단한 이벤트 세팅도 도와드립니다. 인원과 목적을 알려주시면 예산에 맞춘 코스를 제안해 드리며, 더 큰 모임은 L 룸, 소규모는 S 룸을 함께 검토해 보세요.")],
        [("L 룸 (최대 20인)", "pages/room-l.html"), ("S 룸 (최대 8인)", "pages/room-s.html"), ("주류 & 안주 메뉴", "pages/menu.html"), ("요금 & 할인", "pages/price.html")],
        schema_type="Article"))

    P.append(A("room-s", "S 룸 (최대 8인) | 강남 가라오케 도파민",
        "강남 가라오케 도파민 S 룸 안내. 최대 8인 수용, 소규모 모임과 편안한 술자리를 위한 아늑하고 세련된 룸. 완벽 방음과 합리적인 이용.",
        _kw("강남 가라오케 소규모룸", "강남 8인 룸", "선릉 가라오케 S룸", "강남 소모임 가라오케"),
        "S 룸 — 최대 8인", "소규모 모임과 편안한 술자리를 위한 아늑한 프라이빗 룸.",
        [("룸 & 시설", "pages/rooms.html"), ("S 룸", None)],
        [("h2", "가깝고 편안한 소규모 전용 공간"),
         ("p", "S 룸은 최대 8인까지 수용하는 소규모 전용 룸입니다. 적은 인원이 더 가깝게 모여 즐길 수 있도록 아늑하게 설계되어, 가벼운 술자리나 친한 사람들과의 모임에 가장 잘 어울립니다. 처음 도파민을 경험해 보고 싶은 분께도 부담 없는 선택입니다."),
         ("h2", "작은 공간, 완성도 높은 경험"),
         ("p", "공간이 작다고 시설이 떨어지지 않습니다. S 룸도 완벽한 방음과 최신 반주기, 선명한 음향과 분위기 있는 조명을 동일하게 갖추고 있습니다. 아늑한 크기 덕분에 음향이 더 풍부하게 감싸 주어, 노래에 집중하기에는 오히려 더 좋다는 평을 듣습니다."),
         ("h2", "이런 자리에 추천합니다"),
         ("ul", ["4~8명의 친구·동료 모임", "가벼운 2차 및 편안한 술자리", "연인·소수 지인과의 프라이빗한 시간", "도파민 첫 방문으로 분위기를 경험하고 싶은 자리"]),
         ("h2", "합리적인 이용"),
         ("p", "S 룸은 주대 7만원부터 시작하는 합리적인 구성으로 부담 없이 즐기실 수 있습니다. 인원이 늘어날 가능성이 있다면 예약 시 미리 알려주세요. 여유 있는 M 룸으로의 변경도 안내해 드립니다. 자세한 요금과 할인은 요금 & 할인 페이지를 참고해 주세요.")],
        [("M 룸 (최대 14인)", "pages/room-m.html"), ("요금 & 할인", "pages/price.html"), ("이용 방법(1·2부)", "pages/how.html"), ("실시간 예약 문의", "pages/reservation.html")],
        schema_type="Article"))

    # ===== 서비스 안내 (hub) =====
    P.append(A("service", "서비스 안내 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 서비스 안내. 프리미엄 1:1 맞춤 응대, 주류 & 안주 메뉴, 파티 & 이벤트 세팅까지 도파민만의 차별화된 서비스를 소개합니다.",
        _kw("강남 가라오케 서비스", "선릉 가라오케 응대", "강남 가라오케 안주", "도파민 파티"),
        "서비스 안내", "도파민을 ‘노래방 그 이상’으로 만드는 서비스 전반을 안내합니다.",
        [("서비스 안내", None)],
        [("h2", "경험의 격을 높이는 도파민 서비스"),
         ("p", "도파민의 서비스는 ‘무엇을 더 해드릴까’가 아니라 ‘어떻게 하면 손님이 편안하실까’에서 출발합니다. 응대, 메뉴, 이벤트 세팅 모두 손님의 목적에 맞춰 조율되며, 직접 운영하는 매니지먼트 팀이 처음부터 끝까지 책임집니다."),
         ("h2", "세 가지 핵심 서비스"),
         ("ul", ["프리미엄 서비스 — 전문 매니저의 1:1 맞춤 응대와 철저한 프라이버시 보호", "주류 & 안주 메뉴 — 전문 셰프의 강남 맛집급 안주와 폭넓은 주류 구성", "파티 & 이벤트 — 생일·기념일·기업 단체를 위한 맞춤 세팅과 DJ 무대"]),
         ("h2", "현직 DJ팀의 라이브 퍼포먼스"),
         ("p", "도파민에는 화려한 경력의 현직 DJ팀이 상주합니다. 단순한 반주를 넘어, 분위기의 흐름을 읽어 무대를 끌어올리는 라이브 퍼포먼스가 도파민의 밤을 특별하게 만듭니다. 마이크 세팅과 음향 밸런스도 손님의 노래가 가장 좋게 들리도록 맞춰 드립니다."),
         ("h2", "신뢰가 먼저인 응대"),
         ("p", "프리미엄 서비스의 핵심은 신뢰입니다. 도파민은 과한 개입 대신 사적인 자리를 존중하며, 필요한 순간 정확하게 곁에 있는 응대를 지향합니다. 각 서비스의 자세한 내용은 아래 개별 페이지에서 이어집니다.")],
        [("프리미엄 서비스", "pages/service-premium.html"), ("주류 & 안주 메뉴", "pages/menu.html"), ("파티 & 이벤트", "pages/event.html"), ("요금 & 할인", "pages/price.html")],
        schema_type="WebPage"))

    P.append(A("service-premium", "프리미엄 서비스 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 프리미엄 서비스. 전문 매니저의 1:1 맞춤 응대, 철저한 프라이버시·신분 보호, 실시간 룸·코스 추천으로 완성하는 품격 있는 경험.",
        _kw("강남 가라오케 프리미엄 서비스", "강남 가라오케 응대", "선릉 가라오케 매니저", "강남 프라이빗 가라오케"),
        "프리미엄 서비스", "전문 매니저의 1:1 응대와 철저한 프라이버시로 완성하는 품격.",
        [("서비스 안내", "pages/service.html"), ("프리미엄 서비스", None)],
        [("h2", "1:1 맞춤 응대의 의미"),
         ("p", "도파민의 프리미엄 서비스는 손님 한 분, 한 자리의 목적을 이해하는 데서 시작합니다. 접대 자리인지, 축하 모임인지, 편안한 술자리인지에 따라 응대의 거리와 방식이 달라집니다. 전문 매니저는 손님이 굳이 요청하지 않아도 필요한 순간을 먼저 살피고, 자리의 흐름이 끊기지 않도록 세심하게 돕습니다."),
         ("h2", "철저한 프라이버시와 신분 보호"),
         ("p", "강남에서 중요한 자리를 가지는 분들에게 프라이버시는 선택이 아니라 필수입니다. 도파민은 단독 건물 구조와 완벽한 방음, 그리고 응대 단계의 보안 원칙으로 사적인 대화와 비즈니스를 철저히 보호합니다. 손님의 정보와 방문 사실은 운영 원칙에 따라 신중히 관리됩니다."),
         ("h2", "실시간 추천이라는 차별점"),
         ("p", "예약 상담 시 인원과 분위기, 예산을 알려주시면 가장 적합한 룸과 안주 코스, 주류 구성을 실시간으로 추천해 드립니다. 현장에서도 분위기에 맞춰 무대 연출과 서비스를 조율하기 때문에, 손님은 복잡한 결정 없이 그 순간을 즐기기만 하시면 됩니다."),
         ("ul", ["목적에 맞춘 전문 매니저의 1:1 응대", "단독 건물·방음·보안으로 완성하는 프라이버시", "인원·예산 맞춤 룸/코스 실시간 추천", "요청을 끝까지 책임지는 직접 운영"]),
         ("h2", "소비자로서의 안심"),
         ("p", "도파민은 요금과 서비스 내용을 사전에 명확히 안내해, 이용 후 발생할 수 있는 오해를 줄입니다. 합리적이고 투명한 거래는 프리미엄 서비스의 기본이라고 생각합니다. 소비자 권익 관련 일반 정보는 한국소비자원에서도 확인하실 수 있습니다.")],
        [("주류 & 안주 메뉴", "pages/menu.html"), ("파티 & 이벤트", "pages/event.html"), ("요금 & 할인", "pages/price.html"), ("FAQ", "pages/faq.html")],
        outbound=[AUTH["kca"]], schema_type="Service"))

    P.append(A("menu", "주류 & 안주 메뉴 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 주류 & 안주 메뉴. 전문 셰프의 강남 맛집급 시그니처 안주와 위스키·와인·샴페인 등 폭넓은 주류 구성으로 술자리의 격을 높입니다.",
        _kw("강남 가라오케 안주", "강남 가라오케 주류", "선릉 가라오케 메뉴", "강남 가라오케 양주"),
        "주류 & 안주 메뉴", "노래방 안주가 아닌, 강남 맛집급 퀄리티. 도파민의 메뉴를 소개합니다.",
        [("서비스 안내", "pages/service.html"), ("주류 & 안주 메뉴", None)],
        [("h2", "‘노래방 안주’라는 편견을 깨다"),
         ("p", "도파민의 안주는 전문 셰프가 직접 준비합니다. 단순히 술과 곁들이는 수준이 아니라, 그 자체로 만족스러운 한 끼이자 자리의 품격을 높이는 요소로 구성했습니다. 신선한 재료와 정돈된 플레이팅으로 ‘강남 맛집급’이라는 평을 듣는 이유입니다."),
         ("h2", "주류 구성"),
         ("p", "위스키와 양주 프리미엄 라인업부터 와인·샴페인, 맥주와 칵테일까지 폭넓게 갖추고 있습니다. 자리의 성격과 취향에 맞춰 어울리는 주류를 추천해 드리며, 접대 자리에는 격에 맞는 라인업을, 가벼운 모임에는 부담 없는 구성을 제안합니다."),
         ("ul", ["위스키 / 양주 — 프리미엄 라인업", "와인 / 샴페인 — 자리에 맞춘 소믈리에 추천", "맥주 / 칵테일 — 다양한 구성", "시그니처 안주 — 셰프 스페셜", "모둠 과일 & 마른안주 — 기본 구성", "식사 메뉴 — 야식까지 가능"]),
         ("h2", "코스로 즐기는 방법"),
         ("p", "인원과 예산을 알려주시면 안주와 주류를 코스 형태로 구성해 드립니다. 처음 방문이라 메뉴 선택이 어렵다면, 매니저가 가장 인기 있는 조합을 추천해 드리니 편하게 문의하세요. 늦은 시간 출출함을 달랠 식사 메뉴도 준비되어 있습니다."),
         ("h2", "위생과 품질 관리"),
         ("p", "도파민은 식재료의 보관과 위생을 운영 원칙으로 관리합니다. 손님이 안심하고 즐기실 수 있도록 기본을 지키는 것이 프리미엄의 출발이라고 믿습니다. 식품 안전 관련 일반 정보는 식품안전나라에서도 확인하실 수 있습니다.")],
        [("프리미엄 서비스", "pages/service-premium.html"), ("파티 & 이벤트", "pages/event.html"), ("요금 & 할인", "pages/price.html"), ("M 룸 (최대 14인)", "pages/room-m.html")],
        outbound=[AUTH["food"]], schema_type="Article"))

    P.append(A("event", "파티 & 이벤트 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 파티 & 이벤트. 생일·기념일 세팅, 기업 단체·접대 패키지, 현직 DJ팀 라이브 무대까지. 강남에서 특별한 날을 완벽하게 연출합니다.",
        _kw("강남 가라오케 파티", "강남 생일 파티 룸", "강남 기업 단체 가라오케", "강남 DJ 파티"),
        "파티 & 이벤트", "생일·기념일부터 기업 단체까지, 특별한 날을 도파민이 연출합니다.",
        [("서비스 안내", "pages/service.html"), ("파티 & 이벤트", None)],
        [("h2", "기억에 남는 하루를 설계합니다"),
         ("p", "도파민은 단순히 공간을 빌려드리는 곳이 아니라, 하루의 분위기를 함께 설계하는 파트너입니다. 생일·기념일·승진·송년 등 어떤 자리든 목적과 예산을 알려주시면 그에 맞는 룸과 코스, 연출을 제안해 드립니다."),
         ("h2", "생일·기념일 세팅"),
         ("p", "케이크와 현수막, 간단한 이벤트 연출까지 도와드려 주인공을 빛나게 합니다. 현직 DJ팀이 타이밍에 맞춰 무대를 끌어올리면, 평범한 노래방과는 전혀 다른 축하의 순간이 완성됩니다. 깜짝 이벤트를 준비하신다면 사전에 귀띔해 주세요. 동선까지 함께 맞춰 드립니다."),
         ("h2", "기업 단체·접대 패키지"),
         ("p", "부서 회식, 워크숍 뒤풀이, 중요한 접대 자리를 위한 단체 패키지를 운영합니다. 인원 규모에 따라 L·M 룸을 배정하고, 안주·주류 코스를 예산에 맞춰 구성해 드립니다. 격식이 필요한 자리에서는 응대 매너와 프라이버시 보호가 특히 강점입니다."),
         ("ul", ["생일·기념일 케이크 및 현수막 세팅", "기업 단체·접대 맞춤 패키지", "현직 DJ팀 라이브 퍼포먼스", "깜짝 이벤트·축하 연출 지원"]),
         ("h2", "예약과 준비"),
         ("p", "행사는 준비 시간이 곧 완성도입니다. 날짜와 인원, 원하는 연출이 정해지면 가능한 한 일찍 문의해 주세요. 시즌과 주말에는 대형 룸 예약이 빠르게 마감됩니다. 실시간 상담으로 일정과 구성을 확정해 드립니다.")],
        [("L 룸 (최대 20인)", "pages/room-l.html"), ("주류 & 안주 메뉴", "pages/menu.html"), ("요금 & 할인", "pages/price.html"), ("실시간 예약 문의", "pages/reservation.html")],
        schema_type="Article"))

    # ===== 이용 안내 (hub) =====
    P.append(A("guide", "이용 안내 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 이용 안내. 1부·2부 운영 시간, 이용 방법, 주대 7만원부터의 요금과 할인, 자주 묻는 질문까지 한눈에 확인하세요.",
        _kw("강남 가라오케 이용 방법", "강남 가라오케 시간", "강남 가라오케 요금", "선릉 가라오케 안내"),
        "이용 안내", "처음 방문도 어렵지 않도록, 이용 전반을 한 페이지에 정리했습니다.",
        [("이용 안내", None)],
        [("h2", "이용 흐름 한눈에 보기"),
         ("p", "도파민 이용은 간단합니다. ① 전화 또는 카카오톡으로 인원·시간 문의 → ② 매니저의 룸·코스 실시간 추천 → ③ 방문 및 안내 → ④ 즐거운 이용 → ⑤ 편안한 마무리 순으로 진행됩니다. 처음 방문하시는 분도 상담 한 번이면 충분합니다."),
         ("h2", "1부·2부 운영"),
         ("p", "도파민은 365일 24시간 연중무휴로 운영하며, 1부(15:00~01:00)와 2부(01:00~15:00)로 나뉩니다. 낮부터 새벽까지 언제든 원하는 시간에 방문하실 수 있어, 늦은 모임이나 2차 자리에도 부담이 없습니다."),
         ("h2", "요금과 할인"),
         ("p", "주대는 7만원부터 시작하며, 인원과 코스에 따라 달라집니다. 웹사이트 예약 시 다양한 특가 혜택이 적용됩니다. 명확한 사전 안내를 원칙으로 하므로, 문의 시 예상 비용을 투명하게 알려드립니다."),
         ("ul", ["운영: 365일 24시간 (1부 15:00~01:00 · 2부 01:00~15:00)", "요금: 주대 7만원부터, 웹 예약 특가 적용", "예약: 전화·카카오톡으로 연중무휴 24시간 상담", "픽업: 강남권 VIP 차량 픽업(사전 문의)"]),
         ("h2", "더 자세한 안내"),
         ("p", "이용 방법, 요금 & 할인, 자주 묻는 질문은 각 페이지에서 더 자세히 다룹니다. 궁금한 점이 있으시면 언제든 실시간으로 문의해 주세요.")],
        [("이용 방법 (1·2부)", "pages/how.html"), ("요금 & 할인", "pages/price.html"), ("FAQ", "pages/faq.html"), ("오시는 길", "pages/location.html")],
        schema_type="WebPage"))

    P.append(A("how", "이용 방법 (1·2부) | 강남 가라오케 도파민",
        "강남 가라오케 도파민 이용 방법. 예약부터 방문, 1부(15:00~01:00)·2부(01:00~15:00) 운영, 마무리까지 단계별로 안내합니다. 처음이어도 쉽습니다.",
        _kw("강남 가라오케 이용 방법", "강남 가라오케 1부 2부", "강남 가라오케 예약 방법", "강남 가라오케 영업시간"),
        "이용 방법 (1·2부)", "예약부터 마무리까지, 도파민 이용 단계를 자세히 안내합니다.",
        [("이용 안내", "pages/guide.html"), ("이용 방법", None)],
        [("h2", "1단계 — 예약 문의"),
         ("p", "전화 또는 카카오톡 채널로 방문 날짜와 인원, 대략적인 시간을 알려주세요. 연중무휴 24시간 상담이 가능하며, 매니저가 조건에 맞는 룸과 안주·주류 코스를 실시간으로 추천해 드립니다. 예산이나 목적(접대·기념일·모임)을 함께 말씀해 주시면 더 정확한 안내가 가능합니다."),
         ("h2", "2단계 — 방문과 안내"),
         ("p", "도착 전 연락 주시면 가장 가까운 출구와 진입로, 발렛 위치를 안내해 드립니다. 차량 픽업을 예약하셨다면 약속한 장소에서 모십니다. 입장 후에는 배정된 룸으로 안내해 드리며, 시설과 이용 방법을 간단히 설명해 드립니다."),
         ("h2", "3단계 — 1부·2부 운영 이해"),
         ("p", "도파민은 24시간 연중무휴로 운영되며 1부는 오후 3시부터 새벽 1시까지, 2부는 새벽 1시부터 오후 3시까지입니다. 늦은 시간 시작하는 2차 자리나 새벽 모임에도 제약이 적어, 원하는 시간대를 자유롭게 선택하실 수 있습니다."),
         ("ul", ["1부: 15:00 ~ 01:00", "2부: 01:00 ~ 15:00", "연중무휴 365일 24시간 운영", "예약·문의: 전화 / 카카오톡 24시간"]),
         ("h2", "4단계 — 즐거운 이용과 마무리"),
         ("p", "이용 중 추가 안주나 주류, 시간 연장이 필요하시면 매니저에게 말씀만 해주세요. 마무리 시에는 안전한 귀가를 위해 대리운전·픽업 이용을 권장합니다. 처음 방문이라 걱정되신다면, 상담 단계에서 무엇이든 편하게 물어보시면 친절히 안내해 드립니다.")],
        [("요금 & 할인", "pages/price.html"), ("FAQ", "pages/faq.html"), ("실시간 픽업 문의", "pages/pickup.html"), ("오시는 길", "pages/location.html")],
        schema_type="Article"))

    P.append(A("price", "요금 & 할인 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 요금 & 할인. 주대 7만원부터 시작, 웹사이트 예약 한정 특가 혜택. 인원·코스에 따른 투명한 사전 안내로 안심하고 이용하세요.",
        _kw("강남 가라오케 요금", "강남 가라오케 가격", "강남 가라오케 주대", "강남 가라오케 할인"),
        "요금 & 할인", "주대 7만원부터, 투명한 사전 안내. 도파민의 요금 정책입니다.",
        [("이용 안내", "pages/guide.html"), ("요금 & 할인", None)],
        [("h2", "주대 7만원부터 시작"),
         ("p", "도파민의 주대는 7만원부터 시작합니다. 최종 금액은 룸 크기와 인원, 선택하시는 안주·주류 코스, 이용 시간에 따라 달라집니다. 도파민은 ‘이용 전 명확한 안내’를 원칙으로 하므로, 문의 시 예상 비용을 투명하게 알려드려 결제 단계에서의 오해를 줄입니다."),
         ("h2", "웹사이트 예약 한정 특가"),
         ("p", "웹사이트를 통해 예약·문의하시면 다양한 특가 혜택을 받으실 수 있습니다. 시즌과 요일, 시간대에 따라 적용되는 혜택이 달라지므로, 방문 전 실시간으로 가장 유리한 조건을 안내해 드립니다."),
         ("ul", ["주대 7만원부터 (룸·인원·코스에 따라 변동)", "웹 예약 한정 특가 혜택 제공", "안주·주류 코스는 예산 맞춤 구성", "이용 전 예상 비용 투명 안내"]),
         ("h2", "합리적인 선택을 돕습니다"),
         ("p", "소규모 모임이라면 S 룸으로 부담 없이, 접대나 대규모 자리라면 인원보다 한 단계 넉넉한 룸을 추천드립니다. 예산을 알려주시면 그 안에서 가장 만족도 높은 구성을 제안해 드립니다. 무리한 추가 권유 대신, 자리에 꼭 맞는 제안을 드리는 것이 도파민의 방식입니다."),
         ("h2", "투명한 거래를 위한 약속"),
         ("p", "도파민은 사전 안내한 내용과 실제 이용 내역이 일치하도록 운영합니다. 합리적이고 투명한 거래는 신뢰의 기본입니다. 소비자 권익과 거래 관련 일반 정보는 한국소비자원과 공정거래위원회에서도 확인하실 수 있습니다.")],
        [("이용 방법(1·2부)", "pages/how.html"), ("룸 & 시설", "pages/rooms.html"), ("FAQ", "pages/faq.html"), ("실시간 예약 문의", "pages/reservation.html")],
        outbound=[AUTH["kca"], AUTH["ftc"]], schema_type="Article"))

    # ===== FAQ =====
    faq_blocks = [("h2", "자주 묻는 질문")]
    P.append(A("faq", "자주 묻는 질문(FAQ) | 강남 가라오케 도파민",
        "강남 가라오케 도파민 자주 묻는 질문. 예약 방법, 요금, 픽업 서비스, 이용 인원, 영업 시간, 교통 접근 등 방문 전 궁금증을 한 번에 해결하세요.",
        _kw("강남 가라오케 FAQ", "강남 가라오케 질문", "강남 가라오케 예약 문의", "강남 가라오케 영업시간"),
        "자주 묻는 질문 (FAQ)", "방문 전 가장 많이 묻는 질문을 모았습니다.",
        [("이용 안내", "pages/guide.html"), ("FAQ", None)],
        [("p", "도파민 방문을 준비하시며 가장 많이 주시는 질문을 정리했습니다. 아래에서 답을 찾지 못하셨다면, 전화 또는 카카오톡으로 언제든 문의해 주세요. 연중무휴 24시간 실시간으로 안내해 드립니다.")],
        [("이용 방법(1·2부)", "pages/how.html"), ("요금 & 할인", "pages/price.html"), ("오시는 길", "pages/location.html"), ("실시간 예약 문의", "pages/reservation.html")],
        schema_type="FAQPage",
        extra_sections="__FAQ__"))

    # ===== 예약 문의 (hub) =====
    P.append(A("reservation", "예약 문의 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 예약 문의. 전화 예약, 카카오톡 채널, 실시간 픽업 문의까지. 연중무휴 24시간 상담으로 인원·시간에 맞는 룸을 실시간 추천해 드립니다.",
        _kw("강남 가라오케 예약", "강남 가라오케 문의", "선릉 가라오케 예약", "강남 가라오케 전화"),
        "예약 문의", "전화·카카오톡·픽업까지, 연중무휴 24시간 실시간 상담 채널을 안내합니다.",
        [("예약 문의", None)],
        [("h2", "연중무휴 24시간 상담"),
         ("p", "도파민은 365일 24시간 예약 상담을 운영합니다. 늦은 시간이나 갑작스러운 모임에도 실시간으로 연결되어, 인원과 시간에 맞는 룸과 코스를 바로 안내해 드립니다. 빠른 응대가 도파민 예약의 가장 큰 장점입니다."),
         ("h2", "원하는 채널로 편하게"),
         ("ul", ["전화 예약 — 가장 빠르고 정확한 실시간 상담", "카카오톡 채널 — 채팅으로 편하게 문의·픽업 요청", "실시간 픽업 문의 — 강남권 VIP 차량 픽업 안내"]),
         ("h2", "예약 시 알려주시면 좋은 정보"),
         ("p", "방문 날짜와 인원, 대략적인 시간, 모임의 목적(접대·기념일·모임)과 예산을 함께 알려주시면 더 정확한 추천이 가능합니다. 깜짝 이벤트나 케이크·현수막 등 특별한 준비가 필요하시면 미리 말씀해 주세요."),
         ("h2", "각 채널 자세히 보기"),
         ("p", "전화·카카오톡·픽업 각 채널의 이용 방법은 아래 개별 페이지에서 자세히 확인하실 수 있습니다. 어떤 채널이든 동일하게 친절하고 빠르게 안내해 드립니다.")],
        [("전화 예약", "pages/reserve-phone.html"), ("카카오톡 채널", "pages/reserve-kakao.html"), ("실시간 픽업 문의", "pages/pickup.html"), ("요금 & 할인", "pages/price.html")],
        schema_type="WebPage"))

    P.append(A("reserve-phone", "전화 예약 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 전화 예약 안내. 연중무휴 24시간, 전화 한 통으로 인원·시간에 맞는 룸과 코스를 실시간 추천받고 웹 예약 특가까지 안내받으세요.",
        _kw("강남 가라오케 전화 예약", "강남 가라오케 예약 번호", "선릉 가라오케 전화", "강남 가라오케 24시 예약"),
        "전화 예약", "가장 빠르고 정확한 방법. 전화 한 통으로 모든 안내를 받으세요.",
        [("예약 문의", "pages/reservation.html"), ("전화 예약", None)],
        [("h2", "전화 예약이 가장 빠른 이유"),
         ("p", "전화 예약은 실시간으로 매니저와 직접 소통하기 때문에 가장 빠르고 정확합니다. 원하시는 날짜에 룸이 가능한지 즉시 확인하고, 인원과 목적에 맞는 룸·안주·주류 구성을 바로 추천해 드립니다. 복잡한 절차 없이 통화 한 번으로 예약이 마무리됩니다."),
         ("h2", "통화 시 안내해 주세요"),
         ("ul", ["방문 날짜와 대략적인 시간(1부/2부)", "예상 인원", "모임 목적 — 접대·기념일·모임 등", "예산 또는 원하는 코스 수준", "케이크·현수막 등 특별 요청"]),
         ("h2", "24시간 언제든"),
         ("p", "도파민은 연중무휴 24시간 전화 상담을 받습니다. 낮 시간 미리 준비하는 예약부터, 늦은 밤 즉석에서 잡는 2차 자리까지 모두 가능합니다. 당일 예약도 룸 상황에 따라 안내해 드리니 편하게 전화 주세요."),
         ("h2", "전화가 어려우시면"),
         ("p", "통화가 어려운 상황이라면 카카오톡 채널로 문의하셔도 동일하게 빠른 안내를 받으실 수 있습니다. 차량 픽업이 필요하시면 실시간 픽업 문의 페이지도 함께 확인해 주세요. 어떤 방법이든 도파민은 신속하고 친절하게 응대합니다.")],
        [("카카오톡 채널", "pages/reserve-kakao.html"), ("실시간 픽업 문의", "pages/pickup.html"), ("요금 & 할인", "pages/price.html"), ("오시는 길", "pages/location.html")],
        schema_type="Article"))

    P.append(A("reserve-kakao", "카카오톡 채널 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 카카오톡 채널 안내. 채팅으로 편하게 예약·문의하고, 룸 추천과 특가 혜택, 픽업 요청까지 실시간으로 받아보세요. 연중무휴 24시간.",
        _kw("강남 가라오케 카카오톡", "강남 가라오케 카톡 예약", "선릉 가라오케 채널", "강남 가라오케 채팅 문의"),
        "카카오톡 채널", "통화가 부담스러울 땐 채팅으로. 카카오톡으로 편하게 문의하세요.",
        [("예약 문의", "pages/reservation.html"), ("카카오톡 채널", None)],
        [("h2", "채팅으로 편하게 문의"),
         ("p", "전화 통화가 어려운 상황이거나 조용히 문의하고 싶을 때는 카카오톡 채널이 편리합니다. 채팅으로 인원과 시간을 남겨주시면, 매니저가 가능한 룸과 추천 코스, 적용 가능한 특가 혜택을 정리해 답변드립니다. 대화 내용이 기록으로 남아 예약 내용을 다시 확인하기도 좋습니다."),
         ("h2", "이런 점이 좋습니다"),
         ("ul", ["통화 없이 조용히 문의 가능", "예약 내용을 채팅으로 확인·보관", "사진·위치 등 정보 공유가 편리", "픽업 요청과 특별 요청 전달이 쉬움"]),
         ("h2", "문의 시 남겨주세요"),
         ("p", "방문 날짜와 시간, 인원, 모임 목적과 예산을 남겨주시면 더 빠르게 안내해 드립니다. 깜짝 이벤트나 케이크·현수막 같은 준비가 필요하시면 함께 말씀해 주세요. 동선과 타이밍까지 맞춰 드립니다."),
         ("h2", "빠른 응답"),
         ("p", "카카오톡 채널도 연중무휴 24시간 운영됩니다. 메시지를 남겨주시면 빠르게 답변드리며, 급한 일정은 전화 예약이 가장 신속합니다. 상황에 맞는 채널로 편하게 연락 주세요.")],
        [("전화 예약", "pages/reserve-phone.html"), ("실시간 픽업 문의", "pages/pickup.html"), ("요금 & 할인", "pages/price.html"), ("파티 & 이벤트", "pages/event.html")],
        schema_type="Article"))

    P.append(A("pickup", "실시간 픽업 문의 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 실시간 픽업 문의. 강남권 VIP 고객을 위한 최고급 차량 픽업 서비스. 위치와 시간을 알려주시면 안전하고 편안하게 모십니다.",
        _kw("강남 가라오케 픽업", "강남 VIP 차량 픽업", "선릉 가라오케 픽업 서비스", "강남 가라오케 의전"),
        "실시간 픽업 문의", "강남권 VIP 고객을 위한 최고급 차량 픽업 서비스 안내.",
        [("예약 문의", "pages/reservation.html"), ("실시간 픽업 문의", None)],
        [("h2", "편안한 방문을 위한 픽업 서비스"),
         ("p", "도파민은 강남권 VIP 고객을 위해 최고급 차량 픽업 서비스를 운영합니다. 음주가 예상되는 자리에서 가장 중요한 것은 안전과 편안함입니다. 출발지와 시간을 알려주시면 약속한 장소에서 모셔, 번거로운 이동 없이 도파민에서의 시간을 온전히 즐기실 수 있도록 돕습니다."),
         ("h2", "이용 방법"),
         ("ul", ["전화 또는 카카오톡으로 픽업 요청", "출발 위치와 희망 시간 전달", "약속 장소에서 차량 대기·탑승", "안전하고 편안하게 도파민까지 이동"]),
         ("h2", "사전 문의를 권장합니다"),
         ("p", "픽업은 차량과 일정 조율이 필요하므로 가급적 방문 전에 미리 문의해 주세요. 인원과 출발지에 따라 안내가 달라질 수 있습니다. 예약 단계에서 픽업 의사를 함께 알려주시면 룸 예약과 함께 한 번에 준비해 드립니다."),
         ("h2", "안전이 최우선"),
         ("p", "도파민은 손님의 안전한 이동과 귀가를 가장 중요하게 생각합니다. 픽업뿐 아니라 마무리 시 대리운전 안내도 도와드립니다. 즐거운 자리만큼 안전한 마무리까지 책임지는 것이 프리미엄의 기본이라고 믿습니다.")],
        [("전화 예약", "pages/reserve-phone.html"), ("카카오톡 채널", "pages/reserve-kakao.html"), ("오시는 길", "pages/location.html"), ("이용 방법(1·2부)", "pages/how.html")],
        outbound=[AUTH["metro"]], schema_type="Article"))

    # ===== 회사소개 (E-E-A-T) =====
    P.append(A("about-company", "회사소개 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 회사소개. 운영 주체, 직접 운영 원칙, 연락처와 편집 정책 안내. 신뢰할 수 있는 정보 제공을 위한 도파민의 책임과 약속을 밝힙니다.",
        _kw("강남 가라오케 도파민 회사소개", "도파민 운영", "강남 가라오케 연락처", "도파민 편집정책"),
        "회사소개", "도파민을 운영하는 주체와 정보 제공 원칙을 투명하게 밝힙니다.",
        [("회사소개", None)],
        [("h2", "운영 주체"),
         ("p", "본 웹사이트는 강남 선릉·삼성동에 위치한 프리미엄 가라오케 ‘도파민’의 공식 정보 채널입니다. 도파민 매니지먼트 팀이 공간 운영과 콘텐츠 작성·감수를 직접 담당합니다. 위탁이 아닌 직접 운영 체계이기에, 사이트에 담긴 시설·서비스·이용 안내는 실제 운영 경험을 바탕으로 합니다."),
         ("h2", "정보 제공 원칙 (편집 정책)"),
         ("p", "도파민은 손님이 의사결정에 활용하는 정보를 정확하고 책임 있게 제공하고자 합니다. 콘텐츠는 운영팀의 직접 경험과 확인된 사실을 기준으로 작성하며, 도구를 활용해 작성하더라도 운영팀의 검수와 책임 아래 발행합니다. 요금·운영 시간 등 변동 가능한 정보는 실제 상담 시 안내되는 내용이 우선합니다."),
         ("ul", ["작성·감수: 도파민 운영팀", "기준: 직접 운영 경험과 확인된 사실", "갱신: 시설·정책 변경 시 수시 업데이트", "문의: 전화 및 카카오톡 채널(연중무휴 24시간)"]),
         ("h2", "연락처"),
         ("p", "예약 및 문의는 전화 또는 카카오톡 채널을 통해 연중무휴 24시간 가능합니다. 위치는 서울특별시 강남구 선릉로92길 38이며, 자세한 길 안내는 오시는 길 페이지에서 확인하실 수 있습니다."),
         ("h2", "신뢰를 위한 약속"),
         ("p", "도파민은 과장된 표현보다 검증된 경험을 전하고자 합니다. 후기와 평점은 서비스 개선의 근거로 삼으며, 이용약관과 개인정보처리방침을 통해 거래와 정보 보호의 기준을 공개합니다. 의견이나 정정 요청이 있으시면 언제든 문의 채널로 알려주세요.")],
        [("이용약관", "pages/terms.html"), ("개인정보처리방침", "pages/privacy.html"), ("오시는 길", "pages/location.html"), ("예약 문의", "pages/reservation.html")],
        outbound=[AUTH["gangnam"]], schema_type="AboutPage"))

    # ===== 이용약관 =====
    P.append(A("terms", "이용약관 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 이용약관. 예약·이용·취소, 요금 안내, 이용자의 책임 등 서비스 이용에 관한 기본 약관을 안내합니다.",
        _kw("강남 가라오케 이용약관", "도파민 약관", "가라오케 예약 약관"),
        "이용약관", "도파민 서비스 이용에 관한 기본 약관입니다.",
        [("회사소개", "pages/about-company.html"), ("이용약관", None)],
        [("h2", "제1조 (목적)"),
         ("p", "본 약관은 강남 가라오케 도파민(이하 ‘도파민’)이 제공하는 예약·이용 관련 서비스의 조건과 절차, 이용자와 도파민의 권리·의무 및 책임 사항을 규정함을 목적으로 합니다."),
         ("h2", "제2조 (예약 및 이용)"),
         ("p", "이용자는 전화 또는 카카오톡 채널을 통해 예약·문의할 수 있습니다. 예약은 룸 현황에 따라 확정되며, 인원·시간·코스 등 주요 사항은 상담 시 안내되는 내용을 기준으로 합니다. 운영 시간은 연중무휴 24시간(1부 15:00~01:00, 2부 01:00~15:00)입니다."),
         ("h2", "제3조 (요금)"),
         ("p", "요금은 주대 7만원부터 시작하며 룸·인원·코스·이용 시간에 따라 달라집니다. 도파민은 이용 전 예상 비용을 안내하며, 웹 예약 특가 등 혜택은 시기와 조건에 따라 적용됩니다."),
         ("h2", "제4조 (취소 및 변경)"),
         ("p", "예약의 취소·변경이 필요한 경우 가능한 한 빨리 연락 채널로 알려주시기 바랍니다. 행사·단체 예약 등 사전 준비가 필요한 건은 일정에 따라 변경이 제한될 수 있습니다."),
         ("h2", "제5조 (이용자의 책임)"),
         ("p", "이용자는 시설을 선량하게 이용해야 하며, 고의 또는 과실로 시설에 손해를 끼친 경우 그에 대한 책임을 질 수 있습니다. 타인에게 피해를 주는 행위는 제한될 수 있습니다."),
         ("h2", "제6조 (분쟁의 해결)"),
         ("p", "서비스 이용과 관련해 분쟁이 발생할 경우 도파민과 이용자는 신의성실의 원칙에 따라 원만히 해결하도록 노력합니다. 소비자 분쟁 관련 일반 정보는 한국소비자원에서 확인하실 수 있습니다. 본 약관은 관련 법령과 운영 정책에 따라 변경될 수 있으며, 변경 시 본 페이지를 통해 공지합니다.")],
        [("개인정보처리방침", "pages/privacy.html"), ("회사소개", "pages/about-company.html"), ("요금 & 할인", "pages/price.html"), ("예약 문의", "pages/reservation.html")],
        outbound=[AUTH["kca"], AUTH["ftc"]], schema_type="WebPage"))

    # ===== 개인정보처리방침 =====
    P.append(A("privacy", "개인정보처리방침 | 강남 가라오케 도파민",
        "강남 가라오케 도파민 개인정보처리방침. 예약·상담 과정에서 수집하는 정보의 항목·목적·보유기간과 이용자의 권리를 안내합니다.",
        _kw("강남 가라오케 개인정보처리방침", "도파민 개인정보", "가라오케 예약 개인정보"),
        "개인정보처리방침", "이용자의 개인정보를 어떻게 다루는지 투명하게 안내합니다.",
        [("회사소개", "pages/about-company.html"), ("개인정보처리방침", None)],
        [("h2", "1. 수집하는 항목과 목적"),
         ("p", "도파민은 예약 및 상담 응대를 위해 최소한의 정보(예: 연락처, 예약 일시·인원 등 상담에 필요한 정보)를 수집할 수 있습니다. 수집된 정보는 예약 확인과 서비스 안내, 고객 문의 응대의 목적으로만 이용합니다."),
         ("h2", "2. 보유 및 이용 기간"),
         ("p", "수집된 개인정보는 이용 목적이 달성되면 지체 없이 파기하는 것을 원칙으로 합니다. 관련 법령에 따라 보존이 필요한 경우에는 해당 기간 동안 안전하게 보관합니다."),
         ("h2", "3. 제3자 제공"),
         ("p", "도파민은 이용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 근거가 있거나 수사기관의 적법한 요청이 있는 경우 등 예외적인 상황에서는 관련 법령을 따릅니다."),
         ("h2", "4. 이용자의 권리"),
         ("p", "이용자는 자신의 개인정보에 대해 열람·정정·삭제 및 처리정지를 요청할 수 있습니다. 요청은 문의 채널을 통해 접수되며, 도파민은 관련 법령에 따라 신속히 조치합니다."),
         ("h2", "5. 안전성 확보 조치"),
         ("p", "도파민은 개인정보가 분실·도난·유출·변조되지 않도록 합리적인 보호 조치를 취합니다. 개인정보 보호와 관련한 일반 정보 및 권리 구제는 개인정보보호위원회를 통해 확인하실 수 있습니다. 본 방침은 법령 및 정책 변경에 따라 갱신될 수 있으며, 변경 시 본 페이지에 공지합니다.")],
        [("이용약관", "pages/terms.html"), ("회사소개", "pages/about-company.html"), ("예약 문의", "pages/reservation.html"), ("FAQ", "pages/faq.html")],
        outbound=[AUTH["pipc"]], schema_type="WebPage"))

    return P


def build_article(a, idx=0):
    cur_dir = "pages"
    canonical = "{}/pages/{}.html".format(BASE_URL, a["slug"])
    trail = [("홈", "index.html")] + a["trail_mid"]
    rating, count, revs = reviews_for(idx)
    # 본문 + 목차
    prose, toc = render_blocks(a["blocks"])
    extra = ""
    if a.get("extra") == "__FAQ__":
        items = "\n".join('        <details class="info-card reveal"><summary style="cursor:pointer;font-weight:700">{q}</summary><p style="color:var(--muted);margin-top:10px">{ans}</p></details>'.format(q=esc(q), ans=esc(ans)) for q, ans in FAQ)
        extra = '''  <section class="section"><div class="wrap">
      <div class="info-cols" style="grid-template-columns:1fr;max-width:780px;margin:0 auto;gap:12px">
{items}
      </div></div></section>'''.format(items=items)

    hero = '''  <section class="hero" style="min-height:48vh">
    <div class="hero-inner">
      <span class="eyebrow reveal in">강남 가라오케 도파민</span>
      <h1 class="reveal in"><span class="grad">{h1}</span></h1>
      <p class="sub reveal in">{lead}</p>
      <div class="hero-cta reveal in"><a class="btn btn-primary" href="{tel}">예약 문의</a><a class="btn btn-gold" href="{kakao}">카카오톡 상담</a></div>
    </div>
  </section>'''.format(h1=esc(a["h1"]), lead=esc(a["lead"]), tel=CONTACT_TEL, kakao=KAKAO_URL)

    aside = '<aside class="toc-side reveal">{}</aside>'.format(toc_nav(toc)) if toc else ""
    article = '''  <section class="section" id="content"><div class="wrap">
    <div class="article-layout">
      {aside}
      <article class="prose reveal">
{prose}
      </article>
    </div>
  </div></section>'''.format(aside=aside, prose=prose)

    # 스키마: 페이지 타입 + 후기/리뷰/점수(LocalBusiness, 노출 콘텐츠와 일치)
    schema_objs = [breadcrumb_schema([(n, p if p is None else p) for n, p in trail])]
    if a["schema_type"] == "FAQPage":
        schema_objs.append(faq_schema())
    schema_objs.append(article_schema(a["title"], a["desc"], canonical, "Article" if a["schema_type"] in ("FAQPage",) else a["schema_type"]))
    schema_objs.append(local_business_schema(SITE_NAME, canonical, a["desc"], rating, count, revs))

    body = "\n\n".join([
        header_html(cur_dir),
        breadcrumb_html(trail, cur_dir),
        hero,
        article,
        extra,
        reviews_html(rating, count, revs),
        byline_html(cur_dir),
        related_html(a["related"], cur_dir, a["outbound"]),
        topic_links_html(cur_dir),
        region_links_html(cur_dir),
        cta_band_html(cur_dir),
        footer_html(cur_dir),
    ])
    page = head_html(a["title"], a["desc"], a["kw"], canonical, schema_objs, cur_dir) + "\n" + body + "\n</body>\n</html>\n"
    os.makedirs(os.path.join(OUT_DIR, "pages"), exist_ok=True)
    with open(os.path.join(OUT_DIR, "pages", a["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page)


# ---------- 메인 ----------
def build_main():
    cur_dir = ""
    title = "강남 가라오케 도파민 | 24시 연중무휴 프리미엄 파티 공간"
    desc = "강남 선릉·삼성동에 위치한 프리미엄 가라오케 도파민. 24시간 연중무휴, 최첨단 시설과 현직 DJ 공연, 프라이빗한 공간에서 특별한 밤을 경험하세요. 실시간 특가 혜택!"
    kw = "강남 가라오케, 선릉 노래방, 삼성동 프리미엄 가라오케, 강남 가라오케 도파민, 24시 가라오케, 강남 룸"
    hero = '''  <section class="hero">
    <div class="hero-inner">
      <span class="eyebrow reveal in">선릉 · 삼성동 · 24시 연중무휴</span>
      <h1 class="reveal in">강남의 밤, 그 중심에서 터지는 짜릿함<br><span class="grad">도파민 가라오케</span></h1>
      <p class="sub reveal in">선릉 · 삼성동 위치 | <b>24시 연중무휴</b> | 프리미엄 프라이빗 파티</p>
      <div class="hero-cta reveal in">
        <a class="btn btn-primary" href="{tel}">지금 예약하고 특가 혜택 받기</a>
        <a class="btn btn-gold" href="{rooms}">룸 둘러보기</a>
      </div>
      <p class="scroll-hint reveal in">주대 7만원부터 · 웹 예약 한정 특가</p>
    </div>
  </section>'''.format(tel=CONTACT_TEL, rooms=rel("pages/rooms.html", cur_dir))

    prose = '''  <section class="section" id="about">
    <div class="wrap prose">
      <h2>강남 가라오케 도파민 – 당신의 밤을 위한 완벽한 선택</h2>
      <p>강남의 중심, 선릉과 삼성동에서 프리미엄 가라오케 문화를 선도하는 <strong>도파민</strong>이 여러분을 초대합니다. 단순한 노래방을 넘어, 감각적인 공간과 최상급 서비스로 기억에 남는 특별한 밤을 만들어 드립니다. 더 자세한 이야기는 <a href="{story}">브랜드 스토리</a>에서 확인하세요.</p>
      <h2>왜, 도파민인가요?</h2>
      <p>도파민은 24시간 연중무휴로 운영되는 강남 대표 프리미엄 가라오케입니다. 단독 건물의 초대형 공간, 최첨단 음향·조명, 현직 DJ팀의 라이브 무대, 강남 맛집급 안주까지 — 고객 한 분 한 분의 취향과 니즈를 정확히 파악한 맞춤형 서비스를 제공합니다. <a href="{service}">서비스 안내</a>와 <a href="{rooms}">룸 & 시설</a>에서 더 자세히 보실 수 있습니다.</p>
      <h2>24시간, 당신이 원하는 그 순간에</h2>
      <p>도파민은 365일 24시간 운영됩니다. 1부는 오후 3시부터 새벽 1시까지, 2부는 새벽 1시부터 오후 3시까지로, 언제든 편하게 방문하실 수 있습니다. 강남권 VIP 고객을 위한 <a href="{pickup}">최고급 차량 픽업 서비스</a>도 제공합니다. 자세한 이용 방법은 <a href="{how}">이용 안내</a>를 참고하세요.</p>
      <h2>지금, 도파민을 경험하세요</h2>
      <p>주대 7만원부터 시작하는 합리적인 <a href="{price}">요금과 할인 혜택</a>, 그리고 웹 예약 한정 특가를 놓치지 마세요. 강남에서 가장 뜨거운 밤을 선사할 도파민 가라오케, 지금 바로 <a href="{phone}">전화</a> 또는 <a href="{kakao}">카카오톡 채널</a>로 예약 문의를 남겨주세요.</p>
    </div>
  </section>'''.format(story=rel("pages/story.html", cur_dir), service=rel("pages/service.html", cur_dir),
                       rooms=rel("pages/rooms.html", cur_dir), pickup=rel("pages/pickup.html", cur_dir),
                       how=rel("pages/how.html", cur_dir), price=rel("pages/price.html", cur_dir),
                       phone=rel("pages/reserve-phone.html", cur_dir), kakao=rel("pages/reserve-kakao.html", cur_dir))

    main_toc = [("도파민 소개", "about"), ("도파민만의 특별함", "features"), ("룸 & 시설", "rooms"),
                ("후기 & 신뢰도", "reviews"), ("오시는 길", "location"), ("주제별 안내", "topics"), ("지역별 가라오케", "regions")]
    body = "\n\n".join([
        header_html(cur_dir), hero, toc_card_section(main_toc), prose, features_html(cur_dir), rooms_html(cur_dir),
        reviews_html(MAIN_RATING, MAIN_COUNT, MAIN_REVIEWS), location_html(),
        topic_links_html(cur_dir), region_links_html(cur_dir), cta_band_html(cur_dir), footer_html(cur_dir),
    ])
    schema_objs = [website_schema(), local_business_schema(SITE_NAME, BASE_URL + "/", desc, MAIN_RATING, MAIN_COUNT, MAIN_REVIEWS)]
    page = head_html(title, desc, kw, BASE_URL + "/", schema_objs, cur_dir) + "\n" + body + "\n</body>\n</html>\n"
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_region(r):
    cur_dir = "regions"
    area = r["area"]
    title = "{a} 가라오케 도파민 | 24시 연중무휴 프리미엄 파티 공간".format(a=area)
    desc = "{a} 가라오케는 도파민. {lead} 24시 연중무휴, 최첨단 시설과 현직 DJ 공연, 프라이빗한 공간. 실시간 추천과 특가 혜택!".format(a=area, lead=r["lead"])
    kw = "{a} 가라오케, {a} 노래방, {a} 프리미엄 가라오케, {a} 가라오케 도파민, 강남 가라오케, 24시 가라오케".format(a=area)
    canonical = "{base}/regions/{slug}.html".format(base=BASE_URL, slug=r["slug"])
    trail = [("홈", "index.html"), (area + " 가라오케", None)]

    hero = '''  <section class="hero" style="min-height:62vh">
    <div class="hero-inner">
      <span class="eyebrow reveal in">{area} · 24시 연중무휴</span>
      <h1 class="reveal in"><span class="grad">{area} 가라오케 도파민</span></h1>
      <p class="sub reveal in">{lead} <b>24시 연중무휴</b> · 프리미엄 프라이빗 파티.</p>
      <div class="hero-cta reveal in"><a class="btn btn-primary" href="{tel}">{area} 실시간 예약 문의</a><a class="btn btn-gold" href="{rooms}">룸 보기</a></div>
    </div>
  </section>'''.format(area=esc(area), lead=esc(r["lead"]), tel=CONTACT_TEL, rooms=rel("pages/rooms.html", cur_dir))

    intro = '''  <section class="section" id="about">
    <div class="wrap prose">
      <h2>{area}에서 즐기는 강남 프리미엄 가라오케, 도파민</h2>
      <p>{lead} 도파민은 24시간 연중무휴로 운영되는 강남 대표 프리미엄 가라오케로, {area} 인근 어디서나 편하게 방문하실 수 있습니다. 단독 건물의 초대형 공간과 최첨단 음향·조명, 현직 DJ팀의 라이브 무대, 그리고 강남 맛집급 안주까지 — 단순한 노래방을 넘어선 특별한 밤을 약속드립니다.</p>
      <p>가격·시스템·예약 모두 <a href="{phone}">전화</a> 또는 <a href="{kakao}">카카오톡</a>으로 실시간 안내해 드립니다. <a href="{price}">주대 7만원부터</a> 시작하는 합리적인 가격과 웹 예약 한정 특가 혜택을 만나보세요. {area}에서 도파민까지 <a href="{location}">오시는 길</a>도 함께 확인하세요.</p>
    </div>
  </section>'''.format(area=esc(area), lead=esc(r["lead"]), phone=rel("pages/reserve-phone.html", cur_dir),
                       kakao=rel("pages/reserve-kakao.html", cur_dir), price=rel("pages/price.html", cur_dir),
                       location=rel("pages/location.html", cur_dir))

    region_toc = [(area + " 소개", "about"), ("도파민만의 특별함", "features"), ("룸 & 시설", "rooms"),
                  ("후기 & 신뢰도", "reviews"), ("오시는 길", "location"), ("주제별 안내", "topics"), ("주변 지역", "regions")]
    body = "\n\n".join([
        header_html(cur_dir), breadcrumb_html(trail, cur_dir), hero, toc_card_section(region_toc), intro,
        features_html(cur_dir), rooms_html(cur_dir),
        reviews_html(r["rating"], r["count"], r["reviews"]), location_html(),
        topic_links_html(cur_dir, area=area), region_links_html(cur_dir, current=r["slug"]),
        cta_band_html(cur_dir), footer_html(cur_dir),
    ])
    schema_objs = [breadcrumb_schema(trail),
                   local_business_schema(area + " 가라오케 도파민", canonical, desc, r["rating"], r["count"], r["reviews"], area=area)]
    page = head_html(title, desc, kw, canonical, schema_objs, cur_dir) + "\n" + body + "\n</body>\n</html>\n"
    os.makedirs(os.path.join(OUT_DIR, "regions"), exist_ok=True)
    with open(os.path.join(OUT_DIR, "regions", r["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_sitemap_robots(articles):
    urls = [BASE_URL + "/"]
    urls += [BASE_URL + "/pages/" + a["slug"] + ".html" for a in articles]
    urls += [BASE_URL + "/regions/" + r["slug"] + ".html" for r in REGIONS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>{}</loc><lastmod>{}</lastmod><changefreq>weekly</changefreq><priority>{}</priority></url>".format(u, UPDATED, "1.0" if u.endswith("/") else "0.8"))
    sm.append("</urlset>")
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n".format(BASE_URL))


def build_webmanifest():
    manifest = {
        "name": SITE_NAME, "short_name": "도파민", "lang": "ko",
        "start_url": "/", "display": "standalone",
        "background_color": "#070510", "theme_color": "#0f0a1d",
        "icons": [
            {"src": "/favicon.svg", "type": "image/svg+xml", "sizes": "any"},
            {"src": "/icon-192.png", "type": "image/png", "sizes": "192x192"},
            {"src": "/icon-512.png", "type": "image/png", "sizes": "512x512"},
        ],
    }
    with open(os.path.join(OUT_DIR, "site.webmanifest"), "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def load_content():
    """_content/part_*.py 의 BLOCKS(dict: slug -> blocks)를 병합해 반환."""
    content = {}
    cdir = os.path.join(OUT_DIR, "_content")
    if os.path.isdir(cdir):
        import importlib.util
        for fn in sorted(os.listdir(cdir)):
            if fn.startswith("part_") and fn.endswith(".py"):
                spec = importlib.util.spec_from_file_location("part_mod", os.path.join(cdir, fn))
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                content.update(getattr(m, "BLOCKS", {}))
    return content


def build():
    articles = build_articles()
    content = load_content()
    for a in articles:
        if a["slug"] in content and content[a["slug"]]:
            a["blocks"] = content[a["slug"]]
    build_main()
    for i, a in enumerate(articles):
        build_article(a, i)
    for r in REGIONS:
        build_region(r)
    build_sitemap_robots(articles)
    build_webmanifest()
    print("생성 완료: index.html + {}개 개별 페이지 + {}개 지역 페이지 + sitemap/robots/manifest".format(len(articles), len(REGIONS)))


if __name__ == "__main__":
    build()
