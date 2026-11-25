// Kör svenska texter genom fyra gratis AI-detektorer via deras webbsidor, som en vanlig besökare.
// Användning: node detect.js [--only zerogpt,smodin,grammarly,undetectable] [--details] fil.txt ...
// Kräver Playwright (npm i playwright@1) och Chromium. Smodin kräver minst 1 000 tecken.
// --details skriver ut Undetectables röda meningar och Grammarlys markerade stycken på stderr.
// Sidorna ändras: slutar en detektor svara, ta en skärmdump och uppdatera selektorn. Kringgå aldrig captcha.
const { chromium } = require('playwright');
const fs = require('fs');
let args = process.argv.slice(2), only = ['zerogpt', 'smodin', 'grammarly', 'undetectable'];
if (args[0] === '--only') { only = args[1].split(','); args = args.slice(2); }
const DETAILS = args.includes('--details'); args = args.filter(a => a !== '--details');
async function zerogpt(browser, text) {
  const p = await (await browser.newContext({ viewport: { width: 1280, height: 1000 } })).newPage();
  let res = null;
  p.on('response', async r => { if (/detectText/.test(r.url())) { try { res = await r.json(); } catch {} } });
  await p.goto('https://www.zerogpt.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(3000);
  await p.locator('textarea#textArea').fill(text);
  await p.getByRole('button', { name: 'Detect Text' }).first().click();
  for (let i = 0; i < 40 && !res; i++) await p.waitForTimeout(1000);
  await p.context().close();
  if (!res || !res.data) return { err: JSON.stringify(res).slice(0, 160) };
  return { ai: res.data.fakePercentage, flagged: (res.data.h || []).length };
}
async function smodin(browser, text) {
  const p = await (await browser.newContext({ viewport: { width: 1280, height: 1000 } })).newPage();
  let res = null;
  p.on('response', async r => { if (/ai-detection\/v2\/single/.test(r.url())) { try { res = await r.json(); } catch {} } });
  await p.goto('https://smodin.io/sv/ai-inneh%C3%A5llsdetektor', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(3000);
  await p.locator('textarea').first().fill(text);
  await p.waitForTimeout(800);
  await p.getByRole('button', { name: 'Upptäck AI' }).first().click();
  for (let i = 0; i < 40 && !res; i++) await p.waitForTimeout(1000);
  await p.waitForTimeout(2500);
  const body = await p.evaluate(() => document.body.innerText);
  const m = body.match(/AI-genererad\s*\n?\s*(\d+)\s*%/);
  await p.context().close();
  if (!res) return { err: 'no response' };
  const hi = (res.sentenceAnalysis || []).filter(s => s.impactScore === 'high').length;
  return { ai: Math.round(res.completelyGeneratedProbability), teaser: m ? +m[1] : null, high: hi, n: (res.sentenceAnalysis||[]).length };
}
async function grammarly(browser, text) {
  const p = await (await browser.newContext({ viewport: { width: 1280, height: 1000 } })).newPage();
  let res = null;
  p.on('response', async r => { if (/api\/check\/aidetector/.test(r.url())) { try { res = await r.json(); } catch {} } });
  await p.goto('https://www.grammarly.com/ai-detector', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(4000);
  await p.locator('textarea').first().fill(text);
  await p.waitForTimeout(800);
  await p.getByRole('button', { name: 'Scan for AI' }).first().click();
  for (let i = 0; i < 40 && !res; i++) await p.waitForTimeout(1000);
  await p.context().close();
  if (!res) return { err: 'no response' };
  if (DETAILS) console.error('GR SPANS:', (res.alertRanges || []).map(a => text.slice(a.begin, a.end).replace(/\n/g, ' ')).join(' ‖ '));
  return { ai: res.score, spans: (res.alertRanges || []).length };
}
async function undetectable(browser, text) {
  const p = await (await browser.newContext({ viewport: { width: 1280, height: 1000 } })).newPage();
  await p.goto('https://undetectable.ai/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(5000);
  await p.locator('textarea').first().fill(text);
  await p.waitForTimeout(800);
  await p.getByRole('button', { name: 'Check for AI' }).first().click();
  let m = null;
  for (let i = 0; i < 60 && !m; i++) { await p.waitForTimeout(1000); m = (await p.evaluate(() => document.body.innerText)).match(/Your text is ([^\n]+)\n+\s*(\d+)%/); }
  await p.waitForTimeout(1500);
  const hl = await p.evaluate(() => { const seen = new Set(), out = { red: [], green: [] };
    for (const e of document.querySelectorAll('span,mark')) { const c = getComputedStyle(e).backgroundColor, t = e.innerText.trim();
      if (t.length < 8 || seen.has(t)) continue; const m = c.match(/rgb\((\d+), (\d+), (\d+)\)/); if (!m) continue;
      const [r, g] = [+m[1], +m[2]]; if (r > 240 && g < 235) { out.red.push(t); seen.add(t); } else if (g > 245 && r < 235) { out.green.push(t); seen.add(t); } }
    return out; });
  await p.context().close();
  if (!m) return { err: 'no result' };
  if (DETAILS) console.error('UD RED:', hl.red.join(' ‖ '));
  return { ai: +m[2], verdict: m[1].trim(), red: hl.red.length, green: hl.green.length };
}
(async () => {
  const browser = await chromium.launch();
  for (const f of args) {
    const text = fs.readFileSync(f, 'utf8'); const out = { file: f.split('/').pop(), words: text.split(/\s+/).filter(Boolean).length };
    if (only.includes('zerogpt')) { try { out.zerogpt = await zerogpt(browser, text); } catch (e) { out.zerogpt = { err: e.message }; } }
    if (only.includes('smodin')) { try { out.smodin = await smodin(browser, text); } catch (e) { out.smodin = { err: e.message.split('\n')[0] }; } }
    for (const [k, fn] of [['grammarly', grammarly], ['undetectable', undetectable]]) if (only.includes(k)) { try { out[k] = await fn(browser, text); } catch (e) { out[k] = { err: e.message.split('\n')[0] }; } }
    console.log(JSON.stringify(out));
  }
  if (browser) await browser.close();
})();
