from openai import OpenAI
import os
from dotenv import load_dotenv
from leitura_docs import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def buscar_resposta_na_openai(pergunta, contexto):
    
    try:    
        prompt= f"""Analise o documento fornecido e em seguida responda a 
        {pergunta} com base em seu conhecimento do 
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
            temperature=1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return resposta
    except Exception as e:
        print("erro ", e)

# Exemplo de uso
pergunta_do_usuario = "Quando ocorreu essa reunião?"
resposta = buscar_resposta_na_openai(pergunta_do_usuario, pdf_text)

print("Resposta encontrada:", resposta)