#Importação das bibliotecas
from openai import OpenAI
from dotenv import load_dotenv
import os

#Função para leitura do arquivo .env
load_dotenv()

#Conectando a API da openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = input("Faça sua pergunta: ")

# Criação do assistente com nome, instrução,outros parametros da OpenAI e utilizando a tools file_search
assistant = client.beta.assistants.create(
    name="Assistente de bliblioteca",
    instructions="""
            Você é um grande apreciador da literatura nacional e especialista no Programa Círculos de Leitura.
            Você sempre gosta de resumir livros.

        """,
    model="gpt-4o-mini",
    temperature=0,
    tools=[{"type":"file_search"}],
)
# Criando um Vector com o nome de livro
vector_store = client.beta.vector_stores.create(name="Livro")
# Selecionando os documentos que estarão presentes no sistema
# Utilizando a função open do Python para a leitura do documento em formato "bite"
file_paths = ["docs/braudel_lembrancas.pdf", 
              "docs/livreto_contos.pdf", 
              "docs/modulo_amor.pdf",
              "docs/sinfonia_sp.pdf"]
file_streams = [open(path, "rb") for path in file_paths]
# Fazendo upload e o pull das informações pegando o ID do Vector Store criado e o a função de leitura de arquivos.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)
# Printando o progresso do sistema, com seu status e a contagem de arquivos lidos.
print(file_batch.status)
print(file_batch.file_counts)
# Fazendo o updade do assistente dizendo para ele que existe um documento que será consultado
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

# Criando uma conversa onde usamos a regra de usuário e a pergunta que será feita.
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content":prompt,
        }
    ]
)
# Fazendo o print da execução
print(thread.tool_resources.file_search)

# Fazendo a inicialização de todo o sistema
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

# Obtém a lista de mensagens de um determinado thread (tópico de conversa) e execução.
messages =  list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# Obtém o conteúdo da primeira mensagem do thread.
message_content = messages[0].content[0].text
# Obtém as anotações do conteúdo da mensagem.
annotations = message_content.annotations
# Inicializa uma lista para armazenar as citações.
citations = []
# Itera sobre cada anotação do conteúdo da mensagem.
for index, annotation in enumerate(annotations):
# Substitui o texto da anotação no conteúdo da mensagem por um índice de citação (ex: [(0)], [(1)]).
    message_content.value = message_content.value.replace(annotation.text, f"[(index)]")
# Verifica se a anotação tem uma citação de arquivo associada.
    if file_citation := getattr(annotation, "file_citation", None):
# Se houver uma citação de arquivo, recupera o arquivo citado.
        cited_file = client.files.retrieve(file_citation.file_id)
# Adiciona o nome do arquivo citado à lista de citações.
        citations.append(f"{cited_file.filename}")

# Imprime o conteúdo da mensagem com as substituições de citação.
print(message_content.value)

# Imprime a lista de citações.
print((citations))