#Importação das bibliotecas
from openai import OpenAI
from dotenv import load_dotenv
import os

#Função para leitura do arquivo .env
load_dotenv()

#Conectando a API da openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


assistant = client.beta.assistants.create(
    name="Assistente de bliblioteca",
    instructions="""
            Você é um grande apreciador da literatura nacional e especialista no Programa Círculos de Leitura.
            Você sempre gosta de resumir livros.

        """,
    model="gpt-4o",
    temperature=0,
    tools=[{"type":"file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Livro")

file_paths = ["docs/braudel_lembrancas.pdf"]
file_streams = [open(path, "rb") for path in file_paths]

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content":"Quantos textos tem Joana Dafne Magalhães e quais são eles?",
        }
    ]
)

print(thread.tool_resources.file_search)


run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages =  list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

message_content = messages[0].content[0].text
annotations = message_content.annotations
citations = []
for index, annotation in enumerate(annotations):
    message_content.value = message_content.value.replace(annotation.text, f"[(index)]")
    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

print(message_content.value)
print("\n".join(citations))