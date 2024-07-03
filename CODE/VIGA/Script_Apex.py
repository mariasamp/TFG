# VARIABLES
import os
import nastran_exe

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
E = float(datos[15][1])
nu = float(datos[16][1])
rho = float(datos[17][1])

# PRUEBA
import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N-K''')
model_1 = apex.currentModel()

# MATERIAL
material_1 = apex.catalog.createMaterial(name = 'Material 1', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
matModel_ = material_1.getMaterialModel( materialModel = 'MAT1')
if material == "Acero":
    matModel_.update( materialProperties = {'E' : 200000.,'NU' : 0.3,'RHO' : 0.00000785,})
elif material == "Aluminio":
    matModel_.update( materialProperties = {'E' : 70000.,'NU' : 0.33,'RHO' : 0.00000270,})
elif material == "Cobre":
    matModel_.update( materialProperties = {'E' : 110000.,'NU' : 0.34,'RHO' : 0.00000896,})
elif material == "Personalizado": 
    matModel_.update( materialProperties = {'E' : E*10**3,'NU' : nu,'RHO' : rho*10**(-9),})

# AUTOMATIZACIÓN PARA ELEMENTO 1D
if elemento == "1D":
    # Dibujar geometría
    def doSketch_1():
        Viga = model_1.getCurrentPart()
        if Viga is None:
            Viga = model_1.createPart()
        sketch_1 = Viga.createSketchOnGlobalPlane(
            name = 'Sketch 1',
            plane = apex.construct.GlobalPlane.XY,
            alignSketchViewWithViewport = True
        )
        _pointList = [
            Point2D( 0.0, 0.0 ),
            Point2D( L, 0.0 )
        ]
        polyline_1 = sketch_1.createPolyline(
            name = "Polyline 1",
            points = _pointList
        )
        return sketch_1.completeSketch( fillSketches = True )
    newbodies = doSketch_1()

    parts = model_1.getParts(True)
    curves = apex.EntityCollection()
    for part in parts:
        curves += part.getCurves()
    for part in parts:
        updatedPartName_ = part.update( name = "Viga" )
    result = apex.mesh.createCurveMesh(
        name = "",
        target = curves,
        meshSize = meshSize,
        elementOrder = apex.mesh.ElementOrder.Linear
    )

    node_const = apex.EntityCollection()
    meshs = apex.EntityCollection()
    for part in parts:
        meshs += part.getMeshes()
    nodes = apex.EntityCollection()
    for mesh in meshs:
        nodes += mesh.getNodes()

    loc_nodes = []
    for node in nodes:
        loc_nodes.append(node.id)

    for mesh in meshs:
        node_const += mesh.getNodes( ids = loc_nodes[0])

    _constraintProp = apex.attribute.createDisplacementConstraintProperties(
        constrainTranslationX = True, 
        constrainTranslationY = True, 
        constrainTranslationZ = True, 
        constrainRotationX = True, 
        constrainRotationY = True, 
        constrainRotationZ = True
    )
    constraint_1 = apex.environment.createDisplacementConstraint(
        name = "Constraint",
        constraintType = apex.attribute.ConstraintType.General, 
        applicationMethod = apex.attribute.ApplicationMethod.Direct, 
        target = node_const, 
        constraintProperties = _constraintProp, 
        description = "" 
    )

    loaddistributedbeam2_2 = apex.environment.createLoadDistributedBeam2(
        name = "Beam Distributed Load",
        target = curves,
        loadType = apex.attribute.LoadTypeDistributedBeam2.ForceZ,
        scaleType = apex.attribute.ScaleTypeDistributedBeam2.Length,
        loadFactorX1 = (-load*2*(a0+t) if seccion == "Rectangular Hueca" else -load*2*(a0)) if direccion == "Descendente" else (load*2*(a0+t) if seccion == "Rectangular Hueca" else load*2*(a0)),
        inputType = apex.attribute.InputType.ElementUniform
    )

    # # PARA VERSIÓN ESTUDIANTE
    # for i in range(len(loc_nodes)):
    #     node_load = apex.EntityCollection()
    #     for mesh in meshs:
    #         node_load += mesh.getNodes( ids = loc_nodes[i])
    #     forceMomentRep_ = apex.environment.createForceMomentStaticRepByComponent(
    #         name = "",
    #         forceX = 0.0,
    #         forceY = 0.0,
    #         forceZ = ((-load*meshSize*(a0+t) if (i == 0 or i==1) else -load*meshSize*(a0+t)*2) if seccion == "Rectangular Hueca" else (-load*meshSize*(a0) if (i == 0 or i==1) else -load*meshSize*(a0)*2)) if direccion == "Descendente" else ((load*meshSize*(a0+t) if (i == 0 or i==1) else load*meshSize*(a0+t)*2) if seccion == "Rectangular Hueca" else (load*meshSize*(a0) if (i == 0 or i==1) else load*meshSize*(a0)*2)),
    #         description = ""   #defaults to " "
    #     )
    #     forcemoment_2 = apex.environment.createForceMoment(
    #         name = "",
    #         forceMomentRep = forceMomentRep_,
    #         applicationMethod = apex.attribute.ApplicationMethod.Direct,
    #         target = node_load,
    #         description = ""   #defaults to " "
    #     )

    if seccion == "Rectangular Hueca":
        beamshape_1 = apex.attribute.createBeamShapeHollowRectangularSymmetric(
            name = "Beam Shape",
            overallWidth = a0+t,
            overallHeight = b0+t,
            floorCeilingThickness = t,
            sideWallThickness = t
        )
    elif seccion == "Rectangular":
        beamshape_1 = apex.attribute.createBeamShapeSolidRectangle(
            name = "Beam Shape",
            width = a0,
            height = b0
        )
    elif seccion == "Sección en I":
        beamshape_1 = apex.attribute.createBeamShapeISymmetric(
            name = "Beam Shape",
            flangeExtension = (a0-t),
            webThickness = t,
            flangeSeparation = b0-t,
            overallHeight = b0+t
        )

    edges = apex.EntityCollection()
    for curve in curves:
        edges += curve.getEdges()
    beamTarget_ = apex.geometry.EdgeCollection()
    for entity in edges :
        beamTarget_.append(entity.asEdge())
    material_ = apex.catalog.getMaterial( name = "Material 1" )
    beamShape_ = apex.catalog.getBeamShape( 'Beam Shape 1' )
    shapeA_ = beamShape_
    beamShape_ = apex.catalog.getBeamShape( 'Beam Shape 1' )
    shapeB_ = beamShape_
    beamspans = apex.attribute.createBeamSpanFree(
        name = "Span",
        beamTarget = beamTarget_,
        shapeEndA = shapeA_,
        shapeEndB = shapeB_,
        shapeEndA_orientation = 0.0,
        shapeEndB_orientation = 0.0,
        shapeEndA_offset1 = 0.0,
        shapeEndA_offset2 = 0.0,
        shapeEndB_offset1 = 0.0,
        shapeEndB_offset2 = 0.0,
        material = material_,
    )


#   AUTOMATIZACIÓN PARA VIGA 2D O 3D
else:

    # IMPORTAR si es elemento 2D o 3D
    ruta_viga = [os.path.join(folder_path1, "Viga.CATPart").replace("\\", "/")]
    _importFilter = {}
    model_1.importGeometry(
        geometryFileNames = ruta_viga,
        importSolids = True,     #defaults to True
        importSurfaces = True,     #defaults to True
        importCurves = True,     #defaults to True
        importPoints = True,     #defaults to True
        importGeneralBodies = True,     #defaults to True
        importHiddenGeometry = False,     #defaults to False
        importCoordinate = False,     #defaults to True
        importDatumPlane = False,     #defaults to True
        cleanOnImport = True,     #defaults to True
        removeRedundantTopoOnimport = True,     #defaults to False
        loadCompleteTopology = True,     #defaults to True
        sewOnImport = False,     #defaults to False
        skipUnmodified = False,     #defaults to False
        importFilter = _importFilter,
        preview = False,     #defaults to False
        importReviewMode3dxmlCleanOnImport = True,     #defaults to True
        importReviewMode3dxmlSplitOnFeatureVertexAngle = True,     #defaults to True
        importReviewMode3dxmlFeatureAngle = 4.000000000000000e+01,     #defaults to 40.0 degrees
        importReviewMode3dxmlVertexAngle = 4.000000000000000e+01,     #defaults to 40.0 degrees
        importReviewMode3dxmlDetectMachinedFaces = False,     #defaults to False
        importAttributes = False,     #defaults to False
        importPublications = False     #defaults to False
    )
    
    # VARIABLES
    solids = apex.EntityCollection()
    parts = model_1.getParts(True)
    for part in parts:
        solids += part.getSolids()


    # Preparación para elementos 2D
    if elemento == "2D":
        # Espesor
        result = apex.geometry.assignConstantThicknessMidSurface(
            target = solids,
            autoAssignThickness = True,
            autoAssignTolerance = 5.000000000000000e-02
        )

    surfs = apex.EntityCollection()
    for part in parts:
        surfs += part.getSurfaces()


    # ASIGNAR MATERIAL
        #Propiedad 2D
    if elemento == "2D":
         # Extender superficies
        result = apex.geometry.extendToSurfaces(
            target = surfs,
            searchDist = t/2+3,
            cleanupAutomatically = True,
            autoCleanupTol = 5.000000000000000e-01,
            stitchAfterExtend = True,
            surfaceFlatteningSensitivity = 5,
            planarSurfaceAlignmentSensitivity = 4
        )
        propertyelement2d_1 = apex.catalog.getPropertiesElement2D( name = "Property from MidsurfacePropertyField 1" )
        property2DModel_ = propertyelement2d_1.getProperties2DModel( properties2DModel = 'PSHELL')
        property2DModel_.update( elementProperties2D = {
            'MID1' : 1,
            })
        #Propiedad 3D
    elif elemento == "3D":
        propertyelement3d_1 = apex.catalog.createPropertiesElement3D( name = '3D Element Property 1', primaryProperties3D = 'PSOLID',)
        propertyelement3d_1 = apex.catalog.getPropertiesElement3D( name = "3D Element Property 1" )
        property3DModel_ = propertyelement3d_1.getProperties3DModel( properties3DModel = 'PSOLID')
        property3DModel_.update( elementProperties3D = {
            'MID' : 1,
            })
        apex.attribute.assignPropertiesElement3D(target = parts, property = propertyelement3d_1 )

    solids.hide() #Para que se oculte el sólido y queden solo mallas y superficies

    # MALLADO
    if elemento == "2D":
        featuremeshtypes_1 = apex.mesh.FeatureMeshTypeVector()
        result = apex.mesh.createSurfaceMesh(
            name = "",
            target = surfs,
            meshSize = meshSize,
            meshType = apex.mesh.SurfaceMeshElementShape.Quadrilateral,
            meshMethod = apex.mesh.SurfaceMeshMethod.Mapped,
            mappedMeshDominanceLevel = 4, # Para que sea prácticamente al 100% hexaédrico
            elementOrder = apex.mesh.ElementOrder.Linear,
            allQuadBoundary = True,
            refineMeshUsingCurvature = True,
            curvatureType = apex.mesh.CurvatureType.EdgeOnly,
            elementGeometryDeviationRatio = 0.10,
            elementMinEdgeLengthRatio = 0.20,
            proximityRefinement = False,
            growFaceMeshSize = False,
            faceMeshGrowthRatio = 1.2,
            createFeatureMeshes = False,
            featureMeshTypes = featuremeshtypes_1,
            projectMidsideNodesToGeometry = True,
            useMeshFlowOptimization = False,
            meshFlow = apex.mesh.MeshFlow.Grid,
            minimalMesh = False
        )
    elif elemento == "3D":
        result = apex.mesh.createHexMesh(
        name = "",
        target = solids,
        meshSize = meshSize,
        surfaceMeshMethod = apex.mesh.SurfaceMeshMethod.Mapped,
        mappedMeshDominanceLevel = 4, # Para que sea prácticamente al 100% hexaédrico
        elementOrder = apex.mesh.ElementOrder.Linear,
        refineMeshUsingCurvature = False,
        elementGeometryDeviationRatio = 0.10,
        elementMinEdgeLengthRatio = 0.20,
        createFeatureMeshOnWashers = False,
        createFeatureMeshOnArbitraryHoles = False,
        preserveWasherThroughMesh = True,
        sweepFace = apex.EntityCollection(),
        hexMeshMethod = apex.mesh.HexMeshMethod.Auto,
        projectMidsideNodesToGeometry = True
        )
        
    # GIRAR

    # _entities = apex.currentModel().getEntities(pathNames=["Viga/Surface 1"])
    # newEntities = apex.transformRotate(
    #     target = _entities,
    #     axisDirection = [ 1.000000000000000, 0.0, 0.0 ],
    #     axisPoint = apex.Coordinate( 5.000000000000000e+02, 2.475050000000044, -4.3368086899420177e-16 ),
    #     angle = 90,
    #     makeCopy = False
    # )

    # CARGA

    # VARIABLES
    # Si es sección delgada entonces face y edge está dentro de surface
    # Si es maciza entonces face y edge está dentro de solid

    surfs = apex.EntityCollection()
    for part in parts:
        surfs += part.getSurfaces()
    if elemento == "2D":
        faces = apex.entityCollection()
        for surf in surfs:
            faces += surf.getFaces()
    elif elemento == "3D":
        faces = apex.entityCollection()
        for solid in solids:
            faces += solid.getFaces()

    loc_faces = []
    for face in faces:
        loc_faces.append(face.id)

    localizador_faces_sup = []
    localizador_faces_inf = []
    for i in range(len(loc_faces)):
        if elemento == "2D":
            for surf in surfs:
                face_loc = surf.getFaces( ids = loc_faces[i] )
        elif elemento == "3D":
            for solid in solids:
                face_loc = solid.getFaces( ids = loc_faces[i] )
        loc = face_loc.getCentroid( )
        z = loc.getZ()
        if z> (1.01*b1 / 2. if (elemento == "3D" and seccion != "Rectangular") else b1/4.5) and seccion != "Sección en L":
            localizador_faces_sup.append(loc_faces[i])
        if z< (1.01*-b1 / 2. if (elemento == "3D" and seccion != "Rectangular") else -b1/4.5) and seccion != "Sección en T":
            localizador_faces_inf.append(loc_faces[i])

    faces1 = apex.entityCollection()
    if elemento == "2D":
        for surf in surfs:
            for i in range(len(localizador_faces_sup)):
                    faces1 += surf.getFaces( ids = localizador_faces_sup[i])
    elif elemento == "3D":
        for solid in solids:
            for i in range(len(localizador_faces_sup)):
                    faces1 += solid.getFaces( ids = localizador_faces_sup[i])


    faces2 = apex.entityCollection()
    if elemento == "2D":
        for surf in surfs:
            for i in range(len(localizador_faces_inf)):
                    faces2 += surf.getFaces( ids = localizador_faces_inf[i])
    elif elemento == "3D":
        for solid in solids:
            for i in range(len(localizador_faces_inf)):
                faces2 += solid.getFaces( ids = localizador_faces_inf[i])


    if faces2:
        pressureProp_ = apex.environment.createPressurePropertyStaticConstant(
            pressureValue = -load if direccion == "Descendente" else load
        )
        pressure_1 = apex.environment.createLoadPressure(
            name = "Pressure",
            description = "",   #defaults to " "
            target = faces2, #Carga hacia abajo
            loadPressureProperty = pressureProp_
        )

    if faces1:
        pressureProp_ = apex.environment.createPressurePropertyStaticConstant(
            pressureValue = load if direccion == "Descendente" else -load
        )
        pressure_2 = apex.environment.createLoadPressure(
            name = "Pressure",
            description = "",
            target = faces1, # Carga hacia abajo
            loadPressureProperty = pressureProp_
        )

    if elemento == "2D" and seccion != "Sección en I":
        apex.mesh.reverseElement( target = faces )

    # RESTRICCIONES

    edgexs = apex.entityCollection()
    if elemento == "2D":
        for surf in surfs:
            edgexs += surf.getEdges()
    elif elemento == "3D":
        for solid in solids:
            edgexs += solid.getFaces()


    loc_edges = []

    for edgex in edgexs:
        loc_edges.append(edgex.id)

    localizador_edges = []
    for i in range(len(loc_edges)):
        if elemento == "2D":
            for surf in surfs:
                edge_loc = surf.getEdges( ids = loc_edges[i] )
            loc = edge_loc.getAverageCentroid( )
        elif elemento == "3D":
            for solid in solids:
                edge_loc = solid.getFaces( ids = loc_edges[i] )
            loc = edge_loc.getCentroid( )

        x = loc.getX()
        if x < L/10:
            localizador_edges.append(loc_edges[i])

    edges1 = apex.entityCollection()
    if elemento == "2D":
        for surf in surfs:
            for i in range(len(localizador_edges)):
                    edges1 += surf.getEdges( ids = localizador_edges[i])
    elif elemento == "3D":
        for solid in solids:
            for i in range(len(localizador_edges)):
                    edges1 += solid.getFaces( ids = localizador_edges[i])

    _constraintProp = apex.attribute.createDisplacementConstraintProperties(
        constrainTranslationX = True,
        constrainTranslationY = True,
        constrainTranslationZ = True,
        constrainRotationX = True,
        constrainRotationY = True,
        constrainRotationZ = True
    )
    constraint_2 = apex.environment.createDisplacementConstraint(
        name = "Constraint",
        constraintType = apex.attribute.ConstraintType.General,
        applicationMethod = apex.attribute.ApplicationMethod.Direct,
        target = edges1,
        constraintProperties = _constraintProp,
        description = ""
    )

    # MPC Para calcular desplazamiento en el extremo:

    if elemento == "2D":
        edgexs = apex.entityCollection()
        for surf in surfs:
            edgexs += surf.getEdges()

        loc_edges = []
        for edgex in edgexs:
            loc_edges.append(edgex.id)

        localizador_edges = []
        for i in range(len(loc_edges)):
            for surf in surfs:
                edge_loc = surf.getEdges( ids = loc_edges[i] )
            loc = edge_loc.getAverageCentroid( )
            x = loc.getX()
            if x > L/1.1:
                localizador_edges.append(loc_edges[i])

        edges1 = apex.entityCollection()
        
        for i in range(len(localizador_edges)):
            for surf in surfs:
                edges1 += surf.getEdges( ids = localizador_edges[i])

    if elemento == "3D":
        faces = apex.entityCollection()
        for solid in solids:
            faces += solid.getFaces()

        loc_faces = []
        for face in faces:
            loc_faces.append(face.id)

        localizador_faces = []
        for i in range(len(loc_faces)):
            for solid in solids:
                face_loc = solid.getFaces( ids = loc_faces[i] )
            loc = face_loc.getCentroid( )
            x = loc.getX()
            if x> L/1.1:
                localizador_faces.append(loc_faces[i])
        faces1 = apex.EntityCollection()

        for i in range(len(localizador_faces)):
            for solid in solids:
                faces1 += solid.getFaces( ids = localizador_faces[i])
    
    apex.mesh.createNodeByLocation( coordinates = apex.Coordinate(L, 0.0, 0.0), pathName = apex.currentModel().name + "/Viga" )
    
    meshs = apex.EntityCollection()
    for part in parts:
        meshs += part.getMeshes()

    nodes = apex.EntityCollection()
    for mesh in meshs:
        nodes += mesh.getNodes()

    loc_nodes = []
    for node in nodes:
        loc_nodes.append(node.id)

    nodes_1 = apex.getNodes(
        [{"path": apex.currentModel().name + "/Viga", "ids": loc_nodes[0]}]
    )
    _referenceRegion = nodes_1.list()[0]

    # En 3D se cogen caras. En 2D se cogen bordes
    nodetie_1 = apex.attribute.createNodeTie(
        distributionType  = apex.attribute.DistributionType.Compliant,
        distributionMode  = apex.attribute.DistributionMode.Auto,
        dofDefinitionMode  = apex.attribute.DOFDefinitionMode.All,
        referencePoint  = _referenceRegion,
        attachmentRegions  = faces1 if elemento == "3D" else edges1,
    )

    apex.endUndoIndent(description='created node tie')
        

# ANÁLISIS

study = apex.getPrimaryStudy()
study.createScenarioByModelRep( context = part, simulationType = apex.studies.SimulationType.Static )

model_1.save()


if analisis == "Nastran": #Análisis en Nastran, con la obtención del valor numérico
    # Exportar archivo bdf
    study = apex.getPrimaryStudy()
    scenario1 = study.getScenario( name = "Static Scenario Viga" )
    filename_ = os.path.join(path_analisis, "Static Scenario Viga.bdf")
    scenario1.exportFEModel(
        filename = filename_,
        unitSystem = "mm-t-s-N-K-deg",
        exportProperty = apex.ExportProperty.AsDefined
    )

    # Preparar lectura de f06
    if elemento == "3D" or elemento == "2D":
        # TENSIÓN EN LOS NODOS
        # Se almacenan los nodos de tensión máxima en un txt
        parts = model_1.getParts(True)
        solids = apex.EntityCollection()
        for part in parts:
                solids += part.getSolids()
        meshs = apex.EntityCollection()
        for part in parts:
            meshs += part.getMeshes()
        nodes = apex.EntityCollection()
        for mesh in meshs:
            nodes += mesh.getNodes()
        
        localizador_nodes = []
        for node in nodes:
            loc_n = node.getCoordinates()
            z = loc_n.getZ()
            x = loc_n.getX()
            if seccion == "Rectangular" or elemento == "2D":
                if x< L/1000 and z > b0/2/1.1:
                    localizador_nodes.append(node.id)
            elif seccion == "Rectangular Hueca" or seccion == "Sección en I":
                if x< L/1000 and z > b0/2:
                    localizador_nodes.append(node.id)

        # TENSIÓN EN LOS ELEMENTOS:
        # Se almacenan los nodos de tensión máxima en un txt
        parts = model_1.getParts(True)
        solids = apex.EntityCollection()
        for part in parts:
                solids += part.getSolids()
        meshs = apex.EntityCollection()
        for part in parts:
            meshs += part.getMeshes()
        elements = apex.EntityCollection()
        for mesh in meshs:
            elements += mesh.getElements()
        
        localizador_elements = []
        for element in elements:
            node_element = []
            node_element += element.getNodeIds()
            set_list2 = {int(value) for value in localizador_nodes}
            common_count = sum(1 for value in node_element if value in set_list2) # Que los 4 nodos pertenezcan al elemento
            if common_count >= 2:
                localizador_elements.append(element.id)

        nombre_archivo = os.path.join(path_analisis, "Lectura_Nastran.txt")
        with open(nombre_archivo, 'w') as archivo:
            for item in localizador_elements:
                archivo.write(f"{item}\n")
    
    # Se modifican cabeceras bdf, se ejecuta Nastran y se lee el f06
    nastran_exe.main()

    # Se importan los resultados para su visualización
    study = apex.getPrimaryStudy()
    scenario = study.getScenario(name = "Static Scenario Viga")
    resultsfilename_ = os.path.join(path_analisis, "static scenario viga.h5")
    scenario.attachNastranResults(
        resultsFilename = resultsfilename_,
        unitSystenName = "mm-t-s-N-K-deg",
    )


if analisis == "Apex": #Análisis desde Apex
    study = apex.getPrimaryStudy()
    scenario1 = study.getScenario( name = "Static Scenario Viga" )
    scenario1.execute()

# VISUALIZAAR RESULTADOS
result = apex.session.displayMeshCracks( False )

# solid_1 = apex.getSolid( pathName = apex.currentModel().name+"/Part1/PartBody" )
# solid_1.update( renderStyle = apex.session.DisplayRenderStyle.ShadedWithEdges )

result = apex.session.display2DSpans( False )
result = apex.session.display3DSpans( False )
apex.display.displayCutViews(False, False)
apex.display.displayExplodedView(False)
apex.display.hideRotationCenter()
result = apex.session.displayMeshCracks( False )
result = apex.session.displayInteractionMarkers( True )
result = apex.session.displayConnectionMarkers( True )
result = apex.session.display2DSpans( False )
result = apex.session.display3DSpans( True )
result = apex.session.displayLoadsAndBCMarkers( True )
result = apex.session.displaySensorMarkers( True )
result = apex.session.displaySensorMarkers( False )
study = apex.getPrimaryStudy()
scenario1 = study.getScenario(name = "Static Scenario Viga")
executedscenario_1 = scenario1.getLastExecutedScenario()
linearStep1 = executedscenario_1.getLinearStep()
event_1 = executedscenario_1.getEvent(pathName = linearStep1.getPath() + "/Event 1")
stateplot_1 = apex.post.createStatePlot(
    event = event_1,
    resultDataSetIndex = [1]
)

visualizationTarget1 = apex.entityCollection()
study = apex.getPrimaryStudy()
scenario1 = study.getScenario(name = "Static Scenario Viga")
executedscenario_1 = scenario1.getLastExecutedScenario()
#visualizationTarget1.append( executedscenario_1.getPart( pathName = apex.currentModel().name + "/Part1" ))
# deformvisualization_1 = stateplot_1.createDeformVisualization(
#     target = visualizationTarget1,
#     deformScalingMethod = apex.post.DeformScalingMethod.Relative,
#     relativeScalingFactor = 10.,
#     displayUnit = "mm"
# )
