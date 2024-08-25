# Nome do arquivo de texto
nome_arquivo = 'palavras.txt'

# Inicializa uma lista vazia para armazenar as linhas
lista_palavras = []

with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_txt:
        for linha in arquivo_txt:
            linha = linha.strip()  # Remove espaços em branco e quebras de linha no início e no fim
            if linha:
                lista_palavras.append(linha)


