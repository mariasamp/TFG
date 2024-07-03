import os
import shutil
import win32com.client

def leer_medidas(archivo):
    medidas = {}
    with open(archivo, 'r') as f:
        lineas = f.readlines()[:-10]
        for linea in lineas:
            partes = linea.split('\t')
            medidas[partes[0].strip()] = float(partes[1].strip())
    return medidas

def formacion_geometria(medidas, tipo_seccion, forma_seccion):
    CATIA = win32com.client.Dispatch('CATIA.Application')
    CATIA.Visible = True
    documento = CATIA.Documents.Add('Part')
    part = documento.Part
    parameters = part.Parameters
    
    for nombre_parametro, valor in medidas.items():
        try:
            parametro = parameters.Item(nombre_parametro)
        except:
            parametro = parameters.CreateDimension(nombre_parametro, "LENGTH", valor)
            parametro.Rename(nombre_parametro)
        parametro.Value = valor

    part.Update()

    bodies = part.Bodies
    main_body = bodies.Item("PartBody")
    
    a0 = medidas['a0 (mm)']
    b0 = medidas['b0 (mm)']
    a1 = medidas['a1 (mm)']
    b1 = medidas['b1 (mm)']
    L = medidas['L (mm)']
    t = medidas['t (mm)']

    # Sketch 1 en el plano YZ
    planeYZ = part.OriginElements.PlaneYZ
    sketch1 = main_body.Sketches.Add(planeYZ)
    sketch1.name = "Sketch.1"
    
    sketch1.OpenEdition()
    factory2D_1 = sketch1.Factory2D
    if tipo_seccion == "Sección en I":
        crear_seccion_I(factory2D_1, a0, b0+t, t)
    elif tipo_seccion == "Sección en T":
        crear_seccion_T(factory2D_1, a0, b0+t/2, t)
    elif tipo_seccion == "Sección en L":
        crear_seccion_L(factory2D_1, a0+t/2, b0+t/2, t)
    elif tipo_seccion == "Sección en C":
        crear_seccion_C(factory2D_1, a0+t/2, b0+t, t)
    else:
        crear_rectangulo(factory2D_1, a0, b0)

    sketch1.CloseEdition()
    part.Update()
    

    # Plano desplazado
    hybridShapeFactory = part.HybridShapeFactory
    referencePlaneYZ = part.CreateReferenceFromObject(planeYZ)
    L = medidas['L (mm)']
    hybridShapePlaneOffset = hybridShapeFactory.AddNewPlaneOffset(referencePlaneYZ, L, False)
    main_body.InsertHybridShape(hybridShapePlaneOffset)
    part.Update()
    
    # Sketch 2 en el plano desplazado
    referenceToHybridShapePlaneOffset = part.CreateReferenceFromObject(hybridShapePlaneOffset)
    sketch2 = main_body.Sketches.Add(referenceToHybridShapePlaneOffset)
    sketch2.name = "Sketch.2"
    sketch2.OpenEdition()
    factory2D_2 = sketch2.Factory2D

    if tipo_seccion == "Sección en I":
        crear_seccion_I(factory2D_2, a1, b1+t, t)
    elif tipo_seccion == "Sección en T":
        crear_seccion_T(factory2D_2, a1, b1+t/2, t)
    elif tipo_seccion == "Sección en L":
        crear_seccion_L(factory2D_2, a1+t/2, b1+t/2, t)
    elif tipo_seccion == "Sección en C":
        crear_seccion_C(factory2D_2, a1+t/2, b1+t, t)
    else:
        crear_rectangulo(factory2D_2, a1, b1)

    sketch2.CloseEdition()
    part.Update()

    # MULTISECTION
    shapeFactory1 = part.ShapeFactory

    # Crear el objeto loft
    loft1 = shapeFactory1.AddNewLoft()
    hybridShapeLoft1 = loft1.HybridShape
    hybridShapeLoft1.SectionCoupling = 3
    hybridShapeLoft1.Relimitation = 1
    hybridShapeLoft1.CanonicalDetection = 2

    # Asignar los sketches
    bodies1 = part.Bodies
    body1 = bodies1.Item("PartBody")
    sketches1 = body1.Sketches

    sketch1 = sketches1.Item("Sketch.1")
    reference1 = part.CreateReferenceFromObject(sketch1)

    if tipo_seccion == "Sección en I":
            reference2 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.1;12);None:();Cf11:());Face:(Brp:(Sketch.1;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch1
    )
    elif tipo_seccion == "Sección en L":
            reference2 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.1;6);None:();Cf11:());Face:(Brp:(Sketch.1;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch1
    )
    elif tipo_seccion == "Sección en T":
            reference2 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.1;8);None:();Cf11:());Face:(Brp:(Sketch.1;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch1
    )
    elif tipo_seccion == "Sección en C":
            reference2 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.1;8);None:();Cf11:());Face:(Brp:(Sketch.1;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch1
    )
    else:     
        reference2 = part.CreateReferenceFromBRepName(
            "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.1;4);None:();Cf11:());Face:(Brp:(Sketch.1;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", 
            sketch1
        )
    hybridShapeLoft1.AddSectionToLoft(reference1, 1, reference2)

    sketch2 = sketches1.Item("Sketch.2")
    reference3 = part.CreateReferenceFromObject(sketch2)

    if tipo_seccion == "Sección en I":
        reference4 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.2;12);None:();Cf11:());Face:(Brp:(Sketch.2;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch2 
    )
    elif tipo_seccion == "Sección en L":
        reference4 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.2;6);None:();Cf11:());Face:(Brp:(Sketch.2;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch2 
    )
    elif tipo_seccion == "Sección en T":
        reference4 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.2;8);None:();Cf11:());Face:(Brp:(Sketch.2;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch2 
    )
    elif tipo_seccion == "Sección en C":
        reference4 = part.CreateReferenceFromBRepName(
        "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.2;8);None:();Cf11:());Face:(Brp:(Sketch.2;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch2
    )
    else:
        reference4 = part.CreateReferenceFromBRepName(
            "WireFVertex:(Vertex:(Neighbours:(Face:(Brp:(Sketch.2;4);None:();Cf11:());Face:(Brp:(Sketch.2;1);None:();Cf11:()));Cf11:());WithPermanentBody;WithoutBuildError;WithInitialFeatureSupport;MFBRepVersion_CXR15)", sketch2
    )
    hybridShapeLoft1.AddSectionToLoft(reference3, 1, reference4)

    part.InWorkObject = hybridShapeLoft1
    part.Update()

    # SHELL PARA EL CASO DE RECTANGULAR HUECA
    if tipo_seccion == "Rectangular Hueca":
        shapeFactory1 = part.ShapeFactory

        reference1 = part.CreateReferenceFromName("")
        shell1 = shapeFactory1.AddNewShell(reference1, 1.000000, 0.000000)

        relations1 = part.Relations

        param_t = part.Parameters.Item("t (mm)")

        length1 = shell1.InternalThickness
        formula1 = relations1.CreateFormula("Formula.1", "", length1, "`" + param_t.Name + "` / 2")
        formula1.Rename("Formula.1")

        length2 = shell1.ExternalThickness
        formula2 = relations1.CreateFormula("Formula.2", "", length2, "`" + param_t.Name + "` / 2")
        formula2.Rename("Formula.2")

        bodies1 = part.Bodies
        body1 = bodies1.Item("PartBody")
        hybridShapes1 = body1.HybridShapes
        hybridShapeLoft1 = hybridShapes1.Item("Multi-sections Solid.1")

        reference2 = part.CreateReferenceFromBRepName(
            "RSur:(Face:(Brp:(GSMLoft.1;(Brp:(Sketch.2;1);Brp:(Sketch.2;2);Brp:(Sketch.2;3);Brp:(Sketch.2;4)));None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", 
            hybridShapeLoft1
        )
        shell1.AddFaceToRemove(reference2)

        reference3 = part.CreateReferenceFromBRepName(
            "RSur:(Face:(Brp:(GSMLoft.1;(Brp:(Sketch.1;1);Brp:(Sketch.1;2);Brp:(Sketch.1;3);Brp:(Sketch.1;4)));None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", 
            hybridShapeLoft1
        )
        shell1.AddFaceToRemove(reference3)
        part.Update()

    # OCULTAR SKETCHES
    partDocument1 = CATIA.ActiveDocument

    # Sketch 1
    selection1 = partDocument1.Selection
    selection1.Add(sketch1)
    visPropertySet1 = selection1.VisProperties.Parent
    visPropertySet1.SetShow(1)
    selection1.Clear()

    # Sketch 2
    selection2 = partDocument1.Selection
    selection2.Add(sketch2)
    visPropertySet2 = selection2.VisProperties.Parent
    visPropertySet2.SetShow(1)
    selection2.Clear()

    part.Update()

def crear_rectangulo(factory2D, x, y):

    punto1 = factory2D.CreatePoint(-x/2, -y/2)
    punto2 = factory2D.CreatePoint(x/2, -y/2)
    punto3 = factory2D.CreatePoint(x/2, y/2)
    punto4 = factory2D.CreatePoint(-x/2, y/2)

    linea1 = factory2D.CreateLine(-x/2, -y/2, x/2, -y/2)
    linea2 = factory2D.CreateLine(x/2, -y/2, x/2, y/2)
    linea3 = factory2D.CreateLine(x/2, y/2, -x/2, y/2)
    linea4 = factory2D.CreateLine(-x/2, y/2, -x/2, -y/2)

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto3
    linea3.StartPoint = punto3
    linea3.EndPoint = punto4
    linea4.StartPoint = punto4
    linea4.EndPoint = punto1

def crear_seccion_I(factory2D, x, y, t):

    punto1 = factory2D.CreatePoint(-x/2, -y/2)
    punto2 = factory2D.CreatePoint(x/2, -y/2)
    punto3 = factory2D.CreatePoint(x/2, y/2)
    punto4 = factory2D.CreatePoint(-x/2, y/2)
    punto5 = factory2D.CreatePoint(-t/2, -y/2+t)
    punto6 = factory2D.CreatePoint(t/2, -y/2+t)
    punto7 = factory2D.CreatePoint(t/2, y/2-t)
    punto8 = factory2D.CreatePoint(-t/2, y/2-t)
    punto9 = factory2D.CreatePoint(-x/2, -y/2+t)
    punto10 = factory2D.CreatePoint(x/2, -y/2+t)
    punto11 = factory2D.CreatePoint(x/2, y/2-t)
    punto12 = factory2D.CreatePoint(-x/2, y/2-t)

    linea1 = factory2D.CreateLine(-x/2, -y/2, x/2, -y/2)
    linea2 = factory2D.CreateLine(x/2, -y/2, x/2, -y/2+t)
    linea3 = factory2D.CreateLine(x/2, -y/2+t, t/2, -y/2+t)
    linea4 = factory2D.CreateLine(t/2, -y/2+t, t/2, y/2-t)
    linea5 = factory2D.CreateLine(t/2, y/2-t,x/2, y/2-t)
    linea6 = factory2D.CreateLine(x/2, y/2-t,x/2, y/2)
    linea7 = factory2D.CreateLine(x/2, y/2,-x/2, y/2)
    linea8 = factory2D.CreateLine(-x/2, y/2,-x/2, y/2-t)
    linea9 = factory2D.CreateLine(-x/2, y/2-t,-t/2, y/2-t)
    linea10 = factory2D.CreateLine(-t/2, y/2-t,-t/2, -y/2+t)
    linea11 = factory2D.CreateLine(-t/2, -y/2+t,-x/2, -y/2+t)
    linea12 = factory2D.CreateLine(-x/2, -y/2+t,-x/2, -y/2)

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto10
    linea3.StartPoint = punto10
    linea3.EndPoint = punto6
    linea4.StartPoint = punto6
    linea4.EndPoint = punto7
    linea5.StartPoint = punto7
    linea5.EndPoint = punto11
    linea6.StartPoint = punto11
    linea6.EndPoint = punto3
    linea7.StartPoint = punto3
    linea7.EndPoint = punto4
    linea8.StartPoint = punto4
    linea8.EndPoint = punto12
    linea9.StartPoint = punto12
    linea9.EndPoint = punto8
    linea10.StartPoint = punto8
    linea10.EndPoint = punto5
    linea11.StartPoint = punto5
    linea11.EndPoint = punto9
    linea12.StartPoint = punto9
    linea12.EndPoint = punto1

def crear_seccion_T(factory2D, x, y, t):

    punto1 = factory2D.CreatePoint(-t/2, -y/2)
    punto2 = factory2D.CreatePoint(t/2, -y/2)
    punto3 = factory2D.CreatePoint(t/2, y/2-t)
    punto4 = factory2D.CreatePoint(x/2, y/2-t)
    punto5 = factory2D.CreatePoint(x/2, y/2)
    punto6 = factory2D.CreatePoint(-x/2, y/2)
    punto7 = factory2D.CreatePoint(-x/2, y/2-t)
    punto8 = factory2D.CreatePoint(-t/2, y/2-t)

    linea1 = factory2D.CreateLine(-t/2, -y/2, t/2, -y/2)
    linea2 = factory2D.CreateLine(t/2, -y/2, t/2, y/2-t)
    linea3 = factory2D.CreateLine(t/2, y/2-t, x/2, y/2-t)
    linea4 = factory2D.CreateLine(x/2, y/2-t, x/2, y/2)
    linea5 = factory2D.CreateLine(x/2, y/2, -x/2, y/2)
    linea6 = factory2D.CreateLine(-x/2, y/2, -x/2, y/2-t)
    linea7 = factory2D.CreateLine(-x/2, y/2-t,-t/2, y/2-t)
    linea8 = factory2D.CreateLine(-t/2, y/2-t,-t/2, -y/2)

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto3
    linea3.StartPoint = punto3
    linea3.EndPoint = punto4
    linea4.StartPoint = punto4
    linea4.EndPoint = punto5
    linea5.StartPoint = punto5
    linea5.EndPoint = punto6
    linea6.StartPoint = punto6
    linea6.EndPoint = punto7
    linea7.StartPoint = punto7
    linea7.EndPoint = punto8
    linea8.StartPoint = punto8
    linea8.EndPoint = punto1

def crear_seccion_L(factory2D, x, y, t):

    punto1 = factory2D.CreatePoint(-x/2, -y/2)
    punto2 = factory2D.CreatePoint(x/2, -y/2)
    punto3 = factory2D.CreatePoint(x/2, -y/2+t)
    punto4 = factory2D.CreatePoint(-x/2+t, -y/2+t)
    punto5 = factory2D.CreatePoint(-x/2+t, y/2)
    punto6 = factory2D.CreatePoint(-x/2, y/2)

    linea1 = factory2D.CreateLine(-x/2, -y/2, x/2, -y/2)
    linea2 = factory2D.CreateLine(x/2, -y/2, x/2, -y/2+t)
    linea3 = factory2D.CreateLine(x/2, -y/2+t, -x/2+t, -y/2+t)
    linea4 = factory2D.CreateLine(-x/2+t, -y/2+t, -x/2+t, y/2)
    linea5 = factory2D.CreateLine(-x/2+t, y/2, -x/2, y/2)
    linea6 = factory2D.CreateLine(-x/2, y/2, -x/2, -y/2)

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto3
    linea3.StartPoint = punto3
    linea3.EndPoint = punto4
    linea4.StartPoint = punto4
    linea4.EndPoint = punto5
    linea5.StartPoint = punto5
    linea5.EndPoint = punto6
    linea6.StartPoint = punto6
    linea6.EndPoint = punto1

def crear_seccion_C(factory2D, x, y, t):

    punto1 = factory2D.CreatePoint(-x/2, -y/2)
    punto2 = factory2D.CreatePoint(x/2, -y/2)
    punto3 = factory2D.CreatePoint(x/2, -y/2+t)
    punto4 = factory2D.CreatePoint(-x/2+t, -y/2+t)
    punto5 = factory2D.CreatePoint(-x/2+t, y/2-t)
    punto6 = factory2D.CreatePoint(x/2, y/2-t)
    punto7 = factory2D.CreatePoint(x/2, y/2)
    punto8 = factory2D.CreatePoint(-x/2, y/2)

    linea1 = factory2D.CreateLine(-x/2, -y/2, x/2, -y/2)
    linea2 = factory2D.CreateLine(x/2, -y/2, x/2, -y/2+t)
    linea3 = factory2D.CreateLine(x/2, -y/2+t, -x/2+t, -y/2+t)
    linea4 = factory2D.CreateLine(-x/2+t, -y/2+t, -x/2+t, y/2-t)
    linea5 = factory2D.CreateLine(-x/2+t, y/2-t, x/2, y/2-t)
    linea6 = factory2D.CreateLine(x/2, y/2-t, x/2, y/2)
    linea7 = factory2D.CreateLine(x/2, y/2,-x/2, y/2)
    linea8 = factory2D.CreateLine(-x/2, y/2,-x/2, -y/2)

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto3
    linea3.StartPoint = punto3
    linea3.EndPoint = punto4
    linea4.StartPoint = punto4
    linea4.EndPoint = punto5
    linea5.StartPoint = punto5
    linea5.EndPoint = punto6
    linea6.StartPoint = punto6
    linea6.EndPoint = punto7
    linea7.StartPoint = punto7
    linea7.EndPoint = punto8
    linea8.StartPoint = punto8
    linea8.EndPoint = punto1

def guardar_y_sobrescribir_documento(ruta_destino, ruta_temporal):

    CATIA = win32com.client.Dispatch("CATIA.Application")
    documento_activo = CATIA.ActiveDocument

    producto_activo = documento_activo.GetItem("Part1")

    producto_activo.PartNumber = "Viga"

    ruta_temporal = ruta_destino + ".temp"
    documento_activo.SaveAs(ruta_temporal)

    if os.path.exists(ruta_destino):
        os.remove(ruta_destino)
    shutil.move(ruta_temporal, ruta_destino)

    documento_activo.Close()