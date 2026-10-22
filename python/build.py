"""Banco didático de questões: exemplo de orientação a objetos em Python."""
from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass
class Questao:
    title: str
    concept: str
    kind: str
    code: str
    options: list[str]
    answer: int
    explanation: str
    seconds: int = 40

QUESTOES = [
Questao('Uma receita para criar personagens', 'Classe e objeto', 'Conceito', '', ['Classe é um modelo; objeto é uma instância desse modelo.', 'Classe e objeto são sempre a mesma coisa.', 'Objeto é apenas o nome de uma variável.', 'Uma classe só pode criar um objeto.'],0,'Uma classe define atributos e comportamentos. Podemos criar vários objetos a partir dela.'),
Questao('Quem nasceu aqui?', 'Instanciação', 'Preveja a saída', 'class Personagem:\n    pass\n\nluna = Personagem()\nprint(type(luna).__name__)', ['luna','Personagem','str','None'],1,'Personagem() cria uma instância da classe Personagem. O nome do tipo é Personagem.'),
Questao('A mochila de Luna', 'Atributos', 'Preveja a saída', 'class Heroi:\n    def __init__(self, nome):\n        self.nome = nome\n        self.moedas = 10\n\nluna = Heroi("Luna")\nluna.moedas += 5\nprint(luna.moedas)', ['10','5','15','Erro'],2,'O atributo moedas começa em 10. Somar 5 altera o valor do objeto para 15.'),
Questao('Complete o construtor', 'Construtor', 'Complete o código', 'class Robo:\n    def ______(self, nome):\n        self.nome = nome', ['start','__init__','create','__main__'],1,'__init__ inicializa a instância recém-criada. Ele recebe self e os demais argumentos.'),
Questao('O bug escondido', 'self', 'Detetive de bugs', 'class Robo:\n    def __init__(self, nome):\n        nome = nome\n\nr = Robo("Pip")\nprint(r.nome)', ['Trocar nome = nome por self.nome = nome.','Remover o parâmetro self.','Trocar print por return.','Trocar Robo por robo.'],0,'nome = nome só reatribui o parâmetro local. self.nome = nome guarda o valor na instância.'),
Questao('Dois heróis, duas energias', 'Instâncias independentes', 'Preveja a saída', 'class Heroi:\n    def __init__(self):\n        self.energia = 100\n\na = Heroi()\nb = Heroi()\na.energia -= 30\nprint(b.energia)', ['70','30','100','0'],2,'Cada instância tem seu próprio atributo energia. Alterar a não altera b.'),
Questao('O que é um método?', 'Métodos', 'Conceito', '', ['Uma função definida dentro da classe.','Qualquer número guardado em uma variável.','Um arquivo Python.','Uma cópia automática de um objeto.'],0,'Métodos definem comportamentos. Em um método de instância, self representa o objeto que o chamou.'),
Questao('Ativando o escudo', 'Chamada de método', 'Complete o código', 'class Heroi:\n    def defender(self):\n        return "Escudo ativo!"\n\nluna = Heroi()\n# Como chamar o método?', ['Heroi = defender()','luna.defender','luna.defender()','def defender(luna)'],2,'luna.defender() chama o método no objeto luna. Sem os parênteses, temos uma referência ao método.'),
Questao('Dano calculado', 'Alteração de estado', 'Preveja a saída', 'class Heroi:\n    def __init__(self):\n        self.vida = 100\n\n    def receber_dano(self, dano):\n        self.vida -= dano\n\nh = Heroi()\nh.receber_dano(25)\nh.receber_dano(10)\nprint(h.vida)', ['75','90','65','35'],2,'O primeiro método reduz a vida para 75. O segundo a reduz para 65.'),
Questao('Quem é self?', 'self', 'Conceito', 'luna.receber_dano(10)', ['O número 10.','A instância luna dentro do método.','Todas as instâncias da classe.','O nome do arquivo.'],1,'Ao chamar um método de instância, Python passa o próprio objeto como primeiro argumento, convencionalmente chamado self.'),
Questao('Retornar ou mostrar?', 'return', 'Preveja a saída', 'class Calculadora:\n    def dobro(self, numero):\n        return numero * 2\n\nc = Calculadora()\nresultado = c.dobro(4)\nprint(resultado + 1)', ['8','9','4','None'],1,'O método retorna 8, que fica em resultado. Depois somamos 1 e mostramos 9.'),
Questao('O método sem self', 'self', 'Detetive de bugs', 'class Gato:\n    def miar():\n        return "Miau"\n\ng = Gato()\ng.miar()', ['Falta print dentro da classe.','Gato precisa ser uma string.','O método deve receber self: def miar(self):','É obrigatório usar __init__.'],2,'A chamada pela instância passa g ao método. Sem parâmetro para recebê-lo, ocorre TypeError.'),
Questao('Missão final: inventário', 'Objetos e métodos', 'Chefe final', 'class Mochila:\n    def __init__(self):\n        self.itens = []\n\n    def guardar(self, item):\n        self.itens.append(item)\n\na = Mochila()\nb = Mochila()\na.guardar("poção")\na.guardar("mapa")\nb.guardar("chave")\nprint(len(a.itens), len(b.itens))', ['3 3','2 1','1 2','0 0'],1,'As listas são criadas em cada __init__, uma por instância. a tem dois itens e b tem um.',60),
Questao('Missão final: evolução', 'Estado e retorno', 'Chefe final', 'class Heroi:\n    def __init__(self, nome):\n        self.nome = nome\n        self.nivel = 1\n\n    def evoluir(self):\n        self.nivel += 1\n        return self.nivel\n\nh = Heroi("Luna")\nx = h.evoluir()\nh.evoluir()\nprint(x, h.nivel)', ['3 3','2 2','2 3','1 3'],2,'x recebe o inteiro 2 na primeira chamada. A segunda muda o nível para 3, sem alterar x.',60),
Questao('Escolha o modelo', 'Modelagem', 'Conceito', '', ['Uma classe Aluno com nome e método apresentar().','Uma classe para cada letra de um nome.','Usar somente print, sem guardar informações.','Criar uma classe diferente para cada aluno da turma.'],0,'Uma classe Aluno representa características e comportamentos comuns. Cada estudante pode ser uma instância.'),
]

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    questions = [dict(id=i+1, **asdict(q)) for i,q in enumerate(QUESTOES)]
    for q in questions:
        assert len(q['options']) == 4 and 0 <= q['answer'] < 4
        assert q['seconds'] >= 10
    (root/'site/questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
    payload = json.dumps(questions,ensure_ascii=False).replace("'", "''")
    (root/'supabase/02-questions.sql').write_text("-- Banco de questões de Mauricésar Barbosa. Execute após 01-schema.sql.\ninsert into public.pq_questions(id, data) select (q->>'id')::int, q from jsonb_array_elements('"+payload+"'::jsonb) q on conflict(id) do update set data=excluded.data;\n")
    print(f'{len(questions)} questões validadas e geradas.')
