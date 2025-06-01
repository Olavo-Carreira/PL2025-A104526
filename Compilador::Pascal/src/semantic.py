class SymbolTable:
    def __init__(self):
        self.symbols = {}          # Mapeia nomes (variáveis, funções...) para as suas informações
        self.parent = None         # Referência ao escopo pai (para escopos aninhados)
        self.level = 0             # Nível do escopo (0 = global, >0 = aninhado)

    def add(self, name, info):
        """Adiciona um novo símbolo (variável, função, etc.) ao escopo atual."""
        self.symbols[name.lower()] = info  # Pascal é insensível a maiúsculas/minúsculas

    def lookup(self, name):
        """Procura por um símbolo, começando no escopo atual e subindo até o global."""
        name = name.lower()
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        return None

    def lookup_current_scope(self, name):
        """Procura um símbolo apenas neste escopo (sem subir)."""
        return self.symbols.get(name.lower())

    def create_child_scope(self):
        """Cria um novo escopo como filho do atual."""
        child = SymbolTable()
        child.parent = self
        child.level = self.level + 1
        return child


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.errors = []
        self.warnings = []
        
        # Estados úteis durante a análise
        self.in_loop = False
        self.current_function = None
        self.has_return = False
        self.in_lhs_of_assignment = False

    def analyze(self, ast):
        """Inicia a análise semântica da árvore sintática (AST)."""
        if ast:
            self.visit(ast)
        return len(self.errors) == 0, self.errors, self.warnings

    def add_error(self, msg): self.errors.append(msg)
    def add_warning(self, msg): self.warnings.append(msg)

    def enter_scope(self):
        """Entra num novo escopo (por exemplo, dentro de uma função ou bloco)."""
        self.current_scope = self.current_scope.create_child_scope()

    def exit_scope(self):
        """Sai do escopo atual e retorna ao escopo pai."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    def visit(self, node):
        """Despacha a visita de um nó da AST para o método apropriado."""
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Visita padrão: percorre todos os filhos recursivamente."""
        for child in node.children:
            if child:
                self.visit(child)

    # ---- Visitas específicas por tipo de nó ----

    def visit_Program(self, node):
        program_name = node.children[0].leaf
        self.visit(node.children[1])  # Visita o bloco principal do programa

    def visit_Block(self, node):
        self.visit(node.children[0])  # Declarações
        self.visit(node.children[1])  # Instruções

    def visit_Declarations(self, node):
        for child in node.children:
            if child and child.type != 'Empty':
                self.visit(child)

    def visit_DeclarationList(self, node):
        for child in node.children:
            if child:
                self.visit(child)

    def visit_Declaration(self, node):
        id_list = node.children[0]
        type_node = node.children[1]
        type_info = self.get_type_info(type_node)

        for child in id_list.children:
            if child.type == 'ID':
                var_name = child.leaf
                if self.current_scope.lookup_current_scope(var_name):
                    self.add_error(f"Erro: Variável '{var_name}' redeclarada no mesmo escopo")
                else:
                    self.current_scope.add(var_name, {
                        'kind': 'variable',
                        'type': type_info,
                        'initialized': False
                    })

    def get_type_info(self, type_node):
        """Extrai o tipo de um nó de tipo."""
        if type_node.type == 'Type':
            return type_node.leaf
        elif type_node.type == 'ArrayType':
            range_info = type_node.children[0].leaf  # Ex: (1, 10)
            elem_type = self.get_type_info(type_node.children[1])

            if not all(isinstance(b, int) for b in range_info):
                self.add_error("Erro: Limites de array devem ser inteiros")
            if range_info[0] > range_info[1]:
                self.add_error(f"Erro: Limite inferior {range_info[0]} maior que o superior {range_info[1]}")

            return {
                'kind': 'array',
                'range': range_info,
                'elem_type': elem_type
            }
        return None

    def visit_CompoundStatement(self, node):
        if node.children:
            self.visit(node.children[0])  # Lista de instruções

    def visit_StatementList(self, node):
        for child in node.children:
            if child:
                self.visit(child)

    def visit_Assignment(self, node):
        self.in_lhs_of_assignment = True
        var_node = node.children[0]
        var_type = self.visit(var_node)
        self.in_lhs_of_assignment = False

        if not var_type:
            return None

        expr_type = self.visit(node.children[1])
        if not expr_type:
            return None

        if not self.check_type_compatibility(var_type, expr_type):
            name = var_node.leaf if var_node.type == 'Variable' else "elemento de array"
            self.add_error(f"Erro: Incompatibilidade de tipos na atribuição a '{name}'. Esperado '{var_type}', mas recebeu '{expr_type}'")

        if var_node.type == 'Variable':
            var_info = self.current_scope.lookup(var_node.leaf)
            if var_info:
                var_info['initialized'] = True
        elif var_node.type == 'ArrayAccess':
            arr_info = self.current_scope.lookup(var_node.children[0].leaf)
            if arr_info:
                arr_info['initialized'] = True

        return var_type

    def check_type_compatibility(self, expected, actual):
        """Verifica se dois tipos são compatíveis (pode ser expandido)."""
        return expected == actual

    
    def visit_Variable(self, node):
        """Visita uma variável e devolve o seu tipo."""
        var_name = node.leaf
        var_info = self.current_scope.lookup(var_name)
        
        if not var_info:
            self.add_error(f"Erro: A variável '{var_name}' não foi declarada.")
            return None

        # Só avisamos sobre inicialização se a variável estiver a ser usada (não no lado esquerdo de uma atribuição)
        if not self.in_lhs_of_assignment and not var_info.get('initialized', False) and var_info.get('kind') == 'variable':
            self.add_warning(f"Aviso: A variável '{var_name}' pode não ter sido inicializada.")

        if var_info.get('kind') == 'variable':
            return var_info.get('type')
        elif var_info.get('kind') == 'function':
            self.add_error(f"Erro: '{var_name}' é uma função, não uma variável.")
        elif var_info.get('kind') == 'procedure':
            self.add_error(f"Erro: '{var_name}' é um procedimento, não uma variável.")
        
        return None

    def visit_ArrayAccess(self, node):
        """Visita o acesso a um elemento de array e devolve o tipo do elemento."""
        array_node = node.children[0]
        array_name = array_node.leaf
        array_info = self.current_scope.lookup(array_name)

        if not array_info:
            self.add_error(f"Erro: O array '{array_name}' não foi declarado.")
            return None

        if not isinstance(array_info.get('type'), dict) or array_info['type'].get('kind') != 'array':
            self.add_error(f"Erro: '{array_name}' não é um array.")
            return None

        if not self.in_lhs_of_assignment and not array_info.get('initialized', False):
            self.add_warning(f"Aviso: O array '{array_name}' pode não ter sido inicializado.")

        index_node = node.children[1]
        index_type = self.visit(index_node)

        if index_type != 'integer':
            self.add_error(f"Erro: O índice do array deve ser inteiro, mas foi encontrado '{index_type}'.")

        if index_node.type == 'IntegerConstant':
            bounds = array_info['type'].get('range')
            idx_val = index_node.leaf
            if bounds and not (bounds[0] <= idx_val <= bounds[1]):
                self.add_error(f"Erro: O índice {idx_val} está fora dos limites permitidos para o array '{array_name}' [{bounds[0]}..{bounds[1]}].")

        return array_info['type'].get('elem_type')

    def visit_IfStatement(self, node):
        """Visita uma instrução if."""
        condition = node.children[0]
        condition_type = self.visit(condition)

        if condition_type != 'boolean':
            self.add_error(f"Erro: A condição do if deve ser booleana, mas foi '{condition_type}'.")

        # Guarda o estado atual das variáveis inicializadas
        init_before = {name: info.get('initialized', False) for name, info in self.current_scope.symbols.items()}

        # Analisa o bloco then
        self.visit(node.children[1])

        init_then = {name: info.get('initialized', False) for name, info in self.current_scope.symbols.items()}

        # Restaura o estado antes do else
        for name, was_init in init_before.items():
            if name in self.current_scope.symbols:
                self.current_scope.symbols[name]['initialized'] = was_init

        if len(node.children) > 2:
            # Analisa o bloco else
            self.visit(node.children[2])
            init_else = {name: info.get('initialized', False) for name, info in self.current_scope.symbols.items()}

            for name in init_then:
                if name in self.current_scope.symbols:
                    self.current_scope.symbols[name]['initialized'] = init_then[name] and init_else.get(name, False)
        else:
            # Sem else, mantém apenas as variáveis que já estavam inicializadas antes
            for name in init_then:
                if name in self.current_scope.symbols:
                    self.current_scope.symbols[name]['initialized'] = init_before.get(name, False)

    def visit_WhileStatement(self, node):
        """Visita uma instrução while."""
        condition_type = self.visit(node.children[0])

        if condition_type != 'boolean':
            self.add_error(f"Erro: A condição do while deve ser booleana, mas foi '{condition_type}'.")

        # Entramos num loop
        prev_loop_state = self.in_loop
        self.in_loop = True
        self.visit(node.children[1])
        self.in_loop = prev_loop_state

    def visit_ForStatement(self, node):
        """Visita uma instrução for."""
        var_name = node.children[0].leaf
        var_info = self.current_scope.lookup(var_name)

        if not var_info:
            self.add_error(f"Erro: A variável de controlo '{var_name}' não foi declarada.")
        else:
            if var_info.get('type') != 'integer':
                self.add_error(f"Erro: A variável de controlo do for deve ser do tipo 'integer', mas foi '{var_info.get('type')}'.")
            var_info['initialized'] = True

        start_type = self.visit(node.children[1])
        if start_type != 'integer':
            self.add_error(f"Erro: O valor inicial do for deve ser inteiro, mas foi '{start_type}'.")

        end_type = self.visit(node.children[2])
        if end_type != 'integer':
            self.add_error(f"Erro: O valor final do for deve ser inteiro, mas foi '{end_type}'.")

        prev_loop_state = self.in_loop
        self.in_loop = True
        self.visit(node.children[3])
        self.in_loop = prev_loop_state

    def visit_IOCall(self, node):
        """Visita uma chamada de entrada/saída: read, readln, write ou writeln."""
        proc_name = node.leaf.lower()

        if node.children:
            args = node.children[0]

            if proc_name in ('read', 'readln'):
                for var in args.children:
                    if var.type not in ('Variable', 'ArrayAccess'):
                        self.add_error(f"Erro: Os argumentos de {proc_name} devem ser variáveis.")
                    else:
                        self.in_lhs_of_assignment = True
                        self.visit(var)
                        self.in_lhs_of_assignment = False

                        if var.type == 'Variable':
                            var_info = self.current_scope.lookup(var.leaf)
                            if var_info:
                                var_info['initialized'] = True
                        elif var.type == 'ArrayAccess':
                            arr_name = var.children[0].leaf
                            arr_info = self.current_scope.lookup(arr_name)
                            if arr_info:
                                arr_info['initialized'] = True
            else:  # write ou writeln
                for expr in args.children:
                    expr_type = self.visit(expr)
                    if expr_type not in ('integer', 'boolean', 'string', 'Integer') and not isinstance(expr_type, dict):
                        self.add_error(f"Erro: Não é possível imprimir valores do tipo '{expr_type}' com {proc_name}.")

    def visit_ProcedureCall(self, node):
        """Visita uma chamada de procedimento."""
        proc_name = node.leaf
        proc_info = self.current_scope.lookup(proc_name)

        if not proc_info:
            self.add_error(f"Erro: O procedimento '{proc_name}' não foi declarado.")
            return

        if proc_info.get('kind') != 'procedure':
            self.add_error(f"Erro: '{proc_name}' não é um procedimento.")
            return

        if node.children and proc_info.get('params'):
            args = node.children[0]
            expected = proc_info['params']

            if len(args.children) != len(expected):
                self.add_error(f"Erro: O procedimento '{proc_name}' espera {len(expected)} parâmetros, mas recebeu {len(args.children)}.")
            else:
                for i, (arg_node, param_info) in enumerate(zip(args.children, expected)):
                    arg_type = self.visit(arg_node)
                    expected_type = param_info.get('type')

                    if not self.check_type_compatibility(expected_type, arg_type):
                        self.add_error(f"Erro: Tipo incompatível no parâmetro {i+1} de '{proc_name}'. Esperado '{expected_type}', mas foi '{arg_type}'.")


        
        def visit_ProcedureDeclaration(self, node):
            """Visita uma declaração de procedimento."""
            proc_name = node.children[0].leaf
            param_list = node.children[1]
            proc_body = node.children[2]
            
            # Verifica se o procedimento já foi declarado
            if self.current_scope.lookup_current_scope(proc_name):
                self.add_error(f"Erro: Procedimento '{proc_name}' redeclarado")
                return
            
            # Adiciona o procedimento à tabela de símbolos
            proc_info = {
                'kind': 'procedure',
                'params': [],
                'scope': self.current_scope  # Escopo onde foi declarado
            }
            
            self.current_scope.add(proc_name, proc_info)
            
            # Cria um novo escopo para o procedimento
            old_scope = self.current_scope
            proc_scope = self.enter_scope()
            
            # Processa os parâmetros
            if param_list and param_list.children:
                for param in param_list.children:
                    id_list = param.children[0]
                    type_node = param.children[1]
                    param_type = self.get_type_info(type_node)
                    
                    for id_node in id_list.children:
                        param_name = id_node.leaf
                        
                        # Adiciona o parâmetro ao escopo do procedimento
                        proc_scope.add(param_name, {
                            'kind': 'variable',
                            'type': param_type,
                            'initialized': True  # Parâmetros são sempre inicializados
                        })
                        
                        # Registra o parâmetro na lista de parâmetros do procedimento
                        proc_info['params'].append({
                            'name': param_name,
                            'type': param_type
                        })
            
            # Visita o corpo do procedimento
            self.visit(proc_body)
            
            # Restaura o escopo original
            self.current_scope = old_scope
    
    def visit_FunctionCall(self, node):
        """Visita uma chamada de função."""
        func_name = node.leaf
        func_info = self.current_scope.lookup(func_name)
        
        if not func_info:
            self.add_error(f"Erro: Função '{func_name}' não declarada")
            return None
        
        if func_info.get('kind') != 'function':
            self.add_error(f"Erro: '{func_name}' não é uma função")
            return None
        
        # Verifica os parâmetros, se houver
        if node.children and func_info.get('params'):
            expr_list = node.children[0]
            params_info = func_info.get('params', [])
            
            # Verifica o número de parâmetros
            if len(expr_list.children) != len(params_info):
                self.add_error(f"Erro: Número incorreto de parâmetros para '{func_name}'. Esperado {len(params_info)}, encontrado {len(expr_list.children)}")
            else:
                # Verifica cada parâmetro
                for i, (expr_node, param_info) in enumerate(zip(expr_list.children, params_info)):
                    expr_type = self.visit(expr_node)
                    param_type = param_info.get('type')
                    
                    if not self.check_type_compatibility(param_type, expr_type):
                        self.add_error(f"Erro: Tipo incompatível para parâmetro {i+1} de '{func_name}'. Esperado '{param_type}', encontrado '{expr_type}'")
        
        # Retorna o tipo de retorno da função
        return func_info.get('return_type')
    
    def visit_BinaryOperation(self, node):
        """Visita uma operação binária e retorna seu tipo."""
        # Obtém os tipos dos operandos
        left_node = node.children[0]
        right_node = node.children[1]
        operator = node.leaf
        
        left_type = self.visit(left_node)
        right_type = self.visit(right_node)
        
        if not left_type or not right_type:
            return None
        
        # Verifica a compatibilidade dos operandos com o operador
        if operator in ('+', '-', '*', '/', 'div', 'mod'):
            # Operadores aritméticos
            if left_type != 'integer' or right_type != 'integer':
                self.add_error(f"Erro: Operador '{operator}' requer operandos inteiros, encontrado '{left_type}' e '{right_type}'")
                return None
            
            # Verifica divisão por zero quando possível
            if operator in ('/', 'div', 'mod') and right_node.type == 'IntegerConstant' and right_node.leaf == 0:
                self.add_error(f"Erro: Divisão por zero detectada")
            
            return 'integer'
        
        elif operator in ('=', '<>', '<', '<=', '>', '>='):
            # Operadores relacionais
            if not self.check_type_compatibility(left_type, right_type):
                self.add_error(f"Erro: Não é possível comparar '{left_type}' com '{right_type}' usando o operador '{operator}'")
                return None
            
            return 'boolean'
        
        elif operator in ('and', 'or'):
            # Operadores lógicos
            if left_type != 'boolean' or right_type != 'boolean':
                self.add_error(f"Erro: Operador '{operator}' requer operandos booleanos, encontrado '{left_type}' e '{right_type}'")
                return None
            
            return 'boolean'
        
        self.add_error(f"Erro: Operador desconhecido '{operator}'")
        return None
    
    def visit_IntegerConstant(self, node):
        """Visita uma constante inteira."""
        return 'integer'
    
    def visit_StringConstant(self, node):
        """Visita uma constante string."""
        return 'string'
    
    def visit_BooleanConstant(self, node):
        """Visita uma constante booleana."""
        return 'boolean'
    
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
        
        # Outras regras de compatibilidade podem ser adicionadas aqui
        
        return False

# Exemplo de utilização
def analyze_semantics(ast):
    """Função principal para analisar a semântica de uma AST."""
    analyzer = SemanticAnalyzer()
    is_valid, errors, warnings = analyzer.analyze(ast)
    
    # Imprime erros, se houver
    if not is_valid:
        print("Erros semânticos encontrados:")
        for error in errors:
            print(f"  - {error}")
    
    # Imprime avisos, se houver
    if warnings:
        print("Avisos:")
        for warning in warnings:
            print(f"  - {warning}")
    
    return is_valid, errors, warnings

