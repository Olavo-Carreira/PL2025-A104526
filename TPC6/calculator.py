import re

def calcular_expressao(expressao):

    expressao = expressao.strip()
    
    multiplicacao_divisao = r'(\d+\.?\d*)\s*([*/])\s*(\d+\.?\d*)'
    
    match = re.search(multiplicacao_divisao, expressao)
    while match:
        # Extrai os números e o operador
        num1 = float(match.group(1))
        operador = match.group(2)
        num2 = float(match.group(3))
        
        if operador == '*':
            resultado_parcial = num1 * num2
        else:  # operador == '/'
            resultado_parcial = num1 / num2
        
        inicio = match.start()
        fim = match.end()
        expressao = expressao[:inicio] + str(resultado_parcial) + expressao[fim:]
        
        # Procura a próxima multiplicação ou divisão
        match = re.search(multiplicacao_divisao, expressao)
    
    elementos = re.findall(r'(-?\d+\.?\d*)|([+\-])', expressao)
    
    valores = []
    for num, op in elementos:
        if num:  # Se for um número
            valores.append(float(num))
        elif op:  # Se for um operador
            valores.append(op)
  
    if len(valores) > 0 and isinstance(valores[0], str) and valores[0] == '-':
        valores[1] = -valores[1]  # Aplica o sinal negativo ao primeiro número
        valores.pop(0)  # Remove o operador de menos
    
 
    if not valores:
        return 0
        
    resultado = valores[0]  
    

    for i in range(1, len(valores), 2):
        if i+1 < len(valores):
            operador = valores[i]
            numero = valores[i+1]
            
            if operador == '+':
                resultado += numero
            elif operador == '-':
                resultado -= numero
    

    if resultado == int(resultado):
        return int(resultado)
    return resultado


if __name__ == '__main__':
    print("Digite uma expressão para calcular ou 'sair' para encerrar.")
    
    while True:
        try:
            expressao = input("\n>> ")
            
            if expressao.lower() == 'sair':
                print("Encerrado!")
                break
                
            # Calcula e mostra o resultado
            resultado = calcular_expressao(expressao)
            print(resultado)
            
        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro: {e}")
