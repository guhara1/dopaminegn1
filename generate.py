#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
강남 가라오케 도파민 정적 사이트 생성기.

- 메인 페이지 + 모든 지역(롱테일) 페이지를 하나의 템플릿에서 생성
- 모든 페이지에 스키마(JSON-LD) 적용: WebSite / LocalBusiness / AggregateRating / Review / BreadcrumbList
- 내부링크 강화: 상단 네비, 하단 푸터, 본문 "주변 지역" 관련 링크로 모든 페이지 상호 연결
"""
import html
import json
import os

SITE_NAME = "강남 가라오케 도파민"
BASE_URL = "https://www.dopamine-karaoke.com"
PHONE_HINT = "전화 문의"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- 지역(롱테일) 데이터 --------------------------------------------------
# 각 항목이 하나의 지역 랜딩 페이지가 된다.
REGIONS = [
    {
        "slug": "gangnam",
        "area": "강남",
        "lead": "강남역 핵심 상권에서 즐기는 프리미엄 가라오케. 도파민만의 무드와 세련된 분위기.",
        "rating": 4.9, "count": 213,
        "reviews": [
            ("김O준", 5, "강남에서 제일 깔끔합니다. 시스템 설명도 친절하고 가격도 투명해요."),
            ("이O호", 5, "24시 운영이라 늦게 가도 분위기 좋네요. 재방문 의사 100%."),
            ("박O석", 4, "위치 찾기 쉽고 응대가 빠릅니다. 특가 혜택 받아서 만족."),
        ],
    },
    {
        "slug": "seolleung",
        "area": "선릉",
        "lead": "선릉역 도보 거리, 비즈니스 모임과 2차 코스로 딱 맞는 가라오케.",
        "rating": 4.8, "count": 168,
        "reviews": [
            ("정O우", 5, "선릉 근처에서 접대 자리로 자주 이용합니다. 룸 컨디션 최고."),
            ("최O진", 5, "예약 통화 한 번에 추천까지 받아서 편했어요."),
            ("한O민", 4, "가성비 좋고 직원분들 응대가 프로페셔널합니다."),
        ],
    },
    {
        "slug": "samseong",
        "area": "삼성동",
        "lead": "삼성동 코엑스 인근, 행사·모임 후 이어가기 좋은 24시 가라오케.",
        "rating": 4.8, "count": 142,
        "reviews": [
            ("오O택", 5, "코엑스 행사 끝나고 바로 이동. 위치가 정말 편합니다."),
            ("서O빈", 5, "분위기 깔끔하고 음향 좋아요. 노래방 그 이상."),
            ("강O원", 4, "연중무휴라 휴일에도 갈 수 있어 좋네요."),
        ],
    },
    {
        "slug": "yeoksam",
        "area": "역삼",
        "lead": "역삼동 직장인 회식·2차 모임에 최적화된 강남 가라오케.",
        "rating": 4.7, "count": 121,
        "reviews": [
            ("문O혁", 5, "회식 2차로 단골입니다. 단체룸이 넓어요."),
            ("배O성", 4, "예약이 빠르고 응대가 친절합니다."),
            ("윤O아", 5, "특가 혜택 안내가 정확해서 믿고 갑니다."),
        ],
    },
    {
        "slug": "nonhyeon",
        "area": "논현",
        "lead": "논현역 인근, 프라이빗한 무드를 찾는 분께 추천하는 가라오케.",
        "rating": 4.8, "count": 109,
        "reviews": [
            ("조O환", 5, "프라이빗한 분위기가 마음에 듭니다."),
            ("임O재", 4, "위치 안내가 정확하고 깔끔해요."),
            ("신O라", 5, "실시간 추천 받아서 빠르게 자리 잡았습니다."),
        ],
    },
    {
        "slug": "sinnonhyeon",
        "area": "신논현",
        "lead": "신논현역 도보권, 강남 야간 코스의 시작점으로 좋은 가라오케.",
        "rating": 4.7, "count": 96,
        "reviews": [
            ("권O수", 5, "신논현에서 접근성 최고. 늦게까지 운영해서 좋아요."),
            ("황O연", 4, "친절하고 가격이 명확합니다."),
            ("남O우", 5, "분위기 좋고 재방문 의사 있습니다."),
        ],
    },
    {
        "slug": "cheongdam",
        "area": "청담",
        "lead": "청담동 프리미엄 라인, 격이 다른 무드의 고급 가라오케.",
        "rating": 4.9, "count": 88,
        "reviews": [
            ("표O석", 5, "청담 감성 제대로입니다. 인테리어가 고급스러워요."),
            ("진O호", 5, "응대가 세련되고 룸이 넓습니다."),
            ("구O민", 4, "조용하고 프라이빗해서 좋았어요."),
        ],
    },
    {
        "slug": "apgujeong",
        "area": "압구정",
        "lead": "압구정 로데오 인근, 트렌디한 분위기의 24시 가라오케.",
        "rating": 4.8, "count": 77,
        "reviews": [
            ("하O준", 5, "압구정 분위기 그대로. 깔끔하고 트렌디합니다."),
            ("연O지", 4, "위치 좋고 응대 빠릅니다."),
            ("도O한", 5, "연중무휴라 언제 가도 좋아요."),
        ],
    },
]

# 메인 페이지에서 노출할 대표 후기 (집계용)
MAIN_RATING = 4.8
MAIN_COUNT = sum(r["count"] for r in REGIONS)
MAIN_REVIEWS = [
    ("김O준", 5, "강남 선릉 삼성동 어디서든 접근성이 좋아요. 24시라 늘 믿고 갑니다."),
    ("최O진", 5, "전화 한 통에 실시간 추천이랑 특가까지. 응대가 정말 빠릅니다."),
    ("표O석", 5, "도파민만의 무드가 확실합니다. 분위기 끌어올리기 딱 좋아요."),
]


def esc(s):
    return html.escape(s, quote=True)


def stars(n):
    return "★" * int(round(n)) + "☆" * (5 - int(round(n)))


def jsonld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>")


def review_schema(reviews):
    return [{
        "@type": "Review",
        "author": {"@type": "Person", "name": who},
        "reviewRating": {"@type": "Rating", "ratingValue": rate, "bestRating": 5},
        "reviewBody": body,
    } for who, rate, body in reviews]


def local_business_schema(name, url, desc, rating, count, reviews, area=None):
    obj = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "image": f"{BASE_URL}/og-image.jpg",
        "url": url,
        "description": desc,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "강남구",
            "addressRegion": "서울",
            "addressCountry": "KR",
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating, "reviewCount": count,
            "bestRating": 5, "worstRating": 1,
        },
        "review": review_schema(reviews),
    }
    obj["areaServed"] = [area] if area else ["강남", "선릉", "삼성동"]
    return obj


def breadcrumb_schema(area):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": f"{area} 가라오케",
             "item": f"{BASE_URL}/regions/"},
        ],
    }


def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": f"{BASE_URL}/",
    }


def nav_links(active_slug, depth):
    """상단 네비 — 모든 지역으로의 내부링크."""
    prefix = "" if depth == 0 else "../"
    home_cur = ' aria-current="page"' if active_slug is None else ""
    items = [f'<a href="{prefix}index.html"{home_cur}>메인</a>']
    for r in REGIONS:
        cur = ' aria-current="page"' if r["slug"] == active_slug else ""
        items.append(f'<a href="{prefix}regions/{r["slug"]}.html"{cur}>{r["area"]} 가라오케</a>')
    return "\n          ".join(items)


def footer_links(depth):
    prefix = "" if depth == 0 else "../"
    items = [f'<a href="{prefix}index.html">강남 가라오케 도파민 메인</a>']
    for r in REGIONS:
        items.append(f'<a href="{prefix}regions/{r["slug"]}.html">{r["area"]} 가라오케</a>')
    return "\n        ".join(items)


def related_links(current_slug, depth):
    """본문 하단 '주변 지역' — 다른 지역으로의 내부링크(롱테일 강화)."""
    prefix = "" if depth == 0 else "../"
    out = []
    for r in REGIONS:
        if r["slug"] == current_slug:
            continue
        out.append(f'<a href="{prefix}regions/{r["slug"]}.html">{r["area"]} 가라오케 도파민</a>')
    return "\n          ".join(out)


def reviews_html(reviews):
    out = []
    for who, rate, body in reviews:
        out.append(f'''<div class="review">
            <div class="who"><strong>{esc(who)}</strong><span class="stars">{stars(rate)}</span></div>
            <p>{esc(body)}</p>
          </div>''')
    return "\n          ".join(out)


PAGE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="application-name" content="{site_name}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{site_name}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="ko_KR" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />

  {schema}

  <link rel="stylesheet" href="{css}" />
</head>
<body>
  <header>
    <div class="wrap header-inner">
      <a class="brand" href="{home}"><span class="dot">도파민</span><span>{site_name}</span></a>
      <nav class="nav-links">
          {nav}
      </nav>
    </div>
  </header>

  <div class="wrap">
{breadcrumb}
  </div>

  <main>
    <section class="hero wrap">
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="badges">
        <span class="badge">강남 · 선릉 · 삼성동</span>
        <span class="badge">24시 연중무휴</span>
        <span class="badge">실시간 추천 &amp; 특가 혜택</span>
      </div>
      <a class="cta" href="tel:">전화 문의하고 특가 받기</a>
    </section>

    <section class="block wrap">
      <h2>{info_title}</h2>
      <p class="sub">{info_sub}</p>
      <div class="grid">
        <div class="card"><h3>위치</h3><p>{loc_desc}</p></div>
        <div class="card"><h3>운영 시간</h3><p>24시 연중무휴 운영. 언제 방문하셔도 편안하게 즐기실 수 있습니다.</p></div>
        <div class="card"><h3>도파민만의 무드</h3><p>도파민, 감성 들만 모아놓은 신선한 가라오케. 완벽한 분위기를 약속드립니다.</p></div>
        <div class="card"><h3>실시간 혜택</h3><p>전화 한 통이면 실시간 추천과 특가 혜택까지. 지금 바로 문의하세요.</p></div>
      </div>
    </section>

    <section class="block wrap">
      <h2>실제 방문 후기</h2>
      <div class="rating-summary">
        <span class="rating-score">{rating}</span>
        <span class="stars">{rating_stars}</span>
        <span class="sub" style="margin:0">리뷰 {count}개 기준</span>
      </div>
      <div class="grid">
          {reviews}
      </div>
    </section>

    <section class="block wrap">
      <h2>주변 지역 가라오케</h2>
      <p class="sub">가까운 지역의 강남 가라오케 도파민 정보도 확인해 보세요.</p>
      <div class="linklist">
          {related}
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <div class="foot-links">
        {footer_links}
      </div>
      <p>{site_name} · 강남 선릉 삼성동 · 24시 연중무휴</p>
      <p>{base_url}</p>
    </div>
  </footer>
</body>
</html>
"""


def render(*, title, description, keywords, canonical, h1, lead, info_title,
           info_sub, loc_desc, rating, count, reviews, schema_objs,
           active_slug, depth, breadcrumb_html=""):
    schema = "\n  ".join(jsonld(o) for o in schema_objs)
    css = "assets/style.css" if depth == 0 else "../assets/style.css"
    home = "index.html" if depth == 0 else "../index.html"
    return PAGE.format(
        title=esc(title), description=esc(description), keywords=esc(keywords),
        canonical=canonical, site_name=esc(SITE_NAME), schema=schema, css=css,
        home=home, nav=nav_links(active_slug, depth),
        breadcrumb=breadcrumb_html, h1=esc(h1), lead=esc(lead),
        info_title=esc(info_title), info_sub=esc(info_sub), loc_desc=esc(loc_desc),
        rating=rating, rating_stars=stars(rating), count=count,
        reviews=reviews_html(reviews), related=related_links(active_slug, depth),
        footer_links=footer_links(depth), base_url=BASE_URL,
    )


def build():
    # ---- 메인 페이지 ----
    main_html = render(
        title="강남 가라오케 도파민 | 24시 연중무휴",
        description="강남 선릉 삼성동 위치. 도파민, 감성 들만 모아놓은 신선한 가라오케. 24시 연중무휴 전화하면 실시간 추천과 특가 혜택까지!",
        keywords="강남 가라오케, 선릉 가라오케, 삼성동 가라오케, 도파민, 강남 가라오케 도파민, 24시 가라오케",
        canonical=f"{BASE_URL}/",
        h1="강남 가라오케 도파민",
        lead="강남 한복판에서 펼쳐지는 프리미엄 가라오케. 끌어올릴 완벽한 무드, 세련된 분위기까지.",
        info_title="강남 선릉 삼성동, 도파민이 함께합니다",
        info_sub="강남 전 지역 어디서나 편하게 즐기는 24시 가라오케.",
        loc_desc="강남 선릉 삼성동에 위치. 정확한 위치는 지도에서 확인하실 수 있습니다.",
        rating=MAIN_RATING, count=MAIN_COUNT, reviews=MAIN_REVIEWS,
        schema_objs=[
            website_schema(),
            local_business_schema(SITE_NAME, f"{BASE_URL}/",
                                   "강남 선릉 삼성동 위치. 도파민, 감성 들만 모아놓은 신선한 가라오케. 24시 연중무휴.",
                                   MAIN_RATING, MAIN_COUNT, MAIN_REVIEWS),
        ],
        active_slug=None, depth=0,
    )
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(main_html)

    # ---- 지역 페이지 ----
    region_dir = os.path.join(OUT_DIR, "regions")
    os.makedirs(region_dir, exist_ok=True)
    for r in REGIONS:
        area = r["area"]
        title = f"{area} 가라오케 도파민 | 가격·시스템·예약 24시 연중무휴"
        desc = (f"{area} 가라오케는 도파민. {r['lead']} 24시 연중무휴, "
                f"전화하면 실시간 추천과 특가 혜택까지!")
        canonical = f"{BASE_URL}/regions/{r['slug']}.html"
        bc = f'''    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="../index.html">홈</a> › <span>{esc(area)} 가라오케</span>
    </nav>'''
        page = render(
            title=title, description=desc,
            keywords=f"{area} 가라오케, {area} 가라오케 도파민, {area} 노래방, 강남 가라오케, 24시 가라오케",
            canonical=canonical,
            h1=f"{area} 가라오케 도파민",
            lead=r["lead"],
            info_title=f"{area}에서 즐기는 가라오케 도파민",
            info_sub=f"{area} 인근 어디서나 편하게. 가격·시스템·예약 모두 전화 한 통으로.",
            loc_desc=f"{area} 인근에 위치. 정확한 위치는 지도에서 확인하실 수 있습니다.",
            rating=r["rating"], count=r["count"], reviews=r["reviews"],
            schema_objs=[
                breadcrumb_schema(area),
                local_business_schema(f"{area} 가라오케 도파민", canonical, desc,
                                       r["rating"], r["count"], r["reviews"], area=area),
            ],
            active_slug=r["slug"], depth=1, breadcrumb_html=bc,
        )
        with open(os.path.join(region_dir, f"{r['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page)

    # ---- sitemap.xml ----
    urls = [f"{BASE_URL}/"] + [f"{BASE_URL}/regions/{r['slug']}.html" for r in REGIONS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{'1.0' if u.endswith('/') else '0.8'}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")

    # ---- robots.txt ----
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\n" + f"Sitemap: {BASE_URL}/sitemap.xml\n")

    print(f"생성 완료: index.html + {len(REGIONS)}개 지역 페이지 + sitemap.xml + robots.txt")


if __name__ == "__main__":
    build()
