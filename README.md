# 🧠 SAT Solver - DPLL Algorithm

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um **SAT Solver completo** implementando o algoritmo **DPLL (Davis-Putnam-Logemann-Loveland)** com propagação unitária e eliminação de literais puros.

## 🚀 Funcionalidades

✅ **Algoritmo DPLL completo** com backtracking  
✅ **Propagação Unitária** para otimização  
✅ **Eliminação de Literais Puros**  
✅ **Suporte ao formato DIMACS CNF**  
✅ **Parser CNF** com múltiplos formatos de entrada  
✅ **Gerador de Fórmulas Aleatórias** (3-SAT, Pigeon Hole)  
✅ **Visualizador de Resultados** com estatísticas detalhadas  
✅ **Suite de Testes Abrangente** com 20+ casos  
✅ **Exemplos Práticos** (Sudoku, puzzles lógicos)  

## 📦 Instalação

```bash
git clone https://github.com/PresetyX/sat-solver.git
cd sat-solver

# Sem dependências externas - só Python!
python sat_solver.py
```

## ⚡ Início Rápido

```python
from sat_solver import SATSolver

# Define fórmula CNF: (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (¬x₂ ∨ ¬x₃)
cnf = [[1, 2], [-1, 3], [-2, -3]]

# Cria solver e resolve
solver = SATSolver(cnf)
satisfiable, assignment = solver.solve()

if satisfiable:
    print(f"✓ SATISFAZÍVEL - Atribuição: {assignment}")
else:
    print("✗ INSATISFAZÍVEL")
```

### Execute os Exemplos

```bash
# Rode todos os exemplos
python examples.py

# Execute os testes
python test_sat_solver.py
```

## 🧠 O que é SAT?

**Boolean Satisfiability Problem (SAT)** é o problema de determinar se existe uma atribuição de valores verdade para variáveis que torna uma fórmula booleana verdadeira.

### CNF (Forma Normal Conjuntiva)

Uma fórmula está em CNF quando expressa como **conjunção de cláusulas**, onde cada cláusula é uma **disjunção de literais**:

```
(x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂) ∧ (x₂ ∨ ¬x₃)
```

**Neste solver:**
- Inteiros positivos = variáveis: `1` = x₁, `2` = x₂
- Inteiros negativos = negações: `-1` = ¬x₁, `-2` = ¬x₂
- Cláusula = lista: `[1, -2, 3]` significa (x₁ ∨ ¬x₂ ∨ x₃)
- Fórmula = lista de cláusulas: `[[1, -2], [2, 3]]`

### Por que SAT é importante?

- 🎯 **Primeiro Problema NP-Completo** (Teorema de Cook-Levin, 1971)
- 🔧 **Base para Solvers Modernos** (verificação, planejamento, IA)
- 💡 **Aplicações Reais:**
  - Verificação de hardware/software
  - Prova automática de teoremas
  - Design e otimização de circuitos
  - Scheduling e planejamento
  - Criptanálise
  - Resolução de Sudoku e puzzles

## 🔍 O Algoritmo DPLL

### Passos do Algoritmo

```
DPLL(Formula F, Atribuição A):
  1. Se F vazia → return SATISFAZÍVEL
  2. Se F contém cláusula vazia → return INSATISFAZÍVEL
  
  3. Propagação Unitária:
     Enquanto F contém cláusula unitária (l):
       Simplifica F com l=true
       Se conflito → return INSATISFAZÍVEL
  
  4. Eliminação de Literais Puros:
     Remove literais que aparecem com apenas uma polaridade
  
  5. Escolhe variável não atribuída x
  6. Tenta: DPLL(F com x=true)
  7. Senão: DPLL(F com x=false)
```

### Otimizações Principais

**1️⃣ Propagação Unitária**: Se uma cláusula tem apenas um literal, ele **deve** ser verdadeiro

**2️⃣ Eliminação de Literais Puros**: Se uma variável aparece com apenas uma polaridade, atribua para satisfazer

**3️⃣ Backtracking**: Quando um ramo leva a conflito, volta e tenta atribuição oposta

## 📝 Exemplos de Uso

### Exemplo 1: Fórmula Satisfazível Simples

```python
from sat_solver import SATSolver
from visualizer import SATVisualizer

cnf = [[1, 2], [-1, 3]]
solver = SATSolver(cnf)
sat, assignment = solver.solve()

SATVisualizer.print_result(sat, assignment, cnf)
SATVisualizer.print_statistics(solver.get_statistics())
```

### Exemplo 2: Fórmula Insatisfazível

```python
# Contradição: (x₁) ∧ (¬x₁)
cnf = [[1], [-1]]
solver = SATSolver(cnf)
sat, _ = solver.solve()
print(f"Resultado: {'SATISFAZÍVEL' if sat else 'INSATISFAZÍVEL'}")
```

### Exemplo 3: 3-SAT Aleatório

```python
from cnf_parser import CNFGenerator

cnf = CNFGenerator.generate_3sat(num_vars=20, ratio=4.3, seed=42)
solver = SATSolver(cnf)
sat, assignment = solver.solve()
print(f"Variáveis: {len(assignment) if assignment else 0}")
print(f"Cláusulas: {len(cnf)}")
```

### Exemplo 4: Formato DIMACS

```python
from sat_solver import parse_dimacs

dimacs = """
c Comentário
p cnf 3 2
1 -2 0
2 3 0
"""
cnf = parse_dimacs(dimacs)
solver = SATSolver(cnf)
sat, assignment = solver.solve()
```

### Exemplo 5: Princípio da Casa dos Pombos

```python
from cnf_parser import CNFGenerator

# 4 pombos em 3 buracos (impossível!)
cnf = CNFGenerator.generate_pigeon_hole(n=3)
solver = SATSolver(cnf)
sat, _ = solver.solve()
print(f"Resultado: {sat}")  # False - insatisfazível
```

## 📖 Referência da API

### Classe SATSolver

```python
class SATSolver:
    def __init__(self, cnf: List[List[int]])
    def solve(self) -> Tuple[bool, Optional[Dict[int, bool]]]
    def get_statistics(self) -> Dict[str, int]
```

### Classe CNFParser

```python
class CNFParser:
    @staticmethod
    def from_string(formula: str) -> List[List[int]]
    
    @staticmethod
    def to_readable(cnf: List[List[int]]) -> str
```

### Classe CNFGenerator

```python
class CNFGenerator:
    @staticmethod
    def generate_random(num_vars, num_clauses, clause_length, seed)
    
    @staticmethod
    def generate_3sat(num_vars, ratio=4.3, seed=None)
    
    @staticmethod
    def generate_pigeon_hole(n: int)
```

## 🧪 Testes

```bash
python test_sat_solver.py
```

### Cobertura de Testes

✅ Fórmulas satisfazíveis simples  
✅ Fórmulas insatisfazíveis  
✅ Propagação de cláusulas unitárias  
✅ Eliminação de literais puros  
✅ Instâncias 3-SAT  
✅ Parsing DIMACS  
✅ Geração de fórmulas aleatórias  
✅ Princípio da casa dos pombos  

## 📊 Performance

| Tipo de Problema | Variáveis | Cláusulas | Tempo (ms) | Decisões | Resultado |
|------------------|-----------|-----------|------------|----------|----------|
| Simples          | 3         | 3         | <1         | 5        | SAT      |
| 3-SAT Aleatório  | 10        | 43        | 2          | 87       | SAT      |
| 3-SAT Aleatório  | 20        | 86        | 15         | 342      | SAT      |
| Pigeon Hole (3)  | 12        | 22        | 8          | 156      | UNSAT    |

## 🛠️ Estrutura do Projeto

```
sat-solver/
├── sat_solver.py          # Implementação core do DPLL
├── cnf_parser.py          # Parsing e geração CNF
├── visualizer.py          # Visualização de resultados
├── test_sat_solver.py     # Suite de testes
├── examples.py            # Exemplos de uso
├── README.md              # Este arquivo
└── LICENSE                # Licença MIT
```

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. 🐛 **Reporte bugs** - Abra uma issue
2. 💡 **Sugira funcionalidades** - Proponha melhorias
3. 🛠️ **Envie PRs** - Corrija bugs, implemente features

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE)

## 👤 Autor

**Pedro** - [@PresetyX](https://github.com/PresetyX)

- Estudante de Engenharia de Software @ PUC-Campinas
- Interessado em algoritmos, teoria da complexidade e reasoning automatizado

## 🔗 Links

- [Repositório GitHub](https://github.com/PresetyX/sat-solver)
- [SAT Competition](http://www.satcompetition.org/)
- [Especificação DIMACS](http://www.satcompetition.org/2009/format-benchmarks2009.html)

---

**Feito com ❤️ e Python** | **⭐ Dê uma estrela se achou útil!**
