import json
import re
import sys
import os
from datetime import datetime

class MaquinaVending:
    def __init__(self, ficheiro_stock="stock.json"):
        self.stock = []
        self.ficheiro_stock = ficheiro_stock
        self.saldo = 0  # em cêntimos
        self.data_atual = datetime.now().strftime("%Y-%m-%d")  
        self.moedas_troco = {
            200: "2e",
            100: "1e",
            50: "50c",
            20: "20c",
            10: "10c",
            5: "5c",
            2: "2c",
            1: "1c"
        }
        # Definir os comandos disponíveis para o HELP
        self.comandos_disponiveis = {
            "LISTAR": "Lista todos os produtos disponíveis",
            "MOEDA [valores]": "Adiciona moedas ao saldo (ex: MOEDA 1e, 50c, 20c)",
            "SELECIONAR [código]": "Seleciona um produto para compra (ex: SELECIONAR A23)",
            "ADICIONAR [código] \"[nome]\" [quantidade] [preço]": "Adiciona ou atualiza um produto no stock",
            "HELP": "Exibe esta lista de comandos",
            "SAIR": "Sai da máquina e devolve o troco"
        }
        self.carregar_stock()  
    
    def carregar_stock(self):
        """Carrega o stock a partir do ficheiro JSON utilizando regexp para validar o conteúdo."""
        try:
            if os.path.exists(self.ficheiro_stock):
                with open(self.ficheiro_stock, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    if conteudo.strip():  
                        if re.search(r'\[\s*\{\s*"cod"\s*:', conteudo):
                            self.stock = json.loads(conteudo)
                            print(f"maq: {self.data_atual}, Stock carregado, Estado atualizado.")
                        else:
                            print("maq: Formato do JSON inválido.")
                    else:
                        print("maq: Arquivo JSON vazio.")
            else:
                print(f"maq: Arquivo {self.ficheiro_stock} não encontrado.")
        except json.JSONDecodeError as e:
            print(f"maq: Erro ao ler JSON: {str(e)}.")
        except Exception as e:
            print(f"maq: Erro ao carregar stock: {str(e)}. ")
    
    def salvar_stock(self):
        """Salva o stock atual no ficheiro JSON."""
        try:
            with open(self.ficheiro_stock, 'w', encoding='utf-8') as f:
                json.dump(self.stock, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"maq: Erro ao salvar stock: {str(e)}")
    
    def listar_produtos(self):
        """Lista todos os produtos disponíveis na máquina."""
        print("maq:")
        print(f"{'cod':<5} | {'nome':<20} | {'quantidade':<12} | {'preço':<5}")
        print("-" * 50)
        
        # Verificar se há produtos para listar
        if not self.stock or len(self.stock) == 0:
            print("Não há produtos no estoque.")
            return
        
        try:
            for produto in self.stock:
                print(f"{produto['cod']:<5} | {produto['nome']:<20} | {produto['quant']:<12} | {produto['preco']}")
        except Exception as e:
            print(f"Erro ao listar produtos: {str(e)}")
    
    def adicionar_moeda(self, moedas_str):

        padrao = re.compile(r'(\d+)\s*([ec])', re.IGNORECASE)
        moedas = padrao.findall(moedas_str)
        
        if not moedas:
            print("maq: Formato de moeda inválido. Use formatos como '1e' para euros ou '50c' para cêntimos.")
            return
        
        valor_total = 0
        for valor, tipo in moedas:
            if tipo.lower() == 'e':
                valor_total += int(valor) * 100  # euros para cêntimos
            else:  # tipo == 'c'
                valor_total += int(valor)  # cêntimos
        
        self.saldo += valor_total
        self.exibir_saldo()
    
    def exibir_saldo(self):
        """Exibe o saldo atual formatado."""
        euros = self.saldo // 100
        centimos = self.saldo % 100
        
        if euros > 0 and centimos > 0:
            print(f"maq: Saldo = {euros}e{centimos}c")
        elif euros > 0:
            print(f"maq: Saldo = {euros}e")
        else:
            print(f"maq: Saldo = {centimos}c")
    
    def selecionar_produto(self, codigo):
        """Seleciona um produto para compra pelo código."""
        # Validar o formato do código usando expressões regulares
        if not re.match(r'^[A-Z]\d+$', codigo):
            print(f"maq: Código de produto inválido: {codigo}. Use formato como 'A23'.")
            self.exibir_saldo()
            return
            
        # Procurar o produto pelo código
        produto = None
        for p in self.stock:
            if p["cod"] == codigo:
                produto = p
                break
        
        if not produto:
            print(f"maq: Produto com código {codigo} não encontrado.")
            self.exibir_saldo()
            return
        
        # Verificar se o produto está em stock
        if produto["quant"] <= 0:
            print(f"maq: Desculpe, o produto \"{produto['nome']}\" está esgotado.")
            self.exibir_saldo()
            return
        
        # Converter preço para cêntimos
        preco_centimos = int(produto["preco"] * 100)
        
        # Verificar se tem saldo suficiente
        if self.saldo < preco_centimos:
            print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
            print(f"maq: Saldo = {self.saldo//100}e{self.saldo%100}c; Pedido = {preco_centimos//100}e{preco_centimos%100}c")
            return
        
        # Efetuar a compra
        self.saldo -= preco_centimos
        produto["quant"] -= 1
        print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
        self.exibir_saldo()
    
    def calcular_troco(self):
        """Calcula o troco a ser devolvido usando as moedas disponíveis."""
        if self.saldo == 0:
            return []
        
        troco = []
        saldo_restante = self.saldo
        
        # Ordenar valores de moedas em ordem decrescente
        valores_moedas = sorted(self.moedas_troco.keys(), reverse=True)
        
        for valor in valores_moedas:
            quantidade = saldo_restante // valor
            if quantidade > 0:
                troco.append((quantidade, self.moedas_troco[valor]))
                saldo_restante -= quantidade * valor
        
        return troco
    
    def sair(self):
        """Finaliza o uso da máquina, devolvendo o troco."""
        troco = self.calcular_troco()
        
        if not troco:
            print("maq: Até à próxima")
            return
        
        troco_str = ", ".join([f"{quant}x {valor}" for quant, valor in troco])
        print(f"maq: Pode retirar o troco: {troco_str}.")
        print("maq: Até à próxima")
        
        # Zerar o saldo
        self.saldo = 0
    
    def adicionar_produto(self, codigo, nome, quantidade, preco):
        """Adiciona ou atualiza um produto no stock com validação de regex."""
        # Validar o código do produto
        if not re.match(r'^[A-Z]\d+$', codigo):
            print(f"maq: Código de produto inválido: {codigo}. Use formato como 'A23'.")
            return
        
        # Validar o nome do produto (não pode estar vazio)
        if not nome.strip():
            print("maq: O nome do produto não pode estar vazio.")
            return
        
        # Validar a quantidade (deve ser um número positivo)
        if quantidade <= 0:
            print("maq: A quantidade deve ser um número positivo.")
            return
        
        # Validar o preço (deve ser um número positivo)
        if preco <= 0:
            print("maq: O preço deve ser um número positivo.")
            return
            
        # Procurar se o produto já existe
        for produto in self.stock:
            if produto["cod"] == codigo:
                produto["quant"] += quantidade
                produto["nome"] = nome  # Atualiza o nome se necessário
                produto["preco"] = preco  # Atualiza o preço se necessário
                print(f"maq: Produto {codigo} atualizado. Quantidade atual: {produto['quant']}")
                return
        
        # Se não existe, adicionar novo produto
        novo_produto = {
            "cod": codigo,
            "nome": nome,
            "quant": quantidade,
            "preco": preco
        }
        self.stock.append(novo_produto)
        print(f"maq: Novo produto adicionado: {codigo} - {nome}")

    def exibir_ajuda(self):
        """Exibe a lista de comandos disponíveis."""
        print("maq: Comandos disponíveis:")
        print("-" * 50)
        for comando, descricao in self.comandos_disponiveis.items():
            print(f"{comando:<50} - {descricao}")
        print("-" * 50)

    def processar_comando(self, comando):
        """Processa os comandos do usuário usando expressões regulares avançadas."""
        # Comando HELP
        if re.match(r'^HELP$', comando, re.IGNORECASE):
            self.exibir_ajuda()
            return True
            
        # Comando LISTAR
        if re.match(r'^LISTAR$', comando, re.IGNORECASE):
            self.listar_produtos()
            return True
        
        # Comando MOEDA 
        moeda_match = re.match(r'^MOEDA\s+(.+)\s*$', comando, re.IGNORECASE)
        if moeda_match:
            self.adicionar_moeda(moeda_match.group(1))
            return True
        
        # Comando SELECIONAR 
        selecionar_match = re.match(r'^SELECIONAR\s+([A-Z]\d+)\s*$', comando, re.IGNORECASE)
        if selecionar_match:
            self.selecionar_produto(selecionar_match.group(1))
            return True
        
        # Comando ADICIONAR (extra) 
        adicionar_match = re.match(r'^ADICIONAR\s+([A-Z]\d+)\s+"([^"]+)"\s+(\d+)\s+([\d.]+)\s*$', comando, re.IGNORECASE)
        if adicionar_match:
            codigo = adicionar_match.group(1)
            nome = adicionar_match.group(2)
            try:
                quantidade = int(adicionar_match.group(3))
                preco = float(adicionar_match.group(4))
                self.adicionar_produto(codigo, nome, quantidade, preco)
            except ValueError:
                print("maq: Formato inválido para quantidade ou preço. Use números válidos.")
            return True
        
        # Comando SAIR
        if re.match(r'^SAIR$', comando, re.IGNORECASE):
            self.sair()
            self.salvar_stock()
            return False
        
        # Comando desconhecido - sugere HELP
        print(f"maq: Comando desconhecido: {comando}")
        print("maq: Digite HELP para ver a lista de comandos disponíveis.")
        return True

def main():
    """Função principal que inicia a máquina de vending."""
    maquina = MaquinaVending()
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    print("maq: Digite HELP para ver a lista de comandos disponíveis.")
    
    continuar = True
    while continuar:
        try:
            linha = input(">> ")
            continuar = maquina.processar_comando(linha)
        except KeyboardInterrupt:
            print("\nmaq: Operação interrompida.")
            maquina.salvar_stock()
            continuar = False
        except EOFError:
            print("\nmaq: Fim da entrada.")
            maquina.salvar_stock()
            continuar = False
        except Exception as e:
            print(f"maq: Erro: {str(e)}")

if __name__ == "__main__":
    main()
    