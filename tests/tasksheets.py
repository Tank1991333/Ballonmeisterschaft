"""Liest alle Task Sheets und Wetterberichte aus tests/fixtures über die Import-Vorschau ein.
Start wie tests/smoke.py (Server auf Port 8080)."""
import asyncio, os, glob
from playwright.async_api import async_playwright
URL = os.environ.get('WF_URL', 'http://localhost:8080/')
FIX = os.path.join(os.path.dirname(__file__), 'fixtures')
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await (await b.new_context(viewport={'width': 390, 'height': 844})).new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        await page.goto(URL); await page.wait_for_timeout(1000); await page.click('#wl-sim'); await page.wait_for_timeout(400)
        for f in sorted(glob.glob(os.path.join(FIX, '*.txt'))):
            wx = os.path.basename(f).startswith('wetter')
            await page.evaluate("()=>document.querySelectorAll('.back.open').forEach(x=>x.classList.remove('open'))")
            await page.click('#btn-menu'); await page.click('[data-open=brief]'); await page.click('#br-wx' if wx else '#br-ts'); await page.wait_for_timeout(150)
            await page.fill('#ti-text', open(f, encoding='utf-8').read()); await page.click('#ti-parse'); await page.wait_for_timeout(300)
            print('=====', os.path.basename(f)); print(await page.inner_text('#ti-status')); print(await page.inner_text('#ti-preview'))
        print('Fehler:', errs or 'keine')
        await b.close()
asyncio.run(main())
