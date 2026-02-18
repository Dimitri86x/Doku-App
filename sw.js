
const CACHE_NAME = 'baustelle-v1';
const ASSETS = [
    './',
    './index.html',
    './manifest.json'
];

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                return response || fetch(event.request).catch(() => {
                    // Optional: Return a fallback page if offline and not in cache
                    // But for this single-page app, index.html is likely what we want
                });
            })
    );
});
