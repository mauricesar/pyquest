"""Novos jogos autorais: comparação visual, seletores e estrutura semântica."""
SOURCE='Projetos HTML/CSS e Introdução ao HTML • práticas da turma'
def web_games():
    qs=[]
    def question(id,activity,title,concept,code,options,answer,explanation,**extra):
        qs.append(dict(id=id,subject='html-css',curriculum='web-v1',activity=activity,kind={'visual':'Duelo de estilos 🎨','selectors':'Caça aos seletores 🎯','structure':'Monte a página 🧩'}[activity],title=title,concept=concept,code=code,options=options,answer=answer,explanation=explanation,seconds=90,reflection_prompt='',source=SOURCE,position=23+len(qs),**extra))
    visuals=[
        ('Um card com cantos arredondados','Cores e bordas','<article class="card">Meu curso</article>',
         ['.card { background: #e0e7ff; border-radius: 16px; padding: 20px; }','.card { background: #e0e7ff; border-radius: 0; padding: 20px; }','.card { color: #e0e7ff; border-radius: 16px; padding: 20px; }','.card { background: #111827; border-radius: 16px; padding: 20px; }'],0,'background colore o fundo; border-radius arredonda os cantos. O card de referência combina fundo lilás, cantos de 16px e padding de 20px.'),
        ('O espaço fica dentro da borda','Box model','<article class="card">Texto com espaço para respirar</article>',
         ['.card { border: 2px solid navy; margin: 24px; }','.card { border: 2px solid navy; padding: 0; }','.card { border: 2px solid navy; padding: 24px; }','.card { border: 2px solid navy; padding: 2px; }'],2,'A referência tem 24px entre o texto e a borda. Esse espaço é padding. margin pode afastar a caixa de outras caixas, mas não cria esse espaço interno.'),
        ('Dois itens na mesma linha','Flexbox','<div class="menu"><span>Início</span><span>Contato</span></div>',
         ['.menu { display: block; gap: 12px; }','.menu { display: flex; flex-direction: column; gap: 12px; }','.menu { display: flex; gap: 0; }','.menu { display: flex; gap: 12px; }'],3,'display: flex organiza os filhos em linha por padrão. gap: 12px cria o intervalo entre eles, como na referência.'),
        ('Um título centralizado','Tipografia','<h2>Notícias da turma</h2>',
         ['h2 { text-align: left; font-size: 28px; }','h2 { text-align: center; font-size: 28px; }','h2 { text-align: right; font-size: 28px; }','h2 { text-align: center; font-size: 14px; }'],1,'text-align: center centraliza o texto dentro da caixa do h2. font-size: 28px define o tamanho pedido; não muda o nível semântico do título.')]
    for i,(title,concept,html,options,answer,exp) in enumerate(visuals):
        target=html+'<style>'+options[answer]+'</style>'
        variants=[dict(code=html+'\n<style>\n'+css+'\n</style>',output='Este CSS reproduz a referência.' if j==answer else 'Compare o espaçamento, a cor, o alinhamento e o formato com a referência.',passed=j==answer) for j,css in enumerate(options)]
        question(541+i,'visual',title,concept,html+'\n<!-- Qual regra CSS reproduz a referência? -->',options,answer,exp,visual_target=target,visual_instruction=['Observe o fundo lilás e os cantos arredondados.','Reproduza o espaço interno de 24px.','Reproduza a linha com 12px entre os itens.','Reproduza o texto centralizado com 28px.'][i],repair_variants=variants,repair_expected='Este CSS reproduz a referência.')
    html='''<h2 id="titulo">[1] Cursos</h2>
<p class="aviso">[2] Matrículas abertas</p>
<p class="aviso" id="destaque">[3] Últimas vagas</p>
<nav><a href="#curso">[4] Ver cursos</a></nav>
<a href="#inicio">[5] Voltar ao início</a>'''
    for i,(rule,options,answer,exp) in enumerate([
      ('.aviso',['Apenas [1]','Apenas [2] e [3]','Apenas [3]','Todos os cinco elementos'],1,'O ponto seleciona uma classe. Os dois parágrafos têm class="aviso", então [2] e [3] correspondem a .aviso.'),
      ('#destaque',['Apenas [2] e [3]','Apenas [1]','Todos os parágrafos','Apenas [3]'],3,'O # inicia um seletor de id. Só o parágrafo [3] tem id="destaque". A classe aviso não muda essa correspondência.'),
      ('nav a',['Apenas [4]','Apenas [5]','Os links [4] e [5]','Apenas o elemento nav'],0,'O espaço indica descendência: nav a seleciona links dentro de nav. O link [5] está fora do nav, então não corresponde.'),
      ('h2',['Todos os elementos com id','Apenas [2]','Apenas [1]','Apenas os links'],2,'O seletor h2 procura pelo nome da tag. Só o elemento [1] é um h2.')]):
        question(551+i,'selectors','Quem essa regra alcança? '+rule,'Seletores CSS',html+'\n\n/* Qual grupo recebe a cor? */\n'+rule+' { color: purple; }',options,answer,exp,stage_markup=html,visual_instruction='Use os números da página para identificar os elementos selecionados. A prévia está sem a regra de cor para você fazer a previsão.')
    tasks=[
       ('O menu precisa de uma casa','Navegação semântica','<_____>\n    <a href="#inicio">Início</a>\n    <a href="#contato">Contato</a>\n</_____>',['<article>','<footer>','<nav>','<strong>'],2,'nav é apropriado para uma seção de navegação. Ele comunica a função desses links; o alinhamento visual fica por conta do CSS.','Um conjunto de links principais ajuda o visitante a se localizar. Qual tag representa essa função?','<a href="#inicio">Início</a> · <a href="#contato">Contato</a>'),
       ('Qual tag reúne o conteúdo principal?','Conteúdo principal','<header>Nome do site</header>\n<_____>\n    <h1>Sobre o curso</h1>\n    <p>Conheça nossa proposta.</p>\n</_____>\n<footer>Informações finais</footer>',['<main>','<head>','<title>','<nav>'],0,'main reúne o conteúdo principal da página. head guarda metadados; não é a região para o conteúdo visível do curso.','O cabeçalho e o rodapé já existem. Falta identificar a região com o conteúdo principal.','<h1>Sobre o curso</h1><p>Conheça nossa proposta.</p>'),
       ('Etapas que precisam seguir uma ordem','Listas ordenadas','<_____>\n    <li>Crie o arquivo HTML.</li>\n    <li>Adicione o CSS.</li>\n    <li>Teste no navegador.</li>\n</_____>',['<ul>','<p>','<section>','<ol>'],3,'ol representa uma lista em que a ordem dos itens importa. li representa cada etapa dentro dela.','A sequência de preparação precisa ficar clara. Escolha o contêiner adequado para os três itens.','<li>Crie o arquivo HTML.</li><li>Adicione o CSS.</li><li>Teste no navegador.</li>'),
       ('Uma notícia que faz sentido sozinha','Conteúdo independente','<main>\n    <_____>\n        <h2>Inscrições abertas</h2>\n        <p>O curso começa na próxima semana.</p>\n    </_____>\n</main>',['<span>','<article>','<label>','<head>'],1,'article é adequado para uma notícia que pode ser compreendida como conteúdo independente. O main continua reunindo o conteúdo principal da página.','Essa notícia poderia ser compartilhada e compreendida separadamente. Qual tag expressa isso?','<h2>Inscrições abertas</h2><p>O curso começa na próxima semana.</p>')]
    for i,(title,concept,code,options,answer,exp,instruction,inner) in enumerate(tasks):
        variants=[dict(code=code.replace('_____',tag[1:-1]),output='A tag expressa a função pedida no desafio.' if j==answer else 'O navegador pode exibir o conteúdo, mas a tag não expressa a função pedida.',passed=j==answer) for j,tag in enumerate(options)]
        question(561+i,'structure',title,concept,code,options,answer,exp,visual_instruction=instruction,repair_variants=variants,repair_expected='A tag expressa a função pedida no desafio.')
    for q in qs:
        if q['id'] in (541,551,561):
            q['reflection_prompt']={541:'Qual detalhe da referência ajudou você a escolher essa regra CSS?',551:'Como o seletor indica quais elementos recebem o estilo?',561:'Por que essa tag combina com a função dos links?'}[q['id']]
    return qs
