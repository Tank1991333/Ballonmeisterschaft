"""Liest alle Task Sheets und Wetterberichte aus tests/fixtures über die Import-Vorschau ein.
Start wie tests/smoke.py (Server auf Port 8080)."""
import asyncio, os, glob, sys
from playwright.async_api import async_playwright
URL = os.environ.get('WF_URL', 'http://localhost:8080/')
FIX = os.path.join(os.path.dirname(__file__), 'fixtures')
# Erwartete Statuszeile je Datei. Bei einer gewollten Verbesserung des Parsers hier nachziehen.
EXPECT = {
    'tasksheet_deutsch.txt': 'Erkannt: 5 Tasks, 13 Ziele, 0 Sperrgebiete.',
    'tasksheet_krosno.txt': 'Erkannt: 6 Tasks, 8 Ziele, 0 Sperrgebiete.',
    'tasksheet_oesterreich.txt': 'Erkannt: 5 Tasks, 5 Ziele, 0 Sperrgebiete.',
    'tasksheet_slowakei.txt': 'Erkannt: 5 Tasks, 3 Ziele, 0 Sperrgebiete.',
    'tasksheet_torres_pt.txt': 'Erkannt: 5 Tasks, 4 Ziele, 0 Sperrgebiete.',
    'tasksheet_toskana.txt': 'Erkannt: 5 Tasks, 4 Ziele, 0 Sperrgebiete.',
    'wetter_krosno_0920.txt': 'Erkannt: 11 Höhen mit Wind.',
    'wetter_krosno_0924.txt': 'Erkannt: 11 Höhen mit Wind.',
    'wetter_spalten_einzeln.txt': 'Erkannt: 5 Höhen mit Wind.',
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await (await b.new_context(viewport={'width': 390, 'height': 844})).new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e))); bad = []
        await page.goto(URL); await page.wait_for_timeout(1000); await page.click('#wl-sim'); await page.wait_for_timeout(400)
        for f in sorted(glob.glob(os.path.join(FIX, '*.txt'))):
            wx = os.path.basename(f).startswith('wetter')
            await page.evaluate("()=>document.querySelectorAll('.back.open').forEach(x=>x.classList.remove('open'))")
            await page.click('#btn-menu'); await page.click('[data-open=brief]'); await page.click('#br-wx' if wx else '#br-ts'); await page.wait_for_timeout(150)
            await page.fill('#ti-text', open(f, encoding='utf-8').read()); await page.click('#ti-parse'); await page.wait_for_timeout(300)
            name = os.path.basename(f); status = await page.inner_text('#ti-status')
            print('=====', name); print(status); print(await page.inner_text('#ti-preview'))
            if name in EXPECT and not status.startswith(EXPECT[name]): bad.append(name + ': erwartet „' + EXPECT[name] + '“, erhalten „' + status + '“')
        print('Fehler:', errs or 'keine')
        missing = [n for n in EXPECT if not os.path.exists(os.path.join(FIX, n))]
        if missing: bad.append('Testdatei fehlt: ' + ', '.join(missing))
        print('Abweichungen:', '\n'.join(bad) or 'keine')
        await b.close()
        sys.exit(1 if errs or bad else 0)
asyncio.run(main())
