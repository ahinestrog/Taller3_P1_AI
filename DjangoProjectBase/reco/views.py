from django.shortcuts import render
import openai
from movie.models import Movie
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '../api_keys_2.env')
load_dotenv(dotenv_path)

api_key = os.getenv('openai_apikey')

# Configurar la API de OpenAI
openai.api_key = api_key

def reco(request):
    movies = []  # Lista de películas recomendadas que si existen en la base de datos

    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        prompt_text = f"Recomiéndame títulos de películas que podrían estar disponibles en una base de datos de películas, basadas en: {prompt}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=150,
            temperature=0.7
        )

        generated_text = response.choices[0].message['content']

        # Extraer el titulo de la película pero solo el titulo
        recommendations = []
        indice_inicio = 0
        while True:
            indice_inicio = generated_text.find('"', indice_inicio)
            if indice_inicio == -1:
                break
            indice_final = generated_text.find('"', indice_inicio + 1)
            if indice_final == -1:
                break
            title = generated_text[indice_inicio + 1:indice_final]
            recommendations.append(title)
            indice_inicio = indice_final + 1  # Busca el siguiente titulo, para agregarlo a la lista de recomendaciones

        # Busca en la base de datos, algo así como en el home y mira que si exista la película
        for searchTerm in recommendations:
            db_movies = Movie.objects.filter(title__icontains=searchTerm)
            if db_movies.exists():
                movies.extend(db_movies)

    return render(request, 'reco.html', {'recommendations': movies})  # Pasar las películas encontradas