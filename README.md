# Wettfahrt – Ballon-Navigation

Navigationshilfe für Heißluftballon-Wettbewerbe als Web-App (PWA). Läuft im Browser auf Handy, Tablet und Laptop, nach dem ersten Öffnen auch offline.

Ersetzt nicht den offiziellen Logger. Peilungen beziehen sich auf Gitter-Nord, Höhen in Fuß.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `index.html` | die komplette App: HTML, CSS und JavaScript in einer Datei |
| `sw.js` | Service Worker für den Offline-Betrieb |
| `manifest.json`, `icon-192.png`, `icon-512.png` | Installation als App |
| `vercel.json` | Cache-Header für Vercel |
| `CLAUDE.md` | Arbeitsanleitung für Claude Code |
| `CHANGELOG.md` | Versionsverlauf |
| `tests/` | Syntaxprüfung, Rauchtest, Task-Sheet-Test, Testdaten |

## Lokal starten

```bash
python3 -m http.server 8080
# http://localhost:8080 öffnen
```

Für GPS, Offline-Betrieb und Installation braucht der Browser `https` oder `localhost`.

## Veröffentlichen

Repository mit Vercel oder GitHub Pages verbinden, kein Build-Schritt (Vercel: Framework Preset „Other“). Bei jeder neuen Version `index.html` und `sw.js` gemeinsam hochladen.

## Funktionen (Kurzüberblick)

- UTM-Gitterkarte, Ziele mit Kreisen, Farben und Symbolen, Pfeilfeld zum Verschieben
- Task-Sheet- und Wetterbericht-Import (PDF, Text, in der Claude-Version auch Foto), viele Formate und Sprachen
- Höhenplan, Fahrplan, Bodenanflug, Markerabwurf, Windfächer, Variometer
- Windprofil aus Messung, Pibal, Briefing und Modell (DWD ICON-D2/ICON-EU über Open-Meteo)
- Task-Hilfen (HWZ, PDG, FON, CRT, ELB, LRN, ANG, MDT, 3DT u. a.), Deklarationsprüfung, Logger-Erinnerung
- Sperrgebiete, Stromleitungen und Flächen aus KML mit Warnung
- Wettbewerbskarte als Bild oder PDF, Kalibrierung über Gitterzahlen, Feinjustieren
- Startplatz-Planer, Karte mit Vorlauf, Kreis um die eigene Position
- Track-Aufzeichnung, Logbuch, GPX-Export, IGC-Import mit Vergleich
- Externes GPS über USB (Web Serial, NMEA), manuelle Höhe
- Teilen per Link oder QR-Code, Sicherung als Datei
- Startcheck, Ansagen, Simulation, offline installierbar
