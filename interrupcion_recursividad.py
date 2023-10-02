"""
Este programa crea una interfaz gráfica con tkinter que permite iniciar y detener una interrupción programada.
La interrupción muestra "Hola, soy una interrupción" en un cuadro de texto cada cierto intervalo de tiempo,
que se puede configurar en un cuadro de texto de entrada. 
El botón "Iniciar Interrupción" inicia la interrupción con el intervalo especificado,
y el botón cambia a "Detener Interrupción" cuando está en ejecución para permitir su detención.
La aplicación se puede cerrar haciendo clic en la "X" de la ventana o presionando Ctrl+C en la consola.
"""


import tkinter as tk  # Importa la librería tkinter para la interfaz gráfica
import threading     # Importa la librería threading para la gestión de hilos
import time          # Importa la librería time para controlar el tiempo

# Función que se ejecutará como una interrupción programada
def interrupcion_programada():
    if interrupt_running:  # Verifica si la interrupción está habilitada
        text_box.insert(tk.END, "Hola, soy una interrupción\n")  # Agrega texto al cuadro de texto
        intervalo = int(tiempo_intervalo.get())  # Obtiene el intervalo de tiempo desde el cuadro de texto
        timer = threading.Timer(intervalo, interrupcion_programada)  # Programa la próxima ejecución
        timer.daemon = True
        timer.start()

# Función para iniciar o detener la interrupción programada
def toggle_interrupcion_programada():
    global interrupt_running  # Hace referencia a la variable global
    if not interrupt_running:  # Si la interrupción no está en ejecución
        intervalo = int(tiempo_intervalo.get())  # Obtiene el intervalo de tiempo desde el cuadro de texto
        if intervalo > 0:  # Verifica que el intervalo sea mayor que cero
            interrupt_running = True  # Habilita la interrupción
            int_button.config(text="Detener Interrupción")  # Cambia el texto del botón
            interrupcion_programada()  # Inicia la interrupción programada
    else:
        interrupt_running = False  # Deshabilita la interrupción
        int_button.config(text="Iniciar Interrupción")  # Cambia el texto del botón

# Crear la ventana principal
root = tk.Tk()  # Crea una ventana principal
root.title("Interrupción con GUI")  # Establece el título de la ventana

# Crear un cuadro de texto
text_box = tk.Text(root, height=10, width=30)  # Crea un cuadro de texto para mostrar las interrupciones
text_box.pack()  # Coloca el cuadro de texto en la ventana

# Crear un cuadro de texto para configurar el tiempo entre interrupciones
tiempo_intervalo = tk.Entry(root, width=10)  # Crea un cuadro de texto de entrada
tiempo_intervalo.pack()  # Coloca el cuadro de texto de entrada en la ventana
tiempo_intervalo.insert(0, "10")  # Establece el valor predeterminado en el cuadro de texto

# Crear un botón para iniciar/detener la interrupción programada
interrupt_running = False  # Variable global para controlar si la interrupción está habilitada o no
int_button = tk.Button(root, text="Iniciar Interrupción", command=toggle_interrupcion_programada)  # Crea un botón
int_button.pack()  # Coloca el botón en la ventana

# Programa principal
try:
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica
except KeyboardInterrupt:
    # Manejar la interrupción de teclado (Ctrl+C) para detener la aplicación
    interrupt_running = False  # Asegura que la interrupción esté deshabilitada
    root.destroy()  # Cierra la ventana de la interfaz gráfica cuando se interrumpe
