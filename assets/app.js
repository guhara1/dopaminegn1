// 강남 가라오케 도파민 — 인터랙션 (모바일 메뉴 / 드롭다운 / 스크롤 등장 / 예약 폼)
(function () {
  "use strict";

  // ---- 모바일 햄버거 메뉴 ----
  var hamburger = document.querySelector(".hamburger");
  var nav = document.querySelector(".nav");
  var backdrop = document.querySelector(".nav-backdrop");

  function closeMenu() {
    if (!nav) return;
    nav.classList.remove("open");
    if (backdrop) backdrop.classList.remove("show");
    if (hamburger) hamburger.setAttribute("aria-expanded", "false");
  }
  if (hamburger && nav) {
    hamburger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      if (backdrop) backdrop.classList.toggle("show", open);
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  if (backdrop) backdrop.addEventListener("click", closeMenu);

  // ---- 드롭다운: 모바일에서는 탭으로 펼침, 데스크톱은 hover(CSS) ----
  var toggles = document.querySelectorAll(".nav > li > .menu-toggle");
  toggles.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (window.matchMedia("(max-width: 900px)").matches) {
        e.preventDefault();
        var li = btn.parentElement;
        var wasOpen = li.classList.contains("expanded");
        // 같은 레벨 다른 메뉴 닫기
        document.querySelectorAll(".nav > li.expanded").forEach(function (o) {
          if (o !== li) o.classList.remove("expanded");
        });
        li.classList.toggle("expanded", !wasOpen);
      }
    });
  });

  // 메뉴 내 링크 클릭 시 모바일 메뉴 닫기
  document.querySelectorAll(".nav a").forEach(function (a) {
    a.addEventListener("click", closeMenu);
  });

  // ---- 스크롤 등장 애니메이션 ----
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // ---- 읽기 진행바 ----
  var pbar = document.getElementById("progress-bar");
  if (pbar) {
    var updatePbar = function () {
      var el = document.documentElement;
      var max = el.scrollHeight - el.clientHeight;
      pbar.style.width = (max > 0 ? (el.scrollTop / max) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", updatePbar, { passive: true });
    window.addEventListener("resize", updatePbar);
    updatePbar();
  }

  // ---- 목차 스크롤스파이 (현재 섹션 하이라이트) ----
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var targetMap = new Map();
    tocLinks.forEach(function (a) {
      var id = (a.getAttribute("href") || "").replace(/^#/, "");
      var el = id && document.getElementById(id);
      if (el) targetMap.set(el, a);
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var a = targetMap.get(en.target);
          if (a) {
            tocLinks.forEach(function (l) { l.classList.remove("active"); });
            a.classList.add("active");
          }
        }
      });
    }, { rootMargin: "-18% 0px -72% 0px", threshold: 0 });
    targetMap.forEach(function (a, el) { spy.observe(el); });
  }

  // ---- 간편 예약 폼 (정적: 입력 요약 + 연락 채널 안내) ----
  var form = document.querySelector("#reserve-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (form.querySelector("[name=name]").value || "").trim();
      var phone = (form.querySelector("[name=phone]").value || "").trim();
      var people = form.querySelector("[name=people]").value;
      var time = form.querySelector("[name=time]").value;
      var box = form.querySelector(".form-result");
      box.innerHTML =
        "<strong>" + (name || "고객") + "</strong>님, 예약 문의가 접수 준비되었습니다.<br>" +
        "인원 <b>" + people + "</b> · 방문 <b>" + time + "</b> · 연락처 <b>" + (phone || "-") + "</b><br>" +
        "아래 <b>전화</b> 또는 <b>카카오톡</b>으로 연결하시면 실시간 추천과 특가 혜택을 즉시 안내해 드립니다.";
      box.classList.add("show");
      box.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }
})();
