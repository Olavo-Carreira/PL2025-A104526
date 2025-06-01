import ply.lex as lex

# Lista de nomes de tokens reconhecidos pelo lexer
tokens = (
    # Palavras reservadas da linguagem Pascal
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'BOOLEAN', 'STRING', 'ARRAY',
    'OF', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR', 'TO', 'DOWNTO', 'FUNCTION', 'PROCEDURE',
    'READ', 'WRITE', 'WRITELN', 'READLN', 'TRUE', 'FALSE', 'DIV', 'MOD', 'AND', 'OR', 'NOT',

    # Identificadores e literais
    'ID', 'INTEGER_CONST', 'STRING_CONST', 'REAL_CONST',

    # Operadores e pontuação
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'EQUAL', 'NOTEQUAL',
    'LESSTHAN', 'GREATERTHAN', 'LESSEQUAL', 'GREATEREQUAL',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON', 'COLON', 'DOT', 'DOTDOT',
)

# Expressões regulares para tokens simples (operadores e pontuação)
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'\/'
t_ASSIGN      = r':='
t_EQUAL       = r'='
t_NOTEQUAL    = r'<>'
t_LESSTHAN    = r'<'
t_GREATERTHAN = r'>'
t_LESSEQUAL   = r'<='
t_GREATEREQUAL = r'>='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_COMMA       = r','
t_SEMICOLON   = r';'
t_COLON       = r':'
t_DOT         = r'\.'
t_DOTDOT      = r'\.\.'

# Expressões regulares para palavras reservadas (case-insensitive)
# IMPORTANTE: palavras mais longas devem vir ANTES das mais curtas!

def t_PROCEDURE(t):
    r'[pP][rR][oO][cC][eE][dD][uU][rR][eE]'
    t.value = t.value.lower()
    return t

def t_FUNCTION(t):
    r'[fF][uU][nN][cC][tT][iI][oO][nN]'
    t.value = t.value.lower()
    return t

def t_PROGRAM(t):
    r'[pP][rR][oO][gG][rR][aA][mM]'
    t.value = t.value.lower()
    return t

def t_WRITELN(t):
    r'[wW][rR][iI][tT][eE][lL][nN]'
    t.value = t.value.lower()
    return t

def t_READLN(t):
    r'[rR][eE][aA][dD][lL][nN]'
    t.value = t.value.lower()
    return t

def t_DOWNTO(t):
    r'[dD][oO][wW][nN][tT][oO]'
    t.value = t.value.lower()
    return t

def t_INTEGER(t):
    r'[iI][nN][tT][eE][gG][eE][rR]'
    t.value = t.value.lower()
    return t

def t_BOOLEAN(t):
    r'[bB][oO][oO][lL][eE][aA][nN]'
    t.value = t.value.lower()
    return t

def t_STRING(t):
    r'[sS][tT][rR][iI][nN][gG]'
    t.value = t.value.lower()
    return t

def t_BEGIN(t):
    r'[bB][eE][gG][iI][nN]'
    t.value = t.value.lower()
    return t

def t_ARRAY(t):
    r'[aA][rR][rR][aA][yY]'
    t.value = t.value.lower()
    return t

def t_FALSE(t):
    r'[fF][aA][lL][sS][eE]'
    t.value = t.value.lower()
    return t

def t_WHILE(t):
    r'[wW][hH][iI][lL][eE]'
    t.value = t.value.lower()
    return t

def t_WRITE(t):
    r'[wW][rR][iI][tT][eE]'
    t.value = t.value.lower()
    return t

def t_THEN(t):
    r'[tT][hH][eE][nN]'
    t.value = t.value.lower()
    return t

def t_TRUE(t):
    r'[tT][rR][uU][eE]'
    t.value = t.value.lower()
    return t

def t_ELSE(t):
    r'[eE][lL][sS][eE]'
    t.value = t.value.lower()
    return t

def t_READ(t):
    r'[rR][eE][aA][dD]'
    t.value = t.value.lower()
    return t

def t_END(t):
    r'[eE][nN][dD]'
    t.value = t.value.lower()
    return t

def t_FOR(t):
    r'[fF][oO][rR]'
    t.value = t.value.lower()
    return t

def t_MOD(t):
    r'[mM][oO][dD]'
    t.value = t.value.lower()
    return t

def t_NOT(t):
    r'[nN][oO][tT]'
    t.value = t.value.lower()
    return t

def t_VAR(t):
    r'[vV][aA][rR]'
    t.value = t.value.lower()
    return t

def t_DIV(t):
    r'[dD][iI][vV]'
    t.value = t.value.lower()
    return t

def t_AND(t):
    r'[aA][nN][dD]'
    t.value = t.value.lower()
    return t

def t_DO(t):
    r'[dD][oO]'
    t.value = t.value.lower()
    return t

def t_IF(t):
    r'[iI][fF]'
    t.value = t.value.lower()
    return t

def t_OF(t):
    r'[oO][fF]'
    t.value = t.value.lower()
    return t

def t_OR(t):
    r'[oO][rR]'
    t.value = t.value.lower()
    return t

def t_TO(t):
    r'[tT][oO]'
    t.value = t.value.lower()
    return t

# Identificadores: começam com letra, podem conter letras, dígitos e underscore
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    return t

# Constantes string em Pascal: aspas simples, com possível escape
def t_STRING_CONST(t):
    r"'([^'\\]|\\.)*'"
    t.value = t.value[1:-1]  # Remove as aspas exteriores
    return t

# Constantes inteiras
def t_INTEGER_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Constantes reais (número com ponto decimal)
def t_REAL_CONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Atualização do número da linha (necessária para reporting de erros)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comentários entre chaves { ... } — ignorados pelo lexer
def t_COMMENT(t):
    r'\{[^}]*\}'
    pass  # Token descartado (não é devolvido)

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Tratamento de erros: imprime o caractere ilegal e avança
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Criação do analisador léxico
lexer = lex.lex()

# Função auxiliar para testar o lexer com uma string de entrada
def test_lexer(data):
    lexer.input(data)
    tokens_found = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_found.append((tok.type, tok.value))
    return tokens_found

# Função para obter todos os tokens de entrada
def get_tokens(data):
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens