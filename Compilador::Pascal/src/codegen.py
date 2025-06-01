class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table  # Tabela de símbolos do programa
        self.code = []  # Lista de instruções de código geradas
        self.label_counter = 0  # Contador para criação de labels
        self.string_counter = 0  # Contador para constantes de string
        self.strings = {}  # Armazenamento para constantes de string
        self.variable_offsets = {}  # Mapeamento de variáveis para endereços
        self.current_offset = 0  # Offset atual para variáveis no stack
        self.current_scope = 'global'  # Escopo atual (global, procedimento, função)
        self.procedure_starts = {}  # Mapeamento de procedimentos para seus pontos de entrada
        self.function_returns = {}  # Mapeamento de funções para seus tipos de retorno
    
    def generate(self, ast):
        """Gera código a partir da AST."""
        self.visit(ast)
        return self.code
    
    def emit(self, instruction):
        """Adiciona uma instrução ao código."""
        self.code.append(instruction)
    
    def emit_comment(self, comment):
        """Adiciona um comentário ao código."""
        # Comentários desativados para compatibilidade com EWVM
        pass
    
    def create_label(self):
        """Cria um novo label único."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def add_string(self, string_value):
        """Adiciona uma constante de string e retorna seu identificador."""
        # Em EWVM, as strings são definidas diretamente com PUSHS
        return f'"{string_value}"'
    
    def visit(self, node):
        """Visita um nó da AST."""
        method_name = f'generate_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Método genérico para nós sem visitantes específicos."""
        for child in node.children:
            if child:
                self.visit(child)
    
    def generate_Program(self, node):
        """Gera código para um nó de programa."""
        # Adiciona PUSHIs iniciais necessários para EWVM
        self.emit("PUSHI 0")
        self.emit("PUSHI 0")
        self.emit("START")
        
        # Gera código para o bloco do programa
        self.visit(node.children[1])
        
        # Finaliza o programa
        self.emit("STOP")
    
    def generate_ProgramBlock(self, node):
        """Gera código para um bloco de programa (inclui declarações de subprogramas)."""
        # Processa declarações de variáveis
        self.visit(node.children[0])  # Declarations
        
        # Se existem declarações de subprogramas, processa-as
        if len(node.children) > 2:
            # Pula as declarações de subprogramas por enquanto
            subprogram_label = self.create_label()
            self.emit(f"JUMP {subprogram_label}")
            
            # Processa as declarações de subprogramas
            self.visit(node.children[1])  # SubprogramDeclarations
            
            # Marca o início do bloco principal
            self.emit(f"{subprogram_label}:")
            
            # Gera código para o bloco principal
            self.visit(node.children[2])  # CompoundStatement
        else:
            # Não há subprogramas, apenas gera código para o bloco principal
            self.visit(node.children[1])  # CompoundStatement
    
    def generate_Block(self, node):
        """Gera código para um bloco (declarações + instruções)."""
        # Processa declarações para alocar espaço na pilha
        self.visit(node.children[0])  # Declarations
        
        # Gera código para instruções
        self.visit(node.children[1])  # CompoundStatement
    
    def generate_Declarations(self, node):
        """Gera código para declarações de variáveis."""
        # Conta o espaço total necessário para variáveis
        total_space = 0
        
        # Processa cada declaração
        for child in node.children:
            if child and child.type != 'Empty':
                # Se for DeclarationList, processa cada declaração
                if child.type == 'DeclarationList':
                    for decl in child.children:
                        total_space += self.process_declaration(decl)
                else:
                    total_space += self.process_declaration(child)
        
        # Aloca espaço na pilha para as variáveis
        if total_space > 0:
            self.emit(f"ALLOC {total_space}")
    
    def process_declaration(self, node):
        """Processa uma declaração e retorna o espaço necessário."""
        if node.type != 'Declaration':
            return 0
        
        id_list = node.children[0]
        type_node = node.children[1]
        
        # Obtém informações do tipo
        size_per_var = self.get_type_size(type_node)
        total_size = 0
        
        # Processa cada identificador
        for id_node in id_list.children:
            var_name = id_node.leaf
            
            # Armazena o offset da variável
            self.variable_offsets[var_name] = self.current_offset
            self.emit_comment(f"Variable {var_name} at offset {self.current_offset}")
            
            # Atualiza os offsets
            self.current_offset += size_per_var
            total_size += size_per_var
        
        return total_size
    
    def get_type_size(self, type_node):
        """Retorna o tamanho em palavras do tipo especificado."""
        if type_node.type == 'Type':
            # Tipos simples (integer, boolean, string) ocupam 1 palavra
            return 1
        elif type_node.type == 'ArrayType':
            # Tamanho do array é (limite_superior - limite_inferior + 1) * tamanho_elemento
            range_node = type_node.children[0]
            elem_type_node = type_node.children[1]
            
            range_info = range_node.leaf  # (min, max)
            array_length = range_info[1] - range_info[0] + 1
            elem_size = self.get_type_size(elem_type_node)
            
            return array_length * elem_size
        
        # Tipo desconhecido
        return 1
    
    def generate_CompoundStatement(self, node):
        """Gera código para um bloco composto (begin...end)."""
        # Gera código para a lista de instruções
        if node.children:
            self.visit(node.children[0])
    
    def generate_StatementList(self, node):
        """Gera código para uma lista de instruções."""
        for child in node.children:
            if child and child.type != 'Empty':
                self.visit(child)
    
    def generate_Assignment(self, node):
        """Gera código para uma atribuição."""
        variable_node = node.children[0]
        expression_node = node.children[1]
        
        # Gera código para calcular o valor da expressão
        # O resultado fica no topo da pilha
        self.visit(expression_node)
        
        # Armazena o resultado na variável
        if variable_node.type == 'Variable':
            var_name = variable_node.leaf
            var_offset = self.variable_offsets.get(var_name, 0)
            self.emit(f"STOREG {var_offset}")  # Mudou de STORE para STOREG
        elif variable_node.type == 'ArrayAccess':
            array_name = variable_node.children[0].leaf
            array_base = self.variable_offsets.get(array_name, 0)
            
            # Primeiro, calcula o índice
            self.visit(variable_node.children[1])
            
            # Ajusta o índice considerando o limite inferior do array
            # (assume que temos essa informação da tabela de símbolos)
            array_info = self.symbol_table.lookup(array_name)
            if array_info and 'type' in array_info and array_info['type'].get('kind') == 'array':
                lower_bound = array_info['type']['range'][0]
                if lower_bound != 0:
                    self.emit(f"PUSHI {lower_bound}")
                    self.emit("SUB")
            
            # Calcula o endereço: base + índice
            self.emit(f"PUSHG {array_base}")  # Mudou de PUSHI para PUSHG
            self.emit("ADD")  # Poderia ser PADD para EWVM
            
            # Agora temos o endereço no topo da pilha, trocamos com o valor a armazenar
            self.emit("SWAP")
            
            # Armazena o valor no endereço calculado
            self.emit("STOREN")
    
    def generate_Variable(self, node):
        """Gera código para carregar o valor de uma variável."""
        var_name = node.leaf
        var_offset = self.variable_offsets.get(var_name, 0)
        self.emit(f"PUSHG {var_offset}")  # Mudou de LOAD para PUSHG
    
    def generate_ArrayAccess(self, node):
        """Gera código para acessar um elemento de array."""
        array_name = node.children[0].leaf
        array_base = self.variable_offsets.get(array_name, 0)
        
        # Calcula o índice
        self.visit(node.children[1])
        
        # Ajusta o índice considerando o limite inferior do array
        array_info = self.symbol_table.lookup(array_name)
        if array_info and 'type' in array_info and array_info['type'].get('kind') == 'array':
            lower_bound = array_info['type']['range'][0]
            if lower_bound != 0:
                self.emit(f"PUSHI {lower_bound}")
                self.emit("SUB")
        
        # Calcula o endereço: base + índice
        self.emit(f"PUSHG {array_base}")  # Mudou de PUSHI para PUSHG
        self.emit("ADD")  # Poderia ser PADD para EWVM
        
        # Carrega o valor do endereço calculado
        self.emit("LOADN")
    
    def generate_IntegerConstant(self, node):
        """Gera código para uma constante inteira."""
        value = node.leaf
        self.emit(f"PUSHI {value}")
    
    def generate_StringConstant(self, node):
        """Gera código para uma constante string."""
        value = node.leaf
        self.emit(f"PUSHS {self.add_string(value)}")
    
    def generate_BooleanConstant(self, node):
        """Gera código para uma constante booleana."""
        value = 1 if node.leaf.lower() == 'true' else 0
        self.emit(f"PUSHI {value}")
    
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
        elif operator == '/':
            self.emit("DIV")
        elif operator == 'div':
            self.emit("DIV")
        elif operator == 'mod':
            self.emit("MOD")
        elif operator == '=':
            self.emit("EQUAL")
        elif operator == '<>':
            self.emit("EQUAL")
            self.emit("NOT")
        elif operator == '<':
            self.emit("INF")
        elif operator == '<=':
            self.emit("INFEQ")
        elif operator == '>':
            self.emit("SUP")
        elif operator == '>=':
            self.emit("SUPEQ")
        elif operator == 'and':
            self.emit("AND")
        elif operator == 'or':
            self.emit("OR")
    
    def generate_IfStatement(self, node):
        """Gera código para uma instrução if."""
        # Gera código para a condição
        self.visit(node.children[0])
        
        # Cria labels para os saltos
        else_label = self.create_label()
        end_if_label = self.create_label()
        
        # Se a condição for falsa, salta para o else ou para o fim
        self.emit(f"JZ {else_label}")
        
        # Gera código para o bloco then
        self.visit(node.children[1])
        
        # Após o bloco then, salta para o fim do if
        self.emit(f"JUMP {end_if_label}")
        
        # Marca o início do bloco else
        self.emit(f"{else_label}:")
        
        # Se houver um bloco else, gera código para ele
        if len(node.children) > 2:
            self.visit(node.children[2])
        
        # Marca o fim do if
        self.emit(f"{end_if_label}:")

    def generate_WhileStatement(self, node):
        """Gera código para uma instrução while."""
        # Cria labels para os saltos
        start_while = self.create_label()
        end_while = self.create_label()
        
        # Marca o início do loop
        self.emit(f"{start_while}:")
        
        # Gera código para a condição
        self.visit(node.children[0])
        
        # Se a condição for falsa, salta para o fim do loop
        self.emit(f"JZ {end_while}")
        
        # Gera código para o corpo do loop
        self.visit(node.children[1])
        
        # Volta para verificar a condição novamente
        self.emit(f"JUMP {start_while}")
        
        # Marca o fim do loop
        self.emit(f"{end_while}:")
    
    def generate_ForStatement(self, node):
        """Gera código para uma instrução for."""
        var_node = node.children[0]
        start_expr = node.children[1]
        end_expr = node.children[2]
        body = node.children[3]
        direction = node.leaf  # 'to' ou 'downto'
        
        var_name = var_node.leaf
        var_offset = self.variable_offsets.get(var_name, 0)
        
        # Calcula o valor inicial e atribui à variável de controle
        self.visit(start_expr)
        self.emit(f"STOREG {var_offset}")  # Mudou de STORE para STOREG
        
        # Calcula o valor final (limite) e guarda no stack
        self.visit(end_expr)
        
        # Cria labels para os saltos
        start_loop = self.create_label()
        end_loop = self.create_label()
        
        # Marca o início do loop
        self.emit(f"{start_loop}:")
        
        # Compara a variável de controle com o limite
        self.emit(f"PUSHG {var_offset}")  # Mudou de LOAD para PUSHG
        
        # A comparação depende se é 'to' (<=) ou 'downto' (>=)
        if direction == 'to':
            self.emit("SWAP")
            self.emit("INFEQ")
        else:  # downto
            self.emit("SWAP")
            self.emit("SUPEQ")
        
        # Se a condição for falsa, salta para o fim do loop
        self.emit(f"JZ {end_loop}")
        
        # Gera código para o corpo do loop
        self.visit(body)
        
        # Incrementa ou decrementa a variável de controle
        self.emit(f"PUSHG {var_offset}")  # Mudou de LOAD para PUSHG
        if direction == 'to':
            self.emit("PUSHI 1")
            self.emit("ADD")
        else:  # downto
            self.emit("PUSHI 1")
            self.emit("SUB")
        self.emit(f"STOREG {var_offset}")  # Mudou de STORE para STOREG
        
        # Volta para verificar a condição novamente
        self.emit(f"JUMP {start_loop}")
        
        # Marca o fim do loop
        self.emit(f"{end_loop}:")
    
    def generate_IOCall(self, node):
        """Gera código para uma chamada de procedimento de I/O (write, writeln, read, readln)."""
        proc_name = node.leaf.lower()
        
        if proc_name in ('write', 'writeln'):
            # Para write/writeln, avalia cada expressão e imprime
            if node.children:
                expr_list = node.children[0]
                for expr in expr_list.children:
                    # Avalia a expressão
                    self.visit(expr)
                    
                    # Imprime o valor baseado em seu tipo
                    if expr.type == 'StringConstant':
                        self.emit("WRITES")
                    elif expr.type in ('IntegerConstant', 'Variable', 'ArrayAccess', 'BinaryOperation'):
                        self.emit("WRITEI")
                    else:
                        # Para outros tipos, tenta como inteiro
                        self.emit("WRITEI")
            
            # Se for writeln, adiciona uma quebra de linha
            if proc_name == 'writeln':
                self.emit("WRITELN")
        
        elif proc_name in ('read', 'readln'):
            # Para read/readln, lê valores para cada variável
            if node.children:
                var_list = node.children[0]
                for var in var_list.children:
                    if var.type == 'Variable':
                        var_name = var.leaf
                        var_offset = self.variable_offsets.get(var_name, 0)
                        
                        # Lê um valor do input e armazena na variável
                        self.emit("READ")
                        self.emit("ATOI")  # Adicionou conversão para inteiro
                        self.emit(f"STOREG {var_offset}")  # Mudou de STORE para STOREG
                    elif var.type == 'ArrayAccess':
                        array_name = var.children[0].leaf
                        array_base = self.variable_offsets.get(array_name, 0)
                        
                        # Calcula o índice do array
                        self.visit(var.children[1])
                        
                        # Ajusta o índice considerando o limite inferior
                        array_info = self.symbol_table.lookup(array_name)
                        if array_info and 'type' in array_info and array_info['type'].get('kind') == 'array':
                            lower_bound = array_info['type']['range'][0]
                            if lower_bound != 0:
                                self.emit(f"PUSHI {lower_bound}")
                                self.emit("SUB")
                        
                        # Calcula o endereço: base + índice
                        self.emit(f"PUSHG {array_base}")  # Mudou de PUSHI para PUSHG
                        self.emit("ADD")  # Poderia ser PADD para EWVM
                        
                        # Lê um valor e armazena no endereço calculado
                        self.emit("READ")
                        self.emit("ATOI")  # Adicionou conversão para inteiro
                        self.emit("SWAP")
                        self.emit("STOREN")
    
    def generate_ProcedureCall(self, node):
        """Gera código para uma chamada de procedimento."""
        proc_name = node.leaf
        
        # Avalia e empilha os argumentos, se houver
        if node.children:
            expr_list = node.children[0]
            for expr in expr_list.children:
                self.visit(expr)
        
        # Chama o procedimento
        if proc_name in self.procedure_starts:
            proc_label = self.procedure_starts[proc_name]
            self.emit(f"PUSHA {proc_label}")
            self.emit("CALL")
    
    def generate_ProcedureDeclaration(self, node):
        """Gera código para uma declaração de procedimento."""
        proc_name = node.children[0].leaf
        param_list = node.children[1]
        proc_body = node.children[2]
        
        # Cria um label para o início do procedimento
        proc_label = self.create_label()
        self.procedure_starts[proc_name] = proc_label
        
        # Guarda offset atual de variáveis
        old_offset = self.current_offset
        old_variables = self.variable_offsets.copy()
        
        # Reseta o offset para o escopo local do procedimento
        self.current_offset = 0
        self.variable_offsets.clear()
        
        # Marca o início do código do procedimento
        self.emit(f"{proc_label}:")
        
        # Processamento de parâmetros
        param_count = 0
        if param_list and param_list.children:
            for param in param_list.children:
                id_list = param.children[0]
                for id_node in id_list.children:
                    param_name = id_node.leaf
                    # Parâmetros começam em offset negativo relativo ao frame pointer
                    self.variable_offsets[param_name] = -2 - param_count
                    param_count += 1
        
        # Gera código para o corpo do procedimento
        self.visit(proc_body)
        
        # Retorno do procedimento
        self.emit("RETURN")
        
        # Restaura o contexto anterior
        self.current_offset = old_offset
        self.variable_offsets = old_variables
    
    def generate_FunctionDeclaration(self, node):
        """Gera código para uma declaração de função."""
        func_name = node.children[0].leaf
        param_list = node.children[1]
        return_type = node.children[2]
        func_body = node.children[3]
        
        # Semelhante à declaração de procedimento, mas com retorno
        func_label = self.create_label()
        self.procedure_starts[func_name] = func_label
        self.function_returns[func_name] = return_type.leaf
        
        # Guarda offset atual de variáveis
        old_offset = self.current_offset
        old_variables = self.variable_offsets.copy()
        
        # Reseta o offset para o escopo local da função
        self.current_offset = 0
        self.variable_offsets.clear()
        
        # Marca o início do código da função
        self.emit(f"{func_label}:")
        
        # Processamento de parâmetros
        param_count = 0
        if param_list and param_list.children:
            for param in param_list.children:
                id_list = param.children[0]
                for id_node in id_list.children:
                    param_name = id_node.leaf
                    self.variable_offsets[param_name] = -2 - param_count
                    param_count += 1
        
        # Reserva espaço para o valor de retorno
        return_var_offset = self.current_offset
        self.variable_offsets['$return'] = return_var_offset
        self.current_offset += 1
        self.emit("PUSHI 0")  # Inicializa o valor de retorno
        
        # Gera código para o corpo da função
        self.visit(func_body)
        
        # Carrega o valor de retorno antes de retornar
        self.emit(f"PUSHG {return_var_offset}")  # Mudou de LOAD para PUSHG
        self.emit("RETURN")
        
        # Restaura o contexto anterior
        self.current_offset = old_offset
        self.variable_offsets = old_variables
    
    def generate_FunctionCall(self, node):
        """Gera código para uma chamada de função."""
        func_name = node.leaf
        
        # Avalia e empilha os argumentos, se houver
        if node.children:
            expr_list = node.children[0]
            for expr in expr_list.children:
                self.visit(expr)
        
        # Chama a função
        if func_name in self.procedure_starts:
            func_label = self.procedure_starts[func_name]
            self.emit(f"PUSHA {func_label}")
            self.emit("CALL")
        else:
            # Tratamento para funções predefinidas como abs, sqr, etc.
            if func_name.lower() == 'abs':
                # Implementação simplificada de abs
                label_skip = self.create_label()
                self.emit("DUP")
                self.emit("PUSHI 0")
                self.emit("INF")
                self.emit(f"JZ {label_skip}")
                self.emit("PUSHI -1")
                self.emit("MUL")
                self.emit(f"{label_skip}:")
            # Outras funções predefinidas podem ser adicionadas aqui

def generate_code(ast, symbol_table):
    """Função principal para gerar código a partir de uma AST."""
    generator = CodeGenerator(symbol_table)
    code = generator.generate(ast)
    return code