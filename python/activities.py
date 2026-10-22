"""Atividades autorais de vocabulário e depuração; saídas verificadas em Python."""
import contextlib
import io

VOCABULARY_CODE = '''class Mochila:
    def __init__(self, dono, capacidade):
        self.dono = dono
        self.capacidade = capacidade
        self.peso_atual = 0

    def adicionar_peso(self, peso):
        if peso > 0 and self.peso_atual + peso <= self.capacidade:
            self.peso_atual += peso
        else:
            print("Peso recusado")

ana = Mochila("Ana", 5)
ana.adicionar_peso(2)
'''

REFLECTIONS = {
    0: 'Olhe a criação da mochila: quais valores chegam ao construtor e qual atributo começa em zero?',
    4: 'Por que usar > em vez de >= para recusar o peso da mochila?',
    6: 'Por que o saldo deve continuar igual quando o cofre está fechado?',
    8: 'Por que verificar papel e tinta antes de descontar os recursos?',
    9: 'Por que nenhuma das duas notas deve mudar quando uma delas é inválida?',
    10: 'Por que o novo mês zera o consumo e os extras, mas preserva a franquia base?',
    11: 'Por que um andar válido não basta para permitir o movimento do elevador?',
    13: 'Por que a calibração deve ficar separada da leitura original?',
}


def execute(code):
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(code, '<teste-do-robo>', 'exec'), {})
    except AttributeError:
        return 'Erro de atributo: o objeto não possui o atributo solicitado.'
    return out.getvalue().strip()


def extra_questions():
    questions = []
    targets = [
        ('Mochila: o que esse nome representa?', 'Mochila', VOCABULARY_CODE.index('Mochila'), 0,
         'Mochila aparece na definição da classe. Ela é o modelo usado para criar objetos.'),
        ('E ana, o que representa aqui?', 'ana', VOCABULARY_CODE.index('ana ='), 1,
         'ana é a variável que referencia um objeto criado por Mochila("Ana", 5). A classe é Mochila; o objeto é uma instância dela.'),
        ('Uma informação guardada no objeto', 'self.peso_atual', VOCABULARY_CODE.index('self.peso_atual'), 2,
         'self.peso_atual acessa um atributo da instância. Esse atributo armazena o peso atual da mochila.'),
        ('Um comportamento da mochila', 'adicionar_peso', VOCABULARY_CODE.index('adicionar_peso'), 3,
         'adicionar_peso é um método: uma função definida na classe para representar um comportamento da mochila.'),
    ]
    for i, (title, token, start, answer, explanation) in enumerate(targets):
        questions.append(dict(id=321+i, title=title, concept='Vocabulário de POO', kind='Quem sou eu? 🔎',
                              activity='classify', code=VOCABULARY_CODE, focus={'start':start,'end':start+len(token)},
                              options=['Classe', 'Objeto (instância)', 'Atributo', 'Método'], answer=answer,
                              explanation=explanation, seconds=60, source='Prática • questão 6 — Mochila',
                              reflection_prompt='Qual é a diferença entre o nome da classe e a variável que referencia o objeto?' if i==1 else ''))
    cases = [
        dict(title='Pip perdeu o atributo energia', concept='self',
             code='''class Robo:
    def __init__(self, nome, energia):
        self.nome = nome
        energia = energia

pip = Robo("Pip", 80)
print("Energia:", pip.energia)''',
             broken='energia = energia', replacements=['self.energia = 0', 'energia = self.energia', 'self.energia = energia', 'self.nome = energia'], answer=2,
             expected='Energia: 80', diagnosis='Pip recebe a energia ao ser criado, mas esse valor não fica guardado como atributo da instância.',
             explanation='O valor 80 chega pelo parâmetro energia. Ao usar self.energia = energia, o construtor guarda esse valor no objeto. Sem self, a atribuição fica apenas na variável local e pip.energia não é criado.',
             reflection_prompt='Por que energia = energia não cria o atributo energia do robô?', source='Oficina • adaptação do exercício de meta de leitura'),
        dict(title='Gastar energia está carregando o robô', concept='Alteração de estado',
             code='''class Robo:
    def __init__(self, energia):
        self.energia = energia

    def gastar(self, valor):
        if valor <= 0:
            print("Valor inválido")
        elif valor > self.energia:
            print("Energia insuficiente")
        else:
            self.energia += valor

pip = Robo(50)
pip.gastar(20)
print("Energia:", pip.energia)''',
             broken='self.energia += valor', replacements=['self.energia -= valor', 'self.energia = valor', 'self.energia += valor', 'self.energia = 0'], answer=0,
             expected='Energia: 30', diagnosis='Pip deveria gastar energia, mas está ganhando. Veja qual operação o método usa depois das validações.',
             explanation='Pip começa com 50 de energia e gasta 20. Depois das validações, self.energia -= valor faz esse desconto: 50 − 20 = 30.',
             reflection_prompt='O que pode dar errado se a energia mudar antes de o método validar o valor?', source='Oficina • adaptação dos exercícios de mochila e impressora'),
        dict(title='O robô está andando desligado', concept='Estado booleano e validação',
             code='''class Robo:
    def __init__(self):
        self.ligado = False
        self.passos = 0

    def andar(self):
        if self.ligado == False:
            self.passos += 1
        else:
            print("Robô desligado")

pip = Robo()
pip.andar()
print("Passos:", pip.passos)''',
             broken='self.ligado == False', replacements=['self.passos >= 0', 'self.ligado == False', 'self.passos < 10', 'self.ligado == True'], answer=3,
             expected='Robô desligado\nPassos: 0', diagnosis='Pip está desligado e mesmo assim anda. Quando o movimento for recusado, o atributo passos precisa continuar com o mesmo valor.',
             explanation='A condição deve permitir o movimento quando ligado é True. Como o robô começa desligado, a chamada exibe a mensagem e mantém zero passos.',
             reflection_prompt='O que a condição precisa verificar antes de alterar passos?', source='Oficina • adaptação dos exercícios de cofre e elevador'),
        dict(title='A impressora robô está sem tinta', concept='Operação recusada',
             code='''class RoboImpressor:
    def __init__(self, folhas, tinta):
        self.folhas = folhas
        self.tinta = tinta

    def imprimir(self, paginas):
        if paginas <= 0:
            print("Quantidade inválida")
        elif paginas > self.folhas and paginas * 2 > self.tinta:
            print("Recursos insuficientes")
        else:
            self.folhas -= paginas
            self.tinta -= paginas * 2

a = RoboImpressor(4, 6)
b = RoboImpressor(6, 20)
a.imprimir(4)
b.imprimir(2)
print(a.folhas, a.tinta)
print(b.folhas, b.tinta)''',
             broken='paginas > self.folhas and paginas * 2 > self.tinta', replacements=['paginas > self.folhas', 'paginas > self.folhas or paginas * 2 > self.tinta', 'paginas > self.folhas and paginas * 2 > self.tinta', 'paginas * 2 < self.tinta'], answer=1,
             expected='Recursos insuficientes\n4 6\n4 16', diagnosis='Há papel, mas falta tinta para terminar a impressão. Se qualquer um dos recursos faltar, a impressão inteira deve ser recusada.',
             explanation='O operador or recusa quando pelo menos um recurso é insuficiente. O objeto a preserva 4 folhas e tinta 6; b imprime duas páginas e termina com 4 folhas e tinta 16.',
             reflection_prompt='Por que usar or para detectar recursos insuficientes neste caso?', source='Avaliação • exercício 1 — Impressora'),
    ]
    for i, case in enumerate(cases):
        variants = []
        for replacement in case['replacements']:
            code = case['code'].replace(case['broken'], replacement, 1)
            output = execute(code)
            variants.append(dict(code=code, output=output, passed=output==case['expected']))
        assert [j for j,v in enumerate(variants) if v['passed']] == [case['answer']]
        questions.append(dict(id=331+i, title=case['title'], concept=case['concept'], kind='Conserte o robô 🤖',
                              activity='repair', code=case['code'], options=case['replacements'], answer=case['answer'],
                              explanation=case['explanation'], seconds=120 if i==3 else 90, source=case['source'],
                              focus={'start':case['code'].index(case['broken']),'end':case['code'].index(case['broken'])+len(case['broken'])},
                              repair_diagnosis=case['diagnosis'], repair_expected=case['expected'],
                              repair_variants=variants, repair_original_output=execute(case['code']),
                              reflection_prompt=case['reflection_prompt']))
    return questions


def make_bank(base):
    questions = [dict(q, id=301+i, curriculum='poo-v3',activity='quiz',reflection_prompt=REFLECTIONS.get(i,'')) for i,q in enumerate(base)]
    questions.extend(dict(q,curriculum='poo-v3') for q in extra_questions())
    order = [301,321,302,331,303,322,304,305,332,306,323,307,308,333,309,324,310,311,334,312,313,314,315]
    for q in questions:
        q['position'] = order.index(q['id'])
    return sorted(questions,key=lambda q:q['position'])
