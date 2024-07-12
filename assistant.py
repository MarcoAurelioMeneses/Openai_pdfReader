#Importação das bibliotecas
from openai import OpenAI
from dotenv import load_dotenv
import os

#Função para leitura do arquivo .env
load_dotenv()

#Conectando a API da openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Como os assistentes funcionam?
# Os assistentes podem chamar os modelos da OpenAI com as instruções especificas para ajustar suas
# persolnaidades e capacidades.
# Os assistentes podem acessar várias ferramentas em paralelo. Elas podem ser ferramentas hospedadas 
# pelo openai como "code_interpreter" e file_search pi ferramentas que você cria por meio de funções
# Assistentes podem acessar Threads persistentes . Threads simplificam o desenvolvimento de 
# aplicativos de IA armazenando o histórico de mensagens e truncando-o quando a conversa 
# fica muito longa para o comprimento do contexto do modelo. Você cria um Thread uma vez e 
# simplesmente anexa Messages a ele conforme seus usuários respondem.
# Os assistentes podem acessar arquivos em vários formatos — seja como parte de sua criação ou 
# como parte de Threads entre Assistentes e usuários. Ao usar ferramentas, os Assistentes também 
# podem criar arquivos (por exemplo, imagens, planilhas, etc.) e citar arquivos aos quais fazem 
# referência nas Mensagens que criam.

#Criando um assistente insrindo os parametros de treinamento: Nome, Instruções, Tools e o modelo
assistant = client.beta.assistants.create(
    name="Acadêmico Literário",
    instructions="Você é um grande acadêmico literario e sempre responde detalhadamente sobre livros",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

#Criando uma thread que é o fila de conversas com o assistente
thread = client.beta.threads.create()

#Simulando a mensagem do usuário, onde pegamos o ID da thread.
messages = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Eu quero saber tudo sobre o conto Perdoando Deus de Clarice Lispector"
)

#Iniciando a thread e peddindo para se direcionar a um nome de usuário
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)

# Recebendo o status de completo para todas as requisições acima e caso seja "completed",
# retornamos a resposta dentro da thread e exibindo no terminal.
# Caso não estja completo, pedimos para que seja printado o status atual do runtime
if run.status ==  "completed":
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)