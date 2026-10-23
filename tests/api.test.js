import test from 'node:test';import assert from 'node:assert/strict';
test('duas consultas simultâneas renovam a sessão apenas uma vez e ações aceitam 204',async()=>{
 const store=new Map([['pq-auth',JSON.stringify({access_token:'old',refresh_token:'refresh',expires_at:1})]]);
 globalThis.window={PYQUEST_CONFIG:{url:'https://local.test',key:'public-test'}};
 globalThis.sessionStorage={getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)};
 let refreshes=0;globalThis.fetch=async(url,options)=>{if(url.includes('refresh_token')){refreshes++;await new Promise(resolve=>setTimeout(resolve,10));return new Response(JSON.stringify({access_token:'new',refresh_token:'next',expires_in:3600}));}assert.equal(options.headers.Authorization,'Bearer new');return url.endsWith('pq_advance')?new Response(null,{status:204}):new Response('{"status":"active"}');};
 const {rpc}=await import('../site/api.js?test=refresh');const result=await Promise.all([rpc('state'),rpc('state')]);assert.equal(refreshes,1);assert.deepEqual(result,[{status:'active'},{status:'active'}]);assert.equal(await rpc('advance'),null);
});
test('falha de rede mantém uma mensagem útil e não vaza TypeError',async()=>{
 const {rpc}=await import('../site/api.js?test=refresh');globalThis.fetch=async()=>{throw new TypeError('Failed to fetch');};await assert.rejects(rpc('state'),/Não conseguimos confirmar a ação/);
});
test('resposta vazia de leitura não é confundida com uma sala válida',async()=>{
 const {rpc}=await import('../site/api.js?test=refresh');globalThis.fetch=async()=>new Response(null,{status:204});await assert.rejects(rpc('state'),/não devolveu os dados da sala/);
});
