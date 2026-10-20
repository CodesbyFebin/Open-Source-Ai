(function () {
  var form = document.getElementById("osa-filters");
  if (!form) return;
  var base = document.querySelector('script[src*="javascripts/catalog.js"]').src.replace(/javascripts\/catalog\.js.*$/, "");
  fetch(base + "assets/catalog.json").then(function (r) { return r.json(); }).then(init);
  function el(t, txt) { var e = document.createElement(t); if (txt != null) e.textContent = txt; return e; }
  function fill(id, values, labels) {
    var s = document.getElementById(id);
    values.forEach(function (v) { var o = el("option", labels ? labels[v] : v); o.value = v; s.appendChild(o); });
  }
  function uniq(a) { return Array.from(new Set(a)).sort(); }
  function init(data) {
    var P = data.projects, cat = {};
    data.categories.forEach(function (c) { cat[c.id] = c.title; });
    fill("f-category", data.categories.map(function (c) { return c.id; }), cat);
    fill("f-task", uniq([].concat.apply([], P.map(function (p) { return p.tasks; }))));
    fill("f-deployment", uniq([].concat.apply([], P.map(function (p) { return p.deployment; }))));
    fill("f-hardware", uniq(P.map(function (p) { return p.hardware; })));
    fill("f-license", uniq(P.map(function (p) { return p.license_state; })));
    var cutoff = new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10);
    function v(id) { return document.getElementById(id).value; }
    function render() {
      var q = v("f-q").toLowerCase(), tb = document.querySelector("#osa-results tbody");
      var rows = P.filter(function (p) {
        if (q && (p.name + " " + p.description).toLowerCase().indexOf(q) < 0) return false;
        if (v("f-category") && p.category !== v("f-category")) return false;
        if (v("f-task") && p.tasks.indexOf(v("f-task")) < 0) return false;
        if (v("f-deployment") && p.deployment.indexOf(v("f-deployment")) < 0) return false;
        if (v("f-hardware") && p.hardware !== v("f-hardware")) return false;
        if (v("f-license") && p.license_state !== v("f-license")) return false;
        var s = v("f-status");
        if (s === "recent" && !(p.last_commit >= cutoff && p.last_commit !== "–")) return false;
        if (s === "active" && p.status === "archived") return false;
        if (s === "archived" && p.status !== "archived") return false;
        return true;
      }).sort(function (a, b) { return a.name.localeCompare(b.name); });
      tb.textContent = "";
      rows.forEach(function (p) {
        var tr = el("tr"), td = el("td"), a = el("a", p.name);
        a.href = base + "stacks/" + p.category + "/#" + p.id.replace(/\./g, "");
        a.setAttribute("aria-label", p.name + " details");
        td.appendChild(a); tr.appendChild(td);
        [p.description, p.deployment.join(", "), p.hardware, p.license + (p.license_state === "declared" ? "" : " (needs review)"), p.status, p.last_commit]
          .forEach(function (t) { tr.appendChild(el("td", t)); });
        tb.appendChild(tr);
      });
      document.getElementById("osa-count").textContent = rows.length + " of " + P.length + " projects match";
    }
    form.addEventListener("input", render); form.addEventListener("change", render); render();
  }
})();
