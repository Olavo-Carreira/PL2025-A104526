# Processador de Dados Musicais

**Data:** 18 de Fevereiro de 2025  

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa um processador de dados musicais que lê um ficheiro CSV contendo informações sobre obras musicais, compositores e períodos históricos. O programa analisa os dados e gera um relatório estruturado com três seções principais:

1. Lista ordenada alfabeticamente dos compositores musicais
2. Distribuição das obras por período histórico (quantidade e percentagem)
3. Dicionário associando cada período a uma lista alfabética dos títulos das obras

### Funcionalidades:
- Leitura e processamento de ficheiros CSV sem utilizar a biblioteca CSV do Python
- Tratamento adequado de campos com delimitadores dentro de aspas
- Ordenação alfabética ignorando acentuação
- Apresentação formatada dos resultados em tabelas ASCII
- Tratamento robusto de erros

## Comportamento do Processador

O processador opera segundo as seguintes regras:
1. Realiza a leitura do ficheiro CSV caracter por caracter, respeitando campos delimitados por aspas
2. Identifica e valida as colunas necessárias: '_id', 'nome', 'periodo' e 'compositor'
3. Processa os registos para extrair as informações relevantes
4. Formata e apresenta os resultados em tabelas legíveis

### Exemplo de Funcionamento:
================================================================================
                             ANÁLISE DE OBRAS
================================================================================

                             1. COMPOSITORES
--------------------------------------------------------------------------------
  1. Alessandro Stradella
  2. Antonio Maria Abbatini
  3. Bach, Johann Christoph
  4. Bach, Johann Michael
  5. Bach, Wilhelm Friedemann
  ...

                        2. DISTRIBUIÇÃO POR PERÍODO
--------------------------------------------------------------------------------
Período                                  Quantidade           Percentagem
--------------------------------------------------------------------------------
Barroco                                         26                 14.94%
Clássico                                        15                  8.62%
Contemporâneo                                    7                  4.02%
Medival                                         18                 10.34%
--------------------------------------------------------------------------------
...
Total                                          150

                          3. OBRAS POR PERÍODO
================================================================================

BARROCO
--------------------------------------------------------------------------------
Título                                                    ID                  
--------------------------------------------------------------------------------
Ab Irato                                                  O41                
Die Ideale, S.106                                         O58                
Fantasy No. 2                                             O170               
Hungarian Rhapsody No. 16                                 O146               
Hungarian Rhapsody No. 5                                  O44      
...       

CLÁSSICO
--------------------------------------------------------------------------------
Título                                                    ID                  
--------------------------------------------------------------------------------
Bamboula, Op. 2                                           O130               
Capriccio Italien                                         O123               
Czech Suite                                               O153               
French Overture                                           O160               
Hungarian Rhapsody No. 14                                 O168               
Hungarian Rhapsody No. 18                                 O47  
...

- [`csvMusicas.py`](csvMusicas.py) - Código fonte do programa.
- [`obras.csv`](obras.csv) - Ficheiro de entrada csv contendo informações acerca de obras.
- [`README.md`](README.md) - Documentação deste projeto.

## Estrutura do Código

O código está organizado em funções modulares, cada uma com responsabilidade específica:

1. `ler_ficheiro()`: Processa o CSV caracter por caracter
2. `validar_dados()`: Verifica as colunas necessárias e obtém seus índices
3. `listar_compositores()`: Extrai e ordena a lista de compositores
4. `contar_obras_por_periodo()`: Contabiliza obras por período histórico
5. `agrupar_titulos_por_periodo()`: Agrupa títulos de obras por período
6. `process_music_data()`: Coordena o processamento completo dos dados
7. `formatar_resultados()`: Formata os resultados em tabelas ASCII
8. `write_results()`: Apresenta os resultados formatados na saída padrão
9. `main()`: Função principal que coordena todo o fluxo de execução

## Detalhes de Implementação

### Tratamento de CSV sem a biblioteca CSV

O programa implementa um parser próprio para arquivos CSV que:
- Distingue campos dentro e fora de aspas
- Trata corretamente delimitadores (ponto e vírgula) dentro de campos com aspas
- Converte quebras de linha dentro de campos com aspas em espaços


### Formatação dos Resultados

Os resultados são apresentados em tabelas ASCII bem formatadas, com:
- Cabeçalhos destacados
- Alinhamento apropriado de colunas
- Truncamento de títulos muito longos
- Percentagens calculadas com precisão
- Totais de obras por período

## Como Usar

Para utilizar o programa, execute o script Python passando o nome do ficheiro CSV como entrada:

```python
python csvMusicas.py
# O programa solicitará o nome do ficheiro
```

## Tratamento de Erros

O programa implementa tratamento robusto de erros para:
- Ficheiro não encontrado
- Estrutura de colunas inválida
- Linhas malformadas ou incompletas
- Campos vazios ou inválidos

## Limitações Conhecidas

- Caracteres não-Unicode podem causar problemas na remoção de acentos