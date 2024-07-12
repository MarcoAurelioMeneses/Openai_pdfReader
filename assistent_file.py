#Importação das bibliotecas
from openai import OpenAI
from dotenv import load_dotenv
import os

#Função para leitura do arquivo .env
load_dotenv()

#Conectando a API da openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file = client.files.create(
    file=open("docs/assembleia.txt", "rb"),
    purpose='assistants'
)

#Criando um assistente insrindo os parametros de treinamento: Nome, Instruções, Tools e o modelo
assistant = client.beta.assistants.create(
    name="Assistente de escritório",
    instructions="""
            Você é um exelente assistente de escritório e uma de suas principais funções é a 
            de gerar ATAS de reunião mediante conversas inseridas em documentos.
            Você sempre deve utilizar uma linguagem formal.
        """,
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
    tool_resources={
        "code_interpreter":{
            "file_ids":[file.id]
        }
    }
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Crie a ata da reunião baseada na conversa do arquivo.",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}, {"type": "file_search"}]
)

if run.status ==  "completed":
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)