from dotenv import load_dotenv, find_dotenv
import json
import os
from openai import OpenAI
#from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np

import google.generativeai as genai

# Definición de funciones
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

# Configuración de API Key de Gemini 
_ = load_dotenv('api_keys.env')
genai.configure(api_key=os.environ.get('gemini_api_key'))


# Carga de la lista de películas
with open('movie_descriptions.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)

#Esta función devuelve una representación numérica (embedding) de un texto, en este caso
#la descripción de las películas
    
def get_embedding_gemini(text):
    response_emb = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document",
        title="Embedding of single string")
    return response_emb['embedding']

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

emb = get_embedding_gemini(movies[1]['description'])
print(emb)

#Vamos a crear una nueva llave con el embedding de la descripción de cada película en el archivo .json

movies_gemini = [movies[i] for i in [27, 3, 20]]

for i in range(len(movies_gemini)):
  emb = get_embedding_gemini(movies_gemini[i]['description'])
  movies_gemini[i]['embedding'] = emb



#Para saber cuáles películas se parecen más, podemos hacer lo siguiente:
print(movies_gemini[0]['title'])
print(movies_gemini[1]['title'])
print(movies_gemini[2]['title'])

#Calculamos la similitud de coseno entre los embeddings de las descripciones de las películas. Entre más alta la similitud
#más parecidas las películas.

print(f"Similitud entre película {movies_gemini[0]['title']} y {movies_gemini[1]['title']}: {cosine_similarity(movies_gemini[0]['embedding'],movies_gemini[1]['embedding'])}")
print(f"Similitud entre película {movies_gemini[0]['title']} y {movies_gemini[2]['title']}: {cosine_similarity(movies_gemini[0]['embedding'],movies_gemini[2]['embedding'])}")
print(f"Similitud entre película {movies_gemini[1]['title']} y {movies_gemini[2]['title']}: {cosine_similarity(movies_gemini[1]['embedding'],movies_gemini[2]['embedding'])}")

#Si se tuviera un prompt por ejemplo: Película de la segunda guerra mundial, podríamos generar el embedding del prompt y comparar contra 
#los embeddings de cada una de las películas de la base de datos. La película con la similitud más alta al prompt sería la película
#recomendada.

req = "película de la segunda guerra mundial"
emb = get_embedding_gemini(req)

sim = []
for i in range(len(movies_gemini)):
  sim.append(cosine_similarity(emb,movies_gemini[i]['embedding']))
sim = np.array(sim)
idx = np.argmax(sim)
print(movies[idx]['title'])


