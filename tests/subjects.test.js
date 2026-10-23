import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectQuestions,packsFor,codeMarkup,repairMarkup,webDocument} from '../site/activities.js';
const bank=JSON.parse(readFileSync(new URL('../site/questions.json',import.meta.url)));
test('trilhas não misturam questões e cada pacote filtra o conteúdo escolhido',()=>{
 for(const subject of ['python','html-css']){
  for(const [pack,count] of Object.entries({mixed:subject==='python'?23:35,quiz:15,classify:4,repair:4,reflect:8,...(subject==='html-css'?{visual:4,selectors:4,structure:4}:{})})){
   const qs=selectQuestions(bank,pack,subject);assert.equal(qs.length,count,`${subject}/${pack}`);assert.ok(qs.every(q=>q.subject===subject));
  }
 }
 assert.equal(packsFor('html-css').repair.name,'Conserte a página 🛠️');assert.equal(packsFor('python').quiz.name,'Quiz de POO');
});
test('oficina web escapa o código e isola a prévia sem scripts ou rede',()=>{
 for(const q of selectQuestions(bank,'repair','html-css')){
  const html=codeMarkup(q);assert.ok(html.includes('Código HTML e CSS'));assert.ok(!html.includes('<style>'));assert.ok(!html.includes('<input '));
  const preview=repairMarkup(q,q.answer);assert.ok(preview.includes('sandbox=""'));assert.ok(preview.includes('srcdoc="&lt;!doctype html&gt;'));assert.equal(q.repair_variants.filter(v=>v.passed).length,1);
 }
 assert.ok(webDocument('<p>Teste</p>').includes("default-src 'none'"));assert.ok(webDocument('<a href="#teste">Teste</a>').includes('<base href="about:srcdoc">'));
});
