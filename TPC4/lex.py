import ply.lex as lex
import sys

# Lista de nomes de tokens
tokens = (
    'COMENTARIO',
    'SELECT',
    'WHERE',
    'LIMIT',
    'VARIAVEL',
    'TIPO',
    'URI',
    'NOME',
    'LITERAL',
    'LANGTAG',
    'PONTUACAO',
    'NUMERO'
)

# Palavras reservadas
reserved = {
    'select': 'SELECT',
    'where': 'WHERE',
    'LIMIT': 'LIMIT',
    'a': 'TIPO'
}

# Regras para tokens simples
def t_COMENTARIO(t):
    r'\#.*'
    return t

def t_URI(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'URI')
    return t

def t_VARIAVEL(t):
    r'\?[a-zA-Z][a-zA-Z0-9_]*'
    return t

def t_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remover aspas
    return t

def t_LANGTAG(t):
    r'@[a-zA-Z]+'
    return t

def t_NOME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NOME')
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PONTUACAO(t):
    r'[\.\{\}\(\),]'
    return t

# Caracteres ignorados (espaços e tabs)
t_ignore = ' \t'

# Regra para novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer 
def construir_lexer():
    return lex.lex()

# Função para tokenizar um arquivo
def tokenizar_arquivo(arquivo):
    lexer = construir_lexer()

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = f.read()

        lexer.input(data)

        tokens_reconhecidos = []
        for tok in lexer:
            tokens_reconhecidos.append(
                (tok.type, tok.value, tok.lineno, tok.lexpos)
            )

        return tokens_reconhecidos

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return []

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python3 lexer.py <arquivo.txt>")
        sys.exit(1)

    arquivo = sys.argv[1]
    tokens = tokenizar_arquivo(arquivo)

    for token in tokens:
        tipo, valor, linha, pos = token
        print(f"({tipo}, '{valor}', linha {linha}, posição {pos})")

if __name__ == "__main__":
    main()
