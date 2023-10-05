import difflib
import json
import threading
import requests


data_file = "data.json"

def cargar_datos():
    global data
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

def comparar_html():
    old_html = None  # Initialize old_html as None
    for item in data:
        old_html = item['html']  # Assign old_html if the URL is found
        selected_url= item['url']
        response = requests.get(selected_url)
        if response.status_code == 200:
            new_html = response.text
            seq_matcher = difflib.SequenceMatcher(None, old_html, new_html)
            similarity_ratio = seq_matcher.ratio()
            print("Comparación "+selected_url+" ", f"Porcentaje de similitud: {similarity_ratio * 100:.2f}%")
        else:
            print("Error", "No se pudo obtener el HTML reciente de la URL") 

def interrupcion_programada():
    if interrupt_running:  # Verifica si la interrupción está habilitada
        #AQUI VA EL CÓDIGO A REPETIR       
        timer = threading.Timer(tiempo_intervalo, interrupcion_programada)  # Programa la próxima ejecución
        timer.daemon = True
        timer.start()
interrupt_running=True
tiempo_intervalo = 5 #tiempo de repetición en segundos
data=[]    
cargar_datos()
comparar_html()