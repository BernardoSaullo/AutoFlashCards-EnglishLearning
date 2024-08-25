import genanki
import csv
def anki():
    try:
        # Criar o modelo com o estilo CSS
        model = genanki.Model(
            1607392319,
            'Meu Modelo',
            fields=[
                {'name': 'Pergunta'},
                {'name': 'Resposta'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Pergunta}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Resposta}}',
                },
            ],
            css='''
            .card {
                font-family: arial;
                font-size: 20px;
                text-align: center;
                color: black;
                background-color: white;
            }
            '''
        )

        # Criar um baralho (Deck)
        deck = genanki.Deck(
            2059400110,
            'testeteste2'
        )

        # Abrir o arquivo CSV e iterar sobre as linhas
        with open('frases.csv', newline='',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # row[0] = row[0].split(',')
                pergunta = row[0]
                resposta = row[1]
                note = genanki.Note(
                    model=model,
                    fields=[pergunta, resposta]
                )
                deck.add_note(note)

        # Exportar o baralho para um único arquivo .apkg
        package = genanki.Package(deck)
        package.write_to_file('Ingles.apkg')

        print("Arquivo .apkg criado com sucesso!")
    except Exception as e:
        print("Não foi possível adicionar no Anki:", e)