import test from 'node:test';
import assert from 'node:assert/strict';
import {readResponse} from '../site/transport.js';
test('ações sem retorno confirmam sem tentar interpretar JSON vazio',async()=>{
 for(const response of [new Response(null,{status:204}),new Response('',{status:200}),new Response('  ',{status:200}),new Response('null',{status:200})])assert.equal(await readResponse(response),null);
});
test('leituras preservam JSON e erros reais continuam visíveis',async()=>{
 assert.deepEqual(await readResponse(new Response('{"status":"active"}')),{status:'active'});
 await assert.rejects(readResponse(new Response('{"message":"Esta questão não está aberta."}',{status:400})),/Esta questão não está aberta/);
 await assert.rejects(readResponse(new Response('<html>Gateway error</html>',{status:502})),/conectar ao servidor/);
 await assert.rejects(readResponse(new Response('invalid',{status:200})),/resposta inesperada/);
});
