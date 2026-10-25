'use strict';
importScripts('expedition-core.js?v=2.6.1');
self.onmessage=e=>{try{self.postMessage({id:e.data.id,result:PWExpeditionCore.optimize(e.data.items,e.data.options)})}catch(error){self.postMessage({id:e.data.id,error:error.message})}};
