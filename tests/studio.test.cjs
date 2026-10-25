const assert=require('node:assert/strict');
const fs=require('node:fs');
assert.ok(fs.existsSync('assets/studio-core.js'),'studio calculation engine must exist');
const C=require('../assets/studio-core.js');
assert.deepEqual(C.totals([{stats:{Defense:'+10','Mana Cost':'-10%',Damage:'5–10'}}]),{values:{'Defense|flat':10,'Mana Cost|%':-10},excluded:['Damage: 5–10']});
const items=[{name:'Sword',recipe_parts:[{name:'Bar',count:2}]},{name:'Bar',recipe_parts:[{name:'Ore',count:3}]}];
assert.equal(C.farm(items,[{name:'Sword',count:2}],{Bar:1,Ore:2}).leaves.Ore,7);
assert.equal(C.farm([{name:'A',recipe_parts:[{name:'A',count:1}]}],[{name:'A',count:1}],{}).issues.length,1);
assert.throws(()=>C.validateBuild({slots:['unknown']},items));
assert.throws(()=>C.validateBuild({slots:Array(8).fill('Sword')},items));

assert.deepEqual(C.farm([], [{name:'Gold',count:100}],{}),{leaves:{Gold:100},issues:[]});

console.log('studio core: PASS (units, stock, recursion, cycles, imports, currency)');
const gear=[{name:'Ring',category:'장신구'},{name:'Hat',category:'투구'}];
assert.throws(()=>C.validateBuild({slots:['','','','Ring','Ring']},gear));
assert.equal(C.validateBuild({name:'한글 빌드',slots:['','Hat']},gear).slots[1],'Hat');
assert.deepEqual(C.totals([{stats:{Defense:'-2',Bonus:'10%'}},{stats:{Defense:'+5',Bonus:'2'}}]).values,{'Defense|flat':3,'Bonus|%':10,'Bonus|flat':2});
const stock={Bar:1,Ore:2};C.farm(items,[{name:'Sword',count:2}],stock);assert.deepEqual(stock,{Bar:1,Ore:2});
assert.equal(C.farm([{name:'X',recipe_parts:[{name:'Y',count:1}],recipe_complete:false}],[{name:'X',count:1}],{}).issues.length,2);
