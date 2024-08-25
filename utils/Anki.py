import json
import urllib.request
import csv
import sys

sys.path.append(r'C:\Users\saull\Documents\Apps\Anki\utils\geracao_audio.py')

from utils.geracao_audio import gerando_audio

gerando_audio()

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def anki():
    try:

        with open('frases.csv', newline='',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                pergunta = row[0]
                resposta = row[1]
                note = {
                    "deckName": "MyDeck",
                    "modelName": "Basic",
                    "fields": {
                        "Front": f"{pergunta}",
                        "Back": f"{resposta}"
                    },
                    "tags": ["sample_tag"],
                    "options": {
                        "allowDuplicate": True
                    }
                }

                invoke('addNote', note=note)
            print("Todos os cards foram feitos")

    except Exception as e:
        print(f"An error occurred: {e}")