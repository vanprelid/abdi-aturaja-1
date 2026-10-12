#!/usr/bin/env node
// Render sebuah halaman HTML dalam mode terang, gelap, dan lebar ponsel, lalu simpan screenshot.
// Pemakaian: node render_check.js halaman.html folder-output/
// Butuh Playwright (npm i -g playwright, atau NODE_PATH=$(npm root -g)). Bila Chromium sudah ada
// di sistem, set PW_CHROMIUM=/path/ke/chromium.
const fs = require('fs');
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { console.error('Playwright tidak ditemukan. Coba: NODE_PATH=$(npm root -g) node render_check.js ...'); process.exit(1); }

const [src, outDir] = process.argv.slice(2);
if (!src || !outDir) { console.error('Pemakaian: node render_check.js halaman.html folder-output/'); process.exit(1); }
fs.mkdirSync(outDir, { recursive: true });

let html = fs.readFileSync(src, 'utf8');
if (!/^\s*<!doctype/i.test(html)) {
  // halaman Artifact ditulis tanpa kerangka; bungkus supaya render sama dengan saat terbit
  html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">' + html + '</body></html>';
}
const tmp = path.join(outDir, '_preview.html');
fs.writeFileSync(tmp, html);

(async () => {
  const opts = process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {};
  const browser = await chromium.launch(opts);
  for (const [name, width, scheme] of [['terang', 1440, 'light'], ['gelap', 1440, 'dark'], ['ponsel', 400, 'light']]) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, colorScheme: scheme });
    await page.goto('file://' + path.resolve(tmp), { waitUntil: 'networkidle' }).catch(() => {});
    await page.waitForTimeout(700);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    const file = path.join(outDir, `${name}.png`);
    await page.screenshot({ path: file, fullPage: true });
    console.log(`${name}: ${file}${sw > width ? `  PERINGATAN: halaman meluber ke samping (${sw}px > ${width}px)` : ''}`);
  }
  await browser.close();
  fs.unlinkSync(tmp);
})();
