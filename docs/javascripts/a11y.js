// Make horizontally scrollable code blocks and tables keyboard-focusable (WCAG 2.1.1).
function osaFocusable() {
  document.querySelectorAll("pre > code, .osa-table-wrap").forEach(function (e) {
    if (!e.hasAttribute("tabindex")) e.setAttribute("tabindex", "0");
  });
}
if (window.document$) window.document$.subscribe(function () { setTimeout(osaFocusable, 0); });
window.addEventListener("load", osaFocusable);
