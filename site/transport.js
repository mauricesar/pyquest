// Confirmações sem corpo (HTTP 200/204) são respostas válidas de ações void.
export function responseError(data,status){
  const raw=String(data?.msg||data?.message||data?.error_description||'');
  const code=data?.error_code||data?.code||'';
  let message=raw;
  if(status===429)message='Muitas tentativas em pouco tempo. Aguarde um momento e tente novamente.';
  else if(code==='invalid_credentials'||/Invalid login credentials/i.test(raw))message='E-mail ou senha não conferem. Confira os dados e tente novamente.';
  else if(status===401||/JWT expired|refresh token|invalid jwt/i.test(raw))message='Sua sessão expirou. Entre novamente para continuar.';
  else if(status>=500||/SQL|syntax error|relation .* does not exist|PGRST/i.test(raw))message='O servidor não conseguiu concluir a solicitação. Tente novamente em instantes.';
  else if(!/[ãáàâéêíóôõúç]|^(Tempo|Esta |Este |A sala |A etapa |Sua |Nome |Apenas |Conta |Identifique|Use |Configura|Quantidade |Escolha |Dê |Entre |Encerre |Escreva |Aguarde |Banco )/.test(raw))message='Não foi possível concluir a solicitação. Tente novamente.';
  const err=Error(message||'Não foi possível concluir a solicitação. Tente novamente.');
  err.status=status;err.auth=status===401;return err;
}
export function networkError(){return Error('Não conseguimos confirmar a ação por causa da conexão. Aguarde a atualização da sala e tente novamente se necessário.');}
export function isRoundUpdate(error){return /A sala já avançou|Sua resposta já foi registrada|Esta questão não está aberta|Tempo encerrado|A etapa de explicação não está aberta/.test(error?.message||'');}
export async function readResponse(response){
  let text;try{text=await response.text();}catch{throw networkError();}
  let data=null;
  if(text.trim())try{data=JSON.parse(text);}catch{throw Error(response.ok?'O servidor enviou uma resposta inesperada. Atualize a página e tente novamente.':'Não foi possível conectar ao servidor. Tente novamente em instantes.');}
  if(!response.ok)throw responseError(data,response.status);
  return data;
}
