// Serves the built site (mkdocs build -d ../../_site/Open-Source-Ai-Full-Stack) under the real Pages base path.
const { defineConfig, devices } = require("@playwright/test");
const webkit = process.env.SKIP_WEBKIT ? [] : [
  { name: "webkit-desktop", use: { browserName: "webkit", viewport: { width: 1280, height: 800 } } },
  { name: "webkit-iphone13", use: { ...devices["iPhone 13"] } },
];
module.exports = defineConfig({
  testDir: ".",
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["json", { outputFile: "results.json" }]],
  use: { baseURL: "http://127.0.0.1:8123/Open-Source-Ai-Full-Stack/" },
  webServer: { command: "python3 -m http.server 8123 --bind 127.0.0.1 -d ../../_site", url: "http://127.0.0.1:8123/Open-Source-Ai-Full-Stack/", reuseExistingServer: true },
  projects: [
    { name: "chromium-desktop", use: { browserName: "chromium", viewport: { width: 1280, height: 800 } } },
    { name: "chromium-iphone13", use: { ...devices["iPhone 13"], browserName: "chromium" } },
    ...webkit,
  ],
});
