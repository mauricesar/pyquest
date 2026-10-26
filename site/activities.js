import {escapeHTML as e} from './engine.js';
export const PACKS={
 mixed:{name:'Aventura mista',description:'Quiz, Quem sou eu? e Conserte o robô',icon:'✦'},
 quiz:{name:'Quiz de POO',description:'Os 15 desafios alinhados aos exercícios da turma',icon:'ϟ'},
 classify:{name:'Quem sou eu? 🔎',description:'Identifique classe, objeto, atributo e método no código destacado',icon:'🔎'},
 repair:{name:'Conserte o robô 🤖',description:'Escolha a alteração e observe o resultado do teste',icon:'🤖'},
 reflect:{name:'Explique sua escolha 💬',description:'Responda e explique seu raciocínio antes da correção',icon:'💬'}
};
export const SUBJECTS={
 python:{name:'Python · POO',short:'Python',code:'Python',badge:'PYTHON + OBJETOS',description:'Classes, objetos, métodos e estados'},
 'html-css':{name:'HTML e CSS',short:'HTML e CSS',code:'HTML e CSS',badge:'HTML + CSS',description:'Estrutura, semântica e estilo de páginas'},
 html:{name:'Só HTML',short:'Só HTML',code:'HTML',badge:'SÓ HTML',description:'Novos desafios de estrutura, semântica e formulários'},
 css:{name:'Só CSS',short:'Só CSS',code:'CSS',badge:'SÓ CSS',description:'Novos desafios de aparência, seletores e layout'}
};
export function packsFor(subject='python'){
 if(subject==='python')return PACKS;
 const packs={...PACKS,mixed:{...PACKS.mixed,description:'Todos os jogos desta modalidade na mesma aventura'},quiz:{...PACKS.quiz,name:subject==='html'?'Quiz só de HTML':subject==='css'?'Quiz só de CSS':'Quiz de HTML e CSS',description:subject==='html'?'10 questões inéditas de estrutura e semântica':subject==='css'?'10 questões inéditas sobre regras e aparência':'15 desafios de estrutura, semântica e estilo'},classify:{...PACKS.classify,description:subject==='html'?'Reconheça tags, atributos, valores e conteúdo textual':subject==='css'?'Reconheça propriedades, declarações, comentários e unidades':'Reconheça tags, atributos, seletores, propriedades e valores'},repair:{...PACKS.repair,name:subject==='html'?'Conserte o HTML 🛠️':subject==='css'?'Conserte o CSS 🛠️':'Conserte a página 🛠️',description:'Escolha uma correção e compare o resultado no navegador'}};
 if(subject!=='html'){packs.visual={name:'Duelo de estilos 🎨',description:'Compare a referência visual e escolha o CSS que a reproduz',icon:'🎨'};packs.selectors={name:'Caça aos seletores 🎯',description:'Preveja quais elementos uma regra CSS seleciona',icon:'🎯'};}
 if(subject!=='css')packs.structure={name:subject==='html'?'Monte o HTML 🧩':'Monte a página 🧩',description:'Complete a estrutura HTML com a tag adequada',icon:'🧩'};
 return packs;
}
export function selectQuestions(bank,pack='mixed',subject='python'){
 return bank.filter(q=>(q.subject||'python')===subject&&(pack==='mixed'||q.activity===pack||(pack==='reflect'&&q.activity==='quiz'&&q.reflection_prompt)));
}
export function codeMarkup(q){
 if(!q.code)return '<p class="muted">Leia a situação e escolha a alternativa que faz sentido para esse código.</p>';
 const f=q.focus;
 const code=f?e(q.code.slice(0,f.start))+`<mark>${e(q.code.slice(f.start,f.end))}</mark>`+e(q.code.slice(f.end)):e(q.code);
 const stage=q.visual_target||q.stage_markup;
 const board=stage?`<section class="visual-stage"><h3>${q.visual_target?'🎨 Sua referência':'🎯 Página para investigar'}</h3><p class="muted small">${e(q.visual_instruction)}</p><iframe class="web-preview" title="${q.visual_target?'Referência visual do desafio':'Elementos numerados para investigar'}" sandbox="" srcdoc="${e(webDocument(stage))}"></iframe></section>`:q.activity==='structure'?`<div class="puzzle-intro"><b>🧩 Uma peça está faltando</b><p>${e(q.visual_instruction)}</p><span class="small">Escolha a tag que completa a abertura e o fechamento.</span></div>`:'';
 return `${board}${q.activity==='classify'?'<p class="activity-instruction">🔎 Observe o destaque no código. Qual alternativa descreve esse elemento?</p>':''}${q.activity==='repair'?`<div class="notice"><b>${(q.subject||'python')!=='python'?'🛠️':'🤖'} O que precisa de atenção:</b> ${e(q.repair_diagnosis)}</div>`:''}<pre class="source-code" tabindex="0" aria-label="Código ${SUBJECTS[q.subject||'python'].code}"><code>${code}</code></pre>${q.activity==='repair'?`<p class="small muted">${(q.subject||'python')!=='python'?'Comportamento esperado após a correção:':'Saída esperada após a correção:'}</p><pre class="console expected">${e(q.repair_expected)}</pre><p class="small muted">Qual alternativa deve entrar no lugar do trecho destacado para chegar a esse resultado?</p>`:''}`;
}
export function repairMarkup(q,choice){
 if(!q.repair_variants)return '';
 const i=choice??q.answer,variant=q.repair_variants[i];
 return `<section class="repair-workbench"><div class="topline"><h3>${(q.subject||'python')!=='python'?'🛠️':'🤖'} Bancada de testes</h3><span class="badge">Exploração sem pontos extras</span></div><p class="muted small">Sua resposta já está salva. Agora experimente as outras alterações e compare a saída de cada uma. Esta exploração não muda sua pontuação.</p><label class="field">Qual alteração você quer conferir?<select id="repair-variant">${q.options.map((o,j)=>`<option value="${j}" ${j===i?'selected':''}>${'ABCD'[j]} · ${e(o)}</option>`).join('')}</select></label><div class="split"><div><h3>Código com a alteração</h3><pre class="source-code" tabindex="0" aria-label="Código ${SUBJECTS[q.subject||'python'].code}"><code id="repair-code">${e(variant.code)}</code></pre></div><div><h3>${(q.subject||'python')!=='python'?'Leitura do resultado':'Resultado do teste'}</h3><pre class="console" id="repair-output">${e(variant.output)}</pre><p class="test-status ${variant.passed?'success':'error'}" id="repair-status" role="status">${variant.passed?'✓ Deu certo: esta alternativa atende ao objetivo.':'↻ Compare esta alternativa com o objetivo do desafio.'}</p><p class="small muted">Esperado:</p><pre class="console expected">${e(q.repair_expected)}</pre></div></div>${(q.subject||'python')!=='python'?`<h3>Prévia no navegador</h3><iframe id="repair-preview" class="web-preview" title="Prévia da alteração em HTML e CSS" sandbox="" srcdoc="${e(webDocument(variant.preview||variant.code))}"></iframe>`:''}</section>`;
}
export function bindRepair(q,root=document){
 const select=root.querySelector('#repair-variant');
 if(select)select.onchange=()=>{const v=q.repair_variants[Number(select.value)];root.querySelector('#repair-code').textContent=v.code;root.querySelector('#repair-output').textContent=v.output;const frame=root.querySelector('#repair-preview');if(frame)frame.srcdoc=webDocument(v.preview||v.code);const status=root.querySelector('#repair-status');status.textContent=v.passed?'✓ Deu certo: esta alternativa atende ao objetivo.':'↻ Compare esta alternativa com o objetivo do desafio.';status.className='test-status '+(v.passed?'success':'error');};
}
export function reflectionForm(prompt,text='',saved=false){
 return `<section class="reflection-box"><div class="eyebrow">💬 EXPLIQUE SUA ESCOLHA</div><h3>${e(prompt)}</h3><p class="muted small">Conte, com suas palavras, o que você observou no código para escolher a resposta. Uma frase já ajuda. Pode pensar com calma: esta etapa não tem cronômetro e não altera seus pontos.</p><form id="reflection-form"><label class="field" for="reflection-text">Sua explicação</label><textarea id="reflection-text" name="reflection" minlength="8" maxlength="400" rows="4" required placeholder="Escolhi essa resposta porque…">${e(text)}</textarea><div class="topline"><span class="small muted" id="reflection-counter">${text.length}/400 caracteres · mínimo 8</span><span class="small success" id="reflection-saved" role="status">${saved?'✓ Explicação salva':''}</span></div><p class="error" id="reflection-error" role="alert"></p><button class="btn" type="submit" id="save-reflection">${saved?'Atualizar explicação':'Salvar explicação'} →</button></form></section>`;
}
export function bindReflectionCounter(root=document){
 const field=root.querySelector('#reflection-text');
 if(field)field.addEventListener('input',()=>{root.querySelector('#reflection-counter').textContent=field.value.length+'/400 caracteres · mínimo 8';root.querySelector('#reflection-saved').textContent='';});
}
export function validReflection(text){return text.trim().length>=8&&text.trim().length<=400;}

export function webDocument(code){return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; form-action 'none'; base-uri about:"><base href="about:srcdoc"><style>body{font:16px system-ui;color:#172333;background:white;padding:20px}input{font:inherit;padding:8px;border:1px solid #64748b}label{display:block;margin-bottom:8px}</style></head><body>${code}</body></html>`;}
