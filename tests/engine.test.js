import test from 'node:test';
import assert from 'node:assert/strict';
import {score,rank,csv,escapeHTML} from '../site/engine.js';
import {readFileSync} from 'node:fs';
test('acerto prevalece e velocidade só concede bônus limitado',()=>{assert.equal(score(false,0,30),0);assert.equal(score(true,0,30),1000);assert.equal(score(true,15,30),900);assert.equal(score(true,30,30),800);assert.equal(score(true,40,30),800);});
test('desempate considera acertos e tempo nos acertos',()=>{const base={points:1000,correct:1,elapsed:20};const players=[{...base,name:'C'},{...base,name:'B',correct:2},{...base,name:'A',elapsed:10}];assert.deepEqual(rank(players).map(p=>p.name),['B','A','C']);});
test('exportação preserva vírgulas, aspas e neutraliza fórmulas',()=>{const out=csv([{Aluno:'=1+1',Resposta:'"x";y\nz'}]);assert.ok(out.includes('"\'=1+1"'));assert.ok(out.includes('""x"";y\nz'));assert.equal(escapeHTML('<script>'), '&lt;script&gt;');});
test('banco completo sem ids duplicados e respostas válidas',()=>{const qs=JSON.parse(readFileSync(new URL('../site/questions.json',import.meta.url)));assert.equal(qs.length,23);assert.equal(new Set(qs.map(q=>q.id)).size,23);for(const q of qs){assert.equal(q.options.length,4);assert.ok(q.answer>=0&&q.answer<4);assert.ok(q.explanation.length>20);}});
