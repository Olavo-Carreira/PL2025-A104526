# Máquina de Venda Automática (Vending Machine)

**Data:** 12 de Março de 2025

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa uma máquina de venda automática em Python que permite listar produtos, adicionar moedas, selecionar e comprar produtos, adicionar novos produtos ao stock e calcular o troco. O programa utiliza expressões regulares para validar entradas e manipula um ficheiro JSON para persistência dos dados de stock.

### Funcionalidades:
- Listagem de produtos disponíveis (`LISTAR`)
- Inserção de moedas (`MOEDA`)
- Seleção e compra de produtos (`SELECIONAR`)
- Adição de novos produtos ao stock (`ADICIONAR`)
- Exibição de ajuda com todos os comandos (`HELP`)
- Cálculo e devolução de troco (`SAIR`)
- Persistência de dados através de ficheiro JSON
- Tratamento de erros e validação de entradas

## Comportamento da Máquina de Venda

A máquina opera segundo as seguintes regras:
1. Carrega o stock de produtos a partir de um ficheiro JSON ao iniciar.
2. Aceita comandos do utilizador através da linha de comando.
3. Valida todas as entradas usando expressões regulares.
4. Processa as operações de compra, verificando disponibilidade e saldo.
5. Calcula o troco usando um algoritmo guloso para minimizar o número de moedas.
6. Guarda o estado atual do stock ao terminar a execução.

### Exemplos de Comandos:

```bash
Listar
```
Lista todos os produtos

```bash
MOEDA 1e, 50c
```
Adiciona um 1 euro e 50 centimos ao sado atual

Seleciona o produto com código A23 para compra, verificando disponibilidade e saldo.

## Estrutura do Código

O código está organizado em uma classe principal `MaquinaVending` com os seguintes métodos:

1. `__init__`: Inicializa a máquina com valores padrão e carrega o stock.
2. `carregar_stock`: Carrega os produtos a partir do ficheiro JSON.
3. `salvar_stock`: Salva o estado atual do stock no ficheiro JSON.
4. `listar_produtos`: Mostra todos os produtos disponíveis.
5. `adicionar_moeda`: Adiciona moedas ao saldo atual.
6. `exibir_saldo`: Mostra o saldo atual formatado.
7. `selecionar_produto`: Processa a seleção e compra de um produto.
8. `calcular_troco`: Calcula a devolução do troco de forma otimizada.
9. `sair`: Finaliza o uso da máquina, devolvendo o troco.
10. `adicionar_produto`: Adiciona ou atualiza um produto no stock.
11. `exibir_ajuda`: Mostra a lista de comandos disponíveis.
12. `processar_comando`: Processa os comandos do utilizador.

## Ficheiros do Projeto

- [`vending.py`](vending.py) - Código fonte da máquina de venda.
- [`stock.json`](stock.json) - Ficheiro JSON para armazenamento dos produtos.
- [`README.md`](README.md) - Documentação deste projeto.

## Exemplo de Uso

Para iniciar a máquina de venda, execute o script:

```bash
python3 vending.py