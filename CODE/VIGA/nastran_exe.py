import subprocess
import os
import re
import pandas as pd
import time
import statistics


def modificar_bdf(file_path): # Para que solo aparezcan tensiones máximas y desplazamientos máximos
    with open(file_path, 'r') as file:
        lines = file.readlines()

    old_lines = [
        "DISPLACEMENT(PLOT) = ALL\n",
        "STRESS(PLOT,VONMISES,CORNER) = ALL\n",
        "OLOAD(PLOT) = ALL\n",
        "SPCFORCES(PLOT) = ALL\n",
        "GPFORCE(PLOT) = ALL\n",
        "MPCFORCES(SORT1,PLOT) = ALL\n"
    ]
    
    new_lines = [
        "DISPLACEMENT(PRINT,PLOT) = ALL\n",
        "STRESS(PRINTPLOT,MAXS,CORNER) = ALL\n"
    ]
    
    # Archivo modificado
    with open(file_path, 'w') as file:
        for line in lines:
            if line in old_lines:
                if "DISPLACEMENT(PLOT) = ALL" in line:
                    file.write("DISPLACEMENT(PRINT,PLOT) = ALL\n")
                elif "STRESS(PLOT,VONMISES,CORNER) = ALL" in line:
                    file.write("STRESS(PRINT,PLOT,MAXS,CORNER) = ALL\n")
            else:
                file.write(line)

def ejecutar_macro_apex(ruta_apex, archivo_bdf):
    carpeta_bdf = os.path.dirname(archivo_bdf)
    comando = f'cd /d "{carpeta_bdf}" && "{ruta_apex}" "{archivo_bdf}"'
    subprocess.call(comando, shell=True)

def comprobar_archivo(carpeta, nombre_archivo):
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    archivo_no_existe = False

    while not archivo_no_existe:
        if not os.path.exists(ruta_archivo):
            archivo_no_existe = True
        if not archivo_no_existe:
            time.sleep(3)  # Espera 3 segundos antes de volver a comprobar
    return archivo_no_existe

def limpiar_carpeta(carpeta, archivo_excluido):
    for archivo in os.listdir(carpeta):
        archivo_path = os.path.join(carpeta, archivo)
        if archivo_path != archivo_excluido and os.path.isfile(archivo_path):
            os.remove(archivo_path)

def extract_columns(file_path, elemento):
    start_keyword = "                                             D I S P L A C E M E N T   V E C T O R"
    if elemento == "1D":
        stop_keyword = "EVENT 1"
    elif elemento == "3D":
        stop_keyword = "S T R E S S E S   I N   H E X A H E D R O N   S O L I D   E L E M E N T S   ( H E X A )"
    elif elemento == "2D":
        stop_keyword = "S T R E S S E S   I N   Q U A D R I L A T E R A L   E L E M E N T S   ( Q U A D 4 )"
    t3_column = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_index = None
        for i, line in enumerate(lines):
            if start_keyword in line:
                start_index = i + 2 
                break

        if start_index is not None:
            for line in lines[start_index:]:
                if stop_keyword in line:
                    break
                if line.strip():
                    columns = line.split()
                    if len(columns) >= 6:
                        try:
                            t3_value = float(columns[4])
                            t3_column.append(t3_value)
                        except ValueError:
                            continue
    return t3_column

