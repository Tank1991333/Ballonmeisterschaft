#!/usr/bin/env bash
# Prüft die Syntax beider <script>-Blöcke in index.html und von sw.js.
set -e
cd "$(dirname "$0")/.."
python3 - << 'PY'
import re
s = open('index.html', encoding='utf-8').read()
js = re.findall(r'<script>(.*?)</script>', s, re.S)
for i, j in enumerate(js):
    open(f'/tmp/wettfahrt_script{i}.js', 'w', encoding='utf-8').write(j)
print(f'{len(js)} Skriptblöcke gefunden')
PY
for f in /tmp/wettfahrt_script*.js sw.js; do node --check "$f" && echo "ok  $f"; done
grep -o "Version 20[0-9-]*[.0-9]*" index.html | head -1
grep -o "const CACHE = '[^']*'" sw.js
