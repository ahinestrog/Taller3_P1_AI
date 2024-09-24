from django.shortcuts import render
import openai
from movie.models import Movie
from dotenv import load_dotenv
import os
import numpy as np

# Busca el archivo .env en la carpeta raíz del proyecto
load_dotenv('api_keys_2.env')

# Obtiene la API key de OpenAI en el archivo .env
api_key = os.getenv('openai_apikey')

# Configurar la API de OpenAI
openai.api_key = api_key

def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def reco(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        # Obtenemos todos los objetos del modelo de movies
        movies = Movie.objects.all()
        
        # Del prompt obtenemos el embedding
        emb_request = get_embedding(prompt, openai)

        sim = []
        for i in range(len(movies)):
            emb = movies[i].emb
            emb = list(np.frombuffer(emb))
            sim.append(cosine_similarity(emb, emb_request))
        sim = np.array(sim)
        idx = np.argmax(sim)
        idx = int(idx)
        movies = Movie.objects.filter(title=movies[idx].title)
    else:
        movies = Movie.objects.all()

    return render(request, 'reco.html', {'recommendations': movies})