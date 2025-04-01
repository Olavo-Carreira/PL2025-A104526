# Calculadora de Expressões Matemáticas com Parser LL(1)

**Data:** 20 de Março de 2025

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa uma calculadora de expressões matemáticas em Python que permite avaliar operações aritméticas simples, respeitando a precedência dos operadores. A implementação utiliza um analisador sintático do tipo LL(1) para processar e avaliar as expressões matemáticas fornecidas pelo utilizador.

### Funcionalidades:
- Cálculo de expressões matemáticas básicas (adição, subtração, multiplicação, divisão)
- Respeito pela precedência de operadores (multiplicação/divisão antes de adição/subtração)
- Análise léxica e sintática utilizando princípios de gramáticas LL(1)
- Interface de linha de comando interativa
- Tratamento de erros e validação de expressões

## Comportamento da Calculadora

A calculadora opera segundo as seguintes regras:
1. Recebe expressões matemáticas via linha de comando.
2. Realiza análise léxica para identificar números e operadores.
3. Executa análise sintática seguindo uma gramática LL(1).
4. Constrói uma árvore de sintaxe para a expressão.
5. Processa primeiro todas as multiplicações e divisões.
6. Em seguida, calcula as adições e subtrações da esquerda para a direita.
7. Retorna números inteiros quando o resultado é um número inteiro.

## Ficheiros do Projeto

- [`calculadora-ll1.py`](calculadora-ll1.py) - Código fonte da calculadora com parser LL(1).
- [`README.md`](README.md) - Documentação deste projeto.

### Exemplos de Expressões:

```
>> 10 * 3 + 2
32
```
Primeiro calcula 10 * 3 = 30, depois 30 + 2 = 32

```
>> 5 - 1 / 4
4.75
```
Primeiro calcula 1 / 4 = 0.25, depois 5 - 0.25 = 4.75

```
>> 2 + 2 * 2
6
```
Primeiro calcula 2 * 2 = 4, depois 2 + 4 = 6

## Estrutura do Código

O código está organizado em três componentes principais:

1. **AnalisadorLexico**: Responsável por tokenizar a entrada
   - Transforma a string de entrada em uma sequência de tokens (números e operadores)
   - Ignora espaços em branco

2. **AnalisadorSintatico**: Implementa a análise sintática LL(1)
   - Constrói uma árvore de análise seguindo as regras da gramática
   - Utiliza apenas um token de lookahead (característica LL(1))
   - Regras gramaticais:
     - expressao → NUM resto_expressao
     - resto_expressao → OP NUM resto_expressao | ε

3. **Funções de Avaliação**: Calculam o resultado da expressão
   - `processar_mult_div`: Processa operações de multiplicação e divisão
   - `processar_soma_sub`: Processa operações de adição e subtração
   - `avaliar`: Coordena a avaliação respeitando a precedência

## A Abordagem LL(1)

O analisador sintático implementado segue os princípios de um parser LL(1):
- Análise da entrada da esquerda para a direita (primeiro L)
- Derivação mais à esquerda (segundo L)
- Utilização de apenas um token de lookahead (o 1)

Esta abordagem permite analisar expressões aritméticas de forma eficiente, construindo uma árvore sintática que pode ser avaliada posteriormente.

## Exemplo de Uso

Para iniciar a calculadora, execute o script:

```bash
python calculadora-ll1.py
```

Exemplos de interação:

```
Digite uma expressão para calcular ou 'sair' para encerrar.

>> 10 * 3 + 2
32

>> 5 - 1 / 4
4.75

>> 2 + 2 * 2
6

>> sair
Encerrado!
```

## Limitações Atuais

- Não suporta parênteses para controlar a precedência
- Não implementa operações unárias (como negação)
- Limitado a números inteiros na entrada (sem decimais)

## Possíveis Melhorias Futuras

- Adição de suporte a parênteses para controlar a precedência
- Implementação de funções matemáticas avançadas
- Suporte a operadores unários (como negação)
- Adição de operadores como potenciação, módulo, etc.
- Expansão da gramática para suportar expressões mais complexas