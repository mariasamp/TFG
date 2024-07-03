import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import math

def iniciar_guiT():
    metricas_map = {
        "M1.6": 1.6, "M2": 2, "M2.5": 2.5, "M3": 3, "M4": 4, "M5": 5,
        "M6": 6, "M8": 8, "M10": 10, "M12": 12, "M16": 16, "M20": 20
    }

    precarga_map = {
        "Acero": {
        1.6: 610, 2: 1000, 2.5: 1630, 3: 2420, 4: 4210, 5: 6800,
        6: 9660, 8: 17600, 10: 27800, 12: 40500, 16: 75200, 20: 117500 
        },
        "Titanio": {
        1.6: 840, 2: 1380, 2.5: 2250, 3: 3340, 4: 5830, 5: 9420,
        6: 13400, 8: 24300, 10: 38500, 12: 56000, 16: 104000, 20: 163000 
        },
        "Inconel 718": {
        1.6: 1060, 2: 1730, 2.5: 2820, 3: 4190, 4: 7300, 5: 11800,
        6: 16700, 8: 30500, 10: 48300, 12: 70100, 16: 130000, 20: 204000 
        },
        "Personalizado": {
        1.6: 0, 2: 0, 2.5: 0, 3: 0, 4: 0, 5: 0,
        6: 0, 8: 0, 10: 0, 12: 0, 16: 0, 20: 0 
        },
    }
    
    def medidas(M):
        if M == 1.6:
            return 1.6, 3, 1.6, 3.2, 1.3, 0.3, 1.7, 4
        elif M == 2:
            return 2, 3.8, 2, 4, 1.6, 0.3, 2.2, 5
        elif M == 2.5:
            return 2.5, 4.5, 2.5, 5, 2, 0.5, 2.5, 6
        elif M == 3:
            return 3, 5.5, 4, 5.5, 2.4, 0.5, 3.2, 7
        elif M == 4:
            return 4, 7, 4, 7, 3.2, 0.8, 4.3, 9
        elif M == 5:
            return 5, 8.5, 5, 8, 4.7, 1, 5.3, 10
        elif M == 6:
            return 6, 10, 6, 10, 5.2, 1.6, 6.4, 12
        elif M == 8:
            return 8, 13, 8, 13, 6.8, 1.6, 8.4, 16
        elif M == 10:
            return 10, 16, 10, 16, 8.4, 2, 10.5, 20
        elif M == 12:
            return 12, 18, 12, 18, 10.8, 2.5, 13, 24
        elif M == 16:
            return 16, 24, 16, 24, 14.8, 3, 17, 30
        elif M == 20:
            return 20, 30, 20, 30, 18, 3, 21, 37
        else:
            return None

    def mostrar_dimensiones():
        global M, d, dk, k, s, m, h, d1, d2

        metrica_str = metrica_var.get()
        M = metricas_map[metrica_str]
        dimensiones = medidas(M)
        d, dk, k, s, m, h, d1, d2 = dimensiones
        P1 = float(espesor1_var.get())
        P2 = float(espesor2_var.get())
        dext_1 = float(pieza1_var.get())
        dext_2 = float(pieza2_var.get())
        if metrica_str not in metricas_map:
            messagebox.showerror("Error", "Selecciona una métrica válida.")
            return

        x=(P1+P2)/d2
        y=min(dext_1,dext_2)/d2
        tan_phi = 0.362+0.032*math.log(x/2)+0.153*math.log(y)
        Dlim = d2 + (P1+P2)*tan_phi

        if dimensiones is None:
            messagebox.showerror("Error", "Selecciona una métrica válida.")
            return
        
        if dext_1 <= Dlim:
            frase_advertencia1 = "El diámetro exterior de la pieza superior es demasiado pequeño, \nel cono de compresión supera la geometría."
        else:
            frase_advertencia1 = "El diámetro exterior de la pieza superior es suficiente, \nel cono de compresión no superará la geometría."

        if dext_2 <= Dlim:
            frase_advertencia2 = "El diámetro exterior de la pieza inferior es demasiado pequeño, \nel cono de compresión supera la geometría."
        else:
            frase_advertencia2 = "El diámetro exterior de la pieza inferior es suficiente, \nel cono de compresión no superará la geometría."

        resultado.set(f"Dimensiones del tornillo M{M}:\n"
                    f"Diámetro: {d} mm\n"
                    f"Diámetro de la cabeza: {dk} mm\n"
                    f"Longitud de la cabeza: {k} mm\n"
                    f"Diámetro de la tuerca: {s} mm\n"
                    f"Longitud de la tuerca: {m} mm\n"
                    f"Espesor de la arandela: {h} mm\n"
                    f"Diámetro interior de la arandela: {d1} mm\n"
                    f"Diámetro exterior de la arandela: {d2} mm\n"
                    f"Espesor de la pieza superior: {P1} mm\n"
                    f"Espesor de la pieza inferior: {P2} mm\n"
                    f"Diámetro exterior de la pieza superior: {dext_1} mm\n"
                    f"Diámetro exterior de la pieza inferior: {dext_2} mm\n"
                    f"{frase_advertencia1}\n"
                    f"{frase_advertencia2}\n"
                    f"Diámetro límite del cono de compresión = {round(Dlim,2)} mm")
        
    def actualizar_friccion():
        material_tornillo = material_tornillo_var.get()
        material_p1 = material_pieza1_var.get()
        material_p2 = material_pieza2_var.get()

        if material_p1 and material_p2 and material_tornillo:
            if material_tornillo == "Acero":
                friccion_tornillo_arandela_var.set("0.15")
                if material_p1 == "Aluminio":
                    friccion_tornillo_p1_var.set("0.19")
                elif material_p1 == "Acero":
                    friccion_tornillo_p1_var.set("0.15")
                elif material_p1 == "Titanio":
                    friccion_tornillo_p1_var.set("0.25")
                else:
                    friccion_tornillo_p1_var.set("")

                if material_p2 == "Aluminio":
                    friccion_tornillo_p2_var.set("0.19")
                elif material_p2 == "Acero":
                    friccion_tornillo_p2_var.set("0.15")
                elif material_p2 == "Titanio":
                    friccion_tornillo_p2_var.set("0.25")
                else:
                    friccion_tornillo_p2_var.set("")
            elif material_tornillo == "Titanio":
                friccion_tornillo_arandela_var.set("0.35")
                if material_p1 == "Aluminio":
                    friccion_tornillo_p1_var.set("0.3")
                elif material_p1 == "Acero":
                    friccion_tornillo_p1_var.set("0.25")
                elif material_p1 == "Titanio":
                    friccion_tornillo_p1_var.set("0.35")
                else:
                    friccion_tornillo_p1_var.set("")

                if material_p2 == "Aluminio":
                    friccion_tornillo_p2_var.set("0.3")
                elif material_p2 == "Acero":
                    friccion_tornillo_p2_var.set("0.25")
                elif material_p2 == "Titanio":
                    friccion_tornillo_p2_var.set("0.35")
                else:
                    friccion_tornillo_p2_var.set("")
            elif material_tornillo == "Inconel 718":
                friccion_tornillo_arandela_var.set("0.1")
                if material_p1 == "Aluminio":
                    friccion_tornillo_p1_var.set("0.2")
                elif material_p1 == "Acero":
                    friccion_tornillo_p1_var.set("0.1")
                elif material_p1 == "Titanio":
                    friccion_tornillo_p1_var.set("0.2")
                else:
                    friccion_tornillo_p1_var.set("")

                if material_p2 == "Aluminio":
                    friccion_tornillo_p2_var.set("0.2")
                elif material_p2 == "Acero":
                    friccion_tornillo_p2_var.set("0.1")
                elif material_p2 == "Titanio":
                    friccion_tornillo_p2_var.set("0.2")
                else:
                    friccion_tornillo_p2_var.set("")
            else:
                friccion_tornillo_arandela_var.set("")
                if material_p1 == "Aluminio":
                    friccion_tornillo_p1_var.set("")
                elif material_p1 == "Acero":
                    friccion_tornillo_p1_var.set("")
                elif material_p1 == "Titanio":
                    friccion_tornillo_p1_var.set("")
                else:
                    friccion_tornillo_p1_var.set("")

                if material_p2 == "Aluminio":
                    friccion_tornillo_p2_var.set("")
                elif material_p2 == "Acero":
                    friccion_tornillo_p2_var.set("")
                elif material_p2 == "Titanio":
                    friccion_tornillo_p2_var.set("")
                else:
                    friccion_tornillo_p2_var.set("")

            if material_p1 == "Aluminio" and material_p2 == "Aluminio":
                friccion_p1_p2_var.set("0.21")
            elif material_p1 == "Acero" and material_p2 == "Acero":
                friccion_p1_p2_var.set("0.15")
            elif (material_p1 == "Aluminio" and material_p2 == "Acero") or (material_p1 == "Acero" and material_p2 == "Aluminio"):
                friccion_p1_p2_var.set("0.19")
            elif material_p1 == "Titanio" and material_p2 == "Titanio":
                friccion_p1_p2_var.set("0.35")
            elif (material_p1 == "Aluminio" and material_p2 == "Titanio") or (material_p1 == "Titanio" and material_p2 == "Aluminio"):
                friccion_p1_p2_var.set("0.3")
            elif (material_p1 == "Acero" and material_p2 == "Titanio") or (material_p1 == "Titanio" and material_p2 == "Acero"):
                friccion_p1_p2_var.set("0.25")
            else:
                friccion_p1_p2_var.set("")

            friccion_tornillo_p1_label.grid(row=3, column=0, padx=10, pady=5)
            friccion_tornillo_p1_entry.grid(row=3, column=1, padx=10, pady=5)
            friccion_tornillo_p2_label.grid(row=4, column=0, padx=10, pady=5)
            friccion_tornillo_p2_entry.grid(row=4, column=1, padx=10, pady=5)
            friccion_tornillo_arandela_label.grid(row=5, column=0, padx=10, pady=5)
            friccion_tornillo_arandela_entry.grid(row=5, column=1, padx=10, pady=5)
            friccion_p1_p2_label.grid(row=6, column=0, padx=10, pady=5)
            friccion_p1_p2_entry.grid(row=6, column=1, padx=10, pady=5)
        
        if material_tornillo:
            precarga = precarga_map[material_tornillo][M]
            precarga_var.set(str(precarga))
            precarga_label.grid(row=7, column=0, padx=10, pady=5)
            precarga_entry.grid(row=7, column=1, padx=10, pady=5)
            fuerza_axial_label.grid(row=8, column=0, padx=10, pady=5)
            fuerza_axial_entry.grid(row=8, column=1, padx=10, pady=5)
            fuerza_cortante_label.grid(row=9, column=0, padx=10, pady=5)
            fuerza_cortante_entry.grid(row=9, column=1, padx=10, pady=5)

    def mostrar_campos_personalizado(variable, marco, tipo):
        if tipo == "tornillo":
            widgets = [(tk.Label(marco, text="Módulo elástico del tornillo (GPa):"), tk.Entry(marco, textvariable=modulo_tornillo_var)),
                       (tk.Label(marco, text="Coeficiente de Poisson del tornillo:"), tk.Entry(marco, textvariable=poisson_tornillo_var)),
                       (tk.Label(marco, text="Densidad del tornillo (kg/m³):"), tk.Entry(marco, textvariable=densidad_tornillo_var))]
        elif tipo == "P1":
            widgets = [(tk.Label(marco, text="Módulo elástico de la pieza superior (GPa):"), tk.Entry(marco, textvariable=modulo_P1_var)),
                       (tk.Label(marco, text="Coeficiente de Poisson de la pieza superior:"), tk.Entry(marco, textvariable=poisson_P1_var)),
                       (tk.Label(marco, text="Densidad de la pieza superior (kg/m³):"), tk.Entry(marco, textvariable=densidad_P1_var))]
        else:  # tipo == "P2"
            widgets = [(tk.Label(marco, text="Módulo elástico de la pieza inferior (GPa):"), tk.Entry(marco, textvariable=modulo_P2_var)),
                       (tk.Label(marco, text="Coeficiente de Poisson de la pieza inferior:"), tk.Entry(marco, textvariable=poisson_P2_var)),
                       (tk.Label(marco, text="Densidad de la pieza inferior (kg/m³):"), tk.Entry(marco, textvariable=densidad_P2_var))]

        if variable.get() == "Personalizado":
            for i, (label, entry) in enumerate(widgets):
                if tipo == "tornillo":
                    label.grid(row=i, column=2, padx=10, pady=5)
                    entry.grid(row=i, column=3, padx=10, pady=5)
                elif tipo == "P1":
                    label.grid(row=i+3, column=2, padx=10, pady=5)
                    entry.grid(row=i+3, column=3, padx=10, pady=5)
                else:  # tipo == "P2"
                    label.grid(row=i+6, column=2, padx=10, pady=5)
                    entry.grid(row=i+6, column=3, padx=10, pady=5)
            return widgets
        else:
            for label, entry in widgets:
                label.grid_forget()
                entry.grid_forget()
            return widgets

    def guardar_datos():
        global P1, P2, dext_P1, dext_P2, material_tornillo, material_pieza1, material_pieza2, friccion_tornillo_p1, friccion_tornillo_p2, friccion_tornillo_arandela, friccion_p1_p2, precarga, fuerza_axial, fuerza_cortante
        try:
            P1 = float(espesor1_var.get())
            P2 = float(espesor2_var.get())
            dext_P1 = float(pieza1_var.get())
            dext_P2 = float(pieza2_var.get())
            material_tornillo = material_tornillo_var.get()
            material_pieza1 = material_pieza1_var.get()
            material_pieza2 = material_pieza2_var.get()
            friccion_tornillo_p1 = float(friccion_tornillo_p1_var.get())
            friccion_tornillo_p2 = float(friccion_tornillo_p2_var.get())
            friccion_tornillo_arandela = float(friccion_tornillo_arandela_var.get())
            friccion_p1_p2 = float(friccion_p1_p2_var.get())
            precarga = float(precarga_var.get())
            fuerza_axial = float(fuerza_axial_var.get())
            fuerza_cortante = float(fuerza_cortante_var.get())
            if material_tornillo == "Personalizado":
                modulo_tornillo = float(modulo_tornillo_var.get())
                poisson_tornillo = float(poisson_tornillo_var.get())
                densidad_tornillo = float(densidad_tornillo_var.get())
            if material_pieza1 == "Personalizado":
                modulo_P1 = float(modulo_P1_var.get())
                poisson_P1 = float(poisson_P1_var.get())
                densidad_P1 = float(densidad_P1_var.get())
            if material_pieza2 == "Personalizado":
                modulo_P2 = float(modulo_P2_var.get())
                poisson_P2 = float(poisson_P2_var.get())
                densidad_P2 = float(densidad_P2_var.get())
            
            messagebox.showinfo("Datos guardados", 
                                f"Datos guardados correctamente:\n"
                                f"Métrica: M{M}\n"
                                f"Diámetro: {d} mm\n"
                                f"Diámetro de la cabeza: {dk} mm\n"
                                f"Longitud de la cabeza: {k} mm\n"
                                f"Diámetro de la tuerca: {s} mm\n"
                                f"Longitud de la tuerca: {m} mm\n" 
                                f"Espesor de la arandela: {h} mm\n"
                                f"Diámetro interior de la arandela: {d1} mm\n"
                                f"Diámetro exterior de la arandela: {d2} mm\n"
                                f"Espesor P1: {P1} mm\nEspesor P2: {P2} mm\n"
                                f"Dext P1: {dext_P1} mm\nDext P2: {dext_P2} mm\n"
                                f"Material Tornillo: {material_tornillo}\nMaterial Pieza 1: {material_pieza1}\nMaterial Pieza 2: {material_pieza2}\n"
                                f"Fricción Tornillo-P1: {friccion_tornillo_p1}\nFricción Tornillo-P2: {friccion_tornillo_p2}\nFricción P1-P2: {friccion_p1_p2}\n"
                                f"Precarga: {precarga}\nFuerza Axial: {fuerza_axial}\nFuerza Cortante: {fuerza_cortante}")
            
            archivo_metricas = os.path.join(folder_path, "Data_T.txt")
            with open(archivo_metricas, "w") as file:
                file.write(f"d = {d}\n")
                file.write(f"dk = {dk}\n")
                file.write(f"k = {k}\n")
                file.write(f"s = {s}\n")
                file.write(f"m = {m}\n")
                file.write(f"h = {h}\n")
                file.write(f"d1 = {d1}\n")
                file.write(f"d2 = {d2}\n")
                file.write(f"P1 = {P1}\n")
                file.write(f"P2 = {P2}\n")
                file.write(f"Dext P1 = {dext_P1}\n")
                file.write(f"Dext P2 = {dext_P2}\n")
                file.write(f"Material Tornillo = {material_tornillo}\n")
                file.write(f"Material Pieza 1 = {material_pieza1}\n")
                file.write(f"Material Pieza 2 = {material_pieza2}\n")
                file.write(f"Fricción Tornillo-P1 = {friccion_tornillo_p1}\n")
                file.write(f"Fricción Tornillo-P2 = {friccion_tornillo_p2}\n")
                file.write(f"Fricción Tornillo-Arandela = {friccion_tornillo_arandela}\n")
                file.write(f"Fricción P1-P2 = {friccion_p1_p2}\n")
                file.write(f"Precarga = {precarga}\n")
                file.write(f"Fuerza Axial = {fuerza_axial}\n")
                file.write(f"Fuerza Cortante = {fuerza_cortante}\n")
                file.write(f"E Tornillo = {modulo_tornillo if (material_tornillo == 'Personalizado') else 0}\n")
                file.write(f"nu Tornillo = {poisson_tornillo if (material_tornillo == 'Personalizado') else 0}\n")
                file.write(f"ro Tornillo = {densidad_tornillo if (material_tornillo == 'Personalizado') else 0}\n")
                file.write(f"E P1 = {modulo_P1 if material_pieza1 == 'Personalizado' else 0}\n")
                file.write(f"nu P1 = {poisson_P1 if material_pieza1 == 'Personalizado' else 0}\n")
                file.write(f"ro P1 = {densidad_P1 if material_pieza1 == 'Personalizado' else 0}\n")
                file.write(f"E P2 = {modulo_P2 if material_pieza2 == 'Personalizado' else 0}\n")
                file.write(f"nu P2 = {poisson_P2 if material_pieza2 == 'Personalizado' else 0}\n")
                file.write(f"ro P2 = {densidad_P2 if material_pieza2 == 'Personalizado' else 0}\n")
                file.write(f"Análisis path ={analisis_path}\n")

            app.quit()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un valor numérico válido para los espesores y las fuerzas.")

    def browse_folder():
        global folder_path
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("Carpeta seleccionada para el modelo:", folder_path)
        with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt'), 'w') as archivo:
            archivo.write(str(folder_path))
    def browse_folder2():
        global analisis_path
        analisis_path = filedialog.askdirectory()
        if analisis_path:
            print("Carpeta seleccionada para el análisis:", analisis_path)

    app = tk.Tk()
    app.title("Análisis de una unión atornillada")

    metricas = list(metricas_map.keys())
    metrica_var = tk.StringVar(value="Selecciona una métrica")
    resultado = tk.StringVar()

    # Crear el notebook
    notebook = ttk.Notebook(app)
    geometria_frame = ttk.Frame(notebook)
    analisis_frame = ttk.Frame(notebook)

    notebook.add(geometria_frame, text="Geometría")
    notebook.add(analisis_frame, text="Análisis")
    notebook.grid(row=0, column=0, padx=10, pady=10)

    # Widgets de la pestaña Geometría
    metrica_label = tk.Label(geometria_frame, text="Selecciona una métrica:")
    metrica_combo = ttk.Combobox(geometria_frame, textvariable=metrica_var, values=metricas, state="readonly")
    mostrar_button = tk.Button(geometria_frame, text="Mostrar Dimensiones", command=mostrar_dimensiones)
    resultado_label = tk.Label(geometria_frame, textvariable=resultado, justify="left")

    espesor1_label = tk.Label(geometria_frame, text="Espesor de la pieza superior (mm):")
    espesor1_var = tk.StringVar()
    espesor1_entry = tk.Entry(geometria_frame, textvariable=espesor1_var)

    espesor2_label = tk.Label(geometria_frame, text="Espesor de la pieza inferior(mm):")
    espesor2_var = tk.StringVar()
    espesor2_entry = tk.Entry(geometria_frame, textvariable=espesor2_var)

    espesor1_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
    espesor1_entry.grid(row=2, column=1, padx=10, pady=5)
    espesor2_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
    espesor2_entry.grid(row=3, column=1, padx=10, pady=5)

    pieza1_label = tk.Label(geometria_frame, text="Diámetro exterior de la pieza superior (mm):")
    pieza1_var = tk.StringVar()
    pieza1_entry = tk.Entry(geometria_frame, textvariable=pieza1_var)

    pieza2_label = tk.Label(geometria_frame, text="Diámetro exterior de la pieza inferior(mm):")
    pieza2_var = tk.StringVar()
    pieza2_entry = tk.Entry(geometria_frame, textvariable=pieza2_var)

    pieza1_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
    pieza1_entry.grid(row=4, column=1, padx=10, pady=5)
    pieza2_label.grid(row=5, column=0, padx=10, pady=5, sticky='e')
    pieza2_entry.grid(row=5, column=1, padx=10, pady=5)

    metrica_label.grid(row=0, column=0, padx=10, pady=5)
    metrica_combo.grid(row=0, column=1, padx=10, pady=5)
    mostrar_button.grid(row=6, columnspan=2, pady=10)
    resultado_label.grid(row=7, columnspan=2, padx=10, pady=5)

    # Widgets de la pestaña Análisis
    material_tornillo_label = tk.Label(analisis_frame, text="Material del tornillo:")
    material_tornillo_var = tk.StringVar()
    material_tornillo_combo = ttk.Combobox(analisis_frame, textvariable=material_tornillo_var, values=["Acero", "Titanio", "Inconel 718", "Personalizado"], state="readonly", postcommand=actualizar_friccion)
    material_tornillo_combo.bind("<<ComboboxSelected>>", lambda e: mostrar_campos_personalizado(material_tornillo_var, analisis_frame, "tornillo"))

    material_pieza1_label = tk.Label(analisis_frame, text="Material de la primera pieza:")
    material_pieza1_var = tk.StringVar()
    material_pieza1_combo = ttk.Combobox(analisis_frame, textvariable=material_pieza1_var, values=["Aluminio", "Acero", "Titanio", "Personalizado"], state="readonly", postcommand=actualizar_friccion)
    material_pieza1_combo.bind("<<ComboboxSelected>>", lambda e: mostrar_campos_personalizado(material_pieza1_var, analisis_frame, "P1"))

    material_pieza2_label = tk.Label(analisis_frame, text="Material de la segunda pieza:")
    material_pieza2_var = tk.StringVar()
    material_pieza2_combo = ttk.Combobox(analisis_frame, textvariable=material_pieza2_var, values=["Aluminio", "Acero", "Titanio", "Personalizado"], state="readonly", postcommand=actualizar_friccion)
    material_pieza2_combo.bind("<<ComboboxSelected>>", lambda e: mostrar_campos_personalizado(material_pieza2_var, analisis_frame, "P2"))

    friccion_tornillo_p1_label = tk.Label(analisis_frame, text="Fricción Tornillo-Pieza 1:")
    friccion_tornillo_p1_var = tk.StringVar()
    friccion_tornillo_p1_entry = tk.Entry(analisis_frame, textvariable=friccion_tornillo_p1_var)

    friccion_tornillo_p2_label = tk.Label(analisis_frame, text="Fricción Tornillo-Pieza 2:")
    friccion_tornillo_p2_var = tk.StringVar()
    friccion_tornillo_p2_entry = tk.Entry(analisis_frame, textvariable=friccion_tornillo_p2_var)

    friccion_tornillo_arandela_label = tk.Label(analisis_frame, text="Fricción Tornillo-Arandela:")
    friccion_tornillo_arandela_var = tk.StringVar()
    friccion_tornillo_arandela_entry = tk.Entry(analisis_frame, textvariable=friccion_tornillo_arandela_var)

    friccion_p1_p2_label = tk.Label(analisis_frame, text="Fricción Pieza 1-Pieza 2:")
    friccion_p1_p2_var = tk.StringVar()
    friccion_p1_p2_entry = tk.Entry(analisis_frame, textvariable=friccion_p1_p2_var)

    precarga_label = tk.Label(analisis_frame, text="Precarga (N):")
    precarga_var = tk.StringVar()
    precarga_entry = tk.Entry(analisis_frame, textvariable=precarga_var)

    fuerza_axial_label = tk.Label(analisis_frame, text="Fuerza Axial (N):")
    fuerza_axial_var = tk.StringVar()
    fuerza_axial_entry = tk.Entry(analisis_frame, textvariable=fuerza_axial_var)

    fuerza_cortante_label = tk.Label(analisis_frame, text="Fuerza Cortante (N):")
    fuerza_cortante_var = tk.StringVar()
    fuerza_cortante_entry = tk.Entry(analisis_frame, textvariable=fuerza_cortante_var)

    modulo_tornillo_var = tk.StringVar()
    poisson_tornillo_var = tk.StringVar()
    densidad_tornillo_var = tk.StringVar()
    modulo_P1_var = tk.StringVar()
    poisson_P1_var = tk.StringVar()
    densidad_P1_var = tk.StringVar()
    modulo_P2_var = tk.StringVar()
    poisson_P2_var = tk.StringVar()
    densidad_P2_var = tk.StringVar()

    material_tornillo_label.grid(row=0, column=0, padx=10, pady=5)
    material_tornillo_combo.grid(row=0, column=1, padx=10, pady=5)
    material_pieza1_label.grid(row=1, column=0, padx=10, pady=5)
    material_pieza1_combo.grid(row=1, column=1, padx=10, pady=5)
    material_pieza2_label.grid(row=2, column=0, padx=10, pady=5)
    material_pieza2_combo.grid(row=2, column=1, padx=10, pady=5)

    guardar_button = tk.Button(analisis_frame, text="Guardar Datos", command=guardar_datos)
    guardar_button.grid(row=14, columnspan=2, pady=10)

    browse_button = tk.Button(analisis_frame, text="Guardar modelo...", command=browse_folder)
    browse_button.grid(row=12, columnspan=2, pady=10)  

    browse_analisis_button = tk.Button(analisis_frame, text="Guardar resultados análisis...", command=browse_folder2)
    browse_analisis_button.grid(row=13, columnspan=2, pady=10) 

    app.mainloop()