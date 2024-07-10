from openai import OpenAI
import os
from dotenv import load_dotenv
from leituradocs import *

load_dotenv()


cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

contexto = carrega("docs/assembleia.txt")


prompt_sistema = f"""
    Você é um assistente de escritório e sua princiapl tarefa é gerar atas.
    A reunião em questão está especificada do contexto abaixo.
    Leia os documentos e gere a ata da reunião, baseado nos eventos que aconteceram.
    {contexto}
"""

print("Informe sua dúvida ")
prompt_usuario = input()

resposta = cliente.chat.completions.create(
    messages=
    [
        {
            "role": "system",
            "content" : prompt_sistema
        },
        {
            "role": "user",
            "content" : prompt_usuario
        }
    ],
    model="gpt-3.5-turbo",
    temperature=0.5,
    frequency_penalty=1.0
)

print(resposta.choices[0].message.content)