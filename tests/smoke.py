"""Rauchtest der wichtigsten Abläufe in der Simulation.
Start:  python3 -m http.server 8080   (im Projektordner)
dann:   python3 tests/smoke.py        (braucht: pip install playwright && playwright install chromium)
"""
import asyncio, os, sys
from playwright.async_api import async_playwright
URL = os.environ.get('WF_URL', 'http://localhost:8080/')
FIX = os.path.join(os.path.dirname(__file__), 'fixtures')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, accept_downloads=True)
        page = await ctx.new_page(); errs = []; log = []
        page.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
        async def step(name, coro):
            try: await coro; log.append('ok   ' + name)
            except Exception as e: log.append('FAIL ' + name + ': ' + str(e)[:120])
        async def menu(k):
            await page.click('#btn-menu'); await page.click(f'[data-open={k}]'); await page.wait_for_timeout(250)
        await page.goto(URL); await page.wait_for_timeout(1500)
        await page.click('#wl-sim'); await page.wait_for_timeout(600)
        await page.evaluate("()=>{const d=JSON.parse(localStorage.getItem('wettfahrt-v1')); d.settings.simRate=20; localStorage.setItem('wettfahrt-v1',JSON.stringify(d));}")
        await page.reload(); await page.wait_for_timeout(1000)
        for _ in range(8): await page.click('#alt-up')
        await page.wait_for_timeout(6000)
        for _ in range(12): await page.click('#alt-down')
        await page.wait_for_timeout(5000)
        await step('Fahrplan', page.click('#adv-alt')); await page.keyboard.press('Escape')
        for k in ['brief', 'check', 'tasks', 'list', 'wind', 'pz', 'map', 'log', 'reset', 'settings']:
            await step('Menü ' + k, menu(k)); await page.keyboard.press('Escape'); await page.wait_for_timeout(150)
        await menu('list'); await page.click('#tl-new'); await page.fill('#tf-name', 'Test'); await page.fill('#tf-coord', '0300/0100')
        await page.click('#tf-ring-add'); await page.fill('#tf-rings .ringrow:nth-child(1) input', '50')
        await step('Ziel speichern', page.click('#tf-save')); await page.wait_for_timeout(1500)
        await menu('pz'); await page.click('#pz-new'); await page.fill('#pf-center', '0060/0010'); await page.fill('#pf-r', '400')
        await step('Sperrgebiet speichern', page.click('#pf-save')); await page.keyboard.press('Escape')
        await menu('tasks'); await page.click('#task-new'); await page.select_option('#kf-type', 'PDG'); await page.click('#kf-save'); await page.wait_for_timeout(200)
        btns = await page.query_selector_all('#tasklist button'); await btns[0].click(); await page.wait_for_timeout(1200)
        await step('Deklarieren', page.click('#th-decl')); await page.select_option('#dc-target', index=1); await page.click('#dc-ok'); await page.wait_for_timeout(300)
        if await page.is_visible('#dc-ok'): await page.click('#dc-ok')  # zweiter Klick, falls die Prüfung gewarnt hat
        await step('Markierung', page.click('#btn-note')); await page.fill('#nt-text', 'Test'); await page.click('#nt-save')
        await menu('map'); await page.set_input_files('#map-file', os.path.join(FIX, 'testkarte.png')); await page.wait_for_timeout(1500)
        await page.click('#hint-cancel')
        await menu('log'); await step('Fahrt speichern', page.click('#log-save')); await page.wait_for_timeout(600)
        await page.set_input_files('#log-igc', os.path.join(FIX, 'logger.igc')); await page.wait_for_timeout(600)
        log.append('IGC: ' + await page.inner_text('#log-msg'))
        await page.keyboard.press('Escape')
        await menu('pz'); await page.set_input_files('#ln-file', os.path.join(FIX, 'leitungen.kml')); await page.wait_for_timeout(400)
        log.append('KML: ' + await page.inner_text('#ln-state')); await page.keyboard.press('Escape')
        print('\n'.join(log)); print('FEHLER:', '\n'.join(errs) or 'keine')
        await b.close()
        sys.exit(1 if errs or any(l.startswith('FAIL') for l in log) else 0)
asyncio.run(main())
