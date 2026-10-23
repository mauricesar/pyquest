"""HTML/CSS: questões autorais baseadas nos chats indicados pelo professor.
Estruturas HTML e projetos didáticos HUGO XMIN / Simple.css; sem JS para alunos.
"""
HTML_SOURCE='Introdução ao HTML • exercícios básicos e estrutura de páginas'
CSS_SOURCE='Projetos HTML/CSS • reprodução didática de HUGO XMIN e Simple.css'

def web_bank():
    questions=[]
    def add(title,concept,code,options,answer,explanation,reflection='',source=HTML_SOURCE):
        questions.append(dict(id=501+len(questions),subject='html-css',curriculum='web-v1',activity='quiz',kind='Leia o código',title=title,concept=concept,code=code,options=options,answer=answer,explanation=explanation,reflection_prompt=reflection,seconds=90,source=source))
    add('O título aparece onde?','Estrutura do documento','''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Meu primeiro site</title>
</head>
<body>
    <h1>Olá, turma!</h1>
</body>
</html>''',['Os dois textos aparecem apenas na aba.','Meu primeiro site aparece na aba; Olá, turma! aparece no conteúdo.','title e h1 têm a mesma função.','O texto de h1 fica dentro de head.'],1,'title define o título do documento, normalmente exibido na aba. O h1 está no body e aparece como título principal do conteúdo.','Por que title e h1 podem ter textos diferentes?')
    add('Uma seção dentro da página','Hierarquia de títulos','''<h1>Minha apresentação</h1>
<h2>Meus interesses</h2>
<p>Gosto de tecnologia e música.</p>''',['h2 cria uma segunda aba.','h2 serve apenas para deixar o texto menor.','p substitui o título principal.','h2 indica uma seção subordinada ao título h1.'],3,'Os níveis h1, h2 e h3 expressam a hierarquia do conteúdo. O tamanho visual pode ser ajustado com CSS, sem trocar o nível só pela aparência.')
    add('Como marcar uma informação importante?','Semântica do texto','<p>_____ Traga seu caderno. _____</p>',['<strong> e </strong>','<br> e </br>','<img> e </img>','<title> e </title>'],0,'strong indica que o conteúdo tem importância. Por padrão costuma aparecer em negrito, mas seu papel não se limita à aparência.','Por que escolher strong pela importância do texto, e não só pelo negrito?')
    add('Ingredientes ou etapas?','Listas','''<h2>Modo de preparo</h2>
<ol>
    <li>Misture os ingredientes.</li>
    <li>Leve ao forno.</li>
</ol>''',['ol cria uma lista sem itens.','li define a cor da lista.','ol é adequado porque as etapas seguem uma sequência.','Para receitas, apenas ul é permitido.'],2,'ol representa uma lista ordenada. Aqui, a sequência das etapas importa. Cada li representa um item, tanto em ol quanto em ul.')
    add('Um atalho para o contato','Links internos','''<a href="#contato">Fale conosco</a>
<section id="contato">
    <h2>Contato</h2>
</section>''',['O navegador procura um elemento com id="contato" na página.','O navegador cria um arquivo contato.html.','O link envia um e-mail automaticamente.','O texto Contato precisa ser o nome de uma classe CSS.'],0,'O fragmento #contato aponta para o id contato no próprio documento. O navegador pode rolar a página até esse elemento.','O que precisa coincidir entre href e id para o atalho funcionar?')
    add('A imagem também precisa de contexto','Imagens e atributos','<img src="imagens/teclado.jpg" alt="Teclado para computador">',['alt muda o caminho do arquivo.','src descreve a imagem para leitores de tela.','alt define a largura da imagem.','src aponta para o arquivo; alt oferece uma alternativa textual.'],3,'src indica onde buscar a imagem. alt fornece uma alternativa textual; a descrição deve fazer sentido para a função da imagem na página.','Como alt ajuda quando a imagem não pode ser vista?')
    add('Onde entra a notícia?','HTML semântico','''<main>
    <article>
        <h2>Novidades do curso</h2>
        <p>As inscrições estão abertas.</p>
    </article>
</main>''',['article só pode conter imagens.','article representa um conteúdo que faz sentido de forma independente.','main é usado para guardar apenas metadados.','As tags semânticas impedem o uso de CSS.'],1,'Uma notícia é um bom exemplo de article porque pode ser compreendida como conteúdo independente. main reúne o conteúdo principal da página.')
    add('O rótulo conversa com qual campo?','Formulários acessíveis','''<label for="email">Seu e-mail</label>
<input id="email" name="email" type="email" required>''',['for deve repetir o placeholder.','required salva o cadastro em um banco.','for associa o rótulo ao campo com o mesmo id.','type="email" garante que o endereço existe.'],2,'for="email" associa o label ao input cujo id é email. required pede preenchimento na validação do navegador; type="email" verifica o formato básico, sem confirmar a existência do endereço.','Por que manter o label mesmo quando o campo tem placeholder?')
    add('Como o HTML encontra o CSS?','Folha de estilos externa','''<head>
    <link rel="stylesheet" href="style.css">
</head>''',['O navegador carrega style.css como folha de estilos.','link transforma CSS em JavaScript.','O CSS precisa ficar dentro de body para funcionar.','href indica o título da aba.'],0,'rel="stylesheet" identifica a relação com uma folha de estilos. href indica o caminho do arquivo, relativo ao documento neste exemplo.',source=CSS_SOURCE)
    add('Qual regra alcança os cards?','Seletores CSS','''<article class="card">Curso de HTML</article>
<article class="card">Curso de CSS</article>

/* No arquivo CSS: */
.card { color: navy; }''',['Apenas o primeiro article recebe a cor.','A regra seleciona um id chamado card.','A regra seleciona somente a tag card.','Os dois elementos com class="card" recebem a cor.'],3,'O ponto inicia um seletor de classe. Todos os elementos que têm a classe card correspondem a .card, incluindo os dois article.','Qual é a diferença entre .card no CSS e class="card" no HTML?',CSS_SOURCE)
    add('Espaço dentro ou fora?','Box model','''.card {
    padding: 20px;
    margin: 12px;
    border: 1px solid navy;
}''',['margin cria espaço entre o conteúdo e a borda.','padding fica entre o conteúdo e a borda; margin fica fora da borda.','padding e margin são sempre iguais.','border substitui os dois espaçamentos.'],1,'Imagine o card como uma caixa: padding afasta o conteúdo da borda por dentro; margin participa do espaçamento do lado de fora.','Qual propriedade você mudaria para afastar o texto da borda, sem aumentar a margem externa?',CSS_SOURCE)
    add('Uma coluna confortável para leitura','Largura e alinhamento','''main {
    max-width: 800px;
    margin: 0 auto;
}''',['main ocupa sempre exatamente 800px, mesmo em telas menores.','O texto fica automaticamente centralizado.','A largura é limitada a 800px, e as margens laterais automáticas centralizam a caixa quando há espaço.','As margens superior e inferior viram automáticas.'],2,'max-width define um limite máximo, não uma largura mínima. Em uma caixa de bloco comum com espaço disponível, margin: 0 auto distribui as margens laterais igualmente. O texto não é centralizado por essa regra.',source=CSS_SOURCE)
    add('O menu lado a lado','Flexbox','''nav ul {
    display: flex;
    gap: 16px;
    list-style: none;
}''',['flex organiza os filhos diretos em uma linha por padrão, e gap define o espaço entre eles.','gap altera o tamanho da fonte.','list-style: none apaga os links.','flex exige JavaScript para organizar o menu.'],0,'O contêiner flex organiza seus filhos diretos. A direção padrão é row; gap cria espaço entre os itens e list-style: none retira os marcadores da lista.',source=CSS_SOURCE)
    add('O botão mudou quando o mouse chegou','Pseudo-classe :hover','''a:hover {
    color: purple;
    text-decoration: underline;
}''',['A regra vale apenas depois de clicar no link.','hover cria um novo link.','A regra muda o HTML para sempre.','A regra se aplica enquanto o ponteiro está sobre o link.'],3,'A pseudo-classe :hover representa o estado em que o ponteiro está sobre o elemento. Em telas de toque esse comportamento pode variar; não deve ser a única forma de comunicar uma informação.',source=CSS_SOURCE)
    add('O card sobe, mas sem um salto brusco','Transições CSS','''.card {
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-8px);
}''',['transition inicia o movimento sem precisar de uma mudança.','A mudança de transform ocorre ao longo de 0,3 segundo; translateY(-8px) desloca o card para cima.','translateY(-8px) aumenta a margem em 8px.','ease define a cor da sombra.'],1,'O :hover muda transform. transition suaviza a passagem entre os valores durante 0,3 segundo; o deslocamento negativo no eixo Y leva o card para cima. Na regra base, a transição também pode suavizar a volta.','Qual é o papel de :hover e qual é o papel de transition nesse exemplo?',CSS_SOURCE)
    vocab=[
      ('O que é href neste trecho?','<a href="#sobre">Sobre</a>','href',['Tag de abertura','Atributo HTML','Seletor CSS','Propriedade CSS'],1,'href é um atributo da tag a. Seu valor indica o destino do link.'),
      ('Quem seleciona os cards?','.card { color: navy; }','.card',['Seletor CSS','Valor CSS','Atributo HTML','Tag HTML'],0,'.card é o seletor: ele identifica os elementos aos quais a regra se aplica.'),
      ('O que estamos definindo?','.card { padding: 16px; }','padding',['Valor CSS','Tag HTML','Propriedade CSS','Classe de Python'],2,'padding é a propriedade CSS. Ela define o espaçamento interno; 16px é o valor escolhido.'),
      ('E 16px, qual é o seu papel?','.card { padding: 16px; }','16px',['Seletor CSS','Atributo HTML','Método','Valor CSS'],3,'16px é o valor da declaração padding: 16px. O número e a unidade definem o espaçamento nesse exemplo.')]
    for i,(title,code,token,options,answer,exp) in enumerate(vocab):
      start=code.index(token)
      questions.append(dict(id=521+i,subject='html-css',curriculum='web-v1',activity='classify',kind='Quem sou eu? 🔎',title=title,concept='Vocabulário de HTML/CSS',code=code,focus=dict(start=start,end=start+len(token)),options=options,answer=answer,explanation=exp,reflection_prompt='',seconds=60,source=HTML_SOURCE if i==0 else CSS_SOURCE))
    repairs=[
      dict(title='O link não leva ao contato',concept='Links internos',code='<a src="#contato">Contato</a>\n<section id="contato">Fale com a turma</section>',broken='src="#contato"',options=['alt="#contato"','href="contato"','href="#contato"','class="contato"'],answer=2,diagnosis='O destino existe, mas a tag a está usando o atributo errado para criar o link.',expected='O link aponta para o elemento com id="contato".',outputs=['alt não define o destino de um link.','O destino é um caminho relativo chamado contato, sem o fragmento #.','O link aponta para o elemento com id="contato".','class identifica uma classe, mas não cria um destino de navegação.'],reflection='Por que src não substitui href em uma tag a?'),
      dict(title='A cor não chegou ao card',concept='Seletores CSS',code='<p class="card">Curso de CSS</p>\n<style>\ncard { color: navy; }\n</style>',broken='card {',options=['#card {','.card {','href {','padding {'],answer=1,diagnosis='O elemento tem uma classe chamada card. O seletor atual procura uma tag card.',expected='O parágrafo recebe a cor navy.',outputs=['O seletor procura id="card", que não existe aqui.','O parágrafo recebe a cor navy.','O seletor procura uma tag href.','O seletor procura uma tag padding.'],reflection='O que muda quando colocamos um ponto antes de card?'),
      dict(title='O texto continua grudado na borda',concept='Box model',code='<div class="card">Olá, turma!</div>\n<style>\n.card { border: 1px solid navy; padding: 20; }\n</style>',broken='padding: 20;',options=['padding: 20px;','padding: -20px;','padding: auto;','padding: 20;'],answer=0,diagnosis='O navegador ignora esse padding: o comprimento diferente de zero precisa de uma unidade válida.',expected='O card ganha 20px de espaçamento interno nos quatro lados.',outputs=['O card ganha 20px de espaçamento interno nos quatro lados.','Padding negativo é inválido.','auto não é um valor válido para padding.','O comprimento 20 está sem unidade e é inválido nesse caso.'],reflection='Por que 20px é válido para padding, mas 20 sozinho não é?'),
      dict(title='Clicar no rótulo não seleciona o campo',concept='Formulários acessíveis',code='<label for="nome">Seu nome</label>\n<input id="email" name="nome" type="text">',broken='id="email"',options=['class="nome"','id="campo"','title="nome"','id="nome"'],answer=3,diagnosis='O valor de for precisa corresponder ao id do input que o rótulo descreve.',expected='O rótulo Seu nome fica associado ao input.',outputs=['class não substitui id na associação com for.','O id campo ainda é diferente de nome.','title não substitui id na associação com for.','O rótulo Seu nome fica associado ao input.'],reflection='Por que ter name="nome" não resolve sozinho a associação com o label?')]
    for i,r in enumerate(repairs):
      variants=[dict(code=r['code'].replace(r['broken'],o,1),output=r['outputs'][j],passed=j==r['answer']) for j,o in enumerate(r['options'])]
      start=r['code'].index(r['broken'])
      questions.append(dict(id=531+i,subject='html-css',curriculum='web-v1',activity='repair',kind='Conserte a página 🛠️',title=r['title'],concept=r['concept'],code=r['code'],focus=dict(start=start,end=start+len(r['broken'])),options=r['options'],answer=r['answer'],explanation=r['outputs'][r['answer']]+' '+r['diagnosis'],repair_diagnosis=r['diagnosis'],repair_expected=r['expected'],repair_variants=variants,repair_original_output=r['diagnosis'],reflection_prompt=r['reflection'],seconds=90,source=HTML_SOURCE if i in(0,3) else CSS_SOURCE))
    order=[501,521,502,531,503,522,504,505,532,506,523,507,508,533,509,524,510,511,534,512,513,514,515]
    for q in questions:q['position']=order.index(q['id'])
    return sorted(questions,key=lambda q:q['position'])
