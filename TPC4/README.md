# Analisador Léxico para Linguagem de Query

**Data:** 5 de Março de 2025  

## Autor
- **Nome:** [Seu Nome]
- **Número:** [Seu Número]  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa um analisador léxico para uma linguagem de consulta semelhante a SPARQL que reconhece e tokeniza diferentes elementos da linguagem. O programa utiliza a biblioteca PLY (Python Lex-Yacc) para definir padrões de tokens através de expressões regulares, permitindo o reconhecimento de elementos como variáveis, URIs, literais, palavras-chave e pontuação.

### Funcionalidades:
- Reconhecimento de palavras-chave (`SELECT`, `WHERE`, `LIMIT`).
- Identificação de variáveis (começando com `?`).
- Processamento de URIs no formato `prefixo:nome`.
- Reconhecimento de tipos (`a`).
- Identificação de literais entre aspas.
- Processamento de etiquetas de idioma (langtags).
- Reconhecimento de nomes e números.
- Tratamento de pontuação e comentários.

## Comportamento do Analisador Léxico

O analisador opera segundo as seguintes regras:
1. Lê o texto de entrada linha por linha, identificando padrões específicos.
2. Classifica cada token de acordo com as regras definidas para cada tipo.
3. Regista informações sobre cada token, incluindo o tipo, valor, número da linha e posição.
4. Ignora espaços em branco e tabulações, mantendo o controlo do número da linha.

### Exemplos de Reconhecimento de Tokens:
```
SELECT ?nome ?idade
```
Tokens reconhecidos:
```
(SELECT, 'select', linha 1, posição 0)
(VARIAVEL, '?nome', linha 1, posição 7)
(VARIAVEL, '?idade', linha 1, posição 13)
```

```
foaf:name "João Silva" @pt
```
Tokens reconhecidos:
```
(URI, 'foaf:name', linha 1, posição 0)
(LITERAL, 'João Silva', linha 1, posição 10)
(LANGTAG, '@pt', linha 1, posição 22)
```

## Estrutura do Código

O código principal está organizado em funções específicas para cada tipo de token:

1. `t_COMENTARIO(t)`: Reconhece comentários que começam com `#`.
2. `t_URI(t)`: Identifica URIs no formato `prefixo:nome`.
3. `t_VARIAVEL(t)`: Reconhece variáveis que começam com `?`.
4. `t_LITERAL(t)`: Identifica literais entre aspas duplas.
5. `t_LANGTAG(t)`: Reconhece etiquetas de idioma que começam com `@`.
6. `t_NOME(t)`: Identifica nomes de identificadores.
7. `t_NUMERO(t)`: Reconhece números inteiros.
8. `t_PONTUACAO(t)`: Identifica símbolos de pontuação.
9. `construir_lexer()`: Função para construir o analisador léxico.
10. `tokenizar_arquivo(arquivo)`: Função para processar um arquivo completo.

## Ficheiros do Projeto

- [`lex.py`](lex.py) - Código fonte do analisador léxico.
- [`README.md`](README.md) - Documentação deste projeto.
- [`query.txt](query.txt) - Ficheiro de query para testar o analisador.

## Exemplo de Uso

Para usar o analisador léxico, basta executar o script passando o nome do ficheiro a ser analisado como argumento:

```bash
python3 lex.py query.txt
```

O programa irá mostrar cada token reconhecido no formato:
```
(TIPO, 'valor', linha X, posição Y)
```

Também é possível importar as funções do analisador para uso em outros scripts:

```python
from lex import construir_lexer, tokenizar_arquivo

# Tokenizar um arquivo específico
tokens = tokenizar_arquivo('query.txt')

# Processar os tokens
for token in tokens:
    tipo, valor, linha, pos = token
    print(f"Token: {tipo}, Valor: {valor}")
```

### Expressões Regulares

O analisador utiliza expressões regulares através do PLY para identificar padrões no texto. Exemplos de padrões utilizados:

- Comentários: `r'\#.*'`
- URIs: `r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z0-9_]*'`
- Variáveis: `r'\?[a-zA-Z][a-zA-Z0-9_]*'`
- Literais: `r'"[^"]*"'`
- Etiquetas de idioma: `r'@[a-zA-Z]+'`

## Possíveis Melhorias Futuras

- Suporte a mais elementos da linguagem de consulta, como operadores, funções e expressões.
- Adição de uma interface gráfica para visualizar os tokens reconhecidos.
- Expansão para um analisador sintático completo (parser) que construa uma árvore de sintaxe.
- Melhorar o tratamento de erros para entradas mal formatadas.
- Implementação de recursos para coloração de sintaxe em editores de texto.