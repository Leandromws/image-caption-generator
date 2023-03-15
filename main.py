import io
import os
from tkinter import *
from PIL import ImageTk, Image
from google.cloud import vision
import requests
import openai

# Configuração da API do Google Vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ls319/OneDrive/Área de Trabalho/Projeto legenda v2/API/eighth-upgrade-379903-40868f3db38a.json'
client = vision.ImageAnnotatorClient()

# Configuração da API do OpenAI
with open('/Users/ls319/OneDrive/Área de Trabalho/Projeto legenda v2/API/openaiAPI.txt', 'r') as openaiAPI:
    openai.api_key = openaiAPI.read()

# Criação da janela
root = Tk()
root.geometry("600x600")

# Criação dos widgets
label = Label(root)
label.pack(padx=10, pady=10)

entry = Entry(root, width=40)
entry.pack(padx=10, pady=10)

button = Button(root, text="Analisar imagem", command=lambda: analyze_image(entry.get()))
button.pack(padx=10, pady=10)

result_label = Label(root, wraplength=500)
result_label.pack(padx=10, pady=10)

# Função para analisar a imagem
def analyze_image(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))

    # Exibe a imagem na tela
    image = image.resize((400, 400))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img

    # Analisa a imagem utilizando a API do Google Vision
    content = response.content
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    text = ' '.join([label.description for label in labels])

    # Utiliza a API do OpenAI para gerar uma legenda para a imagem
    prompt = "Generate a 5 captions for an Instagram photo of " + text + " using natural language."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.3,
        max_tokens=120,
       #frequency_penalty = 0.4,
        #presence_penalty = 0.4,
        #top_p = 1,
        n=1,
        stop=None,
        timeout=10
    )
    caption = response.choices[0].text.strip()
    print(caption)

    # Exibe a legenda na tela
    result_label.config(text=caption)

# Inicia a aplicação
root.mainloop()