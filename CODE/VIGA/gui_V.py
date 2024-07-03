import customtkinter as ctk
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog

def iniciar_gui(guardar_datos_callback):
    global tipo_seccion, forma_seccion, a0_entry, b0_entry, L_entry, t_entry, a1_entry, b1_entry, mallado_label, mallado_entry, carga_label, carga_entry, direccion_carga, material, tipo_elemento, tab_seccion, tab_mallado_cargas
    global t_label, a1_label, b1_label, images_frame, tipo_analisis, analisis_frame, browse_analisis_button, modulo_elastico_label, modulo_elastico_entry, poisson_label, poisson_entry, densidad_label, densidad_entry

    ctk.set_appearance_mode("Light")  # Puedes elegir entre "System" (Sistema), "Dark" (Oscuro) y "Light" (Claro)
    ctk.set_default_color_theme("dark-blue")  # Puedes elegir entre "blue" (Azul), "dark-blue" (Azul oscuro) y "green" (Verde)

    root = ctk.CTk()
    root.title("Análisis de una viga empotrada")
    root.geometry("825x650")

    tabControl = ctk.CTkTabview(root)
    tabControl.grid(row=0, column=0, columnspan=3, rowspan=10, sticky="nsew")
    
    tab_seccion = tabControl.add("Geometría")
    tab_mallado_cargas = tabControl.add("Análisis")

    tipo_seccion = ctk.StringVar()
    forma_seccion = ctk.StringVar()
    tipo_elemento = ctk.StringVar()
    tipo_analisis = ctk.StringVar()

    tipo_seccion_frame = ctk.CTkFrame(tab_seccion)
    tipo_seccion_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    tipo_seccion_label = ctk.CTkLabel(tipo_seccion_frame, text="Forma de la sección:")
    tipo_seccion_label.grid(row=0, column=0, sticky="e")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # for i in range(4):
    #     tab_seccion.rowconfigure(i, weight=1)
    #     tab_seccion.columnconfigure(i, weight=1)

    rectangular_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Rectangular",
                                        variable=tipo_seccion, value="Rectangular", command=actualizar_gui)
    rectangular_rb.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    rectangular_hueca_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Rectangular Hueca",
                                              variable=tipo_seccion, value="Rectangular Hueca", command=actualizar_gui)
    rectangular_hueca_rb.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    seccion_I_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Sección en I",
                                      variable=tipo_seccion, value="Sección en I", command=actualizar_gui)
    seccion_I_rb.grid(row=1, column=2, sticky="w", padx=10, pady=5)

    seccion_T_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Sección en T",
                                      variable=tipo_seccion, value="Sección en T", command=actualizar_gui)
    seccion_T_rb.grid(row=1, column=3, sticky="w", padx=10, pady=5)

    seccion_L_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Sección en L",
                                      variable=tipo_seccion, value="Sección en L", command=actualizar_gui)
    seccion_L_rb.grid(row=1, column=4, sticky="w", padx=10, pady=5)

    seccion_C_rb = ctk.CTkRadioButton(tipo_seccion_frame, text="Sección en C",
                                      variable=tipo_seccion, value="Sección en C", command=actualizar_gui)
    seccion_C_rb.grid(row=1, column=5, sticky="w", padx=10, pady=5)
    
    forma_seccion_frame = ctk.CTkFrame(tab_seccion)
    forma_seccion_frame.grid(row=1, column=0, columnspan=12, sticky="nsew", padx=10, pady=5)

    forma_seccion_label = ctk.CTkLabel(forma_seccion_frame, text="Tipo de sección:")
    forma_seccion_label.grid(row=0, column=0, sticky="e")

    # for i in range(4):
    #     forma_seccion_frame.rowconfigure(i, weight=1)
    #     forma_seccion_frame.columnconfigure(i, weight=1)

    recta_rb = ctk.CTkRadioButton(forma_seccion_frame, text="Constante",
                                  variable=forma_seccion, value="Recta", command=actualizar_gui)
    recta_rb.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    variable_rb = ctk.CTkRadioButton(forma_seccion_frame, text="Variable",
                                     variable=forma_seccion, value="Variable", command=actualizar_gui)
    variable_rb.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    a0_label = ctk.CTkLabel(forma_seccion_frame, text="a0 (mm):")
    a0_label.grid(row=3, column=0, sticky="e")
    a0_entry = ctk.CTkEntry(forma_seccion_frame)
    a0_entry.grid(row=3, column=1, sticky="ew")

    b0_label = ctk.CTkLabel(forma_seccion_frame, text="b0 (mm):")
    b0_label.grid(row=4, column=0, sticky="e")
    b0_entry = ctk.CTkEntry(forma_seccion_frame)
    b0_entry.grid(row=4, column=1, sticky="ew")

    L_label = ctk.CTkLabel(forma_seccion_frame, text="L (mm):")
    L_label.grid(row=5, column=0, sticky="e")
    L_entry = ctk.CTkEntry(forma_seccion_frame)
    L_entry.grid(row=5, column=1, sticky="ew")

    t_label = ctk.CTkLabel(forma_seccion_frame, text="t (mm):")
    t_label.grid(row=6, column=0, sticky="e")
    t_entry = ctk.CTkEntry(forma_seccion_frame)
    t_entry.grid(row=6, column=1, sticky="ew")

    a1_label = ctk.CTkLabel(forma_seccion_frame, text="a1 (mm):")
    a1_label.grid(row=7, column=0, sticky="e")
    a1_entry = ctk.CTkEntry(forma_seccion_frame)
    a1_entry.grid(row=7, column=1, sticky="ew")

    b1_label = ctk.CTkLabel(forma_seccion_frame, text="b1 (mm):")
    b1_label.grid(row=8, column=0, sticky="e")
    b1_entry = ctk.CTkEntry(forma_seccion_frame)
    b1_entry.grid(row=8, column=1, sticky="ew")

    images_frame = ctk.CTkFrame(tab_seccion)
    images_frame.grid(row=2, column=0, columnspan=12, sticky="nsew", padx=10, pady=5)

    # for i in range(4):
    #     images_frame.rowconfigure(i, weight=1)
    #     images_frame.columnconfigure(i, weight=1)

    save_button = ctk.CTkButton(root, text="Guardar Datos", command=guardar_datos_callback)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

    browse_button = ctk.CTkButton(root, text="Browse...", command=browse_folder)
    browse_button.grid(row=6, column=0, columnspan=2, pady=10)  

    mallado_label = ctk.CTkLabel(tab_mallado_cargas, text="Mallado (mm):")
    mallado_label.grid(column=0, row=0, padx=10, pady=5, sticky="W")
    mallado_entry = ctk.CTkEntry(tab_mallado_cargas)
    mallado_entry.grid(column=1, row=0, padx=10, pady=5, sticky="EW")

    carga_label = ctk.CTkLabel(tab_mallado_cargas, text="Carga (MPa):")
    carga_label.grid(column=0, row=1, padx=10, pady=5, sticky="W")
    carga_entry = ctk.CTkEntry(tab_mallado_cargas)
    carga_entry.grid(column=1, row=1, padx=10, pady=5, sticky="EW")

    ctk.CTkLabel(tab_mallado_cargas, text="Dirección de Carga:").grid(column=0, row=2, padx=10, pady=5, sticky="W")
    direccion_carga = ctk.CTkComboBox(tab_mallado_cargas, values=["Ascendente", "Descendente"], state="readonly", command=actualizar_gui)
    direccion_carga.grid(column=1, row=2, padx=10, pady=5, sticky="EW")

    ctk.CTkLabel(tab_mallado_cargas, text="Material:").grid(column=0, row=3, padx=10, pady=5, sticky="W")
    material = ctk.CTkComboBox(tab_mallado_cargas, values=["Aluminio", "Acero", "Cobre", "Personalizado"], state="readonly", command=actualizar_gui)
    material.grid(column=1, row=3, padx=10, pady=5, sticky="EW")

    modulo_elastico_label = ctk.CTkLabel(tab_mallado_cargas, text="Módulo Elástico (GPa):")
    modulo_elastico_entry = ctk.CTkEntry(tab_mallado_cargas)
    poisson_label = ctk.CTkLabel(tab_mallado_cargas, text="Coeficiente de Poisson:")
    poisson_entry = ctk.CTkEntry(tab_mallado_cargas)
    densidad_label = ctk.CTkLabel(tab_mallado_cargas, text="Densidad (kg/m^3):")
    densidad_entry = ctk.CTkEntry(tab_mallado_cargas)

    ctk.CTkLabel(tab_mallado_cargas, text="Tipo de Elemento:").grid(column=0, row=4, padx=10, pady=5, sticky="W")
    tipo_elemento = ctk.CTkComboBox(tab_mallado_cargas, values=["1D", "2D", "3D"], state="readonly")
    tipo_elemento.grid(column=1, row=4, padx=10, pady=5, sticky="EW")


    analisis_frame = ctk.CTkFrame(tab_mallado_cargas)
    analisis_frame.grid(row=6, column=0, columnspan=12, sticky="nsew", padx=10, pady=5)

    analisis_label = ctk.CTkLabel(analisis_frame, text="Herramienta de análisis:")
    analisis_label.grid(row=1, column=0, sticky="e")

    nastran_rb = ctk.CTkRadioButton(analisis_frame, text="Nastran",
                                  variable=tipo_analisis, value="Nastran", command=actualizar_gui2)
    nastran_rb.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    apex_rb = ctk.CTkRadioButton(analisis_frame, text="Apex",
                                     variable=tipo_analisis, value="Apex", command=actualizar_gui2)
    apex_rb.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    browse_analisis_button = ctk.CTkButton(analisis_frame, text="Guardar resultados análisis...", command=browse_folder2)
    browse_analisis_button.grid(row=3, column=0, columnspan=2, pady=10) 

    root.mainloop()


def obtener_valores():
    valores = {
        "a0 (mm)": a0_entry.get(),
        "b0 (mm)": b0_entry.get(),
        "L (mm)": L_entry.get(),
        "t (mm)": t_entry.get() if tipo_seccion.get() != "Rectangular" else "0",
        "a1 (mm)": a1_entry.get() if forma_seccion.get() == "Variable" else "0",
        "b1 (mm)": b1_entry.get() if forma_seccion.get() == "Variable" else "0",
        "Mallado (mm)": mallado_entry.get(),
        "Carga (MPa)": carga_entry.get(),
        "Tipo de Sección": tipo_seccion.get(),
        "Forma de Sección": forma_seccion.get(),
        "Dirección Carga": direccion_carga.get(),
        "Material": material.get(),
        "Tipo de Elemento": tipo_elemento.get(),
        "Análisis en": tipo_analisis.get(),
        "Path análisis": analisis_path if tipo_analisis.get() == "Nastran" else "0",
        "Módulo elástico (GPa)": modulo_elastico_entry.get() if material.get() == "Personalizado" else "0",
        "Coeficiente de Poisson": poisson_entry.get() if material.get() == "Personalizado" else "0",
        "Densidad (kg/m^3)": densidad_entry.get() if material.get() == "Personalizado" else "0"
    }

    valores["a0 (mm)"] = a0_entry.get() if a0_entry.get() else valores["a0 (mm)"]
    valores["b0 (mm)"] = b0_entry.get() if b0_entry.get() else valores["b0 (mm)"]
    valores["L (mm)"] = L_entry.get() if L_entry.get() else valores["L (mm)"]
    valores["t (mm)"] = t_entry.get() if tipo_seccion.get() != "Rectangular" else valores["t (mm)"]
    valores["a1 (mm)"] = a1_entry.get() if forma_seccion.get() == "Variable" else valores["a0 (mm)"]
    valores["b1 (mm)"] = b1_entry.get() if forma_seccion.get() == "Variable" else valores["b0 (mm)"]
    valores["Mallado (mm)"] = mallado_entry.get() if mallado_entry.get() else valores["Mallado (mm)"]
    valores["Carga (MPa)"] = carga_entry.get() if carga_entry.get() else valores["Carga (MPa)"]
    
    return valores

def actualizar_gui(event=None):

    if tipo_seccion.get() != "Rectangular":
        t_label.grid(row=6, column=0, sticky="e")
        t_entry.grid(row=6, column=1, sticky="ew")
    else:
        t_label.grid_remove()
        t_entry.grid_remove()
        
    if forma_seccion.get() == "Variable":
        a1_label.grid(row=7, column=0, sticky="e")
        a1_entry.grid(row=7, column=1, sticky="ew")
        b1_label.grid(row=8, column=0, sticky="e")
        b1_entry.grid(row=8, column=1, sticky="ew")
    else:
        a1_label.grid_remove()
        a1_entry.grid_remove()
        b1_label.grid_remove()
        b1_entry.grid_remove()

    seccion = tipo_seccion.get()

    if seccion == "Rectangular":
        tipo_elemento.configure(values=["1D", "3D"])
    else:
        tipo_elemento.configure(values=["1D", "2D", "3D"])

    if seccion == "Sección en I":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Seccion_en_I.png"), images_frame, 400, 200)
    elif seccion == "Rectangular Hueca":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Rectangular_Hueca.png"), images_frame, 400, 200)
    elif seccion == "Sección en T":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Seccion_en_T.png"), images_frame, 400, 200)
    elif seccion == "Sección en L":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Seccion_en_L.png"), images_frame, 400, 200)
    elif seccion == "Sección en C":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Seccion_en_C.png"), images_frame, 400, 200)
    elif seccion == "Rectangular":
        mostrar_imagen(os.path.join(os.path.dirname(__file__), "data", "images", "Rectangular.png"), images_frame, 400, 200)

    if forma_seccion.get() == "Recta":
        mostrar_imagen2(os.path.join(os.path.dirname(__file__), "data", "images", "recta.png"), images_frame, 400, 200)
    elif forma_seccion.get() == "Variable":
        mostrar_imagen2(os.path.join(os.path.dirname(__file__), "data", "images", "variable.png"), images_frame, 400, 200)
    
    mostrar_imagen_en_cargas()

    if material.get() == "Personalizado":
        modulo_elastico_label.grid(column=2, row=1, padx=10, pady=5, sticky="W")
        modulo_elastico_entry.grid(column=3, row=1, padx=10, pady=5, sticky="EW")
        poisson_label.grid(column=2, row=2, padx=10, pady=5, sticky="W")
        poisson_entry.grid(column=3, row=2, padx=10, pady=5, sticky="EW")
        densidad_label.grid(column=2, row=3, padx=10, pady=5, sticky="W")
        densidad_entry.grid(column=3, row=3, padx=10, pady=5, sticky="EW")
    else:
        modulo_elastico_label.grid_remove()
        modulo_elastico_entry.grid_remove()
        poisson_label.grid_remove()
        poisson_entry.grid_remove()
        densidad_label.grid_remove()
        densidad_entry.grid_remove()

def actualizar_gui2(event=None):
    if tipo_analisis.get() == "Nastran":
        browse_analisis_button.grid(row=3, column=0, columnspan=2, pady=10)
    else:
        browse_analisis_button.grid_remove()
        

def mostrar_imagen(ruta_imagen, frame_destino, ancho_deseado, alto_deseado):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((ancho_deseado, alto_deseado), Image.ANTIALIAS)
    foto = ImageTk.PhotoImage(imagen)

    label_imagen = ctk.CTkLabel(frame_destino, image=foto, text="")
    label_imagen.image = foto
    label_imagen.grid(row=1, column=0, padx=10, pady=10)

def mostrar_imagen2(ruta_imagen, frame_destino, ancho_deseado, alto_deseado):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((ancho_deseado, alto_deseado), Image.ANTIALIAS)
    foto = ImageTk.PhotoImage(imagen)

    label_imagen = ctk.CTkLabel(frame_destino, image=foto, text="")
    label_imagen.image = foto
    label_imagen.grid(row=1, column=1, padx=10, pady=10)

def mostrar_imagen3(ruta_imagen, frame_destino, ancho_deseado, alto_deseado):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((ancho_deseado, alto_deseado), Image.ANTIALIAS)
    foto = ImageTk.PhotoImage(imagen)

    label_imagen = ctk.CTkLabel(frame_destino, image=foto, text="")
    label_imagen.image = foto
    label_imagen.grid(row=0, column=0, padx=10, pady=10)

def mostrar_imagen_en_cargas():
    if forma_seccion.get() == "Recta":
        if direccion_carga.get() == "Ascendente":
            ruta_imagen = os.path.join(os.path.dirname(__file__), "data", "images", "recta_ascendente.png")
        else:
            ruta_imagen = os.path.join(os.path.dirname(__file__), "data", "images", "recta_descendente_.png")
    else:  # Sección variable
        if direccion_carga.get() == "Ascendente":
            ruta_imagen = os.path.join(os.path.dirname(__file__), "data", "images", "variable_ascendente.png")
        else:
            ruta_imagen = os.path.join(os.path.dirname(__file__), "data", "images", "variable_descendente_.png")

    mostrar_imagen3(ruta_imagen, analisis_frame, 400, 200)

def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("Carpeta seleccionada:", folder_path)
    with open(os.path.join(os.path.dirname(__file__), 'folder_path.txt'), 'w') as archivo:
        archivo.write(str(folder_path))
def browse_folder2():
    global analisis_path
    analisis_path = filedialog.askdirectory()
    if analisis_path:
        print("Carpeta seleccionada para el análisis:", analisis_path)