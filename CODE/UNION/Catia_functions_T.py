import win32com.client as win32
import math
import os
import shutil

def iniciar_catia(Radio, Radio_Cabeza, Longitud_Cabeza, Longitud_Tuerca, Espesor_Pieza1, Espesor_Pieza2, Radio_Pieza1, Radio_Pieza2, Radio_int_arandela, Radio_ext_arandela, Espesor_arandela):
    CATIA = win32.Dispatch('CATIA.Application')
    try:
        documento_anterior = CATIA.ActiveDocument
        documento_anterior.Close()
    except:
        pass
    CATIA.Visible = True
    documents1 = CATIA.Documents
    productDocument1 = documents1.Add("Product")
    product1 = productDocument1.Product
    products1 = product1.Products
    part1 = products1.AddNewComponent("Part", "")
    tornillo(part1, documents1, Radio, Radio_Cabeza, Longitud_Cabeza, Longitud_Tuerca, Espesor_Pieza1, Espesor_Pieza2, Espesor_arandela)
    part2 = products1.AddNewComponent("Part", "")
    pieza(part2, documents1,"Part2.CATPart", Radio*1.01, Radio_Pieza1, Radio_Cabeza, Longitud_Cabeza, Espesor_Pieza1)
    part3 = products1.AddNewComponent("Part", "")
    pieza(part3, documents1, "Part3.CATPart", Radio*1.01, Radio_Pieza2, Radio_Cabeza, Longitud_Cabeza, -Espesor_Pieza2)
    part4 = products1.AddNewComponent("Part", "")
    arandela(part4, documents1, "Part4.CATPart", Radio_int_arandela, Radio_ext_arandela, Espesor_arandela, Espesor_Pieza1)
    part5 = products1.AddNewComponent("Part", "")
    arandela(part5, documents1, "Part5.CATPart", Radio_int_arandela, Radio_ext_arandela, -Espesor_arandela, -Espesor_Pieza2)
    
    # Asignar nombres a las partes
    part1.PartNumber = "Bolt"
    product2 = products1.Item("Part1.1")
    product2.Name = "Bolt"
    part2.PartNumber = "Pieza1"
    product3 = products1.Item("Part2.1")
    product3.Name = "Pieza1"
    part3.PartNumber = "Pieza2"
    product4 = products1.Item("Part3.1")
    product4.Name = "Pieza2"
    product5 = products1.Item("Part4.1")
    product5.Name = "Arandela1"
    product6 = products1.Item("Part5.1")
    product6.Name = "Arandela2"
    documento_activo = CATIA.ActiveDocument
    producto_activo = documento_activo.GetItem("Product1")
    producto_activo.PartNumber = "BoltedJoint"


def tornillo(part, document, Radio, Radio_Cabeza, Longitud_Cabeza, Longitud_Tuerca, Espesor_Pieza1, Espesor_Pieza2, Espesor_arandela):
    partDocument1 = document.Item("Part1.CATPart")
    part = partDocument1.Part
    Longitud_Sup = Espesor_Pieza1 + Espesor_arandela + Longitud_Cabeza
    Longitud_Inf = Espesor_Pieza2 + Espesor_arandela + Longitud_Tuerca
    # Sketch 1 con cuerpo del tornillo en Body 1
    bodies1 = part.Bodies
    body1 = bodies1.Item("PartBody")
    planeXY = part.OriginElements.PlaneXY
    sketch1 = body1.Sketches.Add(planeXY)
    part.InWorkObject = sketch1
    # PARA MALLADO CON CUADRADO CENTRAL
    crear_arco(part, sketch1, -Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), Radio)
    crear_lineas(sketch1, -Radio, -Radio, Radio, -Radio)
    crear_pad(part, sketch1, Longitud_Sup, Longitud_Inf)
    body2 = bodies1.Add()
    planeXY = part.OriginElements.PlaneXY
    sketch2 = body2.Sketches.Add(planeXY)
    part.InWorkObject = sketch2
    crear_arco(part, sketch2, Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), Radio)
    crear_lineas(sketch2, Radio, -Radio, Radio, Radio)
    crear_pad(part, sketch2, Longitud_Sup, Longitud_Inf)
    body3 = bodies1.Add()
    planeXY = part.OriginElements.PlaneXY
    sketch3 = body3.Sketches.Add(planeXY)
    part.InWorkObject = sketch3
    crear_arco(part, sketch3, Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), Radio)
    crear_lineas(sketch3, Radio, Radio, -Radio, Radio)
    crear_pad(part, sketch3, Longitud_Sup, Longitud_Inf)
    body4 = bodies1.Add()
    planeXY = part.OriginElements.PlaneXY
    sketch4 = body4.Sketches.Add(planeXY)
    part.InWorkObject = sketch4
    crear_arco(part, sketch4, -Radio*math.cos(math.pi/4), Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), -Radio*math.cos(math.pi/4), Radio)
    crear_lineas(sketch4, -Radio, Radio, -Radio, -Radio)
    crear_pad(part, sketch4, Longitud_Sup, Longitud_Inf)
    body5 = bodies1.Add()
    planeXY = part.OriginElements.PlaneXY
    sketch5 = body5.Sketches.Add(planeXY)
    part.InWorkObject = sketch5
    crear_rectangulo(sketch5, Radio, Radio)
    crear_pad(part, sketch5, Longitud_Sup, Longitud_Inf)

    # PARA MALLADO TETRA
    # crear_circulo(sketch1, Radio)
    # crear_pad(part, sketch1, Longitud)
    
    # Cabeza de tornillo y de tuerca
    body6 = bodies1.Add()
    hybridShapeFactory = part.HybridShapeFactory
    referencePlaneYZ = part.CreateReferenceFromObject(planeXY)
    hybridShapePlaneOffset = hybridShapeFactory.AddNewPlaneOffset(referencePlaneYZ, Longitud_Sup, False)
    body6.InsertHybridShape(hybridShapePlaneOffset)
    referenceToHybridShapePlaneOffset = part.CreateReferenceFromObject(hybridShapePlaneOffset)
    sketch6 = body6.Sketches.Add(referenceToHybridShapePlaneOffset)
    part.InWorkObject = sketch6
    crear_circulo(sketch6, Radio)
    crear_circulo(sketch6, Radio_Cabeza)
    crear_pad(part, sketch6, 0, Longitud_Cabeza)
    part.Update()

    body7 = bodies1.Add()
    hybridShapeFactory = part.HybridShapeFactory
    referencePlaneYZ = part.CreateReferenceFromObject(planeXY)
    hybridShapePlaneOffset = hybridShapeFactory.AddNewPlaneOffset(referencePlaneYZ, -Longitud_Inf, False)
    body7.InsertHybridShape(hybridShapePlaneOffset)
    referenceToHybridShapePlaneOffset = part.CreateReferenceFromObject(hybridShapePlaneOffset)
    sketch7 = body7.Sketches.Add(referenceToHybridShapePlaneOffset)
    part.InWorkObject = sketch7
    crear_circulo(sketch7, Radio)
    crear_circulo(sketch7, Radio_Cabeza)
    crear_pad(part, sketch7, Longitud_Tuerca, 0)
    part.Update()


def pieza(part, document, PIEZA, Radio_int, Radio_ext, Radio_Cabeza, Longitud_Cabeza, Espesor_Pieza):
    partDocument1 = document.Item(PIEZA)
    part = partDocument1.Part
    bodies1 = part.Bodies
    body1 = bodies1.Item("PartBody")
    planeXY = part.OriginElements.PlaneXY
    sketch1 = body1.Sketches.Add(planeXY)
    part.InWorkObject = sketch1
    crear_circulo(sketch1, Radio_int)
    crear_circulo(sketch1, Radio_ext)
    crear_pad(part, sketch1, Espesor_Pieza,0)

def arandela(part, document, ARANDELA, Radio_int, Radio_ext, Espesor_arandela, Espesor_Pieza):
    partDocument1 = document.Item(ARANDELA)
    part = partDocument1.Part
    bodies1 = part.Bodies
    body1 = bodies1.Item("PartBody")
    hybridShapeFactory = part.HybridShapeFactory
    planeXY = part.OriginElements.PlaneXY
    referencePlaneYZ = part.CreateReferenceFromObject(planeXY)
    hybridShapePlaneOffset = hybridShapeFactory.AddNewPlaneOffset(referencePlaneYZ, Espesor_Pieza, False)
    body1.InsertHybridShape(hybridShapePlaneOffset)
    referenceToHybridShapePlaneOffset = part.CreateReferenceFromObject(hybridShapePlaneOffset)
    sketch7 = body1.Sketches.Add(referenceToHybridShapePlaneOffset)
    part.InWorkObject = sketch7
    crear_circulo(sketch7, Radio_int)
    crear_circulo(sketch7, Radio_ext)
    crear_pad(part, sketch7, Espesor_arandela, 0)
    part.Update()

def crear_circulo(sketch, Radio):
    factory2D1 = sketch.OpenEdition()
    geometricElements1 = sketch.GeometricElements
    axis2D1 = geometricElements1.Item("AbsoluteAxis")
    line2D1 = axis2D1.GetItem("HDirection")
    line2D1.ReportName = 1
    line2D2 = axis2D1.GetItem("VDirection")
    line2D2.ReportName = 2
    circle2D1 = factory2D1.CreateClosedCircle(0.0, 0.0, Radio)
    point2D1 = axis2D1.GetItem("Origin")
    circle2D1.CenterPoint = point2D1
    circle2D1.ReportName = 3
    sketch.CloseEdition()

def crear_arco(part, sketch, x1, y1, x2, y2, Radio):
    factory2D1 = sketch.OpenEdition()
    geometricElements1 = sketch.GeometricElements
    axis2D1 = geometricElements1.Item("AbsoluteAxis")
    line2D1 = axis2D1.GetItem("HDirection")
    line2D2 = axis2D1.GetItem("VDirection")

    point2D1 = factory2D1.CreatePoint(x1, y1)
    point2D2 = factory2D1.CreatePoint(x2, y2)

    circle2D1 = factory2D1.CreateCircle(0.0, 0.0, Radio, 0, math.pi/2)
    point2D3 = axis2D1.GetItem("Origin")
    circle2D1.CenterPoint = point2D3
    circle2D1.StartPoint = point2D1
    circle2D1.EndPoint = point2D2

    constraints1 = sketch.Constraints
    reference2 = part.CreateReferenceFromObject(point2D2)
    reference3 = part.CreateReferenceFromObject(line2D1)
    constraint1 = constraints1.AddBiEltCst(1, reference2, reference3)
    constraint1.Mode = 0

    reference4 = part.CreateReferenceFromObject(point2D1)
    reference5 = part.CreateReferenceFromObject(line2D2)
    constraint2 = constraints1.AddBiEltCst(1, reference4, reference5)
    constraint2.Mode = 0
    sketch.CloseEdition()

def crear_lineas(sketch, x1, y1, x2, y2):
    factory2D = sketch.OpenEdition()
    punto1 = factory2D.CreatePoint(x1*math.cos(math.pi/4), y1*math.cos(math.pi/4))
    punto2 = factory2D.CreatePoint(x1/2, y1/2)
    punto3 = factory2D.CreatePoint(x2/2, y2/2)
    punto4 = factory2D.CreatePoint(x2*math.cos(math.pi/4), y2*math.cos(math.pi/4))

    linea1 = factory2D.CreateLine(x1*math.cos(math.pi/4), y1*math.cos(math.pi/4), x1/2, y1/2)
    linea2 = factory2D.CreateLine(x1/2, y1/2, x2/2, y2/2)
    linea3 = factory2D.CreateLine(x2/2, y2/2, x2*math.cos(math.pi/4), y2*math.cos(math.pi/4))

    linea1.StartPoint = punto1
    linea1.EndPoint = punto2
    linea2.StartPoint = punto2
    linea2.EndPoint = punto3
    linea3.StartPoint = punto3
    linea3.EndPoint = punto4

def crear_rectangulo(sketch, x, y):
    factory2D = sketch.OpenEdition()
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

def crear_pad(part, sketch, Longitud_Sup, Longitud_Inf):
    shapeFactory1 = part.ShapeFactory
    reference1 = part.CreateReferenceFromObject(sketch)
    pad1 = shapeFactory1.AddNewPadFromRef(reference1, Longitud_Inf)
    # Si se quiere que haya tornillo con dos límites 
    limit1 = pad1.SecondLimit
    length1 = limit1.Dimension
    length1.Value = Longitud_Inf
    limit2 = pad1.FirstLimit
    length2 = limit2.Dimension
    length2.Value = Longitud_Sup
    part.Update()

def guardar_y_sobrescribir_documento(ruta_destino, ruta_temporal):
    CATIA = win32.Dispatch("CATIA.Application")
    CATIA.DisplayFileAlerts = False
    documento_activo = CATIA.ActiveDocument
    producto_activo = documento_activo.GetItem("BoltedJoint")
    producto_activo.PartNumber = "BoltedJoint"
    ruta_temporal = ruta_destino + ".temp"
    documento_activo.SaveAs(ruta_temporal)
    if os.path.exists(ruta_destino):
        os.remove(ruta_destino)
    shutil.move(ruta_temporal, ruta_destino)
    CATIA.DisplayFileAlerts = True