# PyQuest

Experiência didática de orientação a objetos em Python, de **Mauricésar Barbosa**.

A versão atual inclui Quem sou eu?, Conserte o robô e Explique sua escolha, em prática individual e nas salas conectadas.

O banco atual está alinhado aos exercícios da turma: veja [o mapa de conteúdo](ALINHAMENTO.md). Os tempos sugeridos vão de 60 a 120 segundos.

## O que funciona sem serviços externos

- Aventura individual com 23 missões (15 questões, 4 classificações e 4 oficinas), tempo, pontuação e feedback explicado.
- Quiz, previsão de saída, completar código, caça ao bug e missões finais.
- Laboratório com duas instâncias independentes de uma classe.
- Revisão individual e download de CSV. O último resultado é salvo neste navegador.
- Layout responsivo e navegação por teclado.

## Partidas de turma

O frontend está preparado para salas Supabase: entrada por código, avatar, controle exclusivo do professor, questões sincronizadas por consultas a cada 2 segundos, prazo e pontuação no banco, uma resposta por questão, ranking, pódio, histórico, diagnóstico, etapa de explicação com leitura pelo professor e CSV (incluindo ausências). Não há sala conectada enquanto `site/config.js` estiver vazio.

### Ativação em projeto Supabase novo

1. Crie o projeto no Supabase. Não configure domínio próprio nem altere outro projeto.
2. No SQL Editor, execute `supabase/01-schema.sql`, depois `supabase/02-questions.sql` e `supabase/04-activities.sql`.
3. Em Authentication, habilite Anonymous Sign-ins para os alunos. Confira o limite de novas sessões anônimas para o tamanho da turma: vários alunos na mesma rede compartilham IP. Ajuste o limite antes da aula conforme o plano disponível.
4. Crie sua conta de professor em Authentication > Users. Defina sua senha pessoalmente. Copie o UUID do usuário e execute no SQL Editor:

```sql
insert into public.pq_teachers(user_id) values ('UUID-DA-SUA-CONTA');
```

5. Em `site/config.js`, preencha a URL do projeto e somente a chave publicável (ou a chave legada anon). Nunca coloque `service_role`, `sb_secret_...` ou senha no código.
6. Faça commit/push. Teste a conta de professor e um aluno em outro navegador antes da aula.

As tabelas têm RLS ativada e acesso direto revogado. As funções conferem a identidade e a participação na sala; apenas o dono controla e exporta sua partida. O aluno não recebe o gabarito pela API antes da revelação. Este é um banco didático aberto: o gabarito do conteúdo de demonstração consta nos arquivos públicos; não use como avaliação sigilosa.

### Regra do jogo

- Acerto: `800 + round(200 × (1 − tempo / duração))`, mínimo 800 e máximo 1000.
- Erro, ausência ou prazo encerrado: zero.
- Desempate: mais acertos, depois menor soma de tempo nas respostas corretas, depois nome.
- O professor pode encerrar uma rodada antecipadamente. A resposta objetiva só pode ser enviada uma vez. Nas questões importantes, abre-se uma etapa de explicação antes do gabarito, sem cronômetro nem alteração dos pontos. O texto pode ser atualizado enquanto a etapa estiver aberta; o professor vê as explicações e pode exportá-las.
- Participantes precisam entrar antes da primeira questão. Quem recarregar a mesma aba pode entrar novamente na mesma sala com a sessão preservada.
- A criação do aluno é anônima; limpar dados ou trocar de navegador perde sua identidade. O professor mantém os registros no banco.

## Python e edição das questões

`python/build.py` usa uma classe `Questao` para definir o banco e gerar o JSON e a carga SQL. Assim o conteúdo pode ser mantido usando Python e servir de exemplo da matéria. A interface roda em JavaScript no navegador; GitHub Pages não executa servidor Python.

```sh
python3 python/build.py
npm test
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m http.server 8765 --directory site
```

Abra `http://localhost:8765`. Requer Python 3.10+ e Node 20+ para os testes. O site publicado não precisa dessas instalações.

## Publicação isolada

Repositório dedicado `mauricesar/pyquest`, GitHub Pages via GitHub Actions. A pasta `site/` é o único artefato público do Pages. Nenhum `CNAME`, domínio personalizado ou alteração no repositório `meu-site` é necessário.

## Antes de uma turma real

Faça uma partida entre dois dispositivos; teste acerto, erro, expiração, clique duplo, reconexão, pódio e CSV. O frontend pode ser testado individualmente antes da ativação. Custos e limites de Supabase dependem do plano escolhido; a aplicação não contrata plano pago.
