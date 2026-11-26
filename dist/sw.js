// 由 tools/build.py 生成，勿手改；版本 bank-569240d6
const V = "bank-569240d6";
self.addEventListener("install", e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(["./bank.html"])));
  self.skipWaiting();
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// network-first：每次联网都拿最新 bank.html 并更新缓存；断网时回退缓存
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && new URL(e.request.url).origin === location.origin) {
      const cp = r.clone();
      caches.open(V).then(c => c.put(e.request, cp));
    }
    return r;
  }).catch(() => caches.match(e.request, {ignoreSearch: true})));
});
