"""
Este código es una aplicación simple que permite agregar URLs,
descargar su contenido HTML, guardar los datos y comparar versiones antiguas y nuevas del HTML.
La interfaz de usuario se crea con la biblioteca tkinter,
y los datos se almacenan en un archivo JSON y en archivos HTML separados en el sistema de archivos local.
"""
# Importación de módulos necesarios
import requests  # Para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # Para analizar el HTML
import difflib  # Para comparar HTML
import tkinter as tk  # Para la interfaz gráfica
from tkinter import messagebox  # Para mostrar cuadros de diálogo
from tkinter import Listbox, Scrollbar, Button, Entry, Text  # Importaciones específicas de widgets de tkinter
import json  # Para trabajar con archivos JSON
import os  # Para operaciones con archivos y directorios

# Nombre del archivo JSON donde se guardarán los datos
data_file = "data.json"

# Función para cargar datos desde el archivo JSON al programa
def cargar_datos():
    try:
        # Intenta abrir el archivo JSON y cargar los datos
        with open(data_file, "r") as file:
            data = json.load(file)
        # Agrega las URL del archivo al widget Listbox
        for item in data:
            url_listbox.insert(tk.END, item['url'])
    except FileNotFoundError:
        pass

# Función para guardar los datos actuales en el archivo JSON y salir del programa
def guardar_datos():
    # Obtiene las URL del widget Listbox y guarda los datos en formato JSON
    data = [{'url': url, 'html': obtener_html(url)} for url in url_listbox.get(0, tk.END)]
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)
    # Cierra la ventana principal
    root.quit()

# Función para obtener el HTML de una URL
def obtener_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        messagebox.showerror("Error", "No se pudo obtener el HTML de la URL")
        return None

# Función para guardar una nueva URL y su HTML en un archivo local
def guardar_url():
    url = url_entry.get()
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # Escribe el HTML en un archivo con el nombre basado en la URL
        with open(f"{url.replace('/', '_')}.html", "w", encoding="utf-8") as file:
            file.write(html)
        # Agrega la URL al widget Listbox
        url_listbox.insert(tk.END, url)
        # Borra el contenido del campo de entrada de URL
        url_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "No se pudo obtener el HTML de la URL")

# Función para eliminar una URL seleccionada y su archivo local asociado
def eliminar_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        selected_url = url_listbox.get(selected_index)
        # Elimina la URL del widget Listbox
        url_listbox.delete(selected_index)
        # Obtiene el nombre del archivo local basado en la URL y lo elimina
        file_name = f"{selected_url.replace('/', '_')}.html"
        try:
            os.remove(file_name)
        except FileNotFoundError:
            pass

# Función para comparar el HTML almacenado localmente con la versión actual de la URL
def comparar_html():
    selected_index = url_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Selecciona una URL para comparar")
        return

    selected_url = url_listbox.get(selected_index)
    file_name = f"{selected_url.replace('/', '_')}.html"
    
    # Lee el HTML almacenado localmente
    with open(file_name, "r", encoding="utf-8") as file:
        old_html = file.read()

    # Obtiene el HTML actual de la URL
    response = requests.get(selected_url)
    if response.status_code == 200:
        new_html = response.text
        # Compara los dos bloques de HTML y calcula el porcentaje de similitud
        seq_matcher = difflib.SequenceMatcher(None, old_html, new_html)
        similarity_ratio = seq_matcher.ratio()
        # Muestra un cuadro de diálogo con el resultado de la comparación
        messagebox.showinfo("Comparación", f"Porcentaje de similitud: {similarity_ratio * 100:.2f}%")
    else:
        messagebox.showerror("Error", "No se pudo obtener el HTML reciente de la URL")

# Configuración inicial de la ventana principal de tkinter
root = tk.Tk()
root.title("Comparador de HTML")

# Creación de widgets y disposición en la interfaz gráfica
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=10, pady=10)

url_entry = Entry(root)
url_entry.grid(row=0, column=1, padx=10, pady=10)

guardar_button = Button(root, text="Guardar", command=guardar_url)
guardar_button.grid(row=0, column=2, padx=10, pady=10)

url_listbox = Listbox(root, width=50, height=10)
url_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

scrollbar = Scrollbar(root, orient=tk.VERTICAL)
scrollbar.grid(row=1, column=3, sticky=tk.NS)
url_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=url_listbox.yview)

eliminar_button = Button(root, text="Eliminar", command=eliminar_url)
eliminar_button.grid(row=2, column=1, padx=10, pady=10)

comparar_button = Button(root, text="Comparar", command=comparar_html)
comparar_button.grid(row=2, column=2, padx=10, pady=10)

# Carga los datos previamente guardados al iniciar el programa
cargar_datos()

# Configuración para guardar datos antes de cerrar la ventana
root.protocol("WM_DELETE_WINDOW", guardar_datos)

# Inicia el bucle principal de tkinter
root.mainloop()
