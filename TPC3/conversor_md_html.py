import re

def convert_headers(text):
    """Converte cabeçalhos Markdown (# texto) para tags HTML <h1>, <h2>, <h3>"""
    # Procura por linhas que começam com # seguido de texto
    pattern = r'^(#{1,3})\s+(.+)$'
    
    def replace_header(match):
        # Determina o nível do cabeçalho com base no número de #
        level = len(match.group(1))
        content = match.group(2).strip()
        return f'<h{level}>{content}</h{level}>'
    
    # Aplica a substituição linha por linha
    return re.sub(pattern, replace_header, text, flags=re.MULTILINE)

def convert_bold(text):
    """Converte texto em negrito (entre **) para tags HTML <b>"""
    pattern = r'\*\*(.+?)\*\*'
    return re.sub(pattern, r'<b>\1</b>', text)

def convert_italic(text):
    """Converte texto em itálico (entre *) para tags HTML <i>"""
    pattern = r'\*(.+?)\*'
    return re.sub(pattern, r'<i>\1</i>', text)

def convert_numbered_list(text):
    """Converte listas numeradas para tags HTML <ol> e <li>"""
    # Identifica blocos de lista numerada (linhas que começam com números seguidos de ponto)
    pattern = r'((?:^\d+\.\s+.+\n?)+)'
    
    def replace_list(match):
        list_block = match.group(1)
        # Identifica cada item da lista
        items = re.findall(r'^\d+\.\s+(.+)$', list_block, re.MULTILINE)
        
        # Constrói a lista HTML
        html_list = "<ol>\n"
        for item in items:
            html_list += f"<li>{item}</li>\n"
        html_list += "</ol>"
        
        return html_list
    
    return re.sub(pattern, replace_list, text, flags=re.MULTILINE)

def convert_links(text):
    """Converte links Markdown [texto](URL) para tags HTML <a href="URL">texto</a>"""
    pattern = r'\[(.+?)\]\((.+?)\)'
    return re.sub(pattern, r'<a href="\2">\1</a>', text)

def convert_images(text):
    """Converte imagens Markdown ![texto alt](URL) para tags HTML <img src="URL" alt="texto alt"/>"""
    pattern = r'!\[(.+?)\]\((.+?)\)'
    return re.sub(pattern, r'<img src="\2" alt="\1"/>', text)

def convert_markdown_to_html(markdown_text):
    """Converte texto Markdown para HTML aplicando todas as conversões"""
    html = markdown_text
    
    # Aplicar as conversões na ordem correta
    html = convert_headers(html)
    html = convert_bold(html)
    html = convert_italic(html)
    html = convert_numbered_list(html)
    html = convert_links(html)
    html = convert_images(html)
    
    return html

def main():

    with open('input.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    html_output = convert_markdown_to_html(markdown_content)
    
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)


if __name__ == "__main__":
    main()