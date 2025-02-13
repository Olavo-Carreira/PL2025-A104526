def somador_on_off():
    soma = 0
    somar_ativo = True  

    try:
        with open("input.txt", 'r') as ficheiro:
            for num_linha, linha in enumerate(ficheiro, 1):
                linha = linha.strip()  
                i = 0
                while i < len(linha):
                    if linha[i].isdigit():
                        numero_atual = ''
                        while i < len(linha) and linha[i].isdigit():
                            numero_atual += linha[i]
                            i += 1
                        if somar_ativo:
                            soma += int(numero_atual)
                    
                    # Verifica se ainda há caracteres para processar
                    if i < len(linha): 
                        if linha[i:i+2].lower() == 'on':  
                            somar_ativo = True
                            i += 2
                        elif linha[i:i+3].lower() == 'off':  
                            somar_ativo = False
                            i += 3
                        elif linha[i] == '=':  
                            print(f"Soma agora: {soma}\n{'-' * 30}")

                            i += 1
                        else:
                            i += 1  
                    else:
                        break  

    except FileNotFoundError:
        print("Erro: O ficheiro não foi encontrado.")

somador_on_off()