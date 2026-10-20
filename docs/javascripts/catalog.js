(function () {
  var form = document.getElementById("osa-filters");
  if (!form) return;
  var base = document.querySelector('script[src*="javascripts/catalog.js"]').src.replace(/javascripts\/catalog\.js.*$/, "");
  var FIELDS = ["q", "category", "task", "deployment", "hardware", "license", "status"];
  function $(id) { return document.getElementById(id); }
  function el(t, txt) { var e = document.createElement(t); if (txt != null) e.textContent = txt; return e; }
  function fill(id, values, labels) {
    var s = $(id);
    values.forEach(function (v) { var o = el("option", labels ? labels[v] : v); o.value = v; s.appendChild(o); });
  }
  function uniq(a) { return Array.from(new Set(a)).sort(); }
  function fromURL() {
    var u = new URLSearchParams(location.search);
    FIELDS.forEach(function (f) {
      var e = $("f-" + f), v = u.get(f) || "";
      if (e.tagName === "SELECT" && v && !Array.prototype.some.call(e.options, function (o) { return o.value === v; })) v = "";
      e.value = v;
    });
  }
  function toURL(push) {
    var u = new URLSearchParams();
    FIELDS.forEach(function (f) { var v = $("f-" + f).value; if (v) u.set(f, v); });
    var qs = u.toString(), url = location.pathname + (qs ? "?" + qs : "");
    if (url !== location.pathname + location.search) history[push ? "pushState" : "replaceState"](null, "", url);
  }
  fetch(base + "assets/catalog.json").then(function (r) { return r.json(); }).then(function (data) {
    var P = data.projects, cat = {};
    data.categories.forEach(function (c) { cat[c.id] = c.title; });
    fill("f-category", data.categories.map(function (c) { return c.id; }), cat);
    fill("f-task", uniq([].concat.apply([], P.map(function (p) { return p.tasks; }))));
    fill("f-deployment", uniq([].concat.apply([], P.map(function (p) { return p.deployment; }))));
    fill("f-hardware", uniq(P.map(function (p) { return p.hardware; })));
    fill("f-license", uniq(P.map(function (p) { return p.license_state; })));
    var cutoff = new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10);
    function v(id) { return $("f-" + id).value; }
    function render() {
      var q = v("q").trim().toLowerCase(), tb = document.querySelector("#osa-results tbody");
      var rows = P.filter(function (p) {
        if (q && (p.name + " " + p.description).toLowerCase().indexOf(q) < 0) return false;
        if (v("category") && p.category !== v("category")) return false;
        if (v("task") && p.tasks.indexOf(v("task")) < 0) return false;
        if (v("deployment") && p.deployment.indexOf(v("deployment")) < 0) return false;
        if (v("hardware") && p.hardware !== v("hardware")) return false;
        if (v("license") && p.license_state !== v("license")) return false;
        var s = v("status");
        if (s === "recent" && !(p.last_commit !== "–" && p.last_commit >= cutoff)) return false;
        if (s === "active" && p.status === "archived") return false;
        if (s === "archived" && p.status !== "archived") return false;
        return true;
      }).sort(function (a, b) { return a.name.localeCompare(b.name); });
      tb.textContent = "";
      rows.forEach(function (p) {
        var tr = el("tr"), td = el("td"), a = el("a", p.name);
        a.href = base + "stacks/" + p.category + "/#" + p.id.replace(/\./g, "");
        td.appendChild(a); tr.appendChild(td);
        [p.description, p.deployment.join(", "), p.hardware].forEach(function (t) { tr.appendChild(el("td", t)); });
        var lt = el("td", p.license + (p.license_state === "declared" ? "" : " (needs review)"));
        if (p.license_reason) lt.title = p.license_reason;
        tr.appendChild(lt);
        var st = el("td");
        if (p.status === "archived") { var b = el("strong", "⚠ archived"); b.className = "osa-archived"; st.appendChild(b); }
        else st.textContent = p.status;
        tr.appendChild(st); tr.appendChild(el("td", p.last_commit));
        tb.appendChild(tr);
      });
      $("osa-count").textContent = rows.length + " of " + P.length + " projects match";
      $("osa-empty").hidden = rows.length > 0;
      document.getElementById("osa-results").hidden = rows.length === 0;
    }
    function clear(e) { if (e) e.preventDefault(); FIELDS.forEach(function (f) { $("f-" + f).value = ""; }); toURL(true); render(); $("f-q").focus(); }
    var t;
    form.addEventListener("input", function (e) { if (e.target.id === "f-q") { clearTimeout(t); t = setTimeout(function () { toURL(false); }, 300); render(); } });
    form.addEventListener("change", function (e) { if (e.target.tagName === "SELECT") { toURL(true); render(); } });
    $("f-q").addEventListener("change", function () { toURL(true); });
    $("f-clear").addEventListener("click", clear);
    $("f-clear-link").addEventListener("click", clear);
    window.addEventListener("popstate", function () { fromURL(); render(); });
    fromURL(); render();
    form.setAttribute("data-ready", "true");
  });
})();
