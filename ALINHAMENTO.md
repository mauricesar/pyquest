# Alinhamento das questões à turma

Autoria: Mauricésar Barbosa.

Referências fornecidas pelo professor: `POO_Questoes_06_a_10_Enunciados.txt` e `Atividade_Avaliativa_POO_Python.txt`.

As orientações desses arquivos definem o recorte pedagógico. As instruções de entrega, ZIP e WhatsApp pertencem aos exercícios originais; não fazem parte do fluxo do PyQuest.

## Recorte adotado

Classes, instâncias, construtor, atributos, `self`, chamadas de métodos, parâmetros, cálculos, `return`, condições simples e combinadas, estados booleanos, limites inclusivos, validação antes da alteração e independência entre objetos. Nas missões finais: percentuais, calibração e outro objeto como parâmetro, todos presentes na atividade avaliativa.

Os códigos mostrados são trechos reduzidos ou adaptações para leitura e raciocínio. Não substituem a implementação completa dos exercícios de origem. Não exigem listas, dicionários, herança, bibliotecas, bancos de dados, `input()`, menus ou laços de repetição.

## Sequência

| Missão | Contexto | Foco | Tempo sugerido |
|---|---|---|---|
| 1 | Mochila | Parâmetros e atributos iniciados em zero | 60 s |
| 2 | Meta de leitura | Atributo com `self` | 60 s |
| 3 | Equipe | Chamada de método | 60 s |
| 4 | Meta de leitura | Acumulação e instâncias independentes | 90 s |
| 5 | Mochila | Capacidade exata e limite `>` | 60 s |
| 6 | Equipe | Cálculo e retorno do total de jogos | 90 s |
| 7 | Cofre | Estado booleano e recusa sem alterar saldo | 90 s |
| 8 | Serviço de pintura | Método chamando outro método | 90 s |
| 9 | Impressora | Validar recursos antes de descontá-los | 90 s |
| 10 | Aluno | Preservar ambas as notas quando uma é inválida | 90 s |
| 11 | Plano de internet | Reiniciar dados mensais e preservar contrato | 60 s |
| 12 | Elevador | Porta aberta impede movimento | 90 s |
| 13 | Votação | Percentuais incluindo votos brancos | 120 s |
| 14 | Sensor | Calibração substitui valor; consulta preserva leitura | 120 s |
| 15 | Sensor | `self` e objeto recebido como parâmetro | 90 s |

As salas com 5 questões usam o aquecimento (1–5); com 10 incluem a prática (1–10); com 15 incluem as situações finais. O professor pode substituir os tempos sugeridos por um tempo fixo, incluindo 120 segundos.

## Atualização e histórico

O banco usa o identificador `poo-v2` e IDs 101–115. Os IDs 1–15 e os registros de partidas antigas são mantidos no banco online. Novas salas passam a selecionar o novo currículo; partidas já criadas continuam usando as questões com que foram abertas.

Em uma instalação existente: execute `supabase/02-questions.sql` e `supabase/03-curriculum.sql`. Em uma instalação nova: execute `01-schema.sql` e `02-questions.sql`.

## Verificação

`python3 -m unittest discover -s tests -p 'test_*.py' -v` executa os códigos com saídas previstas, confere a correção do bug de `self`, verifica respostas numéricas e analisa a sintaxe para impedir conteúdos fora do recorte. `npm test` confere integridade do banco, pontuação, desempate e CSV.
