# CLAUDE.md – Arbeitsanleitung für dieses Repository

## Projekt

„Wettfahrt“ ist eine Navigations-Web-App für Heißluftballon-Wettbewerbe. Der Nutzer ist Ballonpilot, die Oberfläche ist **komplett deutsch**. Er ist kein Programmierer: Änderungen immer vollständig umsetzen, testen und in einfachen Worten erklären.

## Aufbau

Die ganze App steckt in **einer Datei `index.html`** (rund 4700 Zeilen, ohne Build-Schritt, ohne Framework):

1. `<style>` mit allen Farben als CSS-Variablen (hell und dunkel), Querformat-Layout ab 700 px Breite (Karte 70 %, Instrumente 30 %).
2. HTML: Kopfzeile, `.mapwrap` mit `<canvas id="map">` und Overlays, `.hud` mit den Instrumenten, danach alle Blätter (`<div class="back" id="sheet-…">`).
3. Ein kleines frühes `<script>`: roter Fehlerkasten beim Start, Registrierung von Manifest und Service Worker (nur auf der eigenen Seite).
4. Das Hauptskript (eine IIFE). Abschnitte sind mit `/* ---------- Name ---------- */` markiert:

| Abschnitt | Wichtige Funktionen |
| --- | --- |
| Zustand | `defaults()`, `load()`, `save()` (localStorage-Schlüssel `wettfahrt-v1`, Speichern entprellt) |
| Kartenbild im Gerätespeicher | IndexedDB `wettfahrt` für Kartenbild und Logbuch-Fahrten (`idbPut`, `idbGet`) |
| Koordinaten | `ll2utm`, `utm2ll`, `parseCoord` (3/3 bis 6/7, auch „4515 - 0758“), `code44` (Anzeige nach Einstellung `digE`/`digN`), `resolve` (Bezugspunkt) |
| Position, Bewegung, Wind | `pushFix`, `motion`, `measureWind`, `windProfile` (gemessen > Pibal > Briefing „B“ > Modell), `windInterp`, `computePlan`, `getPlan` (adaptive Rechenlast) |
| Modellwind | `fetchModel`, `modelRows`, `loadModel` (Open-Meteo, `icon_d2`, Ausweichen auf `icon_eu`) |
| GPS / Externes GPS | `handleGeo` (gemeinsam für Geräte-GPS und USB), `startGps`, `startSerial`, `onNmea` (GGA, RMC, Prüfsumme), automatische Baudrate |
| Karte zeichnen | `draw`, `drawTargets`, `drawPosSym`, `drawPosRing`, `drawFan`, `drawAreas`, `drawLines`, `drawPlanner`, `drawMapImage` |
| Bedienung der Karte | Gesten, `setTool`, `updateHint`, `followCenter` (Vorlauf), `onTap` |
| Task-Hilfen | `taskHelp` je Task-Art, `markRule` (Abstands- und Zeitregeln), `crtState`, `donutState`, `loggerFor` |
| Task Sheet importieren | `parseTaskSheet` (Heuristik, mehrsprachig), `normTs`, `applyTaskSheet`, `pdfText` (pdf.js), `tsPrompt` (Claude-Version) |
| Logbuch | `storeFlight`, `parseIGC`, Wiedergabe mit Vergleich (`trackAt`) |
| Leitungen aus KML | `parseKmlShapes`, `lineStatus` |
| Startplatz-Planer | `plannerRays`, `evalLaunch` |
| Kalibrieren | `openCalSheet`, `calAnchor`, `fitCal` (Drehung > 8° → Zahlen vertauscht), `openCalpad` |
| Teilen | `packShare`/`unpackShare` (deflate-raw, base64url im Hash `#wf=`), QR über qrcode-generator |

## Regeln

- **Sprache:** Alle Texte deutsch, typografische Anführungszeichen „…“, im Code gerade Quotes.
- **Version:** Bei jeder Änderung die Zeile `Version JJJJ-MM-TT.n` im Menü erhöhen **und** in `sw.js` den Wert `const CACHE = 'wettfahrt-…'` ändern, sonst holen installierte Apps die neue Version nicht.
- **Externe Bibliotheken** nur von cdnjs, mit fester Version, nachgeladen bei Bedarf: pdf.js 3.11.174, qrcode-generator 1.4.4. Beide stehen auch in `sw.js` (`EXTRA`) für offline.
- **Zwei Laufumgebungen:** Die App läuft auch als Claude-Artifact. Dort gibt es `window.claude` (Fähigkeiten `downloads`, `db` für das Verfolgerteam, `sample` für Task Sheets von Fotos), aber kein Netz zu fremden Seiten, keinen Service Worker und kein Web Serial. Code dafür immer mit Prüfung (`window.claude`, `window.__wfOwnSite`).
- **Gespeicherte Daten:** Neue Felder in `defaults()` ergänzen; `load()` mischt vorhandene Daten mit den Standardwerten. Nie Felder entfernen, ohne alte Daten zu berücksichtigen.
- **Kein `?.`, `??`, Lookbehind oder andere neue Syntax**, damit ältere iPhones die App starten.
- **Sicherheit:** Die App ersetzt keinen Logger; Warnungen (Sperrgebiet, Leitung) nie abschwächen.

## Prüfen

```bash
bash tests/check.sh
python3 -m http.server 8080 &
python3 tests/smoke.py
python3 tests/tasksheets.py
```

Bei Änderungen an `parseTaskSheet` immer `tests/tasksheets.py` laufen lassen und die Ausgabe für alle Task Sheets kontrollieren.

## Offene Ideen

Gas und Ausdauer, Lastrechner, automatischer Track (Abheben/Landen), Bluetooth-GPS und Barometer (Web Bluetooth, Android), Live-Verfolgung auf der eigenen Seite (z. B. Firebase), Bedienungsanleitung bei größeren Änderungen nachziehen.
