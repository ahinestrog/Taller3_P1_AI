## Alternativas open source

Para no depender de las API de openAI, se podrían utilizar otras alternativas que no tienen costo como la de Gemini de Google o los modelos de IA alojados en HuggingFace.

Les dejo algunos ejemplos que podría ser útiles:

- Generación de texto y embeddings:
  https://ai.google.dev/tutorials/python_quickstart

  Para esto deben crear una api_key de Gemini

- Generación de imágenes:
  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0?text=car%C3%A1tula+de+la+pel%C3%ADcula+el+padrino

  Para esto deben crear una api_key de HuggingFace

  El archivo [open_source.py](aux_files/open_source.py) muestra ejemplos de cómo utilizar estas herramientas asumiendo que ya crearon las api_key y que están almacenadas en el archivo api_keys.env en diferentes renglones:

````python
gemini_api_key = XXXXX 
hf_api_key = XXXX
````
  
  
