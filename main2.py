from openai import OpenAI
import os
from dotenv import load_dotenv
from leituradocs import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

contexto = carrega("docs/assembleia.txt")

def buscar_resposta_na_openai(pergunta, contexto):
    
    try:    
        prompt= f"""Você é um assistente de escritório e seu principal trabalho é fazer a ata de reuniões com base no contexto fornecido
        com base na {pergunta}
        {contexto}"""

        resposta = client.chat.completions.create(
            messages=[{
                "role":"system",
                "content": prompt
            },
            {
                "role":"user",
                "content": pergunta
            }
            ],
            model="gpt-3.5-turbo",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return resposta
    except Exception as e:
        print("erro ", e)

# Exemplo de uso
pergunta_do_usuario = "Faça a ata da reunião"
resposta = buscar_resposta_na_openai(pergunta_do_usuario, contexto)

print("Resposta encontrada:", resposta)