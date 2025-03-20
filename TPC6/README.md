# Calculadora de Expressões Matemáticas

**Data:** 20 de Março de 2025

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa uma calculadora de expressões matemáticas em Python que permite avaliar operações aritméticas simples, respeitando a precedência dos operadores. O programa utiliza expressões regulares para analisar e processar as expressões matemáticas fornecidas pelo utilizador.

### Funcionalidades:
- Cálculo de expressões matemáticas básicas (adição, subtração, multiplicação, divisão)
- Respeito pela precedência de operadores (multiplicação/divisão antes de adição/subtração)
- Interface de linha de comando interativa
- Tratamento de erros e validação de expressões

## Comportamento da Calculadora

A calculadora opera segundo as seguintes regras:
1. Recebe expressões matemáticas via linha de comando.
2. Processa primeiro todas as multiplicações e divisões.
3. Em seguida, calcula as adições e subtrações da esquerda para a direita.
4. Retorna números inteiros quando o resultado é um número inteiro.
5. Lida com números negativos e decimais.

## Ficheiros do Projeto

- [`calculator.py`](calculator.py) - Código fonte da calculadora.
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

O código está organizado em duas funções principais:

1. `calcular_expressao(expressao)`: Analisa e calcula o valor de uma expressão matemática.
   - Remove espaços em branco.
   - Resolve operações de multiplicação e divisão.
   - Resolve operações de adição e subtração.
   - Lida com casos especiais como números negativos no início da expressão.

2. Função `main` (no bloco `if __name__ == '__main__'`):
   - Executa o programa em modo interativo.
   - Recebe expressões do utilizador através da linha de comando.
   - Termina a execução quando o utilizador digita "sair".

## Uso de Expressões Regulares

O programa utiliza expressões regulares para analisar e processar as expressões matemáticas:

- Identificação de operações de multiplicação e divisão: `r'(\d+\.?\d*)\s*([*/])\s*(\d+\.?\d*)'`
- Extração de números e operadores de adição e subtração: `r'(-?\d+\.?\d*)|([+\-])'`

## Exemplo de Uso

Para iniciar a calculadora, execute o script:

```bash
python calculadora.py
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


## Possíveis Melhorias Futuras

- Adição de suporte a parênteses para controlar a precedência.
- Implementação de funções matemáticas avançadas.
- Adição de operadores como potenciação, módulo, etc.