def extract_s_max_values(file_path, elemento, nodos_tension, seccion, t):
    s_max_values = []
    chunk_size = 1024 * 1024  # 1MB por chunk

    def process_chunk(chunk, start_reading, s_max_values):
        lines = chunk.splitlines()
        for i, line in enumerate(lines):
            if start_reading[0]:
                if "***" in line:
                    start_reading[0] = False
                    break

                if elemento == "1D":
                    match = re.findall(r"([-+]?\d+\.\d+E[-+]?\d+)", line)
                    if len(match) >= 5:
                        s_max_values.append(float(match[4]))
                elif elemento == "3D" or elemento == "2D":
                    # PARA TENSIÓN EN LOS NODOS
                    # if elemento == "3D":
                    #     grid_id_match = re.search(r"^\s*\d+\s+(\d+|CENTER)\s", line)
                    #     normal_x_match = re.search(r"\s+X\s+([-+]?\d+\.\d+E[-+]?\d+)", line)
                    #     if grid_id_match and normal_x_match:
                    #         current_grid_id = grid_id_match.group(1)
                    #         if (current_grid_id == "CENTER"):
                    #             continue
                    #         normal_x = float(normal_x_match.group(1))
                    #         if int(current_grid_id) in nodos_tension:
                    #             s_max_values.append((normal_x))
                    # PARA TENSIÓN EN LOS ELEMENTOS
                    if elemento == "3D":
                        grid_id_match = re.search(r"^\s*\d+\s+(\d+)\s+0GRID CS\s+\d+\s+GP", line)
                        if grid_id_match and i + 1 < len(lines):
                            line_siguiente = lines[i + 1]
                            normal_x_match = re.search(r"\s+X\s+([-+]?\d+\.\d+E[-+]?\d+)", line_siguiente)
                        if grid_id_match and normal_x_match:
                            current_grid_id = grid_id_match.group(1)
                            normal_x = float(normal_x_match.group(1))
                            if int(current_grid_id) in nodos_tension:
                                s_max_values.append((normal_x))
                    # PARA TENSIÓN EN LOS NODOS:
                    # if elemento == "2D":
                    #     if seccion == "Rectangular Hueca":
                    #         grid_id_match = re.search(r"^\s*(\d+|CEN/4)\s", line)
                    #         if grid_id_match:
                    #             current_grid_id = grid_id_match.group(1)
                    #             if current_grid_id == "CEN/4":
                    #                 continue
                    #             if int(current_grid_id) in nodos_tension:
                    #                 value = t/2
                    #                 value1 = f"{-value:.6E}".replace('E+', 'E\\+').replace('.', '\\.')
                    #                 match_neg_5_000000 = re.search(fr"{value1}\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line)
                    #                 if match_neg_5_000000:
                    #                     normal_x = float(match_neg_5_000000.group(2))  # Ahora toma el segundo grupo que corresponde a la columna de la derecha
                    #                     s_max_values.append(normal_x)
                    #     elif seccion == "Sección en I":
                    #             grid_id_match = re.search(r"^\s*(\d+|CEN/4)\s", line)
                    #             if grid_id_match:
                    #                 current_grid_id = grid_id_match.group(1)
                    #                 if current_grid_id == "CEN/4":
                    #                     continue
                    #                 if int(current_grid_id) in nodos_tension:
                    #                     value = t/2
                    #                     value1 = f"{-value:.6E}".replace('E+', 'E\\+').replace('.', '\\.')
                    #                     match_neg_5_000000 = re.search(fr"{value1}\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line)
                    #                     if match_neg_5_000000:
                    #                         normal_x = float(match_neg_5_000000.group(1))  # Ahora toma el segundo grupo que corresponde a la columna de la derecha
                    #                         s_max_values.append(normal_x)
                    # PARA TENSIÓN EN LOS ELEMENTOS:
                    if elemento == "2D":
                        if seccion == "Rectangular Hueca":
                            grid_id_match = re.search(r"^\s*(\d+)\s+(\d+)\s*", line)
                            if grid_id_match:
                                current_grid_id = grid_id_match.group(2)
                                if int(current_grid_id) in nodos_tension:
                                    value = t/2
                                    value1 = f"{-value:.6E}".replace('E+', 'E\\+').replace('.', '\\.')
                                    match_neg_5_000000 = re.search(fr"{value1}\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line)
                                    if match_neg_5_000000:
                                        normal_x = float(match_neg_5_000000.group(2))  # Ahora toma el segundo grupo que corresponde a la columna de la derecha
                                        s_max_values.append(normal_x)
                        elif seccion == "Sección en I":
                                grid_id_match = re.search(r"^\s*(\d+)\s+(\d+)\s*", line)
                                if grid_id_match:
                                    current_grid_id = grid_id_match.group(2)
                                    if int(current_grid_id) in nodos_tension:
                                        value = t/2
                                        value1 = f"{-value:.6E}".replace('E+', 'E\\+').replace('.', '\\.')
                                        match_neg_5_000000 = re.search(fr"{value1}\s+([-+]?\d+\.\d+E[-+]?\d+)\s+([-+]?\d+\.\d+E[-+]?\d+)", line)
                                        if match_neg_5_000000:
                                            normal_x = float(match_neg_5_000000.group(1))  # Ahora toma el segundo grupo que corresponde a la columna de la derecha
                                            s_max_values.append(normal_x)
                    
            else:
                if elemento == "1D" and ("S T R E S S E S   I N   B E A M   E L E M E N T S") in line:
                #if (("S T R E S S E S   I N   B E A M   E L E M E N T S") if elemento == "1D" elif elemento == "2D" ("S T R E S S E S   I N   H E X A H E D R O N   S O L I D   E L E M E N T S   ( H E X A )")) in line:
                    start_reading[0] = True
                elif elemento == "3D" and ("S T R E S S E S   I N   H E X A H E D R O N   S O L I D   E L E M E N T S   ( H E X A )") in line:
                    start_reading[0] = True
                elif elemento == "2D" and ("S T R E S S E S   I N   Q U A D R I L A T E R A L   E L E M E N T S   ( Q U A D 4 )") in line:
                    start_reading[0] = True

    with open(file_path, 'r') as file:
        start_reading = [False]
        chunk = file.read(chunk_size)
        while chunk:
            process_chunk(chunk, start_reading, s_max_values)
            chunk = file.read(chunk_size)

    return s_max_values

def max_absolute_value(values):
    if not values:
        raise ValueError("La lista no puede estar vacía")
    return max(values, key=abs)

def main():
    with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt')) as archivo:
        folder_path1 = archivo.read()
    datos = []
    with open(os.path.join(folder_path1, "Valores_Viga.txt")) as archivo:
        for linea in archivo:
            datos.append(linea.strip().split('\t'))

    a0 = float(datos[0][1])
    b0 = float(datos[1][1])
    L = float(datos[2][1])
    t = float(datos[3][1])
    a1 = float(datos[4][1])
    b1 = float(datos[5][1])
    meshSize = float(datos[6][1])
    load = float(datos[7][1])
    seccion = datos[8][1]
    forma_seccion = datos[9][1]
    direccion = datos[10][1]
    material = datos[11][1]
    elemento = datos[12][1]
    analisis = datos[13][1]
    path_analisis = datos[14][1]

    ruta_nastran = "C:\\Program Files\\MSC.Software\\MSC_Nastran\\2021.4\\bin\\nastranw"
    archivo_bdf = os.path.join(path_analisis, "Static Scenario Viga.bdf")

    nodos_tension = []
    if elemento == "3D" or elemento == "2D":
        with open(os.path.join(path_analisis, "Lectura_Nastran.txt"), 'r') as file:
            for line in file:
                nodos_tension.append(int(line.strip()))

    modificar_bdf(archivo_bdf)
    
    carpeta_bdf = path_analisis
    limpiar_carpeta(carpeta_bdf, archivo_bdf)
    # Ejecutar MSC Nastran
    ejecutar_macro_apex(ruta_nastran, archivo_bdf)
    
    time.sleep(3)
    archivo_desaparecido = comprobar_archivo(carpeta_bdf, "static scenario viga.aeso")

    if archivo_desaparecido:
        # Ruta del archivo .f06 generado
        archivo_f06 = os.path.join(carpeta_bdf, "Static Scenario Viga.f06")
        
        # Extraer columna T3
        
        t3_column = extract_columns(archivo_f06, elemento)
        if elemento == "1D":
            max_abs_t3 = max_absolute_value(t3_column)
        elif elemento == "3D" or elemento == "2D":
            max_abs_t3 = t3_column[-1]

        print(f"El desplazamiento máximo es: {max_abs_t3}")
        # Extraer valores S-MAX
        s_max_vector = extract_s_max_values(archivo_f06, elemento, nodos_tension, seccion, t)
        if elemento == "1D":
            max_s_max = max_absolute_value(s_max_vector)
        elif elemento == "3D" or elemento == "2D":
            max_s_max = statistics.mean(s_max_vector)

        print(f"La tensión máxima es: {abs(max_s_max)}")

if __name__ == "__main__":
    main()