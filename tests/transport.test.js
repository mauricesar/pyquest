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

test('avisos de autenticação e limite usam instruções em português',async()=>{
 const {responseError,isRoundUpdate,networkError}=await import('../site/transport.js');
 assert.match(responseError({error_code:'invalid_credentials',message:'Invalid login credentials'},400).message,/E-mail ou senha/);
 assert.match(responseError({message:'JWT expired'},401).message,/sessão expirou/);
 assert.match(responseError({message:'rate limit exceeded'},429).message,/Aguarde/);
 assert.match(responseError({message:'ERROR SQL relation users does not exist'},500).message,/servidor/);
 assert.ok(!responseError({message:'Unsupported operation syntax'},400).message.includes('Unsupported'));
 assert.equal(isRoundUpdate(Error('Sua resposta já foi registrada.')),true);
 assert.equal(isRoundUpdate(Error('Esta questão não está aberta.')),true);
 assert.equal(isRoundUpdate(Error('Apenas o professor pode controlar a partida.')),false);
 assert.match(networkError().message,/confirmar a ação/);
});
test('conexão interrompida durante a leitura não mostra erro técnico do navegador',async()=>{await assert.rejects(readResponse({text:async()=>{throw new TypeError('Load failed');}}),/Não conseguimos confirmar a ação/);});
