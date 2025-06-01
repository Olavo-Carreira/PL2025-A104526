import ply.yacc as yacc
from lexer import tokens
import sys

# Ativa modo de depuração
DEBUG = True

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children is None:
            self.children = []
        elif isinstance(children, list):
            # Verifica cada filho e substitui strings por nós de erro
            validated_children = []
            for i, child in enumerate(children):
                if not isinstance(child, Node):
                    if DEBUG:
                        print(f"AVISO: Convertendo {type(child)} para Node em {type}")
                    validated_children.append(Node('ErrorNode', [], str(child)))
                else:
                    validated_children.append(child)
            self.children = validated_children
        else:
            # Se não for uma lista, envolvemos em uma lista com um único item
            if not isinstance(children, Node):
                if DEBUG:
                    print(f"AVISO: Convertendo único filho {type(children)} para Node em {type}")
                self.children = [Node('ErrorNode', [], str(children))]
            else:
                self.children = [children]
        
        self.leaf = leaf

    def pretty(self, level=0):
        result = " " * (level * 2) + self.type
        if self.leaf is not None:
            result += f": {self.leaf}"
        result += "\n"
        for child in self.children:
            if not isinstance(child, Node):
                raise TypeError(f"Expected Node object but got {type(child)} in {self.type} node")
            result += child.pretty(level + 1)
        return result

    def __str__(self):
        return self.pretty()


def p_program(p):
    '''program : PROGRAM ID SEMICOLON program_block DOT'''
    p[0] = Node('Program', [Node('ID', [], p[2]), p[4]])

def p_block(p):
    '''block : declarations compound_statement'''
    p[0] = Node('Block', [p[1], p[2]])

def p_program_block(p):
    '''program_block : function_declarations declarations compound_statement
                     | declarations compound_statement'''
    if len(p) > 3:
        p[0] = Node('ProgramBlock', [p[1], p[2], p[3]])
    else:
        p[0] = Node('ProgramBlock', [p[1], p[2]])

def p_declarations(p):
    '''declarations : VAR declaration_list
                    | empty'''
    if len(p) > 2:
        p[0] = Node('Declarations', [p[2]])  
    else:
        p[0] = Node('Declarations', [p[1]]) 

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('DeclarationList', [])
        if not isinstance(p[2], Node):
            p[2] = Node('ErrorNode', [], str(p[2]))
            
        p[1].children.append(p[2])
        p[0] = p[1]
    else:
        p[0] = Node('DeclarationList', [p[1]])

def p_declaration(p):
    '''declaration : id_list COLON type SEMICOLON'''
    # Verificação de segurança
    for i in range(1, 4):
        if i == 2:  # Pula o COLON
            continue
        if not isinstance(p[i], Node):
            if i == 3:  # Se for o tipo, convertê-lo para nó Type
                p[i] = Node('Type', [], p[i])
            else:
                p[i] = Node('ErrorNode', [], str(p[i]))
    
    p[0] = Node('Declaration', [p[1], p[3]])

def p_function_declarations(p):
    '''function_declarations : function_declaration'''
    p[0] = Node('FunctionDeclarations', [p[1]])

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID formal_parameters COLON type SEMICOLON block SEMICOLON'''
    p[0] = Node('FunctionDeclaration', [Node('ID', [], p[2]), p[3], p[5], p[7]])

def p_formal_parameters(p):
    '''formal_parameters : LPAREN parameter_list RPAREN
                         | LPAREN RPAREN'''
    if len(p) > 3:
        p[0] = Node('FormalParameters', [p[2]])
    else:
        p[0] = Node('FormalParameters', [])

def p_parameter_list(p):
    '''parameter_list : parameter'''
    p[0] = Node('ParameterList', [p[1]])

def p_parameter(p):
    '''parameter : id_list COLON type'''
    p[0] = Node('Parameter', [p[1], p[3]])

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('IDList', [])
        
        p[1].children.append(Node('ID', [], p[3]))
        p[0] = p[1]
    else:
        p[0] = Node('IDList', [Node('ID', [], p[1])])
    
def p_type(p):
    '''type : INTEGER
            | BOOLEAN
            | STRING
            | array_type'''
    if isinstance(p[1], str) and p[1].lower() in ('integer', 'boolean', 'string'):
        p[0] = Node('Type', [], p[1])
    else:
        # Se já é um nó (array_type), passá-lo diretamente
        p[0] = p[1]

def p_array_type(p):
    '''array_type : ARRAY LBRACKET INTEGER_CONST DOTDOT INTEGER_CONST RBRACKET OF type'''
    # Verificação de segurança para garantir que p[8] (type) é um Node
    if not isinstance(p[8], Node):
        p[8] = Node('Type', [], p[8])
    
    p[0] = Node('ArrayType', [Node('Range', [], (p[3], p[5])), p[8]])

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = Node('CompoundStatement', [p[2]])

def p_statement_list(p):
    '''statement_list : statement_list SEMICOLON statement
                      | statement'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('StatementList', [])
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        # Só adicione o statement se não for Empty
        if p[3].type != 'Empty':
            p[1].children.append(p[3])
        p[0] = p[1]
    else:
        p[0] = Node('StatementList', [p[1]])

def p_statement(p):
    '''statement : assignment_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | procedure_call
                 | compound_statement
                 | empty'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : variable ASSIGN expression'''
    # Verificação de segurança
    if not isinstance(p[1], Node):
        p[1] = Node('Variable', [], p[1])
    if not isinstance(p[3], Node):
        p[3] = Node('ErrorNode', [], str(p[3]))
        
    p[0] = Node('Assignment', [p[1], p[3]])

def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    # Verificação de segurança
    if not isinstance(p[2], Node):
        p[2] = Node('ErrorNode', [], str(p[2]))
    if not isinstance(p[4], Node):
        p[4] = Node('ErrorNode', [], str(p[4]))
        
    if len(p) > 5:
        if not isinstance(p[6], Node):
            p[6] = Node('ErrorNode', [], str(p[6]))
        p[0] = Node('IfStatement', [p[2], p[4], p[6]])
    else:
        p[0] = Node('IfStatement', [p[2], p[4]])

def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    # Verificação de segurança
    if not isinstance(p[2], Node):
        p[2] = Node('ErrorNode', [], str(p[2]))
    if not isinstance(p[4], Node):
        p[4] = Node('ErrorNode', [], str(p[4]))
        
    p[0] = Node('WhileStatement', [p[2], p[4]])

def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expression TO expression DO statement
                     | FOR ID ASSIGN expression DOWNTO expression DO statement'''
    # Verificação de segurança
    if not isinstance(p[4], Node):
        p[4] = Node('ErrorNode', [], str(p[4]))
    if not isinstance(p[6], Node):
        p[6] = Node('ErrorNode', [], str(p[6]))
    if not isinstance(p[8], Node):
        p[8] = Node('ErrorNode', [], str(p[8]))
        
    direction = 'to' if p[5] == 'to' else 'downto'
    p[0] = Node('ForStatement', [Node('ID', [], p[2]), p[4], p[6], p[8]], direction)

def p_procedure_call(p):
    '''procedure_call : ID LPAREN expression_list RPAREN
                      | ID LPAREN RPAREN
                      | WRITELN LPAREN expression_list RPAREN
                      | WRITELN LPAREN RPAREN
                      | WRITE LPAREN expression_list RPAREN
                      | WRITE LPAREN RPAREN
                      | READLN LPAREN variable_list RPAREN
                      | READLN LPAREN RPAREN
                      | READ LPAREN variable_list RPAREN
                      | READ LPAREN RPAREN'''

    if p[1].lower() in ('writeln', 'readln', 'write', 'read'):
        if len(p) > 4:
            # Verificação de segurança
            if not isinstance(p[3], Node):
                p[3] = Node('ErrorNode', [], str(p[3]))
            p[0] = Node('IOCall', [p[3]], p[1])
        else:
            p[0] = Node('IOCall', [], p[1])
    else:
        if len(p) > 4:
            # Verificação de segurança
            if not isinstance(p[3], Node):
                p[3] = Node('ErrorNode', [], str(p[3]))
            p[0] = Node('ProcedureCall', [p[3]], p[1])
        else:
            p[0] = Node('ProcedureCall', [], p[1])

def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('ExpressionList', [])
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('ErrorNode', [], str(p[1]))
        p[0] = Node('ExpressionList', [p[1]])

def p_variable_list(p):
    '''variable_list : variable_list COMMA variable
                     | variable'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('VariableList', [])
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('ErrorNode', [], str(p[1]))
        p[0] = Node('VariableList', [p[1]])

def p_expression(p):
    '''expression : simple_expression
                  | simple_expression relational_operator simple_expression'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('ErrorNode', [], str(p[1]))
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        p[0] = Node('BinaryOperation', [p[1], p[3]], p[2])
    else:
        p[0] = p[1]

def p_relational_operator(p):
    '''relational_operator : EQUAL
                           | NOTEQUAL
                           | LESSTHAN
                           | LESSEQUAL
                           | GREATERTHAN
                           | GREATEREQUAL'''
    p[0] = p[1]

def p_simple_expression(p):
    '''simple_expression : term
                         | simple_expression additive_operator term'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[1], Node):
            p[1] = Node('ErrorNode', [], str(p[1]))
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        p[0] = Node('BinaryOperation', [p[1], p[3]], p[2])
    else:
        p[0] = p[1]

