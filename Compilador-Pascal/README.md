# Relatório: Compilador Pascal para EWVM

## 1. Introdução

Este relatório descreve o desenvolvimento e a implementação de um compilador para a linguagem Pascal standard, direcionado para a máquina virtual EWVM (Enhanced Web Virtual Machine). O projeto foi desenvolvido como parte da disciplina de Processamento de Linguagens 2025, seguindo os requisitos especificados para a construção de um compilador completo.

O compilador implementa todas as etapas de um processo de compilação típico: análise léxica, análise sintática, análise semântica e geração de código. O sistema tem como entrada programas escritos em Pascal standard e produz como saída código executável na máquina virtual EWVM.

## 2. Arquitetura do Compilador

O compilador foi estruturado de forma modular, onde cada componente é responsável por uma fase específica do processo de compilação. A arquitetura segue o modelo clássico de um compilador, com os seguintes módulos principais:

```
compilador-pascal/
├── main.py            # Programa principal e integração dos módulos
├── lexer.py           # Analisador léxico
├── parser.py          # Analisador sintático
├── semantic.py        # Analisador semântico
└── codegen.py         # Gerador de código
```

O fluxo de processamento do compilador segue as seguintes etapas:

1. O analisador léxico (`lexer.py`) transforma o código fonte em uma sequência de tokens.
2. O analisador sintático (`parser.py`) constrói uma árvore sintática abstrata (AST) a partir dos tokens.
3. O analisador semântico (`semantic.py`) verifica a correção semântica do programa.
4. O gerador de código (`codegen.py`) produz código executável para a máquina virtual EWVM.
5. O módulo principal (`main.py`) coordena o fluxo de dados entre os diferentes componentes.

## 3. Implementação dos Módulos

### 3.1 Analisador Léxico (`lexer.py`)

O analisador léxico foi implementado utilizando a biblioteca PLY (Python Lex-Yacc), que fornece uma implementação do algoritmo Lex para reconhecimento de tokens. O módulo é responsável por identificar os elementos lexicais (tokens) da linguagem Pascal, como palavras-chave, identificadores, operadores e literais.

#### Características principais:
- Definição de tokens para todos os elementos lexicais da linguagem Pascal standard
- Tratamento de comentários entre chaves `{ ... }`
- Reconhecimento de palavras-chave de forma case-insensitive
- Suporte a literais de string com escape de caracteres
- Tratamento de erros léxicos com mensagens informativas

#### Exemplo de definição de token:
```python
# Expressões regulares para palavras reservadas (insensíveis a maiúsculas/minúsculas)
def t_PROGRAM(t):
    r'(?i)program'
    t.value = t.value.lower()
    return t

def t_BEGIN(t):
    r'(?i)begin'
    t.value = t.value.lower()
    return t
```

#### Funções para tokens complexos:
```python
# Identificadores: começam com letra, podem conter letras, dígitos e underscore
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    return t
```

### 3.2 Analisador Sintático (`parser.py`)

O analisador sintático foi implementado utilizando a biblioteca PLY (yacc), que fornece uma implementação do algoritmo LALR para análise sintática. Este módulo é responsável por verificar se a sequência de tokens segue a gramática da linguagem Pascal e construir uma representação estruturada do programa na forma de uma Árvore Sintática Abstrata (AST).

#### Características principais:
- Definição de regras de gramática para todos os construtos da linguagem Pascal
- Construção de uma AST com nós tipados
- Tratamento de precedência de operadores
- Sistema robusto de tratamento de erros sintáticos
- Implementação de nós da AST com verificação de tipos para segurança

#### Exemplo de regra de produção:
```python
def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    if len(p) > 5:
        p[0] = Node('IfStatement', [p[2], p[4], p[6]])
    else:
        p[0] = Node('IfStatement', [p[2], p[4]])
```

#### Implementação da classe Node:
```python
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children is None:
            self.children = []
        elif isinstance(children, list):
            self.children = children
        else:
            self.children = [children]
        self.leaf = leaf
```

### 3.3 Analisador Semântico (`semantic.py`)

O analisador semântico é responsável por verificar a correção semântica do programa após a análise sintática. Ele realiza verificações como análise de tipos, verificação de declaração de variáveis antes do uso, verificação de escopo, entre outras.

#### Características principais:
- Tabela de símbolos para rastreamento de identificadores e seus atributos
- Verificação de tipos em expressões e operações
- Verificação de escopo e visibilidade de variáveis
- Deteção de variáveis não inicializadas
- Validação de índices de arrays
- Suporte a funções e procedimentos com verificação de parâmetros

#### Exemplo de verificação de tipo:
```python
def check_type_compatibility(self, expected_type, actual_type):
    """Verifica se dois tipos são compatíveis."""
    if expected_type is None or actual_type is None:
        return False
    
    # Tipos idênticos são compatíveis
    if expected_type == actual_type:
        return True
    
    # Para casos de arrays, verifica compatibilidade de elementos
    if isinstance(expected_type, dict) and isinstance(actual_type, dict):
        if expected_type.get('kind') == 'array' and actual_type.get('kind') == 'array':
            # Verifica se os tipos de elementos são compatíveis
            return self.check_type_compatibility(
                expected_type.get('elem_type'),
                actual_type.get('elem_type')
            )
    
    return False
```

### 3.4 Gerador de Código (`codegen.py`)

O gerador de código é responsável por traduzir a AST para código executável na máquina virtual EWVM. Este módulo implementa um visitor pattern para percorrer a AST e gerar as instruções correspondentes.

#### Características principais:
- Geração de código para todos os construtos básicos de Pascal
- Suporte a variáveis locais e globais
- Implementação de estruturas de controlo (if, while, for)
- Geração de código para arrays
- Suporte a funções e procedimentos com parâmetros
- Tratamento de expressões aritméticas e lógicas
- Otimização básica de código

#### Exemplo de geração de código para expressão binária:
```python
def generate_BinaryOperation(self, node):
    """Gera código para uma operação binária."""
    # Gera código para os operandos
    self.visit(node.children[0])
    self.visit(node.children[1])
    
    # Aplica o operador
    operator = node.leaf
    if operator == '+':
        self.emit("ADD")
    elif operator == '-':
        self.emit("SUB")
    elif operator == '*':
        self.emit("MUL")
    # ... outros operadores
```

### 3.5 Programa Principal (`main.py`)

O módulo principal integra todos os componentes do compilador e fornece uma interface de linha de comando para o utilizador. Ele coordena o fluxo de dados entre os diferentes estágios de compilação.

#### Características principais:
- Interface de linha de comando com opções variadas
- Suporte a diferentes modos de operação (apenas tokenização, apenas parsing, etc.)
- Geração de ficheiros de saída
- Relatórios verbosos quando solicitado
- Tratamento de erros em todos os estágios

#### Exemplo de interface de linha de comando:
```python
def main():
    parser = argparse.ArgumentParser(description='Compilador Pascal')
    parser.add_argument('source', help='Ficheiro fonte Pascal a ser compilado')
    parser.add_argument('-o', '--output', help='Ficheiro de saída para o código gerado')
    parser.add_argument('-t', '--tokens-only', action='store_true', help='Executa apenas a análise léxica')
    parser.add_argument('-a', '--ast-only', action='store_true', help='Executa a análise sintática e mostra a AST')
    parser.add_argument('-n', '--no-code', action='store_true', help='Não gerar código, apenas analisar')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso, mostra mais informações')
```

## 4. Testes Realizados

Para garantir a qualidade e a correção do compilador, foram realizados diversos testes em diferentes níveis, cobrindo uma ampla gama de construtos da linguagem Pascal.

### 4.1 Testes de Análise Léxica

Foram realizados testes para verificar o reconhecimento correto de todos os tokens da linguagem, incluindo:
- Identificadores e palavras-chave
- Literais (números, strings)
- Operadores e símbolos especiais
- Comentários

**Exemplo de teste léxico:**
```pascal
program Teste;
var
  x: integer;
begin
  x := 10 + 20;  { Uma atribuição simples }
  writeln('Valor: ', x)
end.
```

**Saída do terminal ao executar:**
```
$ python main.py teste.pas --tokens-only
=== Tokens encontrados ===
PROGRAM: program
ID: Teste
SEMICOLON: ;
VAR: var
ID: x
COLON: :
INTEGER: integer
SEMICOLON: ;
BEGIN: begin
ID: x
ASSIGN: :=
INTEGER_CONST: 10
PLUS: +
INTEGER_CONST: 20
SEMICOLON: ;
WRITELN: writeln
LPAREN: (
STRING_CONST: Valor: 
COMMA: ,
ID: x
RPAREN: )
END: end
DOT: .
```

Verificação: todos os tokens são reconhecidos corretamente, incluindo o comentário que é descartado.

### 4.2 Testes de Análise Sintática

Foram realizados testes para verificar a construção correta da AST para diversos construtos da linguagem:
- Declarações de variáveis e tipos
- Expressões aritméticas e lógicas
- Estruturas de controlo (if, while, for)
- Definição e chamada de funções/procedimentos
- Arrays e acesso a elementos

**Exemplo de teste sintático:**
```pascal
program TesteSintatico;
var
  nums: array[1..5] of integer;
  i, soma: integer;
begin
  soma := 0;
  for i := 1 to 5 do
  begin
    nums[i] := i * i;
    soma := soma + nums[i]
  end;
  writeln('Soma dos quadrados: ', soma)
end.
```

**Saída do terminal ao executar:**
```
$ python main.py teste_sintatico.pas --ast-only
=== Árvore Sintática Abstrata (AST) ===
Program: Teste
  ID: TesteSintatico
  ProgramBlock
    Declarations
      DeclarationList
        Declaration
          IDList
            ID: nums
          ArrayType
            Range: (1, 5)
            Type: integer
        Declaration
          IDList
            ID: i
            ID: soma
          Type: integer
    CompoundStatement
      StatementList
        Assignment
          Variable: soma
          IntegerConstant: 0
        ForStatement: to
          ID: i
          IntegerConstant: 1
          IntegerConstant: 5
          CompoundStatement
            StatementList
              Assignment
                ArrayAccess
                  ID: nums
                  Variable: i
                BinaryOperation: *
                  Variable: i
                  Variable: i
              Assignment
                Variable: soma
                BinaryOperation: +
                  Variable: soma
                  ArrayAccess
                    ID: nums
                    Variable: i
        IOCall: writeln
          ExpressionList
            StringConstant: Soma dos quadrados: 
            Variable: soma
```

Verificação: a AST representa corretamente a estrutura do programa, incluindo o array, o loop for e as expressões.

### 4.3 Testes de Análise Semântica

Foram realizados testes para verificar a análise semântica:
- Verificação de tipos em expressões
- Uso de variáveis não declaradas
- Uso de variáveis não inicializadas
- Escopo de variáveis em funções/procedimentos
- Compatibilidade de parâmetros em chamadas de função

**Exemplo de teste semântico:**
```pascal
program TesteSemantico;
var
  x: integer;
  b: boolean;
begin
  x := 5;
  b := x > 10;
  if x then  { Erro semântico: condição deve ser booleana }
    writeln('x é verdadeiro')
end.
```

**Saída do terminal ao executar:**
```
$ python main.py teste_semantico.pas --no-code
=== Erros Semânticos ===
Erro: A condição do if deve ser booleana, mas foi 'integer'.
```

Verificação: o compilador deteta corretamente o erro de tipo na condição do if.

### 4.4 Testes de Geração de Código

Foram realizados testes para verificar a geração correta de código para a máquina virtual EWVM:
- Expressões aritméticas e lógicas
- Estruturas de controlo
- Funções e procedimentos
- Arrays
- Entrada/saída

**Exemplo de teste de geração de código:**
```pascal
program Fatorial;
var
  n, fat: integer;
begin
  writeln('Digite um numero:');
  readln(n);
  fat := 1;
  while n > 0 do
  begin
    fat := fat * n;
    n := n - 1
  end;
  writeln('Fatorial: ', fat)
end.
```

**Saída do terminal ao executar:**
```
$ python main.py fatorial.pas -v
=== Código Gerado ===
PUSHI 0
PUSHI 0
START
ALLOC 2
PUSHS "Digite um numero:"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 1
STOREG 1
L0:
PUSHG 0
PUSHI 0
SUP
JZ L1
PUSHG 1
PUSHG 0
MUL
STOREG 1
PUSHG 0
PUSHI 1
SUB
STOREG 0
JUMP L0
L1:
PUSHS "Fatorial: "
WRITES
PUSHG 1
WRITEI
WRITELN
STOP
```

**Resultado na EWVM:**
```
Digite um numero:
5
Fatorial: 120
```

Verificação: o código gerado calcula corretamente o fatorial quando executado na EWVM.

### 4.5 Exemplos Entrada e Saida

Na pasta [tests](./tests/) podemos ver exemplos de entrada (fornecidos pelos docentes) e de saida pelo nosso programa.

## 5. Decisões de Design

Durante o desenvolvimento do compilador, várias decisões de design foram tomadas para equilibrar complexidade, eficiência e facilidade de implementação.

### 5.1 Representação da AST

A escolha de uma estrutura de nó para a AST com tipo, filhos e valor (leaf) permitiu uma representação flexível e expressiva dos elementos sintáticos do programa. Esta abordagem facilitou a implementação do visitor pattern no gerador de código.

**Alternativas consideradas:**
- Utilizar classes específicas para cada tipo de nó
- Usar uma representação baseada em dicionários
- Adotar uma estrutura de árvore mais genérica

