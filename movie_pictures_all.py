#importar librerías
import os
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np


def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return(image)

#Se lee del archivo .env la api key de openai
_ = load_dotenv('api_keys.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openAI_api_key'),
)

#Se carga la lista de películas de movie_titles.json
with open('movie_descriptions.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)

import time

for i, movie in enumerate(movies[49:]):
    print(i,movie['title'])
    #Se hace la conexión con la API de generación de imágenes. El prompt en este caso es:
    #Alguna escena de la película + "nombre de la película"
    try:
        response = client.images.generate(
        model="dall-e-2",
        prompt=f"Portada de la película {movie['title']}",
        size="256x256",
        quality="standard",
        n=1,
        )
        image_url = response.data[0].url

        # La API devuelve la url de la imagen, por lo que debemos generar una función auxiliar que
        # descargue la imagen.
        # Convert the response content into a PIL Image
        img = fetch_image(image_url)
        img.save('movie_pictures/'+'m_'+movie['title']+'.png')
    except Exception as e:
        print(e)
        print(f"La película {movie['title']} no se pudo procesar")

    print(f"pelicula {i} de {len(movies[45:])}")

    # Add a pause of 1 minute every 6 pictures
    if i % 6 == 0:
        time.sleep(60)