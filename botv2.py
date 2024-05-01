import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from datetime import datetime
import os
import pygame

# Define los comandos y sus configuraciones iniciales
# Formato: nombre_comando: [timeout_segundos, comando activado/desactivado, timeout_activado/desactivado]
comandos_config = {
    "_error": [600, True, True],
    "_pedro": [150, True, True],
    "_jugar": [0, True, False],
    "_pregunta": [0, True, False],
    "_salir": [0, True, False],
    "_puntaje": [0, True, False],
    "_salirsi": [0, True, False],
    "_salirno": [0, True, False],
    "_opciona": [0, True, False],
    "_opcionb": [0, True, False],
    "_opcionc": [0, True, False],
    "_opciond": [0, True, False],
    "_50": [0, True, False],
    "_otrapregunta": [0, True, False],
    "_siguiente": [0, True, False],
    "_reiniciar": [0, True, False],
    "_desaparece": [0, True, False],
    "_penita": [0, True, False],
    "_popin": [0, True, False],
    "_krool": [5.5, True, False]
}

# Inicializar Pygame
pygame.mixer.init()

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

        last_command_times = {command: 0 for command in comandos_config.keys()}

        @tiktok_client.on(CommentEvent)
        async def on_ttcomment(comment_data):
            global last_command_times

            username = comment_data.user.nickname
            comment_text = comment_data.comment

            username = username.lower()

            current_time = time.time()
            formatted_comment = f"[{datetime.now().strftime('%H:%M')}] {username}: {comment_text}"
            print(formatted_comment)

            # Lógica para todos los comandos
            for command, config in comandos_config.items():
                timeout_seconds, activo, timeout_activo = config
                if activo and command in comment_text:
                    print(f"Detectado comando {command}")
                    if timeout_activo:
                        # Verificar si ha pasado el tiempo de timeout desde el último uso del comando
                        if current_time - last_command_times[command] >= timeout_seconds:
                            try:
                                # Ejecutar lógica del comando
                                print(f"Ejecutando comando {command}")
                                # Eliminar el guion bajo del comando para el nombre del archivo
                                file_name = command.lstrip("_")
                                if not os.path.exists("sammicomandos"):
                                    os.makedirs("sammicomandos")
                                # Crear archivo de texto
                                file_path = os.path.join("sammicomandos", f"{file_name}.txt")
                                with open(file_path, "w") as file:
                                    file.write("Archivo creado por el usuario")

                                # Esperar 2 segundos
                                time.sleep(2)

                                # Eliminar archivo de texto
                                os.remove(file_path)
                                
                                last_command_times[command] = current_time
                            except Exception as e:
                                print(f"Error al ejecutar el comando {command}: {e}")
                        else:
                            print(f"El comando {command} solo puede ser usado una vez cada {timeout_seconds} segundos.")
                    else:
                        try:
                            # Ejecutar lógica del comando sin considerar el timeout
                            print(f"Ejecutando comando {command}")
                            # Eliminar el guion bajo del comando para el nombre del archivo
                            file_name = command.lstrip("_")
                            if not os.path.exists("sammicomandos"):
                                os.makedirs("sammicomandos")
                            # Crear archivo de texto
                            file_path = os.path.join("sammicomandos", f"{file_name}.txt")
                            with open(file_path, "w") as file:
                                file.write("Archivo creado por el usuario")

                            # Esperar 2 segundos
                            time.sleep(2)

                            # Eliminar archivo de texto
                            os.remove(file_path)
                            
                            last_command_times[command] = current_time
                        except Exception as e:
                            print(f"Error al ejecutar el comando {command}: {e}")

        print("Connected")
        tiktok_client.run()

        while True:
            time.sleep(1)
    else:
        print("No se ha especificado un nombre de usuario en tiktokchannel.txt.")
