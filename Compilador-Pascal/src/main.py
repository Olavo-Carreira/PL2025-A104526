#!/usr/bin/env python3
"""
Compilador Pascal - Programa Principal
Este módulo integra todas as fases de compilação: análise léxica, análise sintática,
análise semântica e geração de código.
"""

import sys
import os
import argparse
from lexer import lexer, test_lexer
from parser import parse
from semantic import SemanticAnalyzer
from codegen import generate_code

def show_tokens(code, verbose=False):
    """Executa apenas a análise léxica e exibe os tokens."""
    tokens = test_lexer(code)
    print("=== Tokens encontrados ===")
    for token_type, token_value in tokens:
        print(f"{token_type}: {token_value}")
    return tokens

def show_ast(ast, verbose=False):
    """Exibe a árvore sintática abstrata (AST)."""
    if ast:
        print("=== Árvore Sintática Abstrata (AST) ===")
        print(ast)
    else:
        print("Erro: Não foi possível gerar a AST.")
    return ast

def run_semantic_analysis(ast, verbose=False):
    """Executa a análise semântica e exibe os resultados."""
    analyzer = SemanticAnalyzer()
    is_valid, errors, warnings = analyzer.analyze(ast)
    
    if warnings:
        print("=== Avisos Semânticos ===")
        for warning in warnings:
            print(f"Aviso: {warning}")
    
    if not is_valid:
        print("=== Erros Semânticos ===")
        for error in errors:
            print(f"Erro: {error}")
        return None
    
    if verbose:
        print("Análise semântica concluída com sucesso!")
    
    return analyzer.current_scope

def generate_and_show_code(ast, symbol_table, output_file=None, verbose=False):
    """Gera o código intermediário e opcionalmente salva em um arquivo."""
    if not ast or not symbol_table:
        print("Erro: Não é possível gerar código sem AST ou tabela de símbolos válida.")
        return None
    
    code = generate_code(ast, symbol_table)
    
    if verbose:
        print("=== Código Gerado ===")
        for instruction in code:
            print(instruction)
    
    if output_file:
        with open(output_file, 'w') as f:
            for instruction in code:
                f.write(f"{instruction}\n")
        print(f"Código gerado salvo em: {output_file}")
    
    return code

def compile_file(file_path, options):
    """Compila um arquivo Pascal completo."""
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        if options.tokens_only:
            show_tokens(source_code, options.verbose)
            return
        
        # Análise sintática
        ast = parse(source_code)
        if options.ast_only:
            show_ast(ast, options.verbose)
            return
        
        # Análise semântica
        symbol_table = run_semantic_analysis(ast, options.verbose)
        if not symbol_table:
            return  # Erros semânticos encontrados
        
        # Geração de código
        output_file = options.output
        if not output_file and not options.no_code:
            # Nome do arquivo de saída baseado no de entrada
            output_file = os.path.splitext(file_path)[0] + '.ewvm'
        
        if not options.no_code:
            generate_and_show_code(ast, symbol_table, output_file, options.verbose)
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        if options.verbose:
            import traceback
            traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Compilador Pascal')
    parser.add_argument('source', help='Arquivo fonte Pascal a ser compilado')
    parser.add_argument('-o', '--output', help='Arquivo de saída para o código gerado')
    parser.add_argument('-t', '--tokens-only', action='store_true', help='Executa apenas a análise léxica')
    parser.add_argument('-a', '--ast-only', action='store_true', help='Executa a análise sintática e mostra a AST')
    parser.add_argument('-n', '--no-code', action='store_true', help='Não gerar código, apenas analisar')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso, mostra mais informações')
    
    args = parser.parse_args()
    compile_file(args.source, args)

if __name__ == "__main__":
    main()