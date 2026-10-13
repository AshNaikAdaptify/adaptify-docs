(function () {
  var KEY = "adaptify-bookmarks";
  var Q=function(sel){return document.querySelector(".md-sidebar--secondary "+sel)||document.querySelector(sel);};
  var dataEl = document.getElementById("adaptify-page");
  var page = dataEl ? JSON.parse(dataEl.textContent) : null;
  var here = location.pathname;
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} render(); }
  function has(url) { return load().some(function (b) { return b.url === url; }); }
  function toast(msg) { var t = Q(".adaptify-toast"); if (t) { t.textContent = msg; setTimeout(function () { t.textContent = ""; }, 2500); } }
  function copy(text, msg) {
    var done = function () { toast(msg); };
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text).then(done, fallback);
    fallback();
    function fallback() { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) { toast("Copy failed"); } ta.remove(); }
  }
  function render() {
    var list = load();
    var btn = Q("[data-bookmark]");
    if (btn) {
      var on = has(here);
      btn.setAttribute("aria-pressed", on);
      btn.querySelector(".adaptify-star").innerHTML = on ? "&#9733;" : "&#9734;";
      btn.querySelector("[data-bookmark-label]").textContent = on ? "Bookmarked" : "Bookmark";
    }
    var host = document.querySelector(".md-sidebar--primary .md-sidebar__inner");
    if (!host) return;
    var box = host.querySelector(".adaptify-bookmarks");
    if (!box) { box = document.createElement("div"); box.className = "adaptify-bookmarks"; host.insertBefore(box, host.firstChild); }
    box.innerHTML = '<p class="adaptify-bookmarks__title">My bookmarks</p>' + (list.length ? "<ul></ul>" : '<p class="adaptify-bookmarks__empty">Star a page to save it here.</p>');
    var ul = box.querySelector("ul");
    list.forEach(function (b) {
      var li = document.createElement("li"), a = document.createElement("a"), x = document.createElement("button");
      a.href = b.url; a.textContent = b.title;
      x.type = "button"; x.innerHTML = "&times;"; x.title = "Remove bookmark"; x.setAttribute("aria-label", "Remove " + b.title);
      x.onclick = function () { save(load().filter(function (o) { return o.url !== b.url; })); };
      li.appendChild(a); li.appendChild(x); ul.appendChild(li);
    });
  }
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-bookmark],[data-share-toggle],[data-share]");
    var scope = e.target.closest(".adaptify-actions") || document.querySelector(".md-sidebar--secondary .adaptify-actions"); if (!scope) return; var menu = scope.querySelector(".adaptify-share__menu"), tog = scope.querySelector("[data-share-toggle]");
    if (!t) { if (menu && !e.target.closest(".adaptify-share")) { menu.hidden = true; tog.setAttribute("aria-expanded", "false"); } return; }
    var title = page ? page.title : document.title, url = location.href.split("#")[0];
    if (t.matches("[data-bookmark]")) {
      var list = load();
      if (has(here)) { save(list.filter(function (b) { return b.url !== here; })); toast("Bookmark removed"); }
      else { list.push({ url: here, title: title }); save(list); toast("Page bookmarked"); }
    } else if (t.matches("[data-share-toggle]")) {
      menu.hidden = !menu.hidden; t.setAttribute("aria-expanded", String(!menu.hidden));
    } else {
      var kind = t.getAttribute("data-share");
      if (kind === "copy") copy(url, "Link copied");
      else if (kind === "email") { e.preventDefault(); location.href = "mailto:?subject=" + encodeURIComponent(title + " | Adaptify Docs") + "&body=" + encodeURIComponent(url); }
      else if (kind === "native") navigator.share({ title: title, url: url }).catch(function () {});
      else if (kind === "md" && page) copy("# " + title + "\n\nSource: " + url + "\n\n" + page.md.replace(/^\s*#\s[^\n]*\n/, ""), "Markdown copied");
      menu.hidden = true; tog.setAttribute("aria-expanded", "false");
    }
  });
  if (navigator.share) document.querySelectorAll('[data-share="native"]').forEach(function (n) { n.hidden = false; });
  render();
})();
