import requests
import difflib
import tkinter as tk
from tkinter import messagebox, Scrollbar, Button, Entry, ttk
import json

data_file = "data.json"

def cargar_datos():
    global data
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
        for item in data:
            url_listbox.insert("", "end", values=(str(item['porcentaje']) + "%", item['url']))
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
        data.append({'url': url, 'html': html, 'porcentaje': None})  # Inicialmente, el porcentaje es None
        url_listbox.insert("", "end", values=(None, url))
        url_entry.delete(0, tk.END)

def eliminar_url():
    selected_item = url_listbox.selection()
    if selected_item:
        selected_url = url_listbox.item(selected_item, 'values')[1]
        url_listbox.delete(selected_item)
        for item in data:
            if item['url'] == selected_url:
                data.remove(item)
                break

def guardar_porcentaje():
    selected_item = url_listbox.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona una URL para guardar el porcentaje")
        return

    selected_url = url_listbox.item(selected_item, 'values')[1]
    porcentaje = porcentaje_entry.get()
    
    # Validar que el porcentaje sea un número entero entre 0 y 100
    try:
        porcentaje = int(porcentaje)
        if 0 <= porcentaje <= 100:
            # Buscar la URL seleccionada y actualizar el porcentaje
            for item in data:
                if item['url'] == selected_url:
                    item['porcentaje'] = porcentaje
                    break
            # Actualizar el Treeview
            url_listbox.item(selected_item, values=(str(item['porcentaje']) + "%", selected_url))
        else:
            messagebox.showerror("Error", "El porcentaje debe estar entre 0 y 100")
    except ValueError:
        messagebox.showerror("Error", "Porcentaje no válido. Debe ser un número entero.")
    
    # Limpiar el campo de entrada
    porcentaje_entry.delete(0, tk.END)

    

def comparar_html():
    selected_item = url_listbox.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona una URL para comparar")
        return

    selected_url = url_listbox.item(selected_item, 'values')[1]
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

url_listbox = ttk.Treeview(root, columns=("Porcentaje", "URL"), show="headings")
url_listbox.heading("Porcentaje", text="Porcentaje")
url_listbox.heading("URL", text="URL")
url_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=url_listbox.yview)
scrollbar.grid(row=1, column=3, sticky=tk.NS)
url_listbox.configure(yscrollcommand=scrollbar.set)

eliminar_button = Button(root, text="Eliminar", command=eliminar_url)
eliminar_button.grid(row=2, column=1, padx=10, pady=10)

comparar_button = Button(root, text="Comparar", command=comparar_html)
comparar_button.grid(row=2, column=2, padx=10, pady=10)

porcentaje_label = tk.Label(root, text="Porcentaje de similitud:")
porcentaje_label.grid(row=3, column=0, padx=10, pady=10)

porcentaje_entry = Entry(root, width=10)
porcentaje_entry.grid(row=3, column=1, padx=0, pady=10)

guardar_porcentaje_button = Button(root, text="Guardar %", command=guardar_porcentaje)
guardar_porcentaje_button.grid(row=3, column=2, padx=10, pady=10)

data = []  # Lista para almacenar los datos

cargar_datos()

root.protocol("WM_DELETE_WINDOW", guardar_datos)

root.mainloop()
