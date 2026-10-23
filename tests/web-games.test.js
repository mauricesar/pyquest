import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {codeMarkup,repairMarkup,selectQuestions} from '../site/activities.js';
const qs=JSON.parse(readFileSync(new URL('../site/questions.json',import.meta.url)));
test('jogos visuais oferecem alvo antes da resposta e comparações só na correção',()=>{
 for(const q of selectQuestions(qs,'visual','html-css')){const html=codeMarkup(q);assert.ok(html.includes('Referência visual do desafio'));assert.ok(html.includes('sandbox=""'));assert.ok(!html.includes('repair-variant'));assert.equal(q.repair_variants.filter(v=>v.passed).length,1);assert.equal(q.repair_variants[q.answer].passed,true);assert.ok(repairMarkup(q,q.answer).includes('repair-preview'));}
});
test('montagem completa ambas as tags e o mapa de seletores contém os cinco números',()=>{
 for(const q of selectQuestions(qs,'structure','html-css')){assert.ok(q.code.includes('_____'));for(const v of q.repair_variants)assert.ok(!v.code.includes('_____'));assert.ok(codeMarkup(q).includes('Uma peça está faltando'));}
 for(const q of selectQuestions(qs,'selectors','html-css')){for(let i=1;i<=5;i++)assert.ok(q.stage_markup.includes(`[${i}]`));assert.ok(codeMarkup(q).includes('Elementos numerados para investigar'));}
});
