export const score = (correct, elapsed, duration) => correct ? 800 + Math.round(200 * Math.max(0, 1 - elapsed / duration)) : 0;
export const rank = players => [...players].sort((a,b) => b.points-a.points || b.correct-a.correct || a.elapsed-b.elapsed || a.name.localeCompare(b.name));
export const escapeHTML = text => String(text ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function csv(rows){
  if(!rows.length) return '\ufeffSem respostas registradas\r\n';
  const safe = v => {const s=String(v??'');return '"'+(/^[=+@\-\t\r]/.test(s)?"'"+s:s).replaceAll('"','""')+'"';};
  const keys=Object.keys(rows[0]);return '\ufeff'+[keys,...rows.map(r=>keys.map(k=>r[k]))].map(r=>r.map(safe).join(';')).join('\r\n');
}
