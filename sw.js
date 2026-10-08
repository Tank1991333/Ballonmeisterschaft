/* Wettfahrt – Offline-Speicher. Bei jeder neuen Version die Nummer erhöhen. */
const CACHE = 'wettfahrt-2026-10-08-5';
const CORE = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];
const EXTRA = [
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'
];
self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(CORE);
    for (const u of EXTRA) { try { const r = await fetch(u, { mode:'cors' }); if (r.ok) await c.put(u, r); } catch (err) {} }
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {
    /* Seite: erst Netz (mit Zeitlimit), sonst gespeicherte Version */
    e.respondWith((async () => {
      const c = await caches.open(CACHE);
      try {
        const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), 4000);
        const r = await fetch(req, { signal:ctl.signal }); clearTimeout(t);
        if (r.ok) c.put('./index.html', r.clone());
        return r;
      } catch (err) {
        return (await c.match('./index.html')) || (await c.match('./')) || Response.error();
      }
    })());
    return;
  }
  if (url.origin === location.origin || /(^|\.)fonts\.(googleapis|gstatic)\.com$|(^|\.)cdnjs\.cloudflare\.com$/.test(url.hostname)) {
    /* Dateien: sofort aus dem Speicher, im Hintergrund auffrischen */
    e.respondWith((async () => {
      const c = await caches.open(CACHE), hit = await c.match(req);
      const net = fetch(req).then(r => { if (r && (r.ok || r.type === 'opaque')) c.put(req, r.clone()); return r; }).catch(() => null);
      return hit || (await net) || Response.error();
    })());
  }
});
