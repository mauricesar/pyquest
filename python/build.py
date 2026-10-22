"""Questões de Mauricésar Barbosa alinhadas aos exercícios já trabalhados."""
from dataclasses import dataclass, asdict
from pathlib import Path
import json

CURRICULUM = 'poo-v2'

@dataclass
class Questao:
    title: str
    concept: str
    kind: str
    code: str
    options: list[str]
    answer: int
    explanation: str
    seconds: int = 60
    source: str = ''
    expected_output: str | None = None

QUESTOES = [
Questao('Mochila: o que o construtor guarda?', 'Construtor e atributos', 'Preveja a saída', '''class Mochila:
    def __init__(self, dono, capacidade):
        self.dono = dono
        self.capacidade = capacidade
        self.peso_atual = 0

m = Mochila("Ana", 5)
print(m.dono, m.capacidade, m.peso_atual)''',
['Ana 5 5','Ana 0 5','Ana 5 0','dono capacidade peso_atual'],2,
'O construtor recebe dono e capacidade. peso_atual é um atributo inicializado em zero, sem precisar ser recebido como parâmetro.',
source='Prática • questão 6 — Mochila',expected_output='Ana 5 0'),
Questao('Leitura: qual atributo está faltando?', 'self', 'Detetive de bugs', '''class MetaLeitura:
    def __init__(self, nome, meta):
        self.nome = nome
        self.meta = meta
        paginas_lidas = 0

leitor = MetaLeitura("Carla", 20)
print(leitor.paginas_lidas)''',
['Trocar paginas_lidas = 0 por self.paginas_lidas = 0.','Retirar self dos outros atributos.','Trocar o valor inicial de 0 para 20.','Criar uma classe diferente para cada leitor.'],0,
'Para guardar um atributo na instância, usamos self.paginas_lidas. A atribuição sem self cria apenas uma variável local no construtor.',
source='Prática • questão 7 — Meta de leitura'),
Questao('Equipe: como registrar uma vitória?', 'Chamada de método', 'Complete o código', '''class Equipe:
    def __init__(self, nome):
        self.nome = nome
        self.pontos = 0
        self.vitorias = 0

    def registrar_vitoria(self):
        self.vitorias += 1
        self.pontos += 3

azul = Equipe("Azul")
# Qual chamada registra uma vitória de Azul?''',
['azul.registrar_vitoria','registrar_vitoria(azul)','Equipe = registrar_vitoria()','azul.registrar_vitoria()'],3,
'azul.registrar_vitoria() executa o método no objeto azul. O próprio objeto corresponde a self dentro do método.',
source='Prática • questão 8 — Equipe'),
Questao('Dois leitores, dois totais', 'Instâncias independentes', 'Preveja a saída', '''class MetaLeitura:
    def __init__(self, nome):
        self.nome = nome
        self.paginas_lidas = 0

    def registrar_leitura(self, paginas):
        if paginas > 0:
            self.paginas_lidas += paginas
        else:
            print("Quantidade inválida")

carla = MetaLeitura("Carla")
diego = MetaLeitura("Diego")
carla.registrar_leitura(8)
carla.registrar_leitura(15)
diego.registrar_leitura(5)
print(carla.paginas_lidas, diego.paginas_lidas)''',
['28 28','23 5','15 5','23 23'],1,
'Carla acumula 8 + 15 = 23 páginas. Diego recebe apenas 5. Alterar um objeto não modifica o atributo do outro.',90,
'Prática • questão 7 — Meta de leitura','23 5'),
Questao('Mochila: atingir o limite é permitido', 'Validação de limites', 'Complete o código', '''# Trecho do método adicionar_peso(self, peso):
if peso <= 0:
    print("Valor inválido")
elif ______:
    print("Capacidade excedida")
else:
    self.peso_atual += peso

# Recuse apenas se o novo peso ultrapassar a capacidade.
# É permitido atingir exatamente a capacidade.''',
['self.peso_atual + peso >= self.capacidade','peso < self.capacidade','self.peso_atual + peso > self.capacidade','self.peso_atual > peso'],2,
'A comparação deve usar >. Usar >= recusaria também o peso exatamente igual à capacidade, que o exercício permite.',
source='Prática • questão 6 — Mochila'),
Questao('Equipe: calcular sem guardar outro atributo', 'return e cálculo', 'Preveja a saída', '''class Equipe:
    def __init__(self, nome):
        self.nome = nome
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0

    def registrar_vitoria(self):
        self.vitorias += 1

    def registrar_empate(self):
        self.empates += 1

    def calcular_jogos(self):
        return self.vitorias + self.empates + self.derrotas

azul = Equipe("Azul")
azul.registrar_vitoria()
azul.registrar_vitoria()
azul.registrar_empate()
total = azul.calcular_jogos()
print(total)''',
['3','7','2','0'],0,
'O método retorna 2 + 1 + 0 = 3 jogos. Sete seria a pontuação dessa campanha, não a quantidade de jogos. Não é necessário criar um atributo total_jogos.',
90, source='Prática • questão 8 — Equipe',expected_output='3'),
Questao('Cofre fechado: o saldo deve mudar?', 'Estado booleano e validação', 'Preveja a saída', '''class Cofre:
    def __init__(self, dono):
        self.dono = dono
        self.saldo = 0
        self.aberto = False

    def guardar(self, valor):
        if self.aberto == False:
            print("Abra o cofre")
        elif valor <= 0:
            print("Valor inválido")
        else:
            self.saldo += valor

c = Cofre("Elisa")
c.guardar(20)
print(c.saldo)''',
['Mostra Abra o cofre e depois 20.','Mostra apenas 20.','O cofre abre automaticamente e guarda 20.','Mostra Abra o cofre e depois 0.'],3,
'O cofre começa fechado. A primeira condição recusa a operação; o ramo que soma ao saldo não é executado. O saldo permanece zero.',90,
'Prática • questão 9 — Cofre','Abra o cofre\n0'),
Questao('Pintura: um método chama outro', 'Composição de métodos', 'Preveja a saída', '''class ServicoPintura:
    def __init__(self, largura, altura, preco_metro):
        self.largura = largura
        self.altura = altura
        self.preco_metro = preco_metro

    def calcular_area(self):
        return self.largura * self.altura

    def calcular_valor(self):
        return self.calcular_area() * self.preco_metro

s = ServicoPintura(5, 3, 10)
print(s.calcular_valor())''',
['15','150','50','30'],1,
'A área é 5 × 3 = 15 m². calcular_valor() chama self.calcular_area() e multiplica 15 por 10, retornando 150.',90,
'Prática • questão 10 — Serviço de pintura','150'),
Questao('Impressora: validar antes de descontar', 'Operação recusada', 'Detetive de bugs', '''# Trecho INCORRETO de imprimir(self, paginas):
self.folhas -= paginas
self.tinta -= paginas * 2
if self.folhas < 0 or self.tinta < 0:
    print("Recursos insuficientes")

# Uma solicitação recusada deve preservar TODOS
# os atributos. Não pode haver impressão parcial.''',
['Só trocar a mensagem exibida.','Sempre imprimir, mesmo com tinta insuficiente.','Validar páginas positivas, papel e tinta antes de alterar atributos.','Zerar papel e tinta quando a operação for recusada.'],2,
'O trecho desconta os recursos antes de saber se a impressão é possível. Primeiro valide páginas > 0, folhas suficientes e tinta >= paginas * 2. Só então desconte os recursos e atualize os contadores.',90,
'Avaliação • exercício 1 — Impressora'),
Questao('Aluno: notas inválidas preservam o registro', 'Validação conjunta', 'Preveja a saída', '''class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.nota1 = 0
        self.nota2 = 0

    def registrar_notas(self, n1, n2):
        if 0 <= n1 <= 10 and 0 <= n2 <= 10:
            self.nota1 = n1
            self.nota2 = n2
        else:
            print("Notas inválidas")

b = Aluno("Bruno")
b.registrar_notas(5, 7)
b.registrar_notas(9, 12)
print(b.nota1, b.nota2)''',
['Mostra Notas inválidas e depois 5 7.','Mostra Notas inválidas e depois 9 7.','Mostra 9 12, sem recusar.','Mostra Notas inválidas e depois 0 0.'],0,
'Como 12 está fora do intervalo, a segunda chamada não altera nenhuma nota. As notas 5 e 7 da primeira chamada são preservadas juntas.',90,
'Avaliação • exercício 2 — Aluno','Notas inválidas\n5 7'),
Questao('Internet: começar um novo mês', 'Reinicialização de estado', 'Conceito', '''# Atributos do PlanoInternet de Carla:
# titular = "Carla"
# franquia_base = 10
# dados_extras = 5
# consumo = 8
# gasto_extras = 25

# O que iniciar_novo_mes() deve fazer,
# considerando a ampliação do exercício?''',
['Zerar apenas consumo e manter extras e gasto do mês anterior.','Zerar também a franquia_base e apagar o titular.','Somar dados_extras à franquia_base para o próximo mês.','Zerar consumo, dados_extras e gasto_extras; preservar titular e franquia_base.'],3,
'Consumo, extras e gasto_extras são dados mensais e voltam a zero. Titular e franquia_base identificam o contrato e permanecem iguais. Os dados disponíveis voltam a 10 GB.',
source='Avaliação • exercício 3 — Plano de internet, ampliação'),
Questao('Elevador: a porta impede o movimento', 'Condições e preservação de estado', 'Preveja a saída', '''class Elevador:
    def __init__(self, ultimo_andar):
        self.ultimo_andar = ultimo_andar
        self.andar_atual = 0
        self.porta_aberta = True

    def ir_para_andar(self, destino):
        if destino < 0 or destino > self.ultimo_andar:
            print("Andar inválido")
        elif self.porta_aberta:
            print("Feche a porta")
        else:
            self.andar_atual = destino

social = Elevador(8)
social.ir_para_andar(5)
print(social.andar_atual)''',
['Mostra apenas 5.','Mostra Feche a porta e depois 0.','Mostra Feche a porta e depois 5.','Mostra Andar inválido e depois 0.'],1,
'O andar 5 existe, mas a porta está aberta. A movimentação é recusada e andar_atual continua em zero. A verificação precisa ocorrer antes da alteração.',90,
'Avaliação • exercício 4 — Elevador','Feche a porta\n0'),
Questao('Missão final: votos brancos entram no percentual?', 'Percentual e retorno', 'Chefe final', '''class Votacao:
    def __init__(self):
        self.votos_a = 0
        self.votos_b = 0
        self.votos_brancos = 0

    def votar(self, opcao):
        if opcao == 1:
            self.votos_a += 1
        elif opcao == 2:
            self.votos_b += 1
        elif opcao == 0:
            self.votos_brancos += 1
        else:
            print("Opção inválida")

    def calcular_total(self):
        return self.votos_a + self.votos_b + self.votos_brancos

    def percentual_a(self):
        total = self.calcular_total()
        if total == 0:
            return 0
        return self.votos_a * 100 / total

# Trecho reduzido: a votação está aberta.
v = Votacao()
v.votar(1)
v.votar(2)
v.votar(1)
v.votar(0)
print(v.percentual_a())''',
['66.66666666666667','25.0','50.0','100.0'],2,
'O total inclui os votos brancos: 2 + 1 + 1 = 4. O projeto A tem 2 × 100 / 4 = 50%. Incluir brancos no percentual não significa usá-los para escolher o vencedor.',120,
'Avaliação • exercício 5 — Votação, ampliação','50.0'),
Questao('Missão final: calibrar substitui a correção', 'Cálculo sem alterar a leitura', 'Chefe final', '''class SensorTemperatura:
    def __init__(self, local, temperatura):
        self.local = local
        self.temperatura = temperatura
        self.correcao = 0

    def calibrar(self, valor):
        if -5 <= valor <= 5:
            self.correcao = valor
        else:
            print("Correção inválida")

    def calcular_temperatura_corrigida(self):
        return self.temperatura + self.correcao

s = SensorTemperatura("Sala A", 25)
s.calibrar(2)
s.calibrar(-2)
print(s.temperatura, s.calcular_temperatura_corrigida())''',
['25 23','25 25','23 23','25 27'],0,
'A segunda calibração substitui +2 por -2. A leitura original continua em 25; o cálculo retorna 25 + (-2) = 23 sem alterar o objeto.',120,
'Avaliação • exercício 6 — Sensor de temperatura','25 23'),
Questao('Missão final: quem é self na comparação?', 'Objeto como parâmetro', 'Chefe final', '''class SensorTemperatura:
    def __init__(self, local, temperatura):
        self.local = local
        self.temperatura = temperatura
        self.correcao = 0

    def calcular_temperatura_corrigida(self):
        return self.temperatura + self.correcao

    def comparar(self, outro_sensor):
        print(self.local, outro_sensor.local)

sensor1 = SensorTemperatura("Sala A", 25)
sensor2 = SensorTemperatura("Sala B", 28)
sensor1.comparar(sensor2)

# Dentro de comparar(), quem corresponde a self
# e quem corresponde a outro_sensor?''',
['self é sensor2; outro_sensor é sensor1.','Ambos representam sensor1.','self é a classe; outro_sensor é o número 28.','self é sensor1; outro_sensor é sensor2.'],3,
'O objeto que aparece antes do ponto, sensor1, é recebido em self. O argumento sensor2 é recebido em outro_sensor. O método mostrado imprime Sala A Sala B e não altera os sensores.',90,
'Avaliação • exercício 6 — Sensor de temperatura, pergunta A','Sala A Sala B'),
]

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    questions = []
    for i, q in enumerate(QUESTOES):
        data = asdict(q)
        data.pop('expected_output')
        questions.append(dict(id=101+i, curriculum=CURRICULUM, **data))
    for q in questions:
        assert len(q['options']) == 4 and 0 <= q['answer'] < 4
        assert q['seconds'] >= 60 and q['source']
    (root/'site/questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
    payload = json.dumps(questions,ensure_ascii=False).replace("'", "''")
    (root/'supabase/02-questions.sql').write_text("-- Banco alinhado aos exercícios da turma. IDs novos preservam partidas anteriores.\ninsert into public.pq_questions(id, data) select (q->>'id')::int, q from jsonb_array_elements('"+payload+"'::jsonb) q on conflict(id) do update set data=excluded.data;\n")
    print(f'{len(questions)} questões alinhadas e geradas.')
