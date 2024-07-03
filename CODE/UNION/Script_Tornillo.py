import apex
import os
from apex.construct import Point3D, Point2D
import Nastran_T

# DATOS
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

d, dk, k, s, m, h, d1, d2, P1, P2, dext_P1, dext_P2, mat_T, mat_P1, mat_P2, mu_TP1, mu_TP2,  mu_TA, mu_P1P2, Preload, Fz, Fxy,\
E_T, nu_T, ro_T, E_P1, nu_P1, ro_P1, E_P2, nu_P2, ro_P2, path_analisis, folder_path = leer_datos_tornillo()
mesh = 8
mu_TA = 1
# CABECERA
apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N-K''')
model_1 = apex.currentModel()

# IMPORTAR GEOMETRÍA
ruta_bolted_joint = [os.path.join(folder_path, "BoltedJoint.CATProduct").replace("\\", "/")]
model_1.importGeometry(geometryFileNames = ruta_bolted_joint)

# Unir Bodies (merge)
bolt_part = apex.getPart( pathName = apex.currentModel().name + "/BoltedJoint/Bolt" )
bolt_original = apex.EntityCollection()
bolt_original = bolt_part.getSolids()

result = apex.geometry.mergeBoolean(
    target = bolt_original,
    retainOriginalBodies = False,
    mergeSolidsAsCells = True
)

#   Parts y Solids
parts = model_1.getParts(True)
solids = apex.EntityCollection()
for part in parts:
    solids += part.getSolids()

#       Pieza 1
pieza1_part = apex.getPart( pathName = apex.currentModel().name + "/BoltedJoint/Pieza1" )
pieza1_solids = apex.EntityCollection()
pieza1_solids = pieza1_part.getSolids()
#       Pieza 2
pieza2_part = apex.getPart( pathName = apex.currentModel().name + "/BoltedJoint/Pieza2" )
pieza2_solids = apex.EntityCollection()
pieza2_solids = pieza2_part.getSolids()
#       Ambas piezas
piezas_solids = apex.EntityCollection()
piezas_solids += pieza1_part.getSolids()
piezas_solids += pieza2_part.getSolids()
#       Tornillo
bolt_solids = apex.EntityCollection()
bolt_solids = bolt_part.getSolids()
#       Arandela 1
arandela1_part = apex.getPart( pathName = apex.currentModel().name + "/BoltedJoint/Arandela1" )
arandela1_solids = apex.EntityCollection()
arandela1_solids = arandela1_part.getSolids()
#       Arandela 2
arandela2_part = apex.getPart( pathName = apex.currentModel().name + "/BoltedJoint/Arandela2" )
arandela2_solids = apex.EntityCollection()
arandela2_solids = arandela2_part.getSolids()
#       Ambas arandelas
arandelas_solids = apex.EntityCollection()
arandelas_solids += arandela1_part.getSolids()
arandelas_solids += arandela2_part.getSolids()

# MATERIAL
#   Del tornillo, tuerca y arandelas
if mat_T == " Acero":
    material_1 = apex.catalog.createMaterial(name = 'Steel (A2-80)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_1 = material_1.getMaterialModel( materialModel = 'MAT1')
    matModel_1.update( materialProperties = {'E' : 200000.,'NU' : 0.29,'RHO' : 0.000008,})
elif mat_T == " Titanio":
    material_1 = apex.catalog.createMaterial(name = 'Titanium (Ti6Al4V)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_1 = material_1.getMaterialModel( materialModel = 'MAT1')
    matModel_1.update( materialProperties = {'E' : 113000.,'NU' : 0.342,'RHO' : 0.00000443,})
elif mat_T == " Inconel 718":
    material_1 = apex.catalog.createMaterial(name = 'Inconel 718', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_1 = material_1.getMaterialModel( materialModel = 'MAT1')
    matModel_1.update( materialProperties = {'E' : 203000.,'NU' : 0.29,'RHO' : 0.00000819,})
else: # Personalizado
    material_1 = apex.catalog.createMaterial(name = 'Personalizado', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_1 = material_1.getMaterialModel( materialModel = 'MAT1')
    matModel_1.update( materialProperties = {'E' : E_T*10**3,'NU' : nu_T,'RHO' : ro_T*10**(-9),})

#   De la pieza superior
if mat_P1 == " Acero":
    material_2 = apex.catalog.createMaterial(name = 'Steel (A2-80)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_2 = material_2.getMaterialModel( materialModel = 'MAT1')
    matModel_2.update( materialProperties = {'E' : 200000.,'NU' : 0.29,'RHO' : 0.000008,})  
elif mat_P1 == " Aluminio":
    material_2 = apex.catalog.createMaterial(name = 'Aluminium', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_2 = material_2.getMaterialModel( materialModel = 'MAT1')
    matModel_2.update( materialProperties = {'E' : 70000.,'NU' : 0.33,'RHO' : 0.00000270,})
elif mat_P1 == " Titanio":
    material_2 = apex.catalog.createMaterial(name = 'Titanium (Ti6Al4V)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_2 = material_2.getMaterialModel( materialModel = 'MAT1')
    matModel_2.update( materialProperties = {'E' : 113000.,'NU' : 0.342,'RHO' : 0.00000443,})
else: # Personalizado
    material_2 = apex.catalog.createMaterial(name = 'Personalizado', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_2 = material_2.getMaterialModel( materialModel = 'MAT1')
    matModel_2.update( materialProperties = {'E' : E_P1*10**3,'NU' : nu_P1,'RHO' : ro_P1*10**(-9),})

#   De la pieza inferior
if mat_P2 == " Acero":
    material_3 = apex.catalog.createMaterial(name = 'Steel (A2-80)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_3 = material_3.getMaterialModel( materialModel = 'MAT1')
    matModel_3.update( materialProperties = {'E' : 200000.,'NU' : 0.29,'RHO' : 0.000008,})  
elif mat_P2 == " Aluminio":
    material_3 = apex.catalog.createMaterial(name = 'Aluminium', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_3 = material_3.getMaterialModel( materialModel = 'MAT1')
    matModel_3.update( materialProperties = {'E' : 70000.,'NU' : 0.33,'RHO' : 0.00000270,})
elif mat_P2 == " Titanio":
    material_3 = apex.catalog.createMaterial(name = 'Titanium (Ti6Al4V)', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_3 = material_3.getMaterialModel( materialModel = 'MAT1')
    matModel_3.update( materialProperties = {'E' : 113000.,'NU' : 0.342,'RHO' : 0.00000443,})
else: # Personalizado
    material_3 = apex.catalog.createMaterial(name = 'Personalizado', color = [ 0, 0, 0 ], primaryMaterialModel = 'MAT1',)
    matModel_3 = material_3.getMaterialModel( materialModel = 'MAT1')
    matModel_3.update( materialProperties = {'E' : E_P2*10**3,'NU' : nu_P2,'RHO' : ro_P2*10**(-9),})

# ASIGNAR MATERIAL
propertyelement3d_1 = apex.catalog.createPropertiesElement3D(name = 'Bolt property', primaryProperties3D = 'PSOLID',)
propertyelement3d_1 = apex.catalog.getPropertiesElement3D( name = "Bolt property" )
property3DModel_ = propertyelement3d_1.getProperties3DModel( properties3DModel = 'PSOLID')
property3DModel_.update( elementProperties3D = {'MID' : 1,})
target1 = apex.EntityCollection()
target1.append(bolt_part)
apex.attribute.assignPropertiesElement3D(target = target1, property = propertyelement3d_1 )

propertyelement3d_2 = apex.catalog.createPropertiesElement3D(name = 'Pieza 1 property', primaryProperties3D = 'PSOLID',)
propertyelement3d_2 = apex.catalog.getPropertiesElement3D( name = "Pieza 1 property" )
property3DModel_ = propertyelement3d_2.getProperties3DModel( properties3DModel = 'PSOLID')
property3DModel_.update( elementProperties3D = {'MID' : 2,})
target2 = apex.EntityCollection()
target2.append(pieza1_part)
apex.attribute.assignPropertiesElement3D(target = target2, property = propertyelement3d_2 )

propertyelement3d_3 = apex.catalog.createPropertiesElement3D(name = 'Pieza 2 property', primaryProperties3D = 'PSOLID',)
propertyelement3d_3 = apex.catalog.getPropertiesElement3D( name = "Pieza 2 property" )
property3DModel_ = propertyelement3d_3.getProperties3DModel( properties3DModel = 'PSOLID')
property3DModel_.update( elementProperties3D = {'MID' : 3,})
target3 = apex.EntityCollection()
target3.append(pieza2_part)
apex.attribute.assignPropertiesElement3D(target = target3, property = propertyelement3d_3 )

propertyelement3d_4 = apex.catalog.createPropertiesElement3D(name = 'Arandela 1 property', primaryProperties3D = 'PSOLID',)
propertyelement3d_4 = apex.catalog.getPropertiesElement3D( name = "Arandela 1 property" )
property3DModel_ = propertyelement3d_4.getProperties3DModel( properties3DModel = 'PSOLID')
property3DModel_.update( elementProperties3D = {'MID' : 1,})
target4 = apex.EntityCollection()
target4.append(arandela1_part)
apex.attribute.assignPropertiesElement3D(target = target4, property = propertyelement3d_4 )

propertyelement3d_5 = apex.catalog.createPropertiesElement3D(name = 'Arandela 2 property', primaryProperties3D = 'PSOLID',)
propertyelement3d_5 = apex.catalog.getPropertiesElement3D( name = "Arandela 2 property" )
property3DModel_ = propertyelement3d_5.getProperties3DModel( properties3DModel = 'PSOLID')
property3DModel_.update( elementProperties3D = {'MID' : 1,})
target5 = apex.EntityCollection()
target5.append(arandela2_part)
apex.attribute.assignPropertiesElement3D(target = target5, property = propertyelement3d_5 )

# SEED
#   Seed para el tornillo
edges_1 = apex.EntityCollection()
edges_2 = apex.EntityCollection()
edge1s = apex.EntityCollection()
for bolt_solid in bolt_solids:
    edge1s += bolt_solid.getEdges()
loc1_edges = [edge1.id for edge1 in edge1s]
localizador_edges1 = []
localizador_edges2 = []
localizador_edges3 = []
for edge_id in loc1_edges:
    for bolt_solid in bolt_solids:
        edges_in_solid = bolt_solid.getEdges()
        if any(edge.id == edge_id for edge in edges_in_solid):
            edge_loc = bolt_solid.getEdges(ids=edge_id)
            if edge_loc:
                loc = edge_loc.getAverageCentroid()
                x = loc.getX()
                y = loc.getY()
                z = loc.getZ()
                R = (x**2+y**2)**0.5
                # with open("C:\\Users\\maria.sampedro\\Documents\\No Ariel\\TFG\\CASOS\\Viga\\Resultados.txt","a") as archivo:
                #     archivo.write(f"{edge_id, x, y, z, R}\n")
                if (R>d/2*0.9 and R<d/2*0.94) or (abs(R-d/4)<=0.1): # cuerpo del tornillo y cuadrado inscrito
                    localizador_edges1.append((edge_id))
                if (R>d/2*0.85 and R<d/2*0.89) or (R>d/2*0.97 and R<d/2*0.99): # Diagonales y parte del cuerpo del tornillo
                    localizador_edges2.append((edge_id))
                if (R>d/2*0.95 and R<d/2*0.96): # Cabeza de tornillo y de tuerca
                    localizador_edges3.append((edge_id))
for edge_id in localizador_edges1:
    for bolt_solid in bolt_solids:
        edges_in_solid = bolt_solid.getEdges()
        if any(edge.id == edge_id for edge in edges_in_solid):
            edges_1 += bolt_solid.getEdges( ids = edge_id)
for edge_id in localizador_edges2:
    for bolt_solid in bolt_solids:
        edges_in_solid = bolt_solid.getEdges()
        if any(edge.id == edge_id for edge in edges_in_solid):
            edges_2 += bolt_solid.getEdges( ids = edge_id)
result = apex.mesh.createEdgeSeedUniformByNumber(
    target = edges_1,
    numberElementEdges = mesh
)
result = apex.mesh.createEdgeSeedUniformByNumber(
    target = edges_2,
    numberElementEdges = int(mesh/2)
)

edges_3 = apex.EntityCollection()
for edge_id in localizador_edges3:
    for bolt_solid in bolt_solids:
        edges_in_solid = bolt_solid.getEdges()
        if any(edge.id == edge_id for edge in edges_in_solid):
            edges_3 += bolt_solid.getEdges( ids = edge_id)

#   Seed para las piezas 1 y 2
edge2s = apex.EntityCollection()
for pieza1_solid in pieza1_solids:
    edge2s += pieza1_solid.getEdges()
edge3s = apex.EntityCollection()
for pieza2_solid in pieza2_solids:
    edge3s += pieza2_solid.getEdges()
edges_3 += edge2s
edges_3 += edge3s
#   Seed para las arandelas 1 y 2
edge4s = apex.EntityCollection()
for arandela_solids in arandelas_solids:
    edge4s += arandela_solids.getEdges()
edges_3 += edge4s
result = apex.mesh.createEdgeSeedUniformByNumber(
    target = edges_3,
    numberElementEdges = 2*mesh
)

# MALLADO
_SweepFace = apex.EntityCollection()
result = apex.mesh.createHexMesh(
    name = "",
    target = solids,
    meshSize = d/2/mesh,
    surfaceMeshMethod = apex.mesh.SurfaceMeshMethod.Mapped,
    mappedMeshDominanceLevel = 5,
    elementOrder = apex.mesh.ElementOrder.Linear,
    refineMeshUsingCurvature = True,
    elementGeometryDeviationRatio = 0.20,
    elementMinEdgeLengthRatio = 0.20,
    createFeatureMeshOnWashers = False,
    createFeatureMeshOnArbitraryHoles = False,
    preserveWasherThroughMesh = True,
    sweepFace = _SweepFace,
    hexMeshMethod = apex.mesh.HexMeshMethod.Auto,
    projectMidsideNodesToGeometry = True
)

# PRELOAD
Bolts3D = apex.attribute.createBolts3DByCrossSectionAutomatic(
    name = "3D Bolt",
    targets = bolt_solids,
    controlNodeDefinitionMethod = apex.attribute.ControlNodeDefinitionMethod.Mid
)
targetBolts = apex.EntityCollection()
targetBolts = Bolts3D
preloadproperty_4 = apex.environment.createPreloadBoltPropertyStatic( preloadType = apex.environment.BoltPreloadType.Force , force = Preload)
preloadbolt_4 = apex.environment.createPreloadBolt(name = "Bolt Preload", target = targetBolts)
preloadrep_4 = preloadbolt_4.createPreloadBoltRep(repProperty = preloadproperty_4)

# CONSTRAINT Y LOAD
#   Crear los puntos para el NodeTie
apex.mesh.createNodeByLocation( coordinates = apex.Coordinate(0.0, 0.0, -P2), pathName = apex.currentModel().name + "/BoltedJoint/Bolt" )
apex.mesh.createNodeByLocation( coordinates = apex.Coordinate(0.0, 0.0, P1), pathName = apex.currentModel().name + "/BoltedJoint/Bolt" )

#   Cara inferior de la pieza 2 y cara superior de la pieza 1
face2s = apex.entityCollection()
for pieza2_solid in pieza2_solids:
    face2s += pieza2_solid.getFaces()
face1s = apex.entityCollection()
for pieza1_solid in pieza1_solids:
    face1s += pieza1_solid.getFaces()

loc_faces2 = []
for face2 in face2s:
    loc_faces2.append(face2.id)
loc_faces1 = []
for face1 in face1s:
    loc_faces1.append(face1.id)
    
localizador_faces_inf = []
for i in range(len(loc_faces2)):
    for pieza2_solid in pieza2_solids:
        face_loc = pieza2_solid.getFaces( ids = loc_faces2[i] )
    loc = face_loc.getCentroid( )
    z = loc.getZ()
    if abs(z)>(P2*0.99):
        localizador_faces_inf.append(loc_faces2[i])
localizador_faces_sup = []
for i in range(len(loc_faces1)):
    for pieza1_solid in pieza1_solids:
        face_loc = pieza1_solid.getFaces( ids = loc_faces1[i] )
    loc = face_loc.getCentroid( )
    z = loc.getZ()
    if abs(z)>(P1*0.99):
        localizador_faces_sup.append(loc_faces1[i])

#   Identificadores de los nodos
meshs = apex.EntityCollection()
for part in parts:
    meshs += part.getMeshes()
nodes = apex.EntityCollection()
for mesh in meshs:
    nodes += mesh.getNodes()
loc_nodes = []
for node in nodes:
    loc_nodes.append(node.id)
    
#   Node Tie para la constraint (cara inferior)
faces_inf = apex.entityCollection()
for pieza2_solid in pieza2_solids:
    faces_inf.extend( pieza2_solid.getFaces( ids = localizador_faces_inf[0] ) )
nodes_1 = apex.getNodes([{"path": apex.currentModel().name + "/BoltedJoint", "ids": loc_nodes[1]}])
_referenceRegion = nodes_1.list()[0]
nodetie_1 = apex.attribute.createNodeTie(
    distributionType  = apex.attribute.DistributionType.Rigid,
    distributionMode  = apex.attribute.DistributionMode.Auto,
    dofDefinitionMode  = apex.attribute.DOFDefinitionMode.All,
    referencePoint  = _referenceRegion,
    attachmentRegions  = faces_inf,
)

nodeTie_inf = apex.attribute.NodeTieCollection()
nodeTie_inf.append(nodetie_1)

#   Node Tie para la carga (cara superior)
faces_sup = apex.entityCollection()
for pieza1_solid in pieza1_solids:
    faces_sup.extend( pieza1_solid.getFaces( ids = localizador_faces_sup[0] ) )
nodes_2 = apex.getNodes([{"path": apex.currentModel().name + "/BoltedJoint", "ids": loc_nodes[2]}])
_referenceRegion2 = nodes_2.list()[0]
nodetie_2 = apex.attribute.createNodeTie(
    distributionType  = apex.attribute.DistributionType.Rigid,
    distributionMode  = apex.attribute.DistributionMode.Auto,
    dofDefinitionMode  = apex.attribute.DOFDefinitionMode.All,
    referencePoint  = _referenceRegion2,
    attachmentRegions  = faces_sup,
)

nodeTie_sup = apex.attribute.NodeTieCollection()
nodeTie_sup.append(nodetie_2)

#   Constraint
constraintsinglepoint_1 = apex.environment.createConstraintSinglePoint(
    name = "Constraint",
    constrainTranslationX = True,
    constrainTranslationY = True,
    constrainTranslationZ = True,
    constrainRotationX = True,
    constrainRotationY = True,
    constrainRotationZ = True,
    target = nodeTie_inf,
    constraintType = apex.attribute.ConstraintType.General
)

#  Load
loadforcecomponent_1 = apex.environment.createLoadForceComponent(
    name = "Force",
    target = nodeTie_sup,
    scaleFactor = 1.000000000000000,
    forceZ = Fz
)
loadforcecomponent_2 = apex.environment.createLoadForceComponent(
    name = "Force",
    target = nodeTie_sup,
    scaleFactor = 1.000000000000000,
    forceX = Fxy
)

# Crear cuerpos de contacto
contactbodyproperty = apex.attribute.createContactBodyProperty(smoothingState = False,
    shellLayer = apex.attribute.ShellLayer.TopAndButtom,
    ignoreShellThickness = False,
)

entities_1 = apex.EntityCollection()
properties_bolt = apex.catalog.getPropertiesElement3D( name = "Bolt property" )
entities_1.append(properties_bolt)
contactbody_1 = apex.attribute.createContactBody(
    name = 'Bolt',
    description = '',
    bodyType = apex.attribute.ContactBodyType.Deform,
    target = entities_1,
    bodyProperty = contactbodyproperty,
    contactResultCalculation = apex.attribute.ContactResultCalculation.EstimatedCentroid,
)

entities_2 = apex.EntityCollection()
properties_pieza1 = apex.catalog.getPropertiesElement3D( name = "Pieza 1 property" )
entities_2.append(properties_pieza1)
contactbody_2 = apex.attribute.createContactBody(
    name = 'Pieza 1',
    description = '',
    bodyType = apex.attribute.ContactBodyType.Deform,
    target = entities_2,
    bodyProperty = contactbodyproperty,
    contactResultCalculation = apex.attribute.ContactResultCalculation.EstimatedCentroid,
)

entities_3 = apex.EntityCollection()
properties_pieza2 = apex.catalog.getPropertiesElement3D( name = "Pieza 2 property" )
entities_3.append(properties_pieza2)
contactbody_3 = apex.attribute.createContactBody(
    name = 'Pieza 2',
    description = '',
    bodyType = apex.attribute.ContactBodyType.Deform,
    target = entities_3,
    bodyProperty = contactbodyproperty,
    contactResultCalculation = apex.attribute.ContactResultCalculation.EstimatedCentroid,
)

entities_4 = apex.EntityCollection()
properties_arandela1 = apex.catalog.getPropertiesElement3D( name = "Arandela 1 property" )
entities_4.append(properties_arandela1)
contactbody_4 = apex.attribute.createContactBody(
    name = 'Arandela 1',
    description = '',
    bodyType = apex.attribute.ContactBodyType.Deform,
    target = entities_4,
    bodyProperty = contactbodyproperty,
    contactResultCalculation = apex.attribute.ContactResultCalculation.EstimatedCentroid,
)

entities_5 = apex.EntityCollection()
properties_arandela2 = apex.catalog.getPropertiesElement3D( name = "Arandela 2 property" )
entities_5.append(properties_arandela2)
contactbody_5 = apex.attribute.createContactBody(
    name = 'Arandela 2',
    description = '',
    bodyType = apex.attribute.ContactBodyType.Deform,
    target = entities_5,
    bodyProperty = contactbodyproperty,
    contactResultCalculation = apex.attribute.ContactResultCalculation.EstimatedCentroid,
)

# Crear contacto entre cuerpos de contacto
bodyProperty = apex.attribute.createContactBodyProperty(
    smoothingState = False,
)
interactionPropertyGeometric = apex.attribute.createInteractionPropertyGeometric(
    contactToleranceCalculationMethod = apex.AutoManual.Manual ,
    contactTolerance = 0.01,
    ignoreShellThicknessSide1 = False,
    shellLayerSide1 = apex.attribute.ShellLayer.TopAndButtom,
    ignoreShellThicknessSide2 = False,
    shellLayerSide2 = apex.attribute.ShellLayer.TopAndButtom,
    contactSearchOrder = apex.attribute.ContactSearchOrder.DoubleSide,
    stressFreeInitialContact = False,
    delayedSlideOff = False,
    interferenceFit = False,
    initialClearance = False,
)

target_bolt = apex.EntityCollection()
contact_bolt_collection = apex.attribute.ContactBodyCollection()
contact_bolt = apex.attribute.getContactBody( name = "Bolt" )
contact_bolt_collection.append( contact_bolt )
target_bolt.extend( contact_bolt_collection )

target_pieza1 = apex.EntityCollection()
contact_pieza1_collection = apex.attribute.ContactBodyCollection()
contact_pieza1 = apex.attribute.getContactBody( name = "Pieza 1" )
contact_pieza1_collection.append( contact_pieza1 )
target_pieza1.extend( contact_pieza1_collection )

target_pieza2 = apex.EntityCollection()
contact_pieza2_collection = apex.attribute.ContactBodyCollection()
contact_pieza2 = apex.attribute.getContactBody( name = "Pieza 2" )
contact_pieza2_collection.append( contact_pieza2 )
target_pieza2.extend( contact_pieza2_collection )

target_arandela1 = apex.EntityCollection()
contact_arandela1_collection = apex.attribute.ContactBodyCollection()
contact_arandela1 = apex.attribute.getContactBody( name = "Arandela 1" )
contact_arandela1_collection.append( contact_arandela1 )
target_arandela1.extend( contact_arandela1_collection )

target_arandela2 = apex.EntityCollection()
contact_arandela2_collection = apex.attribute.ContactBodyCollection()
contact_arandela2 = apex.attribute.getContactBody( name = "Arandela 2" )
contact_arandela2_collection.append( contact_arandela2 )
target_arandela2.extend( contact_arandela2_collection )

#   Pieza 1 - Pieza 2
interactionProperty_piezapieza = apex.attribute.createInteractionPropertyPhysical(
    frictionCoefficient = mu_P1P2,
)
interaction_1 = apex.attribute.createInteractionManualPair(
    name = 'Pieza1-Pieza2',
    description = '',
    targetSide1 = target_pieza2,
    targetSide2 = target_pieza1,
    body1Property = bodyProperty,
    body2Property = bodyProperty,
)
_activeRep = interaction_1.createInteractionRep(
    name = 'Pieza1-Pieza2',
    description = '',
    interactionType = apex.attribute.InteractionType.GeneralContact,
    interactionPropertyGeometric = interactionPropertyGeometric,
    interactionPropertyPhysical = interactionProperty_piezapieza,
    allowSelfContactSide1 = False,
    allowSelfContactSide2 = False,
)

#   Bolt y Arandela 1 con - Pieza 1
interactionProperty_boltpieza1 = apex.attribute.createInteractionPropertyPhysical(
    frictionCoefficient = mu_TP1,
)
target_BA_P1 = apex.EntityCollection()
target_BA_P1 += target_bolt
target_BA_P1 += target_arandela1
interaction_2 = apex.attribute.createInteractionManualPair(
    name = 'Pieza1-BoltArandela',
    description = '',
    targetSide1 = target_BA_P1,
    targetSide2 = target_pieza1,
    body1Property = bodyProperty,
    body2Property = bodyProperty,
)
_activeRep = interaction_2.createInteractionRep(
    name = 'Pieza1-BoltArandela',
    description = '',
    interactionType = apex.attribute.InteractionType.GeneralContact,
    interactionPropertyGeometric = interactionPropertyGeometric,
    interactionPropertyPhysical = interactionProperty_boltpieza1,
    allowSelfContactSide1 = False,
    allowSelfContactSide2 = False,
)

#   Bolt y Arandela 2 con - Pieza 2
interactionProperty_boltpieza2 = apex.attribute.createInteractionPropertyPhysical(
    frictionCoefficient = mu_TP2,
)
target_BA_P2 = apex.EntityCollection()
target_BA_P2 += target_bolt
target_BA_P2 += target_arandela2
interaction_3 = apex.attribute.createInteractionManualPair(
    name = 'Pieza2-BoltArandela',
    description = '',
    targetSide1 = target_BA_P2,
    targetSide2 = target_pieza2,
    body1Property = bodyProperty,
    body2Property = bodyProperty,
)
_activeRep = interaction_3.createInteractionRep(
    name = 'Pieza2-BoltArandela',
    description = '',
    interactionType = apex.attribute.InteractionType.GeneralContact,
    interactionPropertyGeometric = interactionPropertyGeometric,
    interactionPropertyPhysical = interactionProperty_boltpieza2,
    allowSelfContactSide1 = False,
    allowSelfContactSide2 = False,
)

#   Bolt - Arandelas
interactionProperty_boltpieza2 = apex.attribute.createInteractionPropertyPhysical(
    frictionCoefficient = mu_TA,
)
target_A = apex.EntityCollection()
target_A += target_arandela1
target_A += target_arandela2
interaction_4 = apex.attribute.createInteractionManualPair(
    name = 'Bolt-Arandela',
    description = '',
    targetSide1 = target_bolt,
    targetSide2 = target_A,
    body1Property = bodyProperty,
    body2Property = bodyProperty,
)
_activeRep = interaction_4.createInteractionRep(
    name = 'Bolt-Arandela',
    description = '',
    interactionType = apex.attribute.InteractionType.GeneralContact,
    interactionPropertyGeometric = interactionPropertyGeometric,
    interactionPropertyPhysical = interactionProperty_boltpieza2,
    allowSelfContactSide1 = False,
    allowSelfContactSide2 = False,
)

# CREAR ESCENARIO DE ANÁLISIS

study = apex.getPrimaryStudy()
study.createScenario(
    name = "Nonlinear Scenario",
    description = "",
    scenarioConfiguration = apex.studies.ScenarioConfiguration.NastranSol400Static,
)

modelRep_ = apex.getAssembly( pathName = apex.currentModel().name + "/" )
study = apex.getPrimaryStudy()
scenario1 = study.getScenario(name = "Nonlinear Scenario 1")
scenario1.associateModelRep(modelRep_)

study_1 = apex.getPrimaryStudy()
scenario_1 = study_1.getScenario(name="Nonlinear Scenario 1")
loadcase_1 = scenario_1.getLoadCase(name="Load Case 1")

step1 = loadcase_1.addStep(
    name = "Static Step 2",
    description = "",
    initialStepState = apex.studies.InitialStepState.PreviousStep
)

step1 = loadcase_1.addStep(
    name = "Static Step 3",
    description = "",
    initialStepState = apex.studies.InitialStepState.PreviousStep
)

loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
boltPreload1 = apex.environment.getPreloadBolt(name = "Bolt Preload 1")
loads_.append(boltPreload1)
boltPreloadRep1 = boltPreload1.getActiveRep()
loadReps_.append(boltPreloadRep1)

step_1 = loadcase_1.getStep(name="Static Step 1")
step_1.addLoads(loads = loads_, loadReps = loadReps_)

step_2 = loadcase_1.getStep(name="Static Step 2")
step_2.addLoads(loads = loads_, loadReps = loadReps_)


step_3 = loadcase_1.getStep(name="Static Step 3")
step_3.addLoads(loads = loads_, loadReps = loadReps_)



constraints_ = apex.EntityCollection()
constraint_1 = apex.environment.getConstraint( name = "Constraint 1" )
constraints_.append(constraint_1)

step_1.addConstraints(constraints = constraints_)

step_2.addConstraints(constraints = constraints_)

step_3.addConstraints(constraints = constraints_)


loadforcecomponent1 = apex.environment.getLoadForceComponent(name = "Force 1")
loads_.append(loadforcecomponent1)
loadReps_.append(loadforcecomponent1)

step_2.addLoads(loads = loads_, loadReps = loadReps_)

step_3.addLoads(loads = loads_, loadReps = loadReps_)

loadforcecomponent2 = apex.environment.getLoadForceComponent(name = "Force 2")
loads_.append(loadforcecomponent2)
loadReps_.append(loadforcecomponent2)

step_3.addLoads(loads = loads_, loadReps = loadReps_)


loadCase_ = scenario1.getLoadCase(name = "Load Case 1")
step_ = loadCase_.getStep(name = "Static Step 1")
stepSettings_1_pathName = step_.pathName
stepSettings_1 = apex.studies.NastranSol400StepSettingsStatic(
    id = 1,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)
step_ = loadCase_.getStep(name = "Static Step 2")
stepSettings_2_pathName = step_.pathName
stepSettings_2 = apex.studies.NastranSol400StepSettingsStatic(
    id = 2,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)
step_ = loadCase_.getStep(name = "Static Step 3")
stepSettings_3_pathName = step_.pathName
stepSettings_3 = apex.studies.NastranSol400StepSettingsStatic(
    id = 3,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)


# Cargas 2 para análisis en F06
loadCase1 = scenario_1.addLoadCase(
    name = "Load Case 2",
    description = "",
    stepNumber = 3
)

loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
boltPreload1 = apex.environment.getPreloadBolt(name = "Bolt Preload 1")
loads_.append(boltPreload1)
boltPreloadRep1 = boltPreload1.getActiveRep()
loadReps_.append(boltPreloadRep1)
loadcase_1 = scenario_1.getLoadCase(name="Load Case 2")
step_1 = loadcase_1.getStep(name="Static Step 1")
step_1.addLoads(loads = loads_, loadReps = loadReps_)
loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
boltPreload1 = apex.environment.getPreloadBolt(name = "Bolt Preload 1")
loads_.append(boltPreload1)
boltPreloadRep1 = boltPreload1.getActiveRep()
loadReps_.append(boltPreloadRep1)
step_2 = loadcase_1.getStep(name="Static Step 2")
step_2.addLoads(loads = loads_, loadReps = loadReps_)
loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
boltPreload1 = apex.environment.getPreloadBolt(name = "Bolt Preload 1")
loads_.append(boltPreload1)
boltPreloadRep1 = boltPreload1.getActiveRep()
loadReps_.append(boltPreloadRep1)
step_3 = loadcase_1.getStep(name="Static Step 3")
step_3.addLoads(loads = loads_, loadReps = loadReps_)

loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
loadforcecomponent1 = apex.environment.getLoadForceComponent(name = "Force 1")
loads_.append(loadforcecomponent1)
loadReps_.append(loadforcecomponent1)
step_2.addLoads(loads = loads_, loadReps = loadReps_)
loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
loadforcecomponent1 = apex.environment.getLoadForceComponent(name = "Force 1")
loads_.append(loadforcecomponent1)
loadReps_.append(loadforcecomponent1)
step_3.addLoads(loads = loads_, loadReps = loadReps_)

loads_ = apex.EntityCollection()
loadReps_ = apex.EntityCollection()
loadforcecomponent1 = apex.environment.getLoadForceComponent(name = "Force 2")
loads_.append(loadforcecomponent1)
loadReps_.append(loadforcecomponent1)
step_3.addLoads(loads = loads_, loadReps = loadReps_)

constraints_ = apex.EntityCollection()
constraint_1 = apex.environment.getConstraint( name = "Constraint 1" )
constraints_.append(constraint_1)
step_1.addConstraints(constraints = constraints_)
constraints_ = apex.EntityCollection()
constraint_1 = apex.environment.getConstraint( name = "Constraint 1" )
constraints_.append(constraint_1)
step_2.addConstraints(constraints = constraints_)
constraints_ = apex.EntityCollection()
constraint_1 = apex.environment.getConstraint( name = "Constraint 1" )
constraints_.append(constraint_1)
step_3.addConstraints(constraints = constraints_)

loadCase_ = scenario1.getLoadCase(name = "Load Case 2")
step_ = loadCase_.getStep(name = "Static Step 1")
stepSettings_4_pathName = step_.pathName
stepSettings_4 = apex.studies.NastranSol400StepSettingsStatic(
    id = 4,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)
step_ = loadCase_.getStep(name = "Static Step 2")
stepSettings_5_pathName = step_.pathName
stepSettings_5 = apex.studies.NastranSol400StepSettingsStatic(
    id = 5,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)
step_ = loadCase_.getStep(name = "Static Step 3")
stepSettings_6_pathName = step_.pathName
stepSettings_6 = apex.studies.NastranSol400StepSettingsStatic(
    id = 6,
    stepSettingMethod = apex.studies.StepSettingMethod.Smart,
    predefinedOption = apex.studies.PredefinedOption.QLinear,
    incrementalScheme = apex.studies.IncrementalScheme.Fixed
)

#

stepSettings_ = {
    stepSettings_1_pathName:stepSettings_1,
    stepSettings_2_pathName:stepSettings_2,
    stepSettings_3_pathName:stepSettings_3,
    stepSettings_4_pathName:stepSettings_4,
    stepSettings_5_pathName:stepSettings_5,
    stepSettings_6_pathName:stepSettings_6
}
interactionControl_ = apex.studies.InteractionControl(
    contactMethod = apex.studies.ContactMethod.NodeToSegment,
    normalAugmentationMethod = apex.studies.AugmentationMethod.NotUse,
    normalScaleFactor = 1.,
    tangentAugmentationMethod = apex.studies.AugmentationMethod.NotUse,
    tangentScaleFactor = 1.,
    frictionType = apex.studies.FrictionType.BilinearCoulomb,
    nonSymmetricFrictionMatrix = False,
    linearContact = False,
    linearContactLargeDisplacement = False,
    enablePermanentGlue = True,
    ignoreShellThickness = False,
    separationMethod = apex.studies.SeparationMethod.Force,
    separationIn = apex.studies.SeparationIn.Current,
    notAllowedSeparateNewlyContactedNode = False,
)
controlSettingsObject = apex.studies.SolverControlSettingsNastran(nodeForWeightGeneration = -1,
    maxRunTime = 0.0,
    maxPrintLines = 0,
    unitSystem = "mm-t-s-N-K",
    automaticConstraints = True,
    shellNormalTolerance = 0.0,
    plateStiffnessFactor = 0.0,
    wtmass = 0.0,
    exportAbstractions = False,
    exportWideFormat = False,
    exportHierarchicalFiles = False,
    massCalcuationMethod = apex.studies.MassCalculationMethod.Coupled,
    dataDeckEcho = apex.studies.DataDeckEcho.Unset,
    resultOutputType = apex.attribute.NastranResultOutputType.Hdf5,
    exportProperty = apex.ExportProperty.AsDefined)
simulationSettings_ = apex.studies.SimulationSettingsNastranSol400(
    interactionControl = interactionControl_,
    stepSettings = stepSettings_,
    solverControlSettings = controlSettingsObject
)
scenario1.simulationSettings = simulationSettings_
stepSettings_ = {
    stepSettings_1_pathName:stepSettings_1
}
simulationSettings_.stepSettings = stepSettings_
study = apex.getPrimaryStudy()
scenario1 = study.getScenario( name = "Nonlinear Scenario 1" )
scenario1.exportFEModel(
    filename = os.path.join(path_analisis, "Nonlinear Scenario.bdf"),
    unitSystem = "mm-t-s-N-K-deg",
    exportProperty = apex.ExportProperty.AsDefined
 )

# Preparar lectura F06
meshs = apex.EntityCollection()
meshs = bolt_part.getMeshes()

nodes = apex.EntityCollection()
for mesh in meshs:
    nodes += mesh.getNodes()
loc_nodes = []
for node in nodes:
    loc_n = node.getCoordinates()
    z = loc_n.getZ()
    x = loc_n.getX()
    y = loc_n.getY()
    R = (x**2+y**2)**0.5
    if abs(z)< d/15 and R>d/2*0.99:
        loc_nodes.append(node.id)

elements = apex.EntityCollection()
for mesh in meshs:
    elements += mesh.getElements()

loc_elements = []
for element in elements:
    node_element = []
    node_element += element.getNodeIds()
    set_list2 = {int(value) for value in loc_nodes}
    common_count = sum(1 for value in node_element if value in set_list2) # Que los 4 nodos pertenezcan al elemento
    if common_count >= 4:
        loc_elements.append(element.id)
nombre_archivo = os.path.join(path_analisis, "Lectura_Nastran.txt")
with open(nombre_archivo, 'w') as archivo:
    for item in loc_elements:
        archivo.write(f"{item}\n")

# ANÁLISIS CON NASTRAN, Y OBTENCIÓN DE RESULTADOS EN EL F06
Nastran_T.main()

# POSTPROCESADO
study = apex.getPrimaryStudy()
scenario = study.getScenario(name = "Nonlinear Scenario 1")
scenario.attachNastranResults(
    resultsFilename = os.path.join(path_analisis, "nonlinear scenario.h5"),
    unitSystenName = "mm-t-s-N-K-deg",
    )


result = apex.session.displayMeshCracks( False )

result = apex.session.display2DSpans( False )

result = apex.session.display3DSpans( False )

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
scenario1 = study.getScenario(name = "Nonlinear Scenario 1")
executedscenario_1 = scenario1.getLastExecutedScenario()
step_1 = executedscenario_1.getStep(pathName = executedscenario_1.getPath() + "/Loadcase 0")
event_1 = executedscenario_1.getEvent(pathName = step_1.getPath() + "/Step 0")
stateplot_1 = apex.post.createStatePlot(
    event = event_1,
    resultDataSetIndex = [1]
)

visualizationTarget1 = apex.entityCollection()
study = apex.getPrimaryStudy()
scenario1 = study.getScenario(name = "Nonlinear Scenario 1")
executedscenario_1 = scenario1.getLastExecutedScenario()
visualizationTarget1.append( executedscenario_1.getAssembly( pathName = apex.currentModel().name + "/ar:Model Assembly_Default Rep" ))
deformvisualization_1 = stateplot_1.createDeformVisualization(
    target = visualizationTarget1,
    deformScalingMethod = apex.post.DeformScalingMethod.Absolute,
    absoluteScalingFactor = 1.0,
    displayUnit = "mm"
)