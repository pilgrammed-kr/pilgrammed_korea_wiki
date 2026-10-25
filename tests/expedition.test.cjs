'use strict';
const a=require('node:assert/strict'),fs=require('node:fs');
a.ok(fs.existsSync('assets/expedition-core.js'),'V2.6.1 calculation engine must exist');
const C=require('../assets/expedition-core.js');
a.ok(Math.abs(C.probability(.1,10,1)-(1-.9**10))<1e-12);
a.equal(C.probability(0,100,1),0);a.equal(C.probability(1,4,5),0);a.equal(C.probability(1,5,5),1);
a.ok(Math.abs(C.probability(.5,3,2)-.5)<1e-12);
a.equal(C.probability(.01,1,1,1),1);a.equal(C.probability(.5,2,2,1),.5);
a.equal(C.required(.1,.9,1),22);a.equal(C.required(0,.9,1),Infinity);a.equal(C.required(.1,.9,1,1),1);
a.ok(C.probability(.001,100000,3)>.999999);
a.throws(()=>C.probability(2,4,1));a.throws(()=>C.required(.1,1.1,1));
const items=[{name:'Sword',category:'무기',stats:{Strength:'10'}},{name:'Wand',category:'무기',stats:{Intellect:'20'}},{name:'Cap',category:'투구',stats:{Defense:'4'}},{name:'Armor',category:'갑옷',stats:{Defense:'5'}},...Array.from({length:6},(_,i)=>({name:'R'+i,category:'장신구',stats:{Strength:String(i),Defense:String(6-i)}}))];
let r=C.optimize(items,{goals:[{key:'Strength|flat',weight:1}],constraints:[],locks:{},ownedOnly:false});
a.ok(r.results.length);a.equal(r.results[0].slots[0],'Sword');a.equal(new Set(r.results[0].slots.slice(3,8)).size,5);
r=C.optimize(items,{goals:[{key:'Strength|flat',weight:1}],constraints:[{key:'Defense|flat',min:25}],locks:{0:'Wand'}});a.ok(r.results.length);a.ok(r.results.every(x=>x.values['Defense|flat']>=25&&x.slots[0]==='Wand'));
r=C.optimize(items,{goals:[{key:'Strength|flat',weight:1}],constraints:[],locks:{},ownedOnly:true,owned:['Sword']});a.equal(r.results.length,0);
a.throws(()=>C.optimize(items,{goals:[{key:'Strength|flat',weight:1}],locks:{0:'Cap'}}));
r=C.optimize(items,{goals:[{key:'Strength|flat',weight:-1}],constraints:[],locks:{0:'Sword',3:'R1',4:'R1'}});a.equal(r.results.length,0);
a.deepEqual(C.dropRate({items:['A','B'],chance:100},'A'),{rate:null,first:null});
a.equal(C.dropRate({items:['A','B'],chance:100,individual_chances:{A:50}},'A').rate,.5);
a.equal(C.dropRate({items:['A'],chance:0,first_chance:100},'A').rate,0);

a.equal(C.required(.1,1,1),Infinity);
a.equal(C.required(.1,1,1,1),1);

console.log('V2.6.1 math and search: PASS');
r=C.optimize(items,{goals:[{key:'Intellect|flat',weight:1}],constraints:[],locks:{},weaponType:'magic'});a.equal(r.results.length,0);
