from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import sys 
sys.path.append(r"C:\Users\saull\Documents\Apps\Anki\utils\leitura_palavras.py")

from utils.leitura_palavras import lista_palavras

load_dotenv()

# Instancia qual LLM vamos usar
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# Exemplos de como eu quero que seja suas respostas
exemplos_corretos = [
  {
    "palavra": "reason",
    "csv": "The main reason for the meeting is to discuss the budget./O principal motivo da reunião é discutir o orçamento."
  },
  {
    "palavra": "Take",
    "csv": "Take a look at this document before signing it./Dê uma olhada neste documento antes de assiná-lo."
  },
]

# Exemplos de como não quero que seja suas respostas (com mais exemplos)
exemplos_incorretos = [
  {
    "palavra": "reason",
    "csv": "The reason is important./A razão é importante."  # Frase muito curta e genérica
  },
  {
    "palavra": "Take",
    "csv": "Take this./Pegue isso."  # Frase muito curta e sem contexto
  },
  {
    "palavra": "reason",
    "csv": "Title: Reason for Discussion/The title is not needed here."  # Geração de título, o que é indesejado
  },
  {
    "palavra": "Take",
    "csv": "Introduction: Let's talk about the word 'Take'/This introduction is unnecessary."  # Introdução desnecessária
  },
  {
    "palavra": "Take",
    "csv": "Take/Take your time./Tome o seu tempo."  # Frase muito curta e simplista
  },
  {

    "palavra": "reason",
    "csv": "reason/The main reason for the meeting is to discuss the budget./O principal motivo da reunião é discutir o orçamento."
  },
]

# Definindo quais são as variáveis de input
example_prompt = PromptTemplate(input_variables=["palavra", "csv"], template="{csv}")

# Definindo como vai ser o prompt 
few_prompt = FewShotPromptTemplate(
    examples=exemplos_corretos,
    example_prompt=example_prompt,
    prefix="""ATENÇÃO: A resposta deve ser estritamente no formato CSV, sem introduções, sem títulos, sem explicações ou qualquer texto adicional. Você é um assistente especializado em fornecer respostas no formato CSV com delimitador /. O CSV deve ter duas colunas: a primeira com a frase em inglês e a segunda com a tradução em português. Você sempre receberá uma lista de palavras em inglês. Sua tarefa é criar uma frase cotidiana para cada palavra em inglês, com um mínimo de 15 palavras, e fornecer a tradução correspondente para o português. As frases devem refletir situações do dia a dia, utilizando gírias e linguagem informal quando apropriado. Evite reutilizar as palavras da lista em qualquer frase subsequente. NÃO SIGA ESTES EXEMPLOS INCORRETOS:""",
    suffix="""\nEXEMPLOS INCORRETOS (Evite isso):\n{exemplos_incorretos}\n{input}""",
    input_variables=["input", "exemplos_incorretos"]
)

# Combinando exemplos incorretos e corretos no prompt final
prompt = few_prompt.format(
    input=f"{lista_palavras}",
    exemplos_incorretos="\n".join([f'Palavra: "{ex["palavra"]}"\nResposta: "{ex["csv"]}"' for ex in exemplos_incorretos])
)

# Passando prompt para a LLM
result = llm.invoke(ChatPromptTemplate.from_template(prompt).format_messages())

# Conteúdo da resposta da LLM
text = result.content
print(text)


print('-'*30, '   FRASES GERADAS  ','-'*30)
print(text)
print('-'*79)

# Tratando o conteudo
linhas = [linha for linha in text.strip().split('\n') if linha.strip()]

# Processar cada linha e dividi-la no "/"
conjuntoDeFrases = [linha.split('/') for linha in linhas]