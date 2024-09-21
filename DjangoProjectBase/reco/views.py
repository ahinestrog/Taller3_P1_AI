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
        start_index = 0
        while True:
            start_index = generated_text.find('"', start_index)
            if start_index == -1:
                break
            end_index = generated_text.find('"', start_index + 1)
            if end_index == -1:
                break
            title = generated_text[start_index + 1:end_index]
            recommendations.append(title)
            start_index = end_index + 1  # Busca el siguiente titulo, para agregarlo a la lista de recomendaciones

        # Busca en la base de datos, algo así como en el home y mira que si exista la película
        for searchTerm in recommendations:
            found_movies = Movie.objects.filter(title__icontains=searchTerm)
            if found_movies.exists():
                movies.extend(found_movies)

    return render(request, 'reco.html', {'recommendations': movies})  # Pasar las películas encontradas