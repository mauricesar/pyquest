# Alinhamento das questões à turma

Autoria: Mauricésar Barbosa.

Referências fornecidas pelo professor: `POO_Questoes_06_a_10_Enunciados.txt` e `Atividade_Avaliativa_POO_Python.txt`.

As orientações desses arquivos definem o recorte pedagógico. As instruções de entrega, ZIP e WhatsApp pertencem aos exercícios originais; não fazem parte do fluxo do PyQuest.

## Recorte adotado

Classes, instâncias, construtor, atributos, `self`, chamadas de métodos, parâmetros, cálculos, `return`, condições simples e combinadas, estados booleanos, limites inclusivos, validação antes da alteração e independência entre objetos. Nas missões finais: percentuais, calibração e outro objeto como parâmetro, todos presentes na atividade avaliativa.

Os códigos mostrados são trechos reduzidos ou adaptações para leitura e raciocínio. Não substituem a implementação completa dos exercícios de origem. Não exigem listas, dicionários, herança, bibliotecas, bancos de dados, `input()`, menus ou laços de repetição.

## Trilha Quiz de POO — 15 questões

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

Na atualização anterior, o banco usava o identificador `poo-v2` e IDs 101–115. Esses registros são históricos; a versão atual está descrita abaixo. Os IDs 1–15 e os registros de partidas antigas são mantidos no banco online. Novas salas passam a selecionar o novo currículo; partidas já criadas continuam usando as questões com que foram abertas.

As instruções atuais de instalação e atualização estão na seção Novas atividades — versão 3, abaixo.

## Verificação

`python3 -m unittest discover -s tests -p 'test_*.py' -v` executa os códigos com saídas previstas, confere a correção do bug de `self`, verifica respostas numéricas e analisa a sintaxe para impedir conteúdos fora do recorte. `npm test` confere integridade do banco, pontuação, desempate e CSV.

## Novas atividades — versão 3

A aventura mista passa a ter **23 missões**, intercalando as 15 questões da trilha com:

- **Quem sou eu?**: quatro classificações de um código de Mochila. O destaque identifica a definição da classe, a variável que referencia uma instância, um atributo e um método. A explicação distingue a variável `ana` do objeto que ela referencia.
- **Conserte o robô**: quatro situações adaptadas dos exercícios de leitura, mochila, cofre, elevador e impressora. As alternativas substituem uma linha destacada. Depois da resposta e da etapa de explicação, a bancada permite comparar o código alterado e as saídas dos testes, sem pontos extras. As saídas são geradas e verificadas em Python; não há execução de código arbitrário enviado pelo aluno.
- **Explique sua escolha**: oito questões da trilha original, além das oficinas e de uma classificação, recebem perguntas de raciocínio. A escrita vem depois da resposta objetiva e antes do gabarito. Tem de 8 a 400 caracteres, sem cronômetro e sem pontuação automática.

O painel oferece os pacotes Aventura mista (23), Quiz de POO (15), Quem sou eu? (4), Conserte o robô (4) e Explique sua escolha (8). Na aventura mista, as primeiras cinco missões já incluem classificação e oficina. O professor pode habilitar ou desabilitar a etapa de explicação; no pacote dedicado, ela permanece habilitada.

O banco atual é `poo-v3`: questões da trilha usam IDs 301–315, vocabulário 321–324 e oficinas 331–334. A ordem pedagógica é mantida no campo `position`. Os IDs das versões anteriores ficam preservados no banco online para não alterar salas existentes.

Para atualizar uma instalação existente, execute a carga `02-questions.sql` e depois `04-activities.sql`. Para uma instalação nova: `01-schema.sql`, `02-questions.sql`, `04-activities.sql`. A migração 03 registra a atualização anterior e não precisa ser reaplicada.

### Aplicação em sala

1. O professor cria uma nova sala e escolhe o pacote e a quantidade de missões.
2. Os alunos entram por código ou QR code. As respostas objetivas têm tempo e pontos.
3. Quando necessário, o professor encerra as respostas e abre a escrita. Cada aluno vê apenas seu próprio texto.
4. O professor lê as explicações recebidas e revela a correção quando desejar. Pode avançar mesmo que alguém não tenha enviado o texto.
5. Ao final, as explicações continuam disponíveis em **Ler explicações** e nas colunas **Pergunta_explicacao** e **Justificativa** do CSV. Não há avaliação automática desses textos.

O modo individual serve para prática: seus textos ficam no navegador e no CSV individual. Para o professor coletar respostas, é necessário usar uma sala conectada.

## HTML e CSS — trilha independente

Base: chats de Introdução ao HTML e Projeto HTML CSS Educacional enviados pelo professor. As questões cobrem documento HTML, hierarquia, strong, listas, fragmentos de links, src/alt, article/main, label/for/id, folha externa, classes e seletores, padding/margin, max-width, Flexbox, hover e transition. Não exigem JavaScript, frameworks nem funcionamento de cadastro no servidor.

Quiz: IDs 501–515; vocabulário: 521–524; oficina: 531–534. A separação usa subject e curriculum, preservando os IDs e os códigos de Python.

## Jogos adicionais de HTML/CSS

- Duelo de estilos (541–544): fundo, arredondamento, padding, flex, gap e tipografia; cada alternativa foi comparada ao alvo pelos estilos calculados no navegador.
- Caça aos seletores (551–554): classe, id, descendência e tag; elementos numerados e regras pequenas, sem JavaScript para o aluno.
- Monte a página (561–564): nav, main, ol e article. O navegador pode renderizar escolhas semanticamente inadequadas; a correção explica a função da tag, sem presumir que aparência igual significa HTML correto.
