from openai import OpenAI
import time
import spacy
import os
from dotenv import load_dotenv

load_dotenv()

# Defina sua chave de API da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para dividir o texto em partes menores
def divide_text(text, max_tokens=3000):
    sentences = text.split('. ')
    chunks = []
    chunk = ''
    
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) > max_tokens:
            chunks.append(chunk)
            chunk = sentence + '. '
        else:
            chunk += sentence + '. '
    
    if chunk:
        chunks.append(chunk)
        
    return chunks

# Função para gerar texto usando a API da OpenAI
def generate_text(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo",  # ou outro modelo que você está usando
    )
    return response.choices[0].text.strip()

# Texto longo que você deseja processar
long_text = "docs/assembleia.txt"

# Divida o texto em partes menores
text_chunks = divide_text(long_text)

# Processa cada parte do texto
results = []
for chunk in text_chunks:
    result = generate_text(chunk)
    results.append(result)

# Combine as respostas
final_result = ' '.join(results)

# Exiba o resultado final
print(final_result)


def divide_text_with_context(text, max_tokens=3000, overlap=50):
    sentences = text.split('. ')
    chunks = []
    chunk = ''
    
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) > max_tokens:
            chunks.append(chunk)
            chunk = sentence + '. '
        else:
            chunk += sentence + '. '
    
    if chunk:
        chunks.append(chunk)
    
    # Adiciona sobreposição de contexto
    for i in range(1, len(chunks)):
        chunks[i] = ' '.join(chunks[i-1].split()[-overlap:]) + ' ' + chunks[i]
    
    return chunks



def generate_text_with_retry(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.Completion.create(
                model="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=1000
            )
            return response.choices[0].text.strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise e
            


nlp = spacy.load("en_core_web_sm")

def divide_text_with_spacy(text, max_tokens=3000):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    chunks = []
    chunk = ''
    
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) > max_tokens:
            chunks.append(chunk)
            chunk = sentence
        else:
            chunk += ' ' + sentence
    
    if chunk:
        chunks.append(chunk)
    
    return chunks


