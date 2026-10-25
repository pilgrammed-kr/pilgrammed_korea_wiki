'use strict';
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const listeners={},cache=new Map(),deleted=[],origin='https://example.test',scope=origin+'/wiki/';
let online=true,claimed=false,activated=false;
const normalize=x=>new URL(typeof x==='string'?x:x.url,scope).href;
const store={async addAll(urls){for(const u of urls){const filename=new URL(u,scope).pathname.slice('/wiki/'.length)||'index.html';assert.ok(fs.existsSync(filename),'offline asset exists: '+filename);cache.set(normalize(u),{ok:true,status:200,clone(){return this},marker:filename})}},async match(x){return cache.get(normalize(x))},async put(x,v){cache.set(normalize(x),v)}};
vm.runInNewContext(fs.readFileSync('sw.js','utf8'),{URL,Response,self:{registration:{scope},location:{origin},clients:{claim:async()=>{claimed=true}},skipWaiting:()=>{activated=true},addEventListener:(name,fn)=>{listeners[name]=fn}},caches:{open:async()=>store,keys:async()=>['pilgrammed-wiki-/wiki/-2.6.0','other-app-cache'],delete:async key=>{deleted.push(key)}},fetch:async()=>{if(!online)throw Error('offline');return {ok:true,status:200,clone(){return this},marker:'network'}}});
(async()=>{let pending;listeners.install({waitUntil:p=>{pending=p}});await pending;assert.ok(cache.size>10);listeners.activate({waitUntil:p=>{pending=p}});await pending;assert.deepEqual(deleted,['pilgrammed-wiki-/wiki/-2.6.0']);assert.ok(claimed);listeners.message({data:{type:'ACTIVATE_UPDATE'}});assert.ok(activated);
function request(path,mode='navigate'){let promise;listeners.fetch({request:{url:origin+path,method:'GET',mode},respondWith:p=>{promise=p}});return promise}
assert.equal((await request('/wiki/items/wayfinder.html')).marker,'network');online=false;assert.equal((await request('/wiki/items/wayfinder.html')).marker,'network');assert.equal((await request('/wiki/unknown-document.html')).marker,'index.html');assert.equal(request('/wiki/googleverification.html'),undefined);assert.equal(request('/other-site/'),undefined);
console.log('Service worker cache lifecycle and offline fallback: PASS')})().catch(e=>{console.error(e);process.exitCode=1});
