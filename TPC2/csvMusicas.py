import re

def ler_ficheiro(lines):

    content = "".join(lines)
    data = []
    
    line_pattern = re.compile(r'(?:[^\n\r]+)(?:\r?\n)?')
    line_matches = re.finditer(line_pattern, content)
    
    accumulated_line = ""
    in_quotes = False
    
    for line_match in line_matches:
        line = line_match.group(0)
        
        quotes_count = line.count('"')
        if quotes_count % 2 == 1:  
            in_quotes = not in_quotes
        
        accumulated_line += line
        
        if not in_quotes: 
            if accumulated_line.strip():
                row = []
                field_pattern = re.compile(r'(?:^|;)\s*(?:"((?:[^"]|"")*)"|([^;"]*))')
                for field_match in re.finditer(field_pattern, accumulated_line + ';'):
                    field_value = field_match.group(1) if field_match.group(1) is not None else field_match.group(2)
                    if field_value is not None:
                        field_value = re.sub(r'""', '"', field_value).strip()
                        row.append(field_value)
                
                if row:
                    data.append(row)
            
            accumulated_line = ""
    
    return data


def validar_dados(processed_lines):
    if not processed_lines:
        raise ValueError("Erro: O ficheiro está vazio ou mal formatado.")

    header = processed_lines[0]
    try:
        id_idx = header.index("_id")
        title_idx = header.index("nome")
        period_idx = header.index("periodo")
        composer_idx = header.index("compositor")
    except ValueError:
        raise ValueError(f"Erro: Nome de coluna não encontrado. Colunas detectadas: {header}")
    
    return id_idx, title_idx, period_idx, composer_idx


def listar_compositores(processed_lines, id_idx, title_idx, period_idx, composer_idx):
    composers = set()

    for line in processed_lines[1:]:
        if len(line) <= max(id_idx, title_idx, period_idx, composer_idx):
            continue

        composer = line[composer_idx].strip()
        if composer:
            composers.add(composer)

    return sorted(composers)


def contar_obras_por_periodo(processed_lines, id_idx, title_idx, period_idx, composer_idx):
    period_counter = {}

    for line in processed_lines[1:]:
        if len(line) <= max(id_idx, title_idx, period_idx, composer_idx):
            continue

        period = line[period_idx].strip()
        title = line[title_idx].strip()
        composer = line[composer_idx].strip()

        if not title or not period or not composer:
            continue

        period_counter[period] = period_counter.get(period, 0) + 1

    return dict(sorted(period_counter.items()))


def agrupar_titulos_por_periodo(processed_lines, id_idx, title_idx, period_idx, composer_idx):
    period_titles = {}

    for line in processed_lines[1:]:
        if len(line) <= max(id_idx, title_idx, period_idx, composer_idx):
            continue

        id_value = line[id_idx].strip()
        title = line[title_idx].strip()
        period = line[period_idx].strip()
        composer = line[composer_idx].strip()

        if not title or not period or not composer:
            continue

        period_titles.setdefault(period, []).append((title, id_value))

    return {period: sorted(titles) for period, titles in sorted(period_titles.items())}


def process_music_data(processed_lines):
    id_idx, title_idx, period_idx, composer_idx = validar_dados(processed_lines)
    
    composers = listar_compositores(processed_lines, id_idx, title_idx, period_idx, composer_idx)
    period_counter = contar_obras_por_periodo(processed_lines, id_idx, title_idx, period_idx, composer_idx)
    period_titles = agrupar_titulos_por_periodo(processed_lines, id_idx, title_idx, period_idx, composer_idx)

    return {
        'composers': composers,
        'period_counter': period_counter,
        'period_titles': period_titles
    }


def formatar_resultados(results):
    output = []
    
    output.append("=" * 80)
    output.append("{:^80}".format("ANÁLISE DE OBRAS"))
    output.append("=" * 80)
    
    output.append("\n{:^80}".format("1. COMPOSITORES"))
    output.append("-" * 80)
    
    for i, composer in enumerate(results['composers'], 1):
        output.append(f"  {i:2d}. {composer}")
    
    output.append("\n{:^80}".format("2. DISTRIBUIÇÃO POR PERÍODO"))
    output.append("-" * 80)
    output.append("{:<40} {:>10} {:>20}".format("Período", "Quantidade", "Percentagem"))
    output.append("-" * 80)
    
    total_obras = sum(results['period_counter'].values())
    for period, count in results['period_counter'].items():
        percentage = (count / total_obras) * 100 if total_obras else 0
        output.append("{:<40} {:>10} {:>19.2f}%".format(period, count, percentage))
    
    output.append("-" * 80)
    output.append("{:<40} {:>10}".format("Total", total_obras))
    
    output.append("\n{:^80}".format("3. OBRAS POR PERÍODO"))
    output.append("=" * 80)
    
    for period, titles in results['period_titles'].items():
        output.append(f"\n{period.upper()}")
        output.append("-" * 80)
        output.append("{:<60} {:<19}".format("Título", "ID"))
        output.append("-" * 80)
        
        for title, id_value in titles:
            output.append("{:<60} {:<19}".format(
                (title[:57] + "...") if len(title) > 57 else title,
                id_value
            ))
    
    return "\n".join(output)


def write_results(results):
    formatted_output = formatar_resultados(results)
    print(formatted_output)


def main(ficheiro):
    try:
        with open(ficheiro, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        processed_lines = ler_ficheiro(lines)
        results = process_music_data(processed_lines)
        write_results(results)
        return results
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Erro: O ficheiro '{ficheiro}' não foi encontrado.")
    except Exception as e:
        print(f"Erro: {str(e)}")
        return None


if __name__ == "__main__":
    ficheiro = input("Escreva o nome do ficheiro: ").strip()
    main(ficheiro)