#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
강남 가라오케 도파민 정적 사이트 생성기 (전면 리디자인).

- 드롭다운 상단 메뉴 + 모바일 햄버거
- 메인 페이지: 히어로 / 핵심가치 / 룸투어 / 요금·예약폼 / 후기 / 본문(SEO) / 오시는 길
- 모든 페이지 스키마: WebSite / LocalBusiness / AggregateRating / Review / BreadcrumbList / FAQPage
- 지역(롱테일) 페이지 + 메인↔지역 내부링크
- 모바일 퍼스트 반응형 (assets/style.css, assets/app.js)
"""
import html
import json
import os
import urllib.parse

SITE_NAME = "강남 가라오케 도파민"
BASE_URL = "https://www.dopamine-karaoke.com"
ADDRESS = "서울특별시 강남구 선릉로92길 38"
CONTACT_TEL = "tel:"          # TODO: 실제 전화번호로 교체 (예: tel:010-1234-5678)
KAKAO_URL = "#"               # TODO: 카카오톡 채널 링크로 교체
MAP_SRC = "https://www.google.com/maps?q=" + urllib.parse.quote(ADDRESS) + "&hl=ko&z=16&output=embed"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- 드롭다운 메뉴 구성 ----
# 항목: (라벨, [(서브라벨, 종류, 값)]) / 종류: anchor | tel | kakao
MENU = [
    ("도파민 소개", [("브랜드 스토리", "anchor", "about"), ("오시는 길", "anchor", "location")]),
    ("룸 & 시설", [("L 룸 (최대 20인)", "anchor", "room-l"), ("M 룸 (최대 14인)", "anchor", "room-m"), ("S 룸 (최대 8인)", "anchor", "room-s")]),
    ("서비스 안내", [("프리미엄 서비스", "anchor", "service"), ("주류 & 안주 메뉴", "anchor", "menu"), ("파티 & 이벤트", "anchor", "event")]),
    ("이용 안내", [("이용 방법 (1·2부)", "anchor", "guide"), ("요금 & 할인", "anchor", "price"), ("FAQ", "anchor", "faq")]),
    ("예약 문의", [("전화 예약", "tel", ""), ("카카오톡 채널", "kakao", ""), ("실시간 픽업 문의", "anchor", "reservation")]),
]

# ---- 핵심 가치 ----
FEATURES = [
    ("🏛️", "압도적인 공간 & 최첨단 시설", "단독 건물 전체, 하이테크 음향·조명 시스템과 룸별 개별 공조로 완벽한 무대를 연출합니다."),
    ("⏰", "24시간 멈추지 않는 에너지", "1부 15:00~01:00, 2부 01:00~15:00. 365일 연중무휴, 원하는 순간 언제든."),
    ("🎧", "현직 DJ팀 라이브 퍼포먼스", "화려한 경력의 전문 DJ팀이 상주하여 지루할 틈 없는 라이브 무대를 책임집니다."),
    ("🔒", "완벽한 프라이버시 보장", "철저한 보안과 신분 보호 시스템으로 사적인 자리와 비즈니스를 완벽히 지켜드립니다."),
    ("🍽️", "강남 맛집급 안주 & 식사", "전문 셰프가 준비한 고퀄리티 안주와 다양한 주류로 술자리의 격을 높입니다."),
]

# ---- 룸 ----
ROOMS = [
    ("room-l", "l", "L", "L 룸", "최대 20인", "해외 귀빈 접대, 대규모 회식, VIP 파티에 최적화된 최고급 룸."),
    ("room-m", "m", "M", "M 룸", "최대 14인", "중요한 고객 접대나 가까운 지인들과의 오붓한 생일 파티에 제격."),
    ("room-s", "s", "S", "S 룸", "최대 8인", "소규모 모임이나 편안한 술자리를 위한 아늑하고 세련된 공간."),
]

# ---- 주류 & 안주 ----
MENU_DRINK = [("위스키 / 양주", "프리미엄 라인업"), ("와인 / 샴페인", "소믈리에 추천"), ("맥주 / 칵테일", "다양한 구성")]
MENU_FOOD = [("셰프 스페셜 안주", "시그니처"), ("모둠 과일 & 마른안주", "기본 제공"), ("식사 메뉴", "야식 가능")]

# ---- FAQ ----
FAQ = [
    ("예약은 어떻게 하나요?", "전화 또는 카카오톡 채널로 연중무휴 24시간 상담 가능합니다. 인원과 방문 시간을 알려주시면 실시간으로 최적의 룸을 추천해 드립니다."),
    ("요금은 어떻게 되나요?", "주대 7만원부터 시작하며, 웹사이트 예약 시 다양한 특가 혜택을 제공합니다. 자세한 요금은 문의 시 실시간 안내해 드립니다."),
    ("픽업 서비스가 있나요?", "강남권 VIP 고객을 위한 최고급 차량 픽업 서비스를 운영합니다. 방문 전에 미리 문의해 주세요."),
    ("몇 명까지 이용 가능한가요?", "S 룸 최대 8인, M 룸 최대 14인, L 룸 최대 20인까지 이용 가능합니다. 규모에 맞는 룸을 안내해 드립니다."),
    ("영업 시간이 어떻게 되나요?", "365일 연중무휴 24시간 운영합니다. 1부 15:00~01:00, 2부 01:00~15:00로 언제든 편하게 방문하실 수 있습니다."),
]

# ---- 지역(롱테일) ----
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


def esc(s):
    return html.escape(str(s), quote=True)


def stars(n):
    n = int(round(n))
    return "★" * n + "☆" * (5 - n)


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
        "image": BASE_URL + "/og-image.jpg", "url": url, "description": desc,
        "telephone": "", "priceRange": "₩₩₩",
        "address": {"@type": "PostalAddress", "streetAddress": "선릉로92길 38",
                    "addressLocality": "강남구", "addressRegion": "서울", "addressCountry": "KR"},
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                      "opens": "00:00", "closes": "23:59"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating, "reviewCount": count, "bestRating": 5, "worstRating": 1},
        "review": review_schema(reviews),
        "areaServed": [area] if area else ["강남", "선릉", "삼성동"],
    }


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"}


def faq_schema():
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


def breadcrumb_schema(area):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": BASE_URL + "/"},
                                {"@type": "ListItem", "position": 2, "name": area + " 가라오케", "item": BASE_URL + "/regions/"}]}


# ---------- 공통 컴포넌트 ----------
def href_for(kind, val, depth):
    home = "index.html" if depth == 0 else "../index.html"
    if kind == "anchor":
        return home + "#" + val
    if kind == "tel":
        return CONTACT_TEL
    if kind == "kakao":
        return KAKAO_URL
    return "#"


def header_html(depth):
    home = "index.html" if depth == 0 else "../index.html"
    items = []
    for label, subs in MENU:
        sub_html = "\n".join(
            '          <li><a href="{}">{}</a></li>'.format(href_for(k, v, depth), esc(t)) for t, k, v in subs
        )
        items.append(
            '''      <li>
        <button class="menu-toggle" aria-haspopup="true" aria-expanded="false">{label}<span class="caret"></span></button>
        <ul class="dropdown">
{subs}
        </ul>
      </li>'''.format(label=esc(label), subs=sub_html)
        )
    nav_items = "\n".join(items)
    return '''  <header class="site-header">
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
  <div class="nav-backdrop"></div>'''.format(home=home, nav=nav_items, kakao=KAKAO_URL, tel=CONTACT_TEL)


def features_html():
    cards = "\n".join(
        '''        <div class="feature reveal"><div class="ic">{ic}</div><h3>{t}</h3><p>{d}</p></div>'''.format(ic=ic, t=esc(t), d=esc(d))
        for ic, t, d in FEATURES
    )
    return '''  <section class="section alt" id="features">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">WHY DOPAMINE</span><h2>도파민만의 특별함</h2>
        <p>단순한 노래방이 아닌, 강남 프리미엄 파티 공간의 기준.</p></div>
      <div class="features">
{cards}
      </div>
    </div>
  </section>'''.format(cards=cards)


def rooms_html():
    cards = []
    for rid, cls, cap, name, pers, desc in ROOMS:
        cards.append(
            '''        <article class="room reveal" id="{rid}">
          <div class="thumb {cls}"><span class="cap">{cap}</span><span class="pers">{pers}</span></div>
          <div class="body"><h3>{name}</h3><p>{desc}</p>
            <a class="btn btn-ghost btn-sm" href="#reservation">이 룸으로 예약 문의</a></div>
        </article>'''.format(rid=rid, cls=cls, cap=cap, pers=esc(pers), name=esc(name), desc=esc(desc))
        )
    return '''  <section class="section" id="rooms">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">ROOM TOUR</span><h2>룸 & 시설</h2>
        <p>파티의 규모와 성격에 맞춰 완벽한 공간을 제공합니다. 전 룸 완벽 방음.</p></div>
      <div class="rooms">
{cards}
      </div>
    </div>
  </section>'''.format(cards="\n".join(cards))


def service_html():
    drink = "\n".join('            <li>{}<span class="price">{}</span></li>'.format(esc(a), esc(b)) for a, b in MENU_DRINK)
    food = "\n".join('            <li>{}<span class="price">{}</span></li>'.format(esc(a), esc(b)) for a, b in MENU_FOOD)
    return '''  <section class="section alt" id="service">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">SERVICE</span><h2>서비스 안내</h2>
        <p>도파민만의 차별화된 프리미엄 서비스와 고품격 메뉴를 만나보세요.</p></div>
      <div class="info-cols">
        <div class="info-card reveal"><h3>✨ 프리미엄 서비스</h3>
          <ul><li>전문 매니저의 1:1 맞춤 응대</li><li>철저한 프라이버시 & 신분 보호</li><li>실시간 룸·서비스 추천</li></ul></div>
        <div class="info-card reveal" id="menu"><h3>🥂 주류 & 안주 메뉴</h3>
          <ul>
{drink}
{food}
          </ul></div>
        <div class="info-card reveal" id="event"><h3>🎉 파티 & 이벤트</h3>
          <ul><li>생일·기념일 파티 세팅</li><li>기업 단체·접대 패키지</li><li>현직 DJ팀 라이브 무대</li></ul></div>
      </div>
    </div>
  </section>'''.format(drink=drink, food=food)


def price_reserve_html():
    return '''  <section class="section" id="price">
    <div class="wrap">
      <div class="price-banner reveal">
        <h3>웹사이트 예약 한정 · 주대 <span class="big gold">7만원</span> 특가!</h3>
        <p>예약 문의 시 실시간 추천과 추가 특가 혜택까지 제공해 드립니다.</p>
        <a class="btn" href="#reservation">지금 특가로 예약하기</a>
      </div>
    </div>
  </section>

  <section class="section alt" id="reservation">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">RESERVATION</span><h2>실시간 예약 & 문의</h2>
        <p>연중무휴 24시간 상담 가능. 간편하게 남겨주시면 바로 연락드립니다.</p></div>
      <div class="reserve-grid">
        <form class="reserve-form reveal" id="reserve-form" novalidate>
          <div class="field"><label for="r-name">이름</label><input id="r-name" name="name" type="text" placeholder="성함을 입력해 주세요" required></div>
          <div class="field"><label for="r-phone">연락처</label><input id="r-phone" name="phone" type="tel" placeholder="010-0000-0000" required></div>
          <div class="field"><label for="r-people">인원</label>
            <select id="r-people" name="people"><option>1~4인</option><option>5~8인</option><option>9~14인</option><option>15~20인</option></select></div>
          <div class="field"><label for="r-time">방문 시간</label>
            <select id="r-time" name="time"><option>1부 (15:00~01:00)</option><option>2부 (01:00~15:00)</option></select></div>
          <button class="btn btn-primary" type="submit">예약 문의 보내기</button>
          <p class="form-note">제출 후 전화 또는 카카오톡으로 연결하시면 즉시 안내해 드립니다.</p>
          <div class="form-result" role="status" aria-live="polite"></div>
        </form>
        <div class="reserve-side">
          <div class="contact-card reveal"><h4>📞 전화 예약</h4><p>연중무휴 24시간 상담</p>
            <a class="btn btn-primary" href="{tel}">전화로 예약하기</a></div>
          <div class="contact-card reveal"><h4>💬 카카오톡 채널</h4><p>실시간 채팅 상담·픽업 문의</p>
            <a class="btn btn-kakao" href="{kakao}">카카오톡 상담</a></div>
        </div>
      </div>
    </div>
  </section>'''.format(tel=CONTACT_TEL, kakao=KAKAO_URL)


def reviews_html(rating, count, reviews):
    cards = "\n".join(
        '''        <div class="review reveal"><div class="who"><strong>{w}</strong><span class="stars">{s}</span></div><p>{b}</p></div>'''.format(
            w=esc(w), s=stars(r), b=esc(b)) for w, r, b in reviews
    )
    return '''  <section class="section" id="reviews">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">REVIEWS</span><h2>후기 & 신뢰도</h2>
        <p>연예인·BJ·기업인이 선택한 강남 1등 프리미엄 가라오케.</p></div>
      <div class="rating-summary reveal">
        <span class="rating-score">{rating}</span><span class="stars">{rstars}</span>
        <span style="color:var(--muted)">리뷰 {count}개 기준</span>
      </div>
      <div class="reviews">
{cards}
      </div>
    </div>
  </section>'''.format(rating=rating, rstars=stars(rating), count=count, cards=cards)


def faq_html():
    items = "\n".join(
        '''        <details class="info-card reveal"><summary style="cursor:pointer;font-weight:700">{q}</summary><p style="color:var(--muted);margin-top:10px">{a}</p></details>'''.format(
            q=esc(q), a=esc(a)) for q, a in FAQ
    )
    return '''  <section class="section alt" id="faq">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">FAQ</span><h2>자주 묻는 질문</h2></div>
      <div class="info-cols" style="grid-template-columns:1fr;max-width:760px;margin:0 auto;gap:12px">
{items}
      </div>
    </div>
  </section>'''.format(items=items)


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
          <dt>예약·문의</dt><dd><a href="{tel}" style="color:var(--accent)">전화 예약</a> · <a href="{kakao}" style="color:var(--accent)">카카오톡 채널</a></dd>
          <dt>특별 서비스</dt><dd>강남권 VIP 최고급 차량 픽업 (사전 문의)</dd>
        </dl>
      </div>
    </div>
  </section>'''.format(map=MAP_SRC, addr=esc(ADDRESS), tel=CONTACT_TEL, kakao=KAKAO_URL)


def region_links_html(depth, current=None):
    prefix = "regions/" if depth == 0 else ""
    out = []
    for r in REGIONS:
        if r["slug"] == current:
            continue
        out.append('        <a href="{p}{slug}.html">{area} 가라오케 도파민</a>'.format(p=prefix, slug=r["slug"], area=esc(r["area"])))
    return '''  <section class="section alt" id="regions">
    <div class="wrap">
      <div class="section-head reveal"><span class="tag">AREA</span><h2>강남 지역별 가라오케</h2>
        <p>가까운 지역의 도파민 정보도 확인해 보세요.</p></div>
      <div class="linklist reveal">
{links}
      </div>
    </div>
  </section>'''.format(links="\n".join(out))


def footer_html(depth):
    home = "index.html" if depth == 0 else "../index.html"
    rprefix = "regions/" if depth == 0 else ""
    region_links = "\n".join(
        '        <a href="{p}{slug}.html">{area} 가라오케</a>'.format(p=rprefix, slug=r["slug"], area=esc(r["area"])) for r in REGIONS[:5]
    )
    return '''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-col">
          <h5>강남 가라오케 도파민</h5>
          <p>강남 선릉·삼성동에 위치한 24시 연중무휴 프리미엄 가라오케.</p>
          <p>{addr}</p>
          <p>365일 24시간 · 1부/2부 운영</p>
        </div>
        <div class="footer-col">
          <h5>바로가기</h5>
          <a href="{home}#about">도파민 소개</a><a href="{home}#rooms">룸 & 시설</a>
          <a href="{home}#service">서비스 안내</a><a href="{home}#reservation">예약 문의</a>
        </div>
        <div class="footer-col">
          <h5>지역</h5>
{region_links}
        </div>
        <div class="footer-col">
          <h5>고객센터</h5>
          <a href="{tel}">전화 예약</a><a href="{kakao}">카카오톡 채널</a><a href="{home}#faq">FAQ</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 강남 가라오케 도파민 · {base}</span>
        <span class="legal"><a href="{home}#about">회사소개</a><a href="#">이용약관</a><a href="#">개인정보처리방침</a><a href="{tel}">고객센터</a></span>
      </div>
    </div>
  </footer>
  <div class="float-cta"><a class="btn btn-kakao" href="{kakao}">카톡 상담</a><a class="btn btn-primary" href="{tel}">전화 예약</a></div>
  <script src="{js}"></script>'''.format(addr=esc(ADDRESS), home=home, region_links=region_links,
                                          tel=CONTACT_TEL, kakao=KAKAO_URL, base=BASE_URL,
                                          js="assets/app.js" if depth == 0 else "../assets/app.js")


def head_html(title, desc, keywords, canonical, schema_objs, depth):
    css = "assets/style.css" if depth == 0 else "../assets/style.css"
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
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{site}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="ko_KR" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  {schema}

  <link rel="preconnect" href="https://www.google.com" />
  <link rel="stylesheet" href="{css}" />
</head>
<body>'''.format(title=esc(title), desc=esc(desc), site=esc(SITE_NAME), kw=esc(keywords),
                 canonical=canonical, schema=schema, css=css)


# ---------- 페이지 빌드 ----------
def build_main():
    title = "강남 가라오케 도파민 | 24시 연중무휴 프리미엄 파티 공간"
    desc = "강남 선릉·삼성동에 위치한 프리미엄 가라오케 도파민. 24시간 연중무휴, 최첨단 시설과 현직 DJ 공연, 프라이빗한 공간에서 특별한 밤을 경험하세요. 실시간 특가 혜택!"
    kw = "강남 가라오케, 선릉 노래방, 삼성동 프리미엄 가라오케, 강남 가라오케 도파민, 24시 가라오케, 강남 룸"
    hero = '''  <section class="hero">
    <div class="hero-inner">
      <span class="eyebrow reveal in">선릉 · 삼성동 · 24시 연중무휴</span>
      <h1 class="reveal in">강남의 밤, 그 중심에서 터지는 짜릿함<br><span class="grad">도파민 가라오케</span></h1>
      <p class="sub reveal in">선릉 · 삼성동 위치 | <b>24시 연중무휴</b> | 프리미엄 프라이빗 파티</p>
      <div class="hero-cta reveal in">
        <a class="btn btn-primary" href="#reservation">지금 예약하고 특가 혜택 받기</a>
        <a class="btn btn-ghost" href="#rooms">룸 둘러보기</a>
      </div>
      <p class="scroll-hint reveal in">주대 7만원부터 · 웹 예약 한정 특가</p>
    </div>
  </section>'''

    prose = '''  <section class="section" id="about">
    <div class="wrap prose">
      <h2>강남 가라오케 도파민 – 당신의 밤을 위한 완벽한 선택</h2>
      <p>강남의 중심, 선릉과 삼성동에서 프리미엄 가라오케 문화를 선도하는 <strong>도파민</strong>이 여러분을 초대합니다. 단순한 노래방을 넘어, 감각적인 공간과 최상급 서비스로 기억에 남는 특별한 밤을 만들어 드립니다.</p>

      <h2>왜, 도파민인가요?</h2>
      <p>도파민은 24시간 연중무휴로 운영되는 강남 대표 프리미엄 가라오케입니다. 우리가 추구하는 것은 단순한 유흥이 아닌, 고객 한 분 한 분의 취향과 니즈를 정확히 파악한 맞춤형 서비스입니다.</p>

      <h3>1. 프라이빗함과 최고의 시설</h3>
      <p>도파민은 단독 건물 전체를 사용하는 초대형 공간을 자랑합니다. 최첨단 음향 및 조명 시스템은 물론, 각 룸마다 개별 제어가 가능한 에어컨과 공기청정기를 갖춰 쾌적한 환경을 제공합니다. 사적인 대화나 업무를 완벽히 보호해 드리는 철저한 보안 시스템은 도파민만의 강력한 장점입니다.</p>

      <h3>2. 현직 DJ팀이 선사하는 라이브 퍼포먼스</h3>
      <p>화려한 경력을 가진 전문 DJ팀이 상주하여 파티의 열기를 책임집니다. 고객님의 노래 실력이 한층 돋보일 수 있도록 최적화된 마이크 세팅과 함께, 지루할 틈 없는 라이브 무대가 도파민의 밤을 더욱 특별하게 만듭니다.</p>

      <h3>3. 강남 맛집을 능가하는 안주와 주류</h3>
      <p>노래방 안주가 아님을 바로 증명하듯, 전문 셰프가 준비한 고퀄리티 안주와 다양한 주류를 만나보실 수 있습니다. 술자리의 격을 한층 높여줄 메뉴들로 준비되어 있습니다.</p>

      <h2>고객 맞춤형 공간, 룸 타입 소개</h2>
      <p>도파민은 파티의 규모와 성격에 따라 완벽한 공간을 제공합니다.</p>
      <ul>
        <li><strong>L 룸 (최대 20인):</strong> 해외 귀빈 접대, 대규모 회식, 연예인 및 VIP 파티에 최적화된 최고급 룸입니다.</li>
        <li><strong>M 룸 (최대 14인):</strong> 중요한 고객 접대나 가까운 지인들과의 오붓한 생일 파티에 제격입니다.</li>
        <li><strong>S 룸 (최대 8인):</strong> 소규모 모임이나 편안한 술자리를 원하는 분들을 위한 아늑하고 세련된 공간입니다.</li>
      </ul>
      <p>모든 룸은 최신 반주기와 프라이빗한 분위기를 보장하는 완벽한 방음 시설을 갖추고 있습니다.</p>

      <h2 id="guide">24시간, 당신이 원하는 그 순간에</h2>
      <p>도파민은 365일 24시간 운영됩니다. 언제든 편하게 방문하셔서 부담 없이 즐기실 수 있습니다.</p>
      <ul>
        <li><strong>1부:</strong> 오후 3시 ~ 새벽 1시</li>
        <li><strong>2부:</strong> 새벽 1시 ~ 오후 3시</li>
      </ul>
      <p>강남권에 거주하시는 VIP 고객을 위한 최고급 차량 픽업 서비스도 제공해 드리고 있으니, 방문 전에 미리 문의해 주세요.</p>

      <h2>지금, 도파민을 경험하세요</h2>
      <p>주대 7만원부터 시작하는 합리적인 가격과 웹사이트 예약 시 제공되는 다양한 특가 혜택을 놓치지 마세요. 실시간으로 최적의 룸과 서비스를 추천해 드립니다. 강남에서 가장 뜨거운 밤을 선사할 도파민 가라오케, 지금 바로 전화주시거나 카카오톡 채널을 통해 예약 문의를 남겨주세요.</p>
    </div>
  </section>'''

    body = "\n\n".join([
        header_html(0), hero, prose, features_html(), rooms_html(), service_html(),
        price_reserve_html(), reviews_html(MAIN_RATING, MAIN_COUNT, MAIN_REVIEWS),
        faq_html(), location_html(), region_links_html(0), footer_html(0),
    ])
    schema_objs = [website_schema(),
                   local_business_schema(SITE_NAME, BASE_URL + "/", desc, MAIN_RATING, MAIN_COUNT, MAIN_REVIEWS),
                   faq_schema()]
    page = head_html(title, desc, kw, BASE_URL + "/", schema_objs, 0) + "\n" + body + "\n</body>\n</html>\n"
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_region(r):
    area = r["area"]
    title = "{a} 가라오케 도파민 | 24시 연중무휴 프리미엄 파티 공간".format(a=area)
    desc = "{a} 가라오케는 도파민. {lead} 24시 연중무휴, 최첨단 시설과 현직 DJ 공연, 프라이빗한 공간. 실시간 추천과 특가 혜택!".format(a=area, lead=r["lead"])
    kw = "{a} 가라오케, {a} 노래방, {a} 프리미엄 가라오케, {a} 가라오케 도파민, 강남 가라오케, 24시 가라오케".format(a=area)
    canonical = "{base}/regions/{slug}.html".format(base=BASE_URL, slug=r["slug"])

    bc = '''  <div class="wrap"><nav class="breadcrumb" aria-label="breadcrumb"><a href="../index.html">홈</a> › <span>{} 가라오케</span></nav></div>'''.format(esc(area))
    hero = '''  <section class="hero" style="min-height:62vh">
    <div class="hero-inner">
      <span class="eyebrow reveal in">{area} · 24시 연중무휴</span>
      <h1 class="reveal in"><span class="grad">{area} 가라오케 도파민</span></h1>
      <p class="sub reveal in">{lead} <b>24시 연중무휴</b> · 프리미엄 프라이빗 파티.</p>
      <div class="hero-cta reveal in"><a class="btn btn-primary" href="#reservation">{area} 실시간 예약 문의</a>
        <a class="btn btn-ghost" href="#rooms">룸 보기</a></div>
    </div>
  </section>'''.format(area=esc(area), lead=esc(r["lead"]))
    intro = '''  <section class="section" id="about">
    <div class="wrap prose">
      <h2>{area}에서 즐기는 강남 프리미엄 가라오케, 도파민</h2>
      <p>{lead} 도파민은 24시간 연중무휴로 운영되는 강남 대표 프리미엄 가라오케로, {area} 인근 어디서나 편하게 방문하실 수 있습니다. 단독 건물의 초대형 공간과 최첨단 음향·조명, 현직 DJ팀의 라이브 무대, 그리고 강남 맛집급 안주까지 — 단순한 노래방을 넘어선 특별한 밤을 약속드립니다.</p>
      <p>가격·시스템·예약 모두 전화 한 통 또는 카카오톡으로 실시간 안내해 드립니다. 주대 7만원부터 시작하는 합리적인 가격과 웹 예약 한정 특가 혜택을 만나보세요.</p>
    </div>
  </section>'''.format(area=esc(area), lead=esc(r["lead"]))

    body = "\n\n".join([
        header_html(1), bc, hero, intro, features_html(), rooms_html(),
        price_reserve_html(), reviews_html(r["rating"], r["count"], r["reviews"]),
        location_html(), region_links_html(1, current=r["slug"]), footer_html(1),
    ])
    schema_objs = [breadcrumb_schema(area),
                   local_business_schema(area + " 가라오케 도파민", canonical, desc, r["rating"], r["count"], r["reviews"], area=area)]
    page = head_html(title, desc, kw, canonical, schema_objs, 1) + "\n" + body + "\n</body>\n</html>\n"
    region_dir = os.path.join(OUT_DIR, "regions")
    os.makedirs(region_dir, exist_ok=True)
    with open(os.path.join(region_dir, r["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_sitemap_robots():
    urls = [BASE_URL + "/"] + [BASE_URL + "/regions/" + r["slug"] + ".html" for r in REGIONS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>{}</loc><changefreq>weekly</changefreq><priority>{}</priority></url>".format(u, "1.0" if u.endswith("/") else "0.8"))
    sm.append("</urlset>")
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n".format(BASE_URL))


def build():
    build_main()
    for r in REGIONS:
        build_region(r)
    build_sitemap_robots()
    print("생성 완료: index.html + {}개 지역 페이지 + sitemap.xml + robots.txt".format(len(REGIONS)))


if __name__ == "__main__":
    build()
