import {escapeHTML as e} from './engine.js';
export const PACKS={
 mixed:{name:'Aventura mista',description:'Quiz, Quem sou eu? e Conserte o robô',icon:'✦'},
 quiz:{name:'Quiz de POO',description:'Os 15 desafios alinhados aos exercícios da turma',icon:'ϟ'},
 classify:{name:'Quem sou eu? 🔎',description:'Identifique classe, objeto, atributo e método no código destacado',icon:'🔎'},
 repair:{name:'Conserte o robô 🤖',description:'Escolha a alteração e observe o resultado do teste',icon:'🤖'},
 reflect:{name:'Explique sua escolha 💬',description:'Responda e explique seu raciocínio antes da correção',icon:'💬'}
};
export function selectQuestions(bank,pack='mixed'){
 return bank.filter(q=>pack==='mixed'||q.activity===pack||(pack==='reflect'&&q.activity==='quiz'&&q.reflection_prompt));
}
export function codeMarkup(q){
 if(!q.code)return '<p class="muted">Leia com atenção e escolha a alternativa que melhor responde ao desafio.</p>';
 const f=q.focus;
 const code=f?e(q.code.slice(0,f.start))+`<mark>${e(q.code.slice(f.start,f.end))}</mark>`+e(q.code.slice(f.end)):e(q.code);
 return `${q.activity==='classify'?'<p class="activity-instruction">🔎 Classifique o elemento destacado.</p>':''}${q.activity==='repair'?`<div class="notice"><b>🤖 Diagnóstico:</b> ${e(q.repair_diagnosis)}</div>`:''}<pre><code>${code}</code></pre>${q.activity==='repair'?`<p class="small muted">Saída esperada após a correção:</p><pre class="console expected">${e(q.repair_expected)}</pre><p class="small muted">Escolha a linha que deve substituir o trecho destacado.</p>`:''}`;
}
export function repairMarkup(q,choice){
 if(!q.repair_variants)return '';
 const i=choice??q.answer,variant=q.repair_variants[i];
 return `<section class="repair-workbench"><div class="topline"><h3>🤖 Bancada de testes</h3><span class="badge">Exploração sem pontos extras</span></div><p class="muted small">Sua primeira escolha já foi registrada. Agora você pode comparar outras alterações e suas saídas.</p><label class="field">Alteração para observar<select id="repair-variant">${q.options.map((o,j)=>`<option value="${j}" ${j===i?'selected':''}>${'ABCD'[j]} · ${e(o)}</option>`).join('')}</select></label><div class="split"><div><h3>Código com a alteração</h3><pre><code id="repair-code">${e(variant.code)}</code></pre></div><div><h3>Resultado do teste</h3><pre class="console" id="repair-output">${e(variant.output)}</pre><p class="test-status ${variant.passed?'success':'error'}" id="repair-status" role="status">${variant.passed?'✓ O teste apresentou o resultado esperado.':'↻ O resultado ainda não corresponde ao esperado.'}</p><p class="small muted">Esperado:</p><pre class="console expected">${e(q.repair_expected)}</pre></div></div></section>`;
}
export function bindRepair(q,root=document){
 const select=root.querySelector('#repair-variant');
 if(select)select.onchange=()=>{const v=q.repair_variants[Number(select.value)];root.querySelector('#repair-code').textContent=v.code;root.querySelector('#repair-output').textContent=v.output;const status=root.querySelector('#repair-status');status.textContent=v.passed?'✓ O teste apresentou o resultado esperado.':'↻ O resultado ainda não corresponde ao esperado.';status.className='test-status '+(v.passed?'success':'error');};
}
export function reflectionForm(prompt,text='',saved=false){
 return `<section class="reflection-box"><div class="eyebrow">💬 EXPLIQUE SUA ESCOLHA</div><h3>${e(prompt)}</h3><p class="muted small">Escreva uma frase com seu raciocínio. Esta etapa não tem cronômetro e não altera seus pontos.</p><form id="reflection-form"><label class="field" for="reflection-text">Sua explicação</label><textarea id="reflection-text" name="reflection" minlength="8" maxlength="400" rows="4" required placeholder="Escolhi essa resposta porque…">${e(text)}</textarea><div class="topline"><span class="small muted" id="reflection-counter">${text.length}/400 caracteres · mínimo 8</span><span class="small success" id="reflection-saved" role="status">${saved?'✓ Explicação salva':''}</span></div><p class="error" id="reflection-error" role="alert"></p><button class="btn" type="submit" id="save-reflection">${saved?'Atualizar explicação':'Salvar explicação'} →</button></form></section>`;
}
export function bindReflectionCounter(root=document){
 const field=root.querySelector('#reflection-text');
 if(field)field.addEventListener('input',()=>{root.querySelector('#reflection-counter').textContent=field.value.length+'/400 caracteres · mínimo 8';root.querySelector('#reflection-saved').textContent='';});
}
export function validReflection(text){return text.trim().length>=8&&text.trim().length<=400;}
