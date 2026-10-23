import test from 'node:test';import assert from 'node:assert/strict';
import {historyMarkup} from '../site/room-management.js';
const subjects={python:{short:'Python'}};
test('cada estado oferece a ação correta sem misturar arquivadas na lista principal',()=>{
 const rooms=[{id:'one',title:'Sala aberta',code:'ABC123',status:'active'},{id:'two',title:'Terminada',code:'DEF456',status:'finished'},{id:'three',title:'Arquivo',code:'GHI789',status:'finished',archived_at:'2026-10-23'}];
 const html=historyMarkup(rooms,subjects);assert.ok(html.includes('data-close-room="one"'));assert.ok(!html.includes('data-archive="one"'));assert.ok(html.includes('data-archive="two"'));assert.ok(html.includes('data-restore="three"'));assert.ok(html.indexOf('Arquivo')>html.indexOf('<details'));assert.ok(html.includes('Ver resultados'));assert.ok(html.includes('Partidas arquivadas (1)'));
});
test('histórico vazio e nomes não confiáveis são exibidos com segurança',()=>{assert.ok(historyMarkup([],subjects).includes('Nenhuma partida'));const html=historyMarkup([{id:'1',title:'<script>x</script>',code:'ABC123',status:'lobby'}],subjects);assert.ok(!html.includes('<script>'));assert.ok(html.includes('&lt;script&gt;'));});
