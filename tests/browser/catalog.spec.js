const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const count = (page) => page.locator("#osa-count");
async function open(page, qs = "") {
  await page.goto("catalog/" + qs);
  await expect(page.locator("#osa-filters[data-ready=true]")).toBeAttached();
}
async function total(page) { return Number((await count(page).textContent()).split(" of ")[1].split(" ")[0]); }

test("loads all projects", async ({ page }) => {
  await open(page);
  await expect(count(page)).toHaveText(/^(\d+) of \1 projects match$/);
  expect(await total(page)).toBeGreaterThan(50);
});

test("text search narrows results and updates the URL", async ({ page }) => {
  await open(page);
  await page.getByLabel("Search projects", { exact: true }).fill("ollama");
  await expect(page.locator("#osa-results tbody tr").first()).toContainText("Ollama");
  await expect(count(page)).not.toHaveText(/^(\d+) of \1 /);
  await expect(page).toHaveURL(/[?&]q=ollama/);
});

test("filters combine, clear resets, no-results message", async ({ page }) => {
  await open(page);
  const all = await total(page);
  await page.getByLabel("Category").selectOption("local-models");
  await expect(page).toHaveURL(/category=local-models/);
  const rows = page.locator("#osa-results tbody tr");
  const n = await rows.count();
  expect(n).toBeGreaterThan(0); expect(n).toBeLessThan(all);
  await page.getByLabel("Search projects", { exact: true }).fill("zzzz-no-such-project");
  await expect(page.locator("#osa-empty")).toBeVisible();
  await expect(count(page)).toHaveText(`0 of ${all} projects match`);
  await page.getByRole("button", { name: "Clear filters" }).click();
  await expect(count(page)).toHaveText(`${all} of ${all} projects match`);
  await expect(page.locator("#osa-empty")).toBeHidden();
  await expect(page).toHaveURL(/catalog\/$/);
});

test("archived projects are labelled", async ({ page }) => {
  await open(page, "?status=archived");
  const rows = page.locator("#osa-results tbody tr");
  expect(await rows.count()).toBeGreaterThan(0);
  for (const r of await rows.all()) await expect(r.locator(".osa-archived")).toHaveText("⚠ archived");
});

test("state survives reload and back/forward", async ({ page }) => {
  await open(page);
  await page.getByLabel("Category").selectOption("memory");
  await page.getByLabel("Licence state").selectOption("declared");
  await page.reload();
  await expect(page.locator("#osa-filters[data-ready=true]")).toBeAttached();
  await expect(page.getByLabel("Category")).toHaveValue("memory");
  await expect(page.getByLabel("Licence state")).toHaveValue("declared");
  await page.goBack();
  await expect(page.getByLabel("Licence state")).toHaveValue("");
  await expect(page.getByLabel("Category")).toHaveValue("memory");
  await page.goForward();
  await expect(page.getByLabel("Licence state")).toHaveValue("declared");
});

test("invalid URL values are ignored", async ({ page }) => {
  await open(page, "?category=<script>&q=");
  await expect(page.getByLabel("Category")).toHaveValue("");
});

test("keyboard: controls reachable with Tab and have visible focus", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on phone emulation");
  await open(page);
  await page.getByLabel("Search projects", { exact: true }).focus();
  const seen = [];
  for (let i = 0; i < 8; i++) {
    const info = await page.evaluate(() => { const e = document.activeElement, s = getComputedStyle(e); return { id: e.id, outline: s.outlineStyle !== "none" && parseFloat(s.outlineWidth) >= 1 || s.boxShadow !== "none" }; });
    seen.push(info.id); expect(info.outline, `focus visible on ${info.id}`).toBeTruthy();
    await page.keyboard.press("Tab");
  }
  for (const id of ["f-q", "f-category", "f-task", "f-deployment", "f-hardware", "f-license", "f-status", "f-clear"]) expect(seen).toContain(id);
  await page.getByLabel("Category").focus();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByLabel("Category")).not.toHaveValue("");
});

test("every control has an accessible label", async ({ page }) => {
  await open(page);
  for (const id of ["Search projects", "Category", "Task", "Deployment", "Hardware", "Licence state", "Activity"]) await expect(page.getByLabel(id, { exact: true })).toBeVisible();
});

test("axe: no serious or critical violations (catalog, home, a stack page)", async ({ page }) => {
  for (const path of ["catalog/", "", "stacks/memory/", "freshness/"]) {
    await page.goto(path);
    if (path === "catalog/") await expect(page.locator("#osa-filters[data-ready=true]")).toBeAttached();
    const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const bad = r.violations.filter((v) => ["serious", "critical"].includes(v.impact));
    expect(bad.map((v) => `${path}: ${v.id} (${v.nodes.length}) ${v.nodes[0].target}`)).toEqual([]);
  }
});

test("phone layout: no horizontal page overflow, table scrolls inside its wrapper", async ({ page, isMobile }) => {
  test.skip(!isMobile, "mobile only");
  await open(page);
  const { doc, vw } = await page.evaluate(() => ({ doc: document.documentElement.scrollWidth, vw: window.innerWidth }));
  expect(doc).toBeLessThanOrEqual(vw + 1);
  const box = await page.getByLabel("Search projects", { exact: true }).boundingBox();
  expect(box.width).toBeGreaterThan(100); expect(box.x + box.width).toBeLessThanOrEqual(vw);
  const tap = await page.getByRole("button", { name: "Clear filters" }).boundingBox();
  expect(tap.height).toBeGreaterThanOrEqual(24);
});
