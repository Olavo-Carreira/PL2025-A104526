#!/usr/bin/env python3
import sys

class AnalisadorLexico:
    def __init__(self, entrada):
        self.entrada = entrada
        self.posicao = 0
        self.simbolos = []
        self.extrair_simbolos()
    
    def extrair_simbolos(self):
        texto = self.entrada.strip()
        i = 0
        
        while i < len(texto):
            c = texto[i]
            
            if c.isspace():
                i += 1
                continue
            
            if c in "+-*/":
                self.simbolos.append((c, c))
                i += 1
                continue
            
            if c.isdigit():
                inicio = i
                while i < len(texto) and texto[i].isdigit():
                    i += 1
                valor = int(texto[inicio:i])
                self.simbolos.append(('NUM', valor))
                continue
            
            i += 1
    
    def proximo_simbolo(self):
        if self.posicao < len(self.simbolos):
            simbolo = self.simbolos[self.posicao]
            self.posicao += 1
            return simbolo
        return None

class AnalisadorSintatico:
    def __init__(self, lexico):
        self.lexico = lexico
        self.simbolo_atual = None
        self.obter_proximo_simbolo()
    
    def obter_proximo_simbolo(self):
        self.simbolo_atual = self.lexico.proximo_simbolo()
    
    def falha(self):
        raise ValueError("Expressão inválida")
    
    def expressao(self):
        if self.simbolo_atual and self.simbolo_atual[0] == 'NUM':
            primeiro_operando = self.simbolo_atual[1]
            self.obter_proximo_simbolo()
            return (primeiro_operando, self.resto_expressao())
        else:
            self.falha()
    
    def resto_expressao(self):
        if not self.simbolo_atual:
            return None
        
        if self.simbolo_atual[0] in ['+', '-', '*', '/']:
            op = self.simbolo_atual[0]
            self.obter_proximo_simbolo()
            
            if self.simbolo_atual and self.simbolo_atual[0] == 'NUM':
                valor = self.simbolo_atual[1]
                self.obter_proximo_simbolo()
                return (op, (valor, self.resto_expressao()))
            else:
                self.falha()
        
        self.falha()
    
    def analisar(self):
        return self.expressao()

def processar_mult_div(acumulador, arvore):
    if arvore is None:
        return acumulador, None
    
    operador, (valor, resto) = arvore
    
    if operador == '*':
        acumulador = acumulador * valor
        return processar_mult_div(acumulador, resto)
    elif operador == '/':
        if valor == 0:
            raise ValueError("Divisão por zero")
        acumulador = acumulador / valor
        return processar_mult_div(acumulador, resto)
    else:
        return (acumulador, (operador, (valor, resto)))

def processar_soma_sub(acumulador, arvore):
    if arvore is None:
        return acumulador, None
    
    operador, (valor, resto) = arvore
    
    if operador == '+':
        acumulador = acumulador + valor
        return processar_soma_sub(acumulador, resto)
    elif operador == '-':
        acumulador = acumulador - valor
        return processar_soma_sub(acumulador, resto)
    else:
        raise ValueError("Operador não reconhecido")

def avaliar(arvore):
    acumulador, resto = arvore
    
    acumulador, resto = processar_mult_div(acumulador, resto)
    
    if resto is not None:
        acumulador, resto = processar_soma_sub(acumulador, resto)
    
    if isinstance(acumulador, float) and acumulador.is_integer():
        return int(acumulador)
    
    return acumulador

def avaliar_expressao(expressao):
    try:
        lexico = AnalisadorLexico(expressao)
        sintatico = AnalisadorSintatico(lexico)
        arvore = sintatico.analisar()
        resultado = avaliar(arvore)
        return resultado
    except ValueError as e:
        return f"Erro: {e}"

if __name__ == '__main__':
    print("Digite uma expressão para calcular ou 'sair' para encerrar.")
    
    while True:
        try:
            expressao = input("\n>> ")
            
            if expressao.lower() == 'sair':
                print("Encerrado!")
                break
                
            resultado = avaliar_expressao(expressao)
            print(resultado)
            
        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo user.")
            break
        except Exception as e:
            print(f"Erro: {e}", file=sys.stderr)