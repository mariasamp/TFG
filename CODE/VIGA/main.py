import os
import shutil
import win32com.client
from tkinter import messagebox
from gui_V import iniciar_gui, obtener_valores
from catia_functions import leer_medidas, formacion_geometria, guardar_y_sobrescribir_documento
import time
import pyautogui
import subprocess

def guardar_datos():
    global folder_path1
    with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt')) as archivo:
        folder_path1 = archivo.read()
    valores = obtener_valores()
    ruta_archivo = os.path.join(folder_path1, "Valores_Viga.txt")
    try:
        with open(ruta_archivo, 'w') as archivo:
            for key, valor in valores.items():
                archivo.write(f"{key}\t{valor}\n")
        messagebox.showinfo("Guardar datos", "Datos guardados exitosamente en " + folder_path1)
    except Exception as e:
        messagebox.showerror("Error", "Ha ocurrido un error al guardar los datos: " + str(e))

def ejecutar_macro_apex(ruta_apex):
    comando = f'"{ruta_apex}"'

    subprocess.call(comando, shell=True)
    imagen =  os.path.join(os.path.dirname(__file__), "data", "macro_apex", "Play.PNG")
    start_time = time.time()
    max_time = 30  # tiempo máximo en segundos
    time.sleep(20) 
    while time.time() - start_time < max_time:
        location = pyautogui.locateCenterOnScreen(imagen)
        x_actual = location.x  
        nueva_x = x_actual + 122
        if location is not None:
            pyautogui.click(nueva_x, location.y)
            print(f"Imagen encontrada y pulsada en la posición: {location}")
            return True
        else:
            print("Imagen no encontrada, reintentando en 3 segundos...")
        
        time.sleep(3)  # Espera 3 segundos antes de volver a comprobar

    print("No se encontró la imagen en 30 segundos.")
    return False


if __name__ == "__main__":
    iniciar_gui(guardar_datos)
    archivo_medidas = os.path.join(folder_path1, "Valores_Viga.txt")
    medidas = leer_medidas(archivo_medidas)

    with open(archivo_medidas, 'r') as archivo:
        lineas = archivo.readlines()
        valores = {linea.split('\t')[0].strip(): linea.split('\t')[1].strip() for linea in lineas}

    tipo_seccion = valores.get("Tipo de Sección")
    forma_seccion = valores.get("Forma de Sección")
    tipo_elemento = valores.get("Tipo de Elemento")
    formacion_geometria(medidas, tipo_seccion, forma_seccion)

    ruta_destino = os.path.join(folder_path1, "Viga.CATPart")
    ruta_temporal = os.path.join(folder_path1, "Viga_temporal.CATPart")
    guardar_y_sobrescribir_documento(ruta_destino, ruta_temporal)
    quit()
    ruta_apex = "C:\\Program Files\\MSC.Software\\MSC Apex\\2024-011290\\runMSC_Apex"
    ejecutar_macro_apex(ruta_apex)