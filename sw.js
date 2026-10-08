/* Wettfahrt – Offline-Speicher. Bei jeder neuen Version die Nummer erhöhen. */
const CACHE = 'wettfahrt-2026-10-08-10';
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
    /* Seite: Netz bevorzugt. Ist es zu langsam, sofort die gespeicherte Version zeigen
       und im Hintergrund weiterladen, damit beim nächsten Start die neue Version da ist. */
    e.respondWith((async () => {
      const c = await caches.open(CACHE), cached = (await c.match('./index.html')) || (await c.match('./'));
      const oldText = cached ? await cached.clone().text() : null;
      let servedCache = false;
      const net = fetch(req, { cache:'no-store' }).then(async r => {
        if (r && r.ok) {
          const fresh = await r.clone().text();
          await c.put('./index.html', r.clone());
          if (servedCache && oldText !== null && oldText !== fresh) {
            for (const cl of await self.clients.matchAll({ type:'window' })) cl.postMessage('wf-updated');
          }
        }
        return r;
      });
      e.waitUntil(net.catch(() => null));
      if (!cached) { try { return await net; } catch (err) { return Response.error(); } }
      const timeout = new Promise(res => setTimeout(() => res(null), 4000));
      const r = await Promise.race([net.catch(() => null), timeout]);
      if (r) return r;
      servedCache = true;
      return cached;
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
