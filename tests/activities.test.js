import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectQuestions,codeMarkup,repairMarkup,reflectionForm,validReflection} from '../site/activities.js';
const bank=JSON.parse(readFileSync(new URL('../site/questions.json',import.meta.url)));
test('pacotes têm escopo correto e atividade mista intercala novos tipos',()=>{
 assert.equal(selectQuestions(bank,'quiz').length,15);assert.equal(selectQuestions(bank,'classify').length,4);assert.equal(selectQuestions(bank,'repair').length,4);assert.equal(selectQuestions(bank,'reflect').length,8);
 assert.ok(bank.slice(0,5).some(q=>q.activity==='classify'));assert.ok(bank.slice(0,5).some(q=>q.activity==='repair'));
});
test('destaque identifica o elemento sem executar o código',()=>{
 for(const q of selectQuestions(bank,'classify')){const html=codeMarkup(q);assert.ok(html.includes('<mark>'));assert.ok(q.focus.end>q.focus.start);assert.equal(q.options.length,4);}
});
test('cada oficina tem exatamente uma alteração que passa no teste',()=>{
 for(const q of selectQuestions(bank,'repair')){assert.equal(q.repair_variants.length,4);assert.deepEqual(q.repair_variants.flatMap((v,i)=>v.passed?[i]:[]),[q.answer]);assert.notEqual(q.repair_original_output,q.repair_expected);assert.ok(repairMarkup(q,q.answer).includes('O teste apresentou o resultado esperado.'));}
});
test('explicações têm limites e textos são escapados na interface',()=>{
 assert.equal(validReflection('        '),false);assert.equal(validReflection('curto'),false);assert.equal(validReflection('Minha justificativa usa self.'),true);assert.equal(validReflection('a'.repeat(401)),false);
 const html=reflectionForm('<script>prompt</script>','</textarea><script>texto</script>');assert.ok(!html.includes('<script>'));assert.ok(html.includes('&lt;script&gt;'));
});
