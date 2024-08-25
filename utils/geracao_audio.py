import os
import requests
from dotenv import load_dotenv
import csv
import sys 
sys.path.append(r'C:\Users\saull\Documents\Apps\Anki\utils\geracao_frases.py')
from utils.geracao_frases import conjuntoDeFrases

load_dotenv()

def gerando_audio():
    try:
        # Separando apenas as frases em inglês
        conjuntoDeFrasesEmIngles = []
        for i,frase in enumerate(conjuntoDeFrases):
            conjuntoDeFrasesEmIngles.append(conjuntoDeFrases[i][0])
        
        # Esse loop gera o arquivo em audio,trata algumas strings e armazena em uma pasta
        lista_caminhos = []
        for frase in conjuntoDeFrasesEmIngles:

            # Obter a chave de API do Deepgram das variáveis de ambiente
            dg_api_key = os.getenv("DG_API_KEY")
            if not dg_api_key:
                raise ValueError("A chave de API do Deepgram não foi encontrada nas variáveis de ambiente.")

            # Configurar o URL e os cabeçalhos da solicitação
            url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Token {dg_api_key}"
            }

            data = {
                "text": frase
            }

            # Fazer a solicitação POST para a API do Deepgram
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code != 200:
                raise Exception(f"Erro na solicitação: {response.status_code} - {response.text}")
            
            # Tratando frase e definindo o caminho onde vai ser armazenado o arquivo
            if not frase.endswith('.'):
                frase += '.'

            if frase.endswith('?') or frase.endswith('!'):
                frase = frase[:-1]

            frase = frase.replace('"','')
            frase = frase.replace("'","")
            frase = frase.replace('?','')
            frase = frase.replace('!','')
            frase = frase.replace('’','')
        

            separar = frase.split()
            juntar = "_".join(separar)
            pasta = "C:/Users/saull/Documents/Apps/Anki/audios/"
            FILENAME = pasta + juntar + "wav"

            # Salvar o audio na pasta
            with open(FILENAME, "wb") as audio_file:
                audio_file.write(response.content)

            print(f"Áudio salvo em: {FILENAME}")


            
            som = '[sound:' + FILENAME + ']'

            lista_caminhos.append(som)

    except Exception as e:
        print(f"Exception: {e}")
    


    try:
        for i,frase in enumerate(lista_caminhos):
            conjuntoDeFrases[i][0] = conjuntoDeFrasesEmIngles[i] + lista_caminhos[i]

        
        nome_arquivo = 'frases.csv'

        # Limpando o arquivo CSV
        open(nome_arquivo, mode='w').close()

        print(f"Conteúdo do arquivo {nome_arquivo} excluído com sucesso.")

        # Escrevendo no arquivo CSV
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
            escritor = csv.writer(file)
            escritor.writerows(conjuntoDeFrases)


        print(f"Dados escritos no arquivo {nome_arquivo} com sucesso.")


    except Exception as e:
        print(f"Exception: {e}")




