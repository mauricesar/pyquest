import {readResponse} from './transport.js?v=subjects-v5';
const config=window.PYQUEST_CONFIG;
export const configured=Boolean(config.url && config.key);
let session=JSON.parse(sessionStorage.getItem('pq-auth')||'null');
async function request(path,body,token){
  const response=await fetch(config.url.replace(/\/$/,'')+path,{method:'POST',headers:{'Content-Type':'application/json',apikey:config.key,...(token?{Authorization:'Bearer '+token}:{})},body:JSON.stringify(body)});
  return readResponse(response);
}
function save(data){data.expires_at=data.expires_at||Math.floor(Date.now()/1000)+data.expires_in;session=data;sessionStorage.setItem('pq-auth',JSON.stringify(data));}
export async function login(email,password){save(await request('/auth/v1/token?grant_type=password',{email,password}));}
export async function anonymous(){if(!session)save(await request('/auth/v1/signup',{}));}
let refreshing=null;
export async function rpc(name,args={}){
  if(!session)throw Error('Entre novamente para continuar.');
  if(session.expires_at*1000<Date.now()+60000){
    if(!refreshing)refreshing=request('/auth/v1/token?grant_type=refresh_token',{refresh_token:session.refresh_token}).then(data=>save(data)).finally(()=>{refreshing=null;});
    await refreshing;
  }
  return request('/rest/v1/rpc/pq_'+name,args,session.access_token);
}
export function logout(){session=null;sessionStorage.removeItem('pq-auth');sessionStorage.removeItem('pq-room');}