A alternativa escolhida ofereceu um bom equilíbrio entre tipagem e flexibilidade, além de facilitar a depuração com métodos de pretty printing.

### 5.2 Tabela de Símbolos

A tabela de símbolos foi implementada com suporte a escopos aninhados, permitindo variáveis locais com o mesmo nome em diferentes escopos. Esta escolha aproxima o comportamento do compilador ao esperado em Pascal standard.

**Alternativas consideradas:**
- Tabela de símbolos plana com qualificadores de escopo
- Múltiplas tabelas independentes para cada escopo

A estrutura hierárquica adotada permite uma pesquisa eficiente, primeiro no escopo atual e depois escalando para os escopos mais externos, simulando o comportamento real da resolução de nomes em Pascal.

### 5.3 Geração de Código

A geração de código foi implementada para produzir código diretamente compatível com a EWVM, em vez de gerar um código intermediário genérico. Esta decisão simplificou o processo de compilação, eliminando a necessidade de uma etapa adicional de tradução.

**Alternativas consideradas:**
- Gerar código intermediário e depois traduzir para EWVM
- Utilizar uma representação intermediária de mais baixo nível
- Gerar código para uma máquina virtual personalizada

A abordagem direta para EWVM foi escolhida por sua simplicidade e eficiência, evitando camadas desnecessárias de tradução.

### 5.4 Tratamento de Erros

Foi implementado um sistema robusto de tratamento de erros em todos os estágios do compilador, com mensagens claras e informativas para o utilizador. Esta decisão melhora significativamente a experiência de desenvolvimento.

**Alternativas consideradas:**
- Parar na primeira ocorrência de erro
- Acumular erros apenas em certos estágios
- Usar códigos de erro numéricos

O sistema implementado permite a recuperação de erros em certos casos e acumula erros ao longo das fases do compilador, oferecendo um relatório completo ao utilizador.


## 6. Possíveis Melhorias

Embora o compilador atenda aos requisitos básicos, há várias áreas onde melhorias poderiam ser implementadas:

### 6.1 Otimizações de Código

O compilador atual realiza poucas otimizações. Algumas possíveis melhorias incluem:

- **Eliminação de código morto**: Implementação de uma análise de fluxo de controlo para identificar e remover instruções que nunca são executadas. Isso seria feito através de um passo adicional após a geração de código, onde seria construído um grafo de fluxo e as instruções inalcançáveis seriam eliminadas.

- **Propagação de constantes**: Análise estática para identificar variáveis que têm sempre o mesmo valor, substituindo referências a essas variáveis diretamente pelo valor. A implementação exigiria um mecanismo de rastreamento dos valores das variáveis durante a etapa de análise semântica.

- **Eliminação de subexpressões comuns**: Deteção de cálculos repetidos e substituição por referências a resultados anteriores. Seria necessário adicionar uma fase de análise da AST para identificar subexpressões idênticas e modificar a AST para reutilizar resultados.

- **Otimização de loops**: Técnicas como desenrolamento de loops e movimentação de código invariante para fora do loop. Isso exigiria alterações no gerador de código para reconhecer padrões específicos de loops e aplicar transformações adequadas.

### 6.2 Melhorias no Tratamento de Erros

O tratamento de erros poderia ser aprimorado com:
- Sugestões de correção para erros comuns
- Recuperação mais robusta de erros sintáticos
- Localização mais precisa de erros (linha e coluna)
- Mensagens de erro mais contextualizadas

## 7. Conclusão

O compilador Pascal para EWVM implementado neste projeto atende aos requisitos definidos, permitindo a compilação e execução de programas Pascal standard. A arquitetura modular facilita a manutenção e expansão futura.

O processo de desenvolvimento do compilador proporcionou uma compreensão profunda das técnicas de compilação, desde a análise léxica até a geração de código, e permitiu aplicar conceitos teóricos em um projeto prático.

Os testes realizados demonstram que o compilador é capaz de processar corretamente diversos programas Pascal, incluindo exemplos com complexidade variada, desde simples cálculos aritméticos até programas com funções, procedimentos e estruturas de dados.

Embora existam oportunidades de melhoria, conforme discutido na secção anterior, o compilador em seu estado atual representa uma implementação funcional e educativa de um compilador Pascal, adequado para fins académicos e de aprendizagem.

Em resumo, o projeto cumpre seu objetivo principal de implementar um compilador funcional para a linguagem Pascal standard, com todas as etapas de compilação necessárias e geração de código para a máquina virtual EWVM.
