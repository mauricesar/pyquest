import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {SUBJECTS,packsFor,selectQuestions,codeMarkup,repairMarkup} from '../site/activities.js';
const bank=JSON.parse(readFileSync(new URL('../site/questions.json',import.meta.url)));
test('modalidades novas têm bancos próprios e só oferecem os jogos correspondentes',()=>{
 for(const [subject,counts] of Object.entries({html:{mixed:22,quiz:10,classify:4,repair:4,reflect:5,structure:4},css:{mixed:26,quiz:10,classify:4,repair:4,reflect:5,visual:4,selectors:4}})){
  for(const [pack,count] of Object.entries(counts)){const qs=selectQuestions(bank,pack,subject);assert.equal(qs.length,count,subject+'/'+pack);assert.ok(qs.every(q=>q.subject===subject));}
  assert.deepEqual(Object.keys(packsFor(subject)).sort(),Object.keys(counts).sort());
  for(const q of selectQuestions(bank,'repair',subject)){assert.ok(codeMarkup(q).includes('Código '+SUBJECTS[subject].code));assert.ok(repairMarkup(q,q.answer).includes('sandbox=""'));}
 }
 assert.equal(selectQuestions(bank,'mixed','python').length,23);assert.equal(selectQuestions(bank,'mixed','html-css').length,35);
});
test('nenhum enunciado novo é copiado das modalidades anteriores ou da outra modalidade nova',()=>{
 const old=bank.filter(q=>['python','html-css'].includes(q.subject)),fresh=bank.filter(q=>['html','css'].includes(q.subject));
 const normalize=s=>s.replace(/\s+/g,' ').trim().toLowerCase();const titles=new Set(old.map(q=>normalize(q.title)));const codes=new Set(old.map(q=>normalize(q.code)));
 for(const q of fresh){assert.ok(!titles.has(normalize(q.title)),q.title);assert.ok(!codes.has(normalize(q.code)),q.title);titles.add(normalize(q.title));codes.add(normalize(q.code));}
});
test('HTML não cobra CSS e os gabaritos das oficinas correspondem a uma única alternativa',()=>{
 for(const q of selectQuestions(bank,'mixed','html')){assert.ok(!q.code.includes('<style>'));assert.ok(!/\bstyle=/.test(q.code));assert.ok(!q.visual_target);}
 for(const q of bank.filter(q=>['html','css'].includes(q.subject)&&q.repair_variants)){assert.deepEqual(q.repair_variants.flatMap((v,i)=>v.passed?[i]:[]),[q.answer]);}
});
test('oficinas só de CSS mantêm código CSS e renderizam um contexto HTML fixo',()=>{
 for(const q of selectQuestions(bank,'repair','css'))for(const v of q.repair_variants){assert.ok(!v.code.includes('<style>'));assert.ok(v.preview.includes('<style>'));assert.ok(v.preview.includes(v.code));}
});
