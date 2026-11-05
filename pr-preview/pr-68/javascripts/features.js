(function () {
  var KEY = "adaptify-bookmarks";
  var TAB_KEY = "adaptify-sidebar-tab";

  function Q(sel) {
    return document.querySelector(".md-sidebar--secondary " + sel) || document.querySelector(sel);
  }
  function pageData() {
    var el = document.getElementById("adaptify-page");
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
    render();
  }
  function has(url) {
    return load().some(function (b) { return b.url === url; });
  }
  function toast(msg) {
    var t = Q(".adaptify-toast");
    if (t) {
      t.textContent = msg;
      setTimeout(function () { t.textContent = ""; }, 2500);
    }
  }
  function copy(text, msg) {
    var done = function () { toast(msg); };
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text).then(done, fallback);
    fallback();
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); done(); } catch (e) { toast("Copy failed"); }
      ta.remove();
    }
  }
  function render() {
    var here = location.pathname;
    var list = load();
    var btn = Q("[data-bookmark]");
    if (btn) {
      var on = has(here);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      var star = btn.querySelector(".adaptify-star");
      var label = btn.querySelector("[data-bookmark-label]");
      if (star) star.innerHTML = on ? "&#9733;" : "&#9734;";
      if (label) label.textContent = on ? "Bookmarked" : "Bookmark";
    }
    var box = document.querySelector(".md-sidebar--primary [data-bookmarks]");
    if (!box) return;
    box.innerHTML = list.length ? "<ul></ul>" : '<p class="adaptify-bookmarks__empty">Star a page to save it here.</p>';
    var ul = box.querySelector("ul");
    if (!ul) return;
    list.forEach(function (b) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      var x = document.createElement("button");
      a.href = b.url;
      a.textContent = b.title;
      if (b.title) a.setAttribute("data-tip", b.title);
      if (b.url === here) a.className = "is-current";
      x.type = "button";
      x.innerHTML = "&times;";
      x.setAttribute("aria-label", "Remove " + b.title);
      x.addEventListener("click", function () {
        save(load().filter(function (o) { return o.url !== b.url; }));
      });
      li.appendChild(a);
      li.appendChild(x);
      ul.appendChild(li);
    });
  }
  var TIP_SEL = ".md-sidebar--primary a[data-tip], .md-sidebar--primary label.md-nav__link[data-tip], .adaptify-bookmarks a[data-tip]";
  var tipTimer = 0;
  function titles() {
    document.querySelectorAll(".md-sidebar--primary .md-ellipsis").forEach(function (el) {
      var text = (el.textContent || "").replace(/\s+/g, " ").trim();
      var link = el.closest("a") || el.closest("label.md-nav__link");
      if (!link) return;
      link.removeAttribute("title");
      if (text) link.setAttribute("data-tip", text);
      else link.removeAttribute("data-tip");
    });
    document.querySelectorAll(".adaptify-bookmarks a, .adaptify-sidenav__tool").forEach(function (el) {
      el.removeAttribute("title");
    });
  }
  function floatTip() {
    var tip = document.getElementById("adaptify-float-tip");
    if (tip) return tip;
    tip = document.createElement("div");
    tip.id = "adaptify-float-tip";
    tip.className = "adaptify-float-tip";
    tip.setAttribute("popover", "manual");
    tip.setAttribute("aria-hidden", "true");
    document.body.appendChild(tip);
    return tip;
  }
  function hideTip() {
    clearTimeout(tipTimer);
    document.querySelectorAll("[data-tip-on]").forEach(function (el) { el.removeAttribute("data-tip-on"); });
    var tip = document.getElementById("adaptify-float-tip");
    if (tip && tip.matches(":popover-open")) tip.hidePopover();
  }
  function scheduleTip(link) {
    clearTimeout(tipTimer);
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    var text = link.getAttribute("data-tip");
    if (!text) return;
    tipTimer = setTimeout(function () {
      document.querySelectorAll("[data-tip-on]").forEach(function (el) {
        if (el !== link) el.removeAttribute("data-tip-on");
      });
      link.setAttribute("data-tip-on", "");
      var tip = floatTip();
      tip.textContent = text;
      if (!tip.matches(":popover-open")) tip.showPopover();
    }, 280);
  }
  function tipTarget(node) {
    return node && node.closest ? node.closest(TIP_SEL) : null;
  }
  function setExpanded(input, open) {
    input.checked = open;
    var item = input.parentElement;
    var nav = item && item.querySelector(":scope > nav.md-nav");
    if (nav) nav.setAttribute("aria-expanded", open ? "true" : "false");
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }
  function setAll(open) {
    document.querySelectorAll("#adaptify-panel-home .md-nav__toggle").forEach(function (input) {
      if (input.id === "__toc") return;
      setExpanded(input, open);
    });
    requestAnimationFrame(titles);
  }
  function applyTab(name, persist) {
    var homeBtn = document.getElementById("adaptify-tab-home");
    var marksBtn = document.getElementById("adaptify-tab-bookmarks");
    var homePanel = document.getElementById("adaptify-panel-home");
    var marksPanel = document.getElementById("adaptify-panel-bookmarks");
    if (!homeBtn || !marksBtn || !homePanel || !marksPanel) return;
    var marks = name === "bookmarks";
    function paint(btn, panel, on) {
      btn.setAttribute("aria-selected", on ? "true" : "false");
      btn.tabIndex = on ? 0 : -1;
      panel.hidden = !on;
    }
    paint(homeBtn, homePanel, !marks);
    paint(marksBtn, marksPanel, marks);
    hideTip();
    document.documentElement.setAttribute("data-sidebar-tab", marks ? "bookmarks" : "home");
    if (persist) {
      try { localStorage.setItem(TAB_KEY, marks ? "bookmarks" : "home"); } catch (e) {}
    }
    if (!marks) requestAnimationFrame(titles);
  }
  function boot() {
    var saved = "home";
    try { saved = localStorage.getItem(TAB_KEY) === "bookmarks" ? "bookmarks" : "home"; } catch (e) {}
    applyTab(saved, false);
    render();
    if (navigator.share) {
      document.querySelectorAll('[data-share="native"]').forEach(function (n) { n.hidden = false; });
    }
    requestAnimationFrame(titles);
  }
  document.addEventListener("click", function (e) {
    var tab = e.target.closest(".adaptify-sidenav__tab");
    if (tab) {
      applyTab(tab.id === "adaptify-tab-bookmarks" ? "bookmarks" : "home", true);
      return;
    }
    var tool = e.target.closest("[data-nav-expand]");
    if (tool) {
      setAll(tool.getAttribute("data-nav-expand") === "all");
      return;
    }
    var t = e.target.closest("[data-bookmark],[data-share-toggle],[data-share]");
    var scope = e.target.closest(".adaptify-actions") || document.querySelector(".md-sidebar--secondary .adaptify-actions");
    if (!scope) return;
    var menu = scope.querySelector(".adaptify-share__menu");
    var tog = scope.querySelector("[data-share-toggle]");
    if (!t) {
      if (menu && !e.target.closest(".adaptify-share")) {
        menu.hidden = true;
        if (tog) tog.setAttribute("aria-expanded", "false");
      }
      return;
    }
    var page = pageData();
    var title = page ? page.title : document.title;
    var url = location.href.split("#")[0];
    var here = location.pathname;
    if (t.matches("[data-bookmark]")) {
      var list = load();
      if (has(here)) {
        save(list.filter(function (b) { return b.url !== here; }));
        toast("Bookmark removed");
      } else {
        list.push({ url: here, title: title });
        save(list);
        toast("Page bookmarked");
      }
    } else if (t.matches("[data-share-toggle]")) {
      menu.hidden = !menu.hidden;
      t.setAttribute("aria-expanded", String(!menu.hidden));
    } else {
      var kind = t.getAttribute("data-share");
      if (kind === "copy") copy(url, "Link copied");
      else if (kind === "email") {
        e.preventDefault();
        location.href = "mailto:?subject=" + encodeURIComponent(title + " | Adaptify Docs") + "&body=" + encodeURIComponent(url);
      } else if (kind === "native") {
        navigator.share({ title: title, url: url }).catch(function () {});
      } else if (kind === "md" && page) {
        copy("# " + title + "\n\nSource: " + url + "\n\n" + page.md.replace(/^\s*#\s[^\n]*\n/, ""), "Markdown copied");
      }
      if (menu) menu.hidden = true;
      if (tog) tog.setAttribute("aria-expanded", "false");
    }
  });
  document.addEventListener("keydown", function (e) {
    var tab = e.target.closest && e.target.closest(".adaptify-sidenav__tab");
    if (!tab) return;
    var tabs = Array.prototype.slice.call(tab.parentElement.querySelectorAll("[role='tab']"));
    var i = tabs.indexOf(tab);
    var next = null;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") next = tabs[(i + 1) % tabs.length];
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = tabs[(i - 1 + tabs.length) % tabs.length];
    else if (e.key === "Home") next = tabs[0];
    else if (e.key === "End") next = tabs[tabs.length - 1];
    else return;
    e.preventDefault();
    next.focus();
    applyTab(next.id === "adaptify-tab-bookmarks" ? "bookmarks" : "home", true);
  });
  document.addEventListener("mouseover", function (e) {
    var link = tipTarget(e.target);
    if (!link) return;
    if (e.relatedTarget && link.contains(e.relatedTarget)) return;
    scheduleTip(link);
  });
  document.addEventListener("mouseout", function (e) {
    var link = tipTarget(e.target);
    if (!link) return;
    if (e.relatedTarget && link.contains(e.relatedTarget)) return;
    hideTip();
  });
  document.addEventListener("focusin", function (e) {
    var link = tipTarget(e.target);
    if (!link || !link.matches(":focus-visible")) return;
    scheduleTip(link);
  });
  document.addEventListener("focusout", hideTip);
  document.addEventListener("scroll", function (e) {
    if (e.target && e.target.closest && e.target.closest(".md-sidebar--primary")) hideTip();
  }, true);
  if (navigator.share) {
    document.querySelectorAll('[data-share="native"]').forEach(function (n) { n.hidden = false; });
  }
  if (typeof document$ !== "undefined" && document$.subscribe) document$.subscribe(boot);
  else boot();
})();
