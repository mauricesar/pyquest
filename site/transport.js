// RPCs que retornam void podem confirmar a ação sem corpo (HTTP 204 ou 200).
export async function readResponse(response){
  const text=await response.text();
  let data=null;
  if(text.trim()){
    try{data=JSON.parse(text);}catch{
      throw Error(response.ok?'O servidor enviou uma resposta inesperada. Atualize a página e tente novamente.':'Não foi possível conectar ao servidor. Tente novamente em instantes.');
    }
  }
  if(!response.ok)throw Error(data?.msg||data?.message||data?.error_description||'Não foi possível conectar. Tente novamente.');
  return data;
}
