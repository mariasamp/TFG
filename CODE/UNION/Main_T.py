import os
import re
from Catia_functions_T import iniciar_catia, guardar_y_sobrescribir_documento
from gui_T import iniciar_guiT
import time
import subprocess
import pyautogui

def leer_datos_tornillo():
    
    with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt')) as archivo:
        folder_path = archivo.read()
    datos = []
    with open(os.path.join(folder_path, "Data_T.txt")) as archivo:
        for linea in archivo:
            datos.append(linea.strip().split('='))

    d = float(datos[0][1])
    dk = float(datos[1][1])
    k = float(datos[2][1])
    s = float(datos[3][1])
    m = float(datos[4][1])
    h = float(datos[5][1])
    d1 = float(datos[6][1])
    d2 = float(datos[7][1])
    P1 = float(datos[8][1])
    P2 = float(datos[9][1])
    dext_P1 = float(datos[10][1])
    dext_P2 = float(datos[11][1])
    mat_T = datos[12][1]
    mat_P1 = datos[13][1]
    mat_P2 = datos[14][1]
    mu_TP1 = float(datos[15][1])
    mu_TP2 = float(datos[16][1])
    mu_TA = float(datos[17][1])
    mu_P1P2 = float(datos[18][1])
    Preload = float(datos[19][1])
    Fz = float(datos[20][1])
    Fxy = float(datos[21][1])
    E_T = float(datos[22][1])
    nu_T = float(datos[23][1])
    ro_T = float(datos[24][1])
    E_P1 = float(datos[25][1])
    nu_P1 = float(datos[26][1])
    ro_P1 = float(datos[27][1])
    E_P2 = float(datos[28][1])
    nu_P2 = float(datos[29][1])
    ro_P2 = float(datos[30][1])
    analisis_path = datos[31][1]

    return d, dk, k, s, m, h, d1, d2, P1, P2, dext_P1, dext_P2, mat_T, mat_P1, mat_P2, mu_TP1, mu_TP2, mu_TA, mu_P1P2, Preload, Fz, Fxy,\
    E_T, nu_T, ro_T, E_P1, nu_P1, ro_P1, E_P2, nu_P2, ro_P2, analisis_path, folder_path

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
    iniciar_guiT()
    d, dk, k, s, m, h, d1, d2, P1, P2, dext_P1, dext_P2, mat_T, mat_P1, mat_P2, mu_TP1, mu_TP2, mu_TA, mu_P1P2, Preload, Fz, Fxy,\
    E_T, nu_T, ro_T, E_P1, nu_P1, ro_P1, E_P2, nu_P2, ro_P2, analisis_path, folder_path = leer_datos_tornillo()
    print(analisis_path, folder_path)
    Radio = d/2
    Radio_Cabeza = dk/2
    Longitud_Cabeza = k
    Longitud_Tuerca = m
    Espesor_Pieza1 = P1
    Espesor_Pieza2 = P2
    Radio_Pieza1 = dext_P1/2
    Radio_Pieza2 = dext_P2/2
    Radio_int_arandela = d1/2
    Radio_ext_arandela = d2/2
    Espesor_arandela = h
    iniciar_catia(Radio, Radio_Cabeza, Longitud_Cabeza, Longitud_Tuerca, Espesor_Pieza1, Espesor_Pieza2, Radio_Pieza1, Radio_Pieza2, Radio_int_arandela, Radio_ext_arandela, Espesor_arandela)
    ruta_destino = os.path.join(folder_path, "BoltedJoint.CATProduct")
    ruta_temporal = os.path.join(folder_path, "BoltedJoint_temporal.CATProduct")
    guardar_y_sobrescribir_documento(ruta_destino, ruta_temporal)
    quit()
    ruta_apex = "C:\\Program Files\\MSC.Software\\MSC Apex\\2024-011290\\runMSC_Apex"
    ejecutar_macro_apex(ruta_apex)