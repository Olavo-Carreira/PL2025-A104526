# Somador On/Off - Processador de Números com Opções de Ativação

**Data:** 9 de Fevereiro de 2025  

## Autor
- **Nome:** Olavo Rafael Fernandes Malainho Santos Carreira
- **Número:** 104526  
 ![Foto do Autor](../fotoCara.png)

## Resumo

Este projeto implementa um processador de números que lê de um ficheiro de texto, realizando somas baseadas num estado de ativação. O programa começa com o somador ativo por padrão e mantém esse estado até encontrar explicitamente o comando "off". Somente após encontrar um "off", o somador precisa de um comando "on" para voltar a somar.

### Funcionalidades:
- Leitura linha a linha do ficheiro `input.txt`.
- Soma de números com controlo baseado nos comandos `on` e `off`.
- Exibição de somas parciais sempre que encontrar o caractere `=`.
- Tratamento de erros se o ficheiro `input.txt` não for encontrado.

## Comportamento do Somador

O somador opera segundo as seguintes regras:
1. O somador começa sempre em estado ativo, ou seja, somando números.
2. Ao encontrar o comando `off`, o somador desativa a soma até encontrar explicitamente um comando `on`.
3. A cada `=`, o somador exibe a soma acumulada até aquele ponto.
4. O somador ignora números quando está desativado (entre um `off` e um `on`).

### Exemplos de Comportamento:
```plaintext
123=456=         # Soma 123 + 456 porque o somador está ativo.
123off456=       # Soma apenas 123, pois o comando 'off' desativa o somador até o 'on'.
123off456on789=  # Soma 123 + 789, ignorando 456, pois está entre 'off' e 'on'.
```

## Estrutura do Código

O código principal está contido na função `somador_on_off()` que:
1. Inicializa com estado de soma ativo (`somar_ativo = True`).
2. Lê o ficheiro `input.txt` linha a linha.
3. Processa cada caractere sequencialmente:
   - Acumula dígitos para formar números.
   - Desativa a soma ao encontrar `off`.
   - Reativa a soma ao encontrar `on` (após um `off`).
   - Mostra resultados parciais ao encontrar `=`.

## Ficheiros do Projeto

- [`somador_on_off.py`](somador_on_off.py) - Código fonte do processador.
- [`input.txt`](input.txt) - Ficheiro de entrada contendo números e comandos `on`/`off`.
- [`README.md`](README.md) - Documentação deste projeto.

## Exemplo de Uso

O programa espera um ficheiro `input.txt` com conteúdo no seguinte formato:

```plaintext
5on7off3on2=off4on6=
1off2on3=4
1o2on3off4on55
```

A saída será apresentada no formato:

```plaintext
Soma agora: 14
------------------------------
Soma agora: 20
------------------------------
Soma agora: 24
------------------------------
```

## Possíveis Melhorias Futuras

- Suporte a números negativos e decimais.
- Refatoração do código para permitir um maior controlo sobre os comandos, como por exemplo, permitir múltiplos comandos `on` e `off` em uma linha.
- Inclusão de um argumento para o nome do ficheiro de entrada via linha de comandos, tornando o código mais flexível.
- Melhorar o tratamento de erros para entradas mal formatadas.
- Implementar testes automatizados para validar diferentes casos de entrada.
