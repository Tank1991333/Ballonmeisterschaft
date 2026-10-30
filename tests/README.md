# Tests

| Datei | Zweck |
| --- | --- |
| `check.sh` | Syntaxprüfung beider Skriptblöcke in `index.html` und von `sw.js`, zeigt Version und Cache-Namen |
| `smoke.py` | Rauchtest in der Simulation: Menüs, Ziel, Sperrgebiet, Task, Deklaration, Karte, Logbuch, IGC, KML |
| `tasksheets.py` | Liest alle Task Sheets und Wetterberichte aus `fixtures/` über die Import-Vorschau und vergleicht mit den erwarteten Zahlen (`EXPECT`) |
| `sicherung.py` | Sicherung mit Logbuch-Fahrt und Kartenbild von einem Gerät auf ein frisches zweites Gerät übertragen |
| `extract-pdf-text.mjs` | Erzeugt aus einem PDF denselben Text wie die App (für neue Testfälle) |

## Ausführen

```bash
pip install playwright && playwright install chromium   # einmalig
npm install                                              # einmalig, für extract-pdf-text.mjs
python3 -m http.server 8080 &                            # im Projektordner
bash tests/check.sh
python3 tests/smoke.py
python3 tests/tasksheets.py
python3 tests/sicherung.py
```

Alle Tests laufen außerdem automatisch bei jedem Hochladen auf GitHub (`.github/workflows/tests.yml`, Reiter „Actions“). Ein rotes Kreuz am Commit heißt: ein Test ist fehlgeschlagen.

## Testdaten (`fixtures/`)

- `pdf/` Original-Task-Sheets (Krosno, Slowakei, Österreich, Toskana, Torres/Portugiesisch, deutsches Aufgabenblatt) und zwei Wetterberichte
- `*.txt` daraus erzeugter Text, so wie die App ihn sieht
- `testkarte.png` Gitter mit 100 px Abstand zum Kalibrieren
- `logger.igc` künstlicher Logger-Track mit einem E-Ereignis
- `leitungen.kml` eine Leitung und eine Fläche
- `wetter_spalten_einzeln.txt` Windtabelle, deren Werte einzeln untereinander stehen (wie manche PDFs sie liefern)