def p_additive_operator(p):
    '''additive_operator : PLUS
                         | MINUS'''
    p[0] = p[1]

def p_term(p):
    '''term : factor
            | term multiplicative_operator factor'''
    if len(p) > 2:
        if not isinstance(p[1], Node):
            p[1] = Node('ErrorNode', [], str(p[1]))
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
            
        p[0] = Node('BinaryOperation', [p[1], p[3]], p[2])
    else:
        p[0] = p[1]

def p_multiplicative_operator(p):
    '''multiplicative_operator : TIMES
                               | DIVIDE
                               | DIV
                               | MOD
                               | AND'''
    p[0] = p[1]

def p_logical_expression(p):
    '''expression : expression AND expression
                  | expression OR expression  
                  | NOT expression'''         
    p[0] = Node('LogicalOperation', [p[1], p[3]], p[2])

def p_factor(p):
    '''factor : variable
              | INTEGER_CONST
              | REAL_CONST
              | STRING_CONST
              | LPAREN expression RPAREN
              | function_call
              | TRUE
              | FALSE'''
    if isinstance(p[1], int):
        p[0] = Node('IntegerConstant', [], p[1])
    elif isinstance(p[1], float):
        p[0] = Node('RealConstant', [], p[1])
    elif p.slice[1].type == 'STRING_CONST':
        # Removendo aspas se estiverem presentes
        value = p[1]
        if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        p[0] = Node('StringConstant', [], value)
    elif p.slice[1].type == 'TRUE' or p.slice[1].type == 'FALSE':
        p[0] = Node('BooleanConstant', [], p[1])
    elif p.slice[1].type == 'LPAREN':
        # Verificação de segurança
        if not isinstance(p[2], Node):
            p[2] = Node('ErrorNode', [], str(p[2]))
        p[0] = p[2]
    elif isinstance(p[1], Node):
        p[0] = p[1]
    else:
        p[0] = Node('Variable', [], p[1])

def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN
                     | ID LPAREN RPAREN'''
    if len(p) > 4:
        # Verificação de segurança
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
        p[0] = Node('FunctionCall', [p[3]], p[1])
    else:
        p[0] = Node('FunctionCall', [], p[1])

def p_variable(p):
    '''variable : ID
                | ID LBRACKET expression RBRACKET'''
    if len(p) > 2:
        # Verificação de segurança
        if not isinstance(p[3], Node):
            p[3] = Node('ErrorNode', [], str(p[3]))
        p[0] = Node('ArrayAccess', [Node('ID', [], p[1]), p[3]])
    else:
        p[0] = Node('Variable', [], p[1])

def p_empty(p):
    'empty :'
    p[0] = Node('Empty')

# Sistema de tratamento de erros melhorado
error_messages = {
    'PROGRAM': "Esperado 'program' para iniciar o programa",
    'ID': "Esperado identificador",
    'SEMICOLON': "Esperado ';'",
    'BEGIN': "Esperado 'begin'",
    'END': "Esperado 'end'",
    'DOT': "Esperado '.' no final do programa",
    'COLON': "Esperado ':'",
    'ASSIGN': "Esperado ':=' para atribuição",
    'LPAREN': "Esperado '('",
    'RPAREN': "Esperado ')'",
    'LBRACKET': "Esperado '['",
    'RBRACKET': "Esperado ']'",
    'COMMA': "Esperado ','",
    'DOTDOT': "Esperado '..' para definir intervalo de array"
}

def p_error(p):
    if p:
        token_value = p.value
        line_number = p.lineno if hasattr(p, 'lineno') else '?'
        
        # Tentar sugerir a correção
        expected_token = None
        for token_type, message in error_messages.items():
            # Tenta adivinhar o token esperado com base no contexto
            if hasattr(parser, 'symstack') and p.type != token_type and token_type in parser.symstack[-2:]:
                expected_token = token_type
                break
        
        error_msg = f"Erro de sintaxe na linha {line_number}: Token inesperado '{token_value}'"
        if expected_token:
            error_msg += f"\nPode estar faltando um {error_messages.get(expected_token, expected_token)}"
        
        print(error_msg)
    else:
        print("Erro de sintaxe: fim de arquivo inesperado")
    
    sys.exit(1)

# Build the parser
parser = yacc.yacc()

# Parse function
def parse(data):
    return parser.parse(data)

