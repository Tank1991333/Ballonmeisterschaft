"""Sicherung von Gerät A auf ein frisches Gerät B übertragen: Ziele, Logbuch-Fahrt und Kartenbild müssen ankommen.
Start wie tests/smoke.py (Server auf Port 8080)."""
import asyncio, os, sys
from playwright.async_api import async_playwright
URL = os.environ.get('WF_URL', 'http://localhost:8080/')
FIX = os.path.join(os.path.dirname(__file__), 'fixtures')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []; log = []
        def check(name, cond, extra=''): log.append(('ok   ' if cond else 'FAIL ') + name + (' ' + str(extra) if extra else ''))
        # Gerät A: Simulation, Karte laden, Fahrt speichern, Sicherung herunterladen
        a = await (await b.new_context(viewport={'width': 390, 'height': 844}, accept_downloads=True)).new_page()
        a.on('pageerror', lambda e: errs.append('A ' + str(e)))
        await a.goto(URL); await a.wait_for_timeout(800); await a.click('#wl-sim'); await a.wait_for_timeout(4000)
        await a.click('#btn-menu'); await a.click('#sheet-menu [data-open=map]')
        await a.set_input_files('#map-file', os.path.join(FIX, 'testkarte.png')); await a.wait_for_timeout(1500)
        await a.click('#hint-cancel') if await a.is_visible('#hint-cancel') else None
        await a.click('#btn-menu'); await a.click('#sheet-menu [data-open=log]'); await a.click('#log-save'); await a.wait_for_timeout(600)
        await a.keyboard.press('Escape')
        await a.click('#btn-menu'); await a.click('#sheet-menu [data-open=settings]')
        async with a.expect_download() as dl:
            await a.click('#bk-save')
        path = await (await dl.value).path()
        await a.wait_for_timeout(300)
        check('Sicherung erstellt', 'Fahrt' in await a.inner_text('#bk-msg'), await a.inner_text('#bk-msg'))
        # Gerät B: frisch, Sicherung laden und einspielen
        bp = await (await b.new_context(viewport={'width': 390, 'height': 844})).new_page()
        bp.on('pageerror', lambda e: errs.append('B ' + str(e)))
        await bp.goto(URL); await bp.wait_for_timeout(800); await bp.click('#wl-sim'); await bp.wait_for_timeout(500)
        await bp.click('#btn-menu'); await bp.click('#sheet-menu [data-open=settings]')
        await bp.set_input_files('#bk-load', path); await bp.wait_for_timeout(400)
        check('Sicherung erkannt', 'Kartenbild' in await bp.inner_text('#bk-msg'), await bp.inner_text('#bk-msg'))
        await bp.click('#bk-apply'); await bp.wait_for_timeout(2500)
        st = await bp.evaluate("()=>{const d=JSON.parse(localStorage.getItem('wettfahrt-v1'));return {f:d.flights.length,map:d.map.has,cal:d.map.cal}}")
        check('Logbuch-Fahrt übernommen', st['f'] == 1, st)
        check('Kartenbild übernommen', st['map'], st)
        await bp.click('#btn-menu'); await bp.click('#sheet-menu [data-open=log]')
        await bp.click('#loglist li button:has-text("Ansehen")'); await bp.wait_for_timeout(600)
        check('Fahrt lässt sich ansehen', not await bp.is_hidden('#replay'))
        print('\n'.join(log)); print('FEHLER:', '\n'.join(errs) or 'keine')
        await b.close()
        sys.exit(1 if errs or any(l.startswith('FAIL') for l in log) else 0)
asyncio.run(main())
