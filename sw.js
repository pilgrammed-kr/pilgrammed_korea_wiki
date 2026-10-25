'use strict';
const PREFIX='pilgrammed-wiki-'+new URL(self.registration.scope).pathname+'-',CACHE=PREFIX+'2.6.1';
const ASSETS=['./','index.html','assets/studio.css?v=2.6.1','assets/studio-core.js?v=2.6.1','assets/studio.js?v=2.6.1','assets/expedition-core.js?v=2.6.1','assets/expedition.js?v=2.6.1','assets/expedition-worker.js?v=2.6.1','assets/offline.js?v=2.6.1','manifest.webmanifest','assets/icon.svg','assets/icon-192.png','assets/icon-512.png'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS))));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith(PREFIX)&&key!==CACHE)await caches.delete(key);await self.clients.claim()})()));
self.addEventListener('message',event=>{if(event.data?.type==='ACTIVATE_UPDATE')self.skipWaiting()});
self.addEventListener('fetch',event=>{const req=event.request,url=new URL(req.url);if(req.method!=='GET'||url.origin!==self.location.origin||!url.href.startsWith(self.registration.scope)||/\/google[^/]*\.html$/.test(url.pathname))return;
if(req.mode==='navigate'){event.respondWith((async()=>{const cache=await caches.open(CACHE);try{const response=await fetch(req);if(response.ok)await cache.put(req,response.clone());if(response.status>=500){const saved=await cache.match(req)||await cache.match(new URL('./',self.registration.scope).href);if(saved)return saved}return response}catch{return await cache.match(req)||await cache.match(new URL('./',self.registration.scope).href)||Response.error()}})());return}
if(url.pathname.includes('/assets/')||url.pathname.endsWith('/manifest.webmanifest'))event.respondWith((async()=>{const cache=await caches.open(CACHE),saved=await cache.match(req);if(saved)return saved;const response=await fetch(req);if(response.ok)await cache.put(req,response.clone());return response})());
});
