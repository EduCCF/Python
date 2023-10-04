import requests
from bs4 import BeautifulSoup
import difflib
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Button, Entry, Text
import json
import os

data_file = "data.json"

def cargar_datos():
    global data
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
        for item in data:
            url_listbox.insert(tk.END, item['url'])
    except FileNotFoundError:
        pass

def guardar_datos():
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)
    root.quit()

def obtener_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        messagebox.showerror("Error", "No se pudo obtener el HTML de la URL")
        return None

def guardar_url():
    url = url_entry.get()
    html = obtener_html(url)
    if html is not None:
        data.append({'url': url, 'html': html})
        url_listbox.insert(tk.END, url)
        url_entry.delete(0, tk.END)

def eliminar_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        selected_url = url_listbox.get(selected_index)
        url_listbox.delete(selected_index)
        for item in data:
            if item['url'] == selected_url:
                data.remove(item)
                break

def comparar_html():
    selected_index = url_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Selecciona una URL para comparar")
        return

    selected_url = url_listbox.get(selected_index)
    old_html = None  # Initialize old_html as None
    for item in data:
        if item['url'] == selected_url:
            old_html = item['html']  # Assign old_html if the URL is found
            break

    if old_html is None:
        messagebox.showerror("Error", "No se encontró el HTML almacenado para esta URL")
        return

    response = requests.get(selected_url)
    if response.status_code == 200:
        new_html = response.text
        seq_matcher = difflib.SequenceMatcher(None, old_html, new_html)
        similarity_ratio = seq_matcher.ratio()
        messagebox.showinfo("Comparación", f"Porcentaje de similitud: {similarity_ratio * 100:.2f}%")
    else:
        messagebox.showerror("Error", "No se pudo obtener el HTML reciente de la URL")


root = tk.Tk()
root.title("Comparador de HTML")

url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=10, pady=10)

url_entry = Entry(root, width=35)
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

data = []  # Lista para almacenar los datos

cargar_datos()

root.protocol("WM_DELETE_WINDOW", guardar_datos)

root.mainloop()
