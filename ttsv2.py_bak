import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent  # Importar CommentEvent
import pyttsx3
from datetime import datetime
import os
import pygame

# Inicializar Pygame
pygame.mixer.init()

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Variable global para controlar el estado de text-to-speech
tts_enabled = True  # Puedes ajustar el valor inicial según tus necesidades

# Lista de palabras a ignorar en el text-to-speech
excluded_words = {
    "arriba": "w",
    "abajo": "s",
    "izquierda": "a",
    "derecha": "d",
    "botona": "q",
    "botonb": "e",
    "botonl": "o",
    "botonr": "p",
    "carriba": "y",
    "cabajo": "h",
    "cizquierda": "g",
    "cderecha": "j",
    "start": "m",
    "select": "l",
    # Inglés
    "up": "w",
    "down": "s",
    "left": "a",
    "right": "d",
    "buttona": "q",
    "buttonb": "e",
    "buttonl": "o",
    "buttonr": "p",
    "cup": "y",
    "cdown": "h",
    "cleft": "g",
    "cright": "j",
    "start": "m",
    "select": "l",
    # Palabras adicionales a excluir
    "_jugar": "",
    "_pregunta": "",
    "_salir": "",
    "_puntaje": "",
    "_salirsi": "",
    "_salirno": "",
    "_opciona": "",
    "_opcionb": "",
    "_opcionc": "",
    "_opciond": "",
    "_50": "",
    "_otrapr": "",
    "_siguiente": "",
    "_reiniciar": "",
    "_desaparece": "",
    "_penita": "",
    "_popin": "",
    "_krool": ""
}

def ignore_word(word):
    return word.startswith("_") and len(word) > 1 or word.lower() in excluded_words

def get_allowed_user():
    try:
        with open("tiktokchannel.txt", "r") as file:
            return file.read().strip().lower()
    except FileNotFoundError:
        print("El archivo tiktokchannel.txt no se ha encontrado.")
        return None

if __name__ == "__main__":
    allowed_user = get_allowed_user()

    if allowed_user:
        tiktok_username = "@" + allowed_user
        tiktok_client = TikTokLiveClient(unique_id=tiktok_username)

        # Corregir el manejo del evento de comentario
        @tiktok_client.on(CommentEvent)  # Utilizar el decorador adecuado
        async def on_ttcomment(comment_data):
            global tts_enabled

            username = comment_data.user.nickname
            comment_text = comment_data.comment

            # Verificar si comment_text es None antes de intentar llamar a lower()
            if comment_text is not None:
                comment_text = comment_text.lower()
            else:
                # Manejar el caso en que comment_text sea None
                pass

            username = username.lower()

            current_time = datetime.now().strftime("%H:%M")
            formatted_comment = f"[{current_time}] {username}: {comment_text}"
            print(formatted_comment)
            
            words = comment_text.split()
            filtered_words = [word for word in words if not ignore_word(word)]

            # Unir las partes del comentario y leer el resultado en el texto a voz
            final_comment = " ".join(filtered_words)

            # Leer el nick del usuario seguido del comentario si no está vacío
            if final_comment.strip():
                engine.say(f"{username} dijo: {final_comment}")
                engine.runAndWait()

        # Ejecutar el cliente de TikTok fuera de la función de comentario
        tiktok_client.run()
        
        while True:
            time.sleep(1)
    else:
        print("No se ha especificado un nombre de usuario en tiktokchannel.txt.")
