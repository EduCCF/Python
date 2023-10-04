import tkinter as tk
import asyncio
from tkinter import messagebox
from telegram import Bot

# Función asincrónica para enviar un mensaje a través de Telegram
async def enviar_mensaje():
    mensaje = mensaje_text.get("1.0", "end-1c")  # Obtiene el texto del campo de texto
    if mensaje:
        try:
            bot = Bot(token=TOKEN)  # Crea un nuevo bot cada vez que se envía un mensaje
            await bot.send_message(chat_id=chat_id, text=mensaje)  # Envia el mensaje utilizando el nuevo bot
            messagebox.showinfo("Éxito", "Mensaje enviado correctamente")  # Muestra un mensaje de éxito
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {str(e)}")  # Muestra un mensaje de error si falla
    else:
        messagebox.showerror("Error", "El campo de mensaje está vacío")  # Muestra un mensaje de error si el campo de texto está vacío

# Token de tu bot de Telegram (reemplaza 'TU_TOKEN' con tu token real)
TOKEN = 'your bot token'

# ID de chat de destino (puedes obtenerlo enviando /start a tu bot y leyendo los registros)
chat_id = 'your chat id'

# Configuración de la ventana de la interfaz gráfica
ventana = tk.Tk()  # Crea una nueva ventana
ventana.title("Envío de Mensaje a Telegram")  # Establece el título de la ventana

# Campo de texto (TextArea) para ingresar el mensaje
mensaje_text = tk.Text(ventana, height=5, width=40)  # Crea un campo de texto
mensaje_text.pack()  # Muestra el campo de texto en la ventana

# Botón para enviar el mensaje
enviar_button = tk.Button(ventana, text="Enviar Mensaje", command=lambda: asyncio.run(enviar_mensaje()))  # Crea un botón
enviar_button.pack()  # Muestra el botón en la ventana

ventana.mainloop()  # Inicia el bucle principal de la interfaz gráfica

