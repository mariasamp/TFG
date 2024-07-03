import subprocess
import os
import statistics
import re
import time

def leer_datos_tornillo():
    
    with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt')) as archivo:
        folder_path = archivo.read()
    datos = []
    with open(os.path.join(folder_path, "Data_T.txt")) as archivo:
        for linea in archivo:
            datos.append(linea.strip().split('='))

    analisis_path = datos[31][1]

    return analisis_path

def generar_set_1(filename):
    with open(filename, 'r') as f:
        numeros = f.read().split()

    set_1_lines = []
    line_prefix = "SET 1 = "
    continuation_prefix = "+       "
    line_length = 8  # Número de elementos por línea (excepto la primera)

    # Generar la primera línea
    set_1_lines.append(line_prefix + ', '.join(numeros[:line_length]) + ',')

    # Generar las líneas de continuación
    for i in range(line_length, len(numeros), line_length):
        set_1_lines.append(continuation_prefix + ', '.join(numeros[i:i+line_length]) + ',')

    # Eliminar la coma al final de la última línea
    set_1_lines[-1] = set_1_lines[-1][:-1]

    return '\n'.join(set_1_lines)

def modificar_bdf(file_path, numeros_filename): # Para que solo aparezcan tensiones máximas y desplazamientos máximos
    with open(file_path, 'r') as file:
        lines = file.readlines()
    set_1_lines = generar_set_1(numeros_filename)

    start_keyword = "SUBCASE 2"
    # Archivo modificado
    start_change = False
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() == 'ECHO=NONE':
                file.write(line)
                file.write(set_1_lines + '\n')
            if start_keyword in line:
                start_change = True
            if start_change:
                if 'DISPLACEMENT(PLOT) = ALL' in line or 'NLSTRESS(PLOT) = ALL' in line or 'OLOAD(PLOT) = ALL' in line or 'SPCFORCES(PLOT) = ALL' in line or 'BOUTPUT(PLOT) = ALL' in line or 'MPCFORCES(SORT1,PLOT) = ALL' in line:
                    continue
                elif "STRESS(PLOT,VONMISES,CORNER) = ALL" in line:
                    file.write("  STRESS(PRINT,PLOT,VONMISES,CORNER) = 1\n")
                else:
                    file.write(line)
            else:
                file.write(line)

def limpiar_carpeta(carpeta, archivo_excluido):
    for archivo in os.listdir(carpeta):
        archivo_path = os.path.join(carpeta, archivo)
        if archivo_path != archivo_excluido and os.path.isfile(archivo_path):
            os.remove(archivo_path)

def ejecutar_nastran(ruta_nastran, archivo_bdf):
    carpeta_bdf = os.path.dirname(archivo_bdf)
    comando = f'cd /d "{carpeta_bdf}" && "{ruta_nastran}" "{archivo_bdf}"'
    subprocess.call(comando, shell=True)

def comprobar_archivo(carpeta, nombre_archivo):
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    archivo_existe = False

    while not archivo_existe:
        if os.path.exists(ruta_archivo):
            archivo_existe = True
        if not archivo_existe:
            time.sleep(10)  # Espera 3 segundos antes de volver a comprobar
    return archivo_existe

def extract_s_max_values(file_path,caso):
    s_max_values = []
    chunk_size = 1024 * 1024  # 1MB por chunk

    def process_chunk(chunk, start_reading, start_reading2, s_max_values):
        lines = chunk.splitlines()
        for i, line in enumerate(lines):
            if start_reading[0] and start_reading2[0]:
                if ("***") in line:
                    start_reading[0] = False
                    break
                else:
                    grid_id_match = re.search(r"^\s*\d+\s+(\d+)\s+0GRID CS\s+\d+\s+GP", line)
                    if grid_id_match and i + 1 < len(lines):
                        line_siguiente = lines[i + 1]
                        normal_x_match = re.search(r"\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line_siguiente)
                        contador = 1
                        while (not normal_x_match) and contador<10:
                            contador += 1
                            line_siguiente = lines[i + contador]
                            normal_x_match = re.search(r"\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line_siguiente)
                    if grid_id_match and normal_x_match:
                        normal_x = float(normal_x_match.group(2))
                        s_max_values.append((normal_x))
            else:
                if ("S T R E S S E S   I N   H E X A H E D R O N   S O L I D   E L E M E N T S   ( H E X A )") in line:
                    start_reading[0] = True
                if start_reading[0] and (caso) in line:
                        start_reading2[0] = True

    with open(file_path, 'r') as file:
        start_reading = [False]
        start_reading2 = [False]
        chunk = file.read(chunk_size)
        while chunk:
            process_chunk(chunk, start_reading, start_reading2,s_max_values)
            chunk = file.read(chunk_size)

    return s_max_values

def main():
    analisis_path = leer_datos_tornillo()
    ruta_nastran = "C:\\Program Files\\MSC.Software\\MSC_Nastran\\2021.4\\bin\\nastranw"
    archivo_bdf = os.path.join(analisis_path, "Nonlinear Scenario.bdf")
    lectura_nastran = os.path.join(analisis_path, "Lectura_Nastran.txt")
    modificar_bdf(archivo_bdf, lectura_nastran)
    carpeta_bdf = os.path.dirname(archivo_bdf)
    limpiar_carpeta(carpeta_bdf, archivo_bdf)
    ejecutar_nastran(ruta_nastran, archivo_bdf)

    time.sleep(3)
    archivo_desaparecido = comprobar_archivo(carpeta_bdf, "nonlinear")

    if archivo_desaparecido:
        archivo_f06 =  os.path.join(analisis_path, "nonlinear scenario.f06")
        caso = "STATIC STEP 3" #1 para precarga, 2 para carga axial
        s_max_vector = extract_s_max_values(archivo_f06, caso)
        max_s_max = statistics.mean(s_max_vector)
        print(f"La tensión en el centro es de: {max_s_max}")

if __name__ == "__main__":
    main()