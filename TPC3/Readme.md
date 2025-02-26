# Conversor de Markdown para HTML - Um Processador de Texto Simples

**Data:** 26 de Fevereiro de 2025  

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa um conversor de Markdown para HTML que processa texto no formato Markdown e o transforma em HTML equivalente. O programa utiliza expressões regulares para identificar e substituir padrões específicos de Markdown, como cabeçalhos, texto em negrito, itálico, listas numeradas, links e imagens.

### Funcionalidades:
- Conversão de cabeçalhos (# texto, ## texto, ### texto) para tags HTML (`<h1>`, `<h2>`, `<h3>`).
- Conversão de texto em negrito (**texto**) para tags HTML (`<b>texto</b>`).
- Conversão de texto em itálico (*texto*) para tags HTML (`<i>texto</i>`).
- Processamento de listas numeradas para HTML (`<ol>` e `<li>`).
- Conversão de links no formato `[texto](URL)` para tags `<a href="URL">texto</a>`.
- Processamento de imagens no formato `![texto alternativo](URL)` para tags `<img>`.

## Comportamento do Conversor

O conversor opera segundo as seguintes regras:
1. Processa o texto Markdown linha por linha, identificando padrões específicos.
2. Aplica transformações na ordem correta para evitar conflitos entre padrões semelhantes.
3. Preserva a estrutura do texto original enquanto substitui os elementos de Markdown por suas equivalências em HTML.

### Exemplos de Conversão:
```markdown
# Exemplo
```
```html
<h1>Exemplo</h1>
```

```markdown
Este é um **exemplo** em negrito e um *exemplo* em itálico.
```
```html
Este é um <b>exemplo</b> em negrito e um <i>exemplo</i> em itálico.
```

## Estrutura do Código

O código principal está organizado em funções específicas para cada tipo de conversão:

1. `convert_headers(text)`: Converte cabeçalhos Markdown para tags HTML `<h1>`, `<h2>`, `<h3>`.
2. `convert_bold(text)`: Converte texto em negrito para tags HTML `<b>`.
3. `convert_italic(text)`: Converte texto em itálico para tags HTML `<i>`.
4. `convert_numbered_list(text)`: Converte listas numeradas para tags HTML `<ol>` e `<li>`.
5. `convert_links(text)`: Converte links Markdown para tags HTML `<a>`.
6. `convert_images(text)`: Converte imagens Markdown para tags HTML `<img>`.
7. `convert_markdown_to_html(markdown_text)`: Função principal que aplica todas as conversões.

## Ficheiros do Projeto

- [`markdown_converter.py`](markdown_converter.py) - Código fonte do conversor.
- [`README.md`](README.md) - Documentação deste projeto.
- [`input.md`](input.md) - Documento de teste para testar o programa
- [`output.html`](output.html) - Ficheiro de output dado como resultado do programa

## Exemplo de Uso

Para usar o conversor, basta chamar a função `convert_markdown_to_html()` escolhendo um documento em formato .md como parametro

```python
# Ler o arquivo Markdown
with open('documento.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()
    
# Converter para HTML
html_output = convert_markdown_to_html(markdown_content)

# Salvar o resultado
with open('documento.html', 'w', encoding='utf-8') as f:
    f.write(html_output)
```

### Expressões Regulares

O conversor utiliza expressões regulares do módulo `re` do Python para identificar padrões no texto. Exemplos de padrões utilizados:

- Cabeçalhos: `r'^(#{1,3})\s+(.+)$'`
- Negrito: `r'\*\*(.+?)\*\*'`
- Itálico: `r'\*(.+?)\*'`
- Links: `r'\[(.+?)\]\((.+?)\)'`
- Imagens: `r'!\[(.+?)\]\((.+?)\)'`

## Possíveis Melhorias Futuras

- Suporte a mais elementos de Markdown, como listas não ordenadas, citações, blocos de código, etc.
- Adição de uma interface de linha de comando para processar arquivos diretamente.
- Melhorar o tratamento de erros para entradas mal formatadas.


