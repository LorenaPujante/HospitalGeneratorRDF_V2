from classes import *
from alphabets import *
from makerRoomsBeds import setBeds

from makerAreasCorridors import *
from makerRoomsBeds import *

import re

###############################################################
#  All Functions related to the creation of FLOOR 0 are here  #
###############################################################


################################
# UNIDADES Y SERVICIOS VANILLA #
################################

def createServicesAndHospUnits_Vanilla_v2(index):
    dicServices = {}
    dicHospUnits = {}

    # ER
    s = Service(index, "Emergency Service", "ER")
    dicServices[s.id] = s
    index += 1
    u = HospUnit(index, "Emergency Unit", "ERU")
    u.service = s
    dicHospUnits[u.id] = u
    index += 1
    s.hospUnits.append(u.id)

    # ICU
    s = Service(index, "Intensive Care Unit Service", "ICU")
    dicServices[s.id] = s
    index += 1
    u = HospUnit(index, "Intensive Care Unit", "ICUU")
    u.service = s
    dicHospUnits[u.id] = u
    index += 1
    s.hospUnits.append(u.id)
    
    # RAD
        # 1 Servicio
        # 6 HUs:
    s = Service(index, "Radiology Service", "RAD")
    dicServices[s.id] = s
    index += 1
    #
    for i in range(6):
        u = HospUnit(index, "Radiology Unit {}".format(i), "RADU{}".format(i))
        u.service = s
        dicHospUnits[u.id] = u
        index += 1
        s.hospUnits.append(u.id)

    # SURG
        # 17 Servicios (tantos como Servicios normales)
        # 1 HU por Servicio
        # 27 Quirófanos
    '''for i in range(18):
        s = Service(index, "Surgery Service {}".format(i), "SURG{}".format(i))
        dicServices[s.id] = s
        index += 1
        
        u = HospUnit(index, "Surgery Unit {}".format(i), "SURGU{}".format(i))
        u.service = s
        dicHospUnits[u.id] = u
        index += 1
        s.hospUnits.append(u.id)'''

    return dicServices, dicHospUnits, index



###########
# FLOOR 0 #
###########

def createFloor0_v2(index, dicBuildings, dicHospUnits, dicRooms, dicBeds, roomsER, roomsIC):
    dicFloors = {}
    floor = Floor(index, "f0")
    index += 1
    dicFloors[floor.id] = floor

    # Assign HUs [ERU, ICUU, RADU, SURGU]
    for hu in dicHospUnits.values():
        if hu.abrev.startswith('ERU')  or  hu.abrev.startswith('ICUU')  or  hu.abrev.startswith('RADU')  or  hu.abrev.startswith('SURGU'):
            floor.hospUnits.append(hu)
    
    layout = ['A0','J1','J1', 'J0','J0'],['J0','J0','J0', 'J1','J1']
    nRows = 2
    nColumns = 5

    # Create Units and Blocks
    dicUnits, index = createUnits(nRows,index,floor)
    dicBlocks, index = createBlocks(nColumns,index,floor)

    # Create Areas
    dicAreas, gridAreas, index = createAreas(layout, nRows, nColumns, index, floor, dicUnits, dicBlocks)
    
    # Create Corridors
    dicCorridors, index = createCorridors(gridAreas, nRows, nColumns, index)
    
    # Assign Rooms
    # Rooms must be in this order:
    # 1º Surg
    # 2º IC
    # 3º Rad
    # 4º ER
    listRooms = getRoomsF0(floor, dicRooms, roomsER, roomsIC)
    setRooms_v2(nRows, nColumns, gridAreas, listRooms)
    setExternalNeighbors(nRows, nColumns, gridAreas, dicCorridors)

    # Añadir al nombre de la Room el Servicio
    setServicesToRoomsName_f0(dicCorridors, dicRooms)
    
    # Set description and Beds neighbors
    setBeds(listRooms, dicBeds)

    # Add Floor to the Building
    idBuild = list(dicBuildings.keys())[0]   # We can do this because there is only one Building
    dicBuildings[idBuild].floors.append(floor)

    return dicFloors, dicUnits, dicBlocks, dicAreas, dicCorridors, index


def getRoomsF0(floor, dicRooms, roomsER, roomsIC):
    listRooms = []
    
    listRooms_Surg = getSurgRooms(dicRooms)
    listRooms.extend(listRooms_Surg)
    
    listRooms_IC = getRoomsByService_IC_ER(floor, dicRooms, 'ICUU', roomsIC)
    listRooms.extend(listRooms_IC)
    
    listRooms_Rad = getRoomsByService(floor, dicRooms, 'RADU')
    listRooms.extend(listRooms_Rad)
    
    listRooms_ER = getRoomsByService_IC_ER(floor, dicRooms, 'ERU', roomsER)
    listRooms.extend(listRooms_ER)
    
    return listRooms

def getRoomsByService(floor, dicRooms, prefix):
    listRooms = []
    for hu in floor.hospUnits:
        if hu.abrev.startswith(prefix):
            for id in hu.rooms:
                r = dicRooms[id]
                listRooms.append(r)
                
    return listRooms

def getRoomsByService_IC_ER(floor, dicRooms, prefix, roomsER_IC):
    listRooms = []
    for hu in floor.hospUnits:
        if hu.abrev.startswith(prefix):
            for id in hu.rooms:
                if id in roomsER_IC:
                    r = dicRooms[id]
                    listRooms.append(r)
                
    return listRooms

def getSurgRooms(dicRooms):
    listRooms = []
    for r in dicRooms.values():
        if r.description.startswith('surgery'):
            listRooms.append(r)
            
    return listRooms


def setServicesToRoomsName_f0(dicCorridors, dicRooms):
    for cKey in dicCorridors.keys():
        corrDesc = dicCorridors[cKey].description
        if wordInName('a0A', corrDesc) or wordInName('a1A', corrDesc) or wordInName('a2A', corrDesc):
            for i in range(len(dicCorridors[cKey].rooms)):
                setServiceToRoomsName(dicCorridors, dicRooms, cKey, i, 'SURG')
        
        elif wordInName('a3A', corrDesc) or wordInName('a4A', corrDesc):
            for i in range(len(dicCorridors[cKey].rooms)):
                setServiceToRoomsName(dicCorridors, dicRooms, cKey, i, 'IC')

        if wordInName('a0B', corrDesc) or wordInName('a1B', corrDesc) or wordInName('a2B', corrDesc):
            for i in range(len(dicCorridors[cKey].rooms)):
                setServiceToRoomsName(dicCorridors, dicRooms, cKey, i, 'RAD')
        
        elif wordInName('a3B', corrDesc) or wordInName('a4B', corrDesc):
            for i in range(len(dicCorridors[cKey].rooms)):
                setServiceToRoomsName(dicCorridors, dicRooms, cKey, i, 'ER')

def wordInName(word, roomDesc):
    m = re.search(word, roomDesc)
    return m

def setServiceToRoomsName(dicCorridors, dicRooms, cKey, ind, servAbrev):
    nameRoom = dicRooms[dicCorridors[cKey].rooms[ind].id].description
    nameRoom_end = nameRoom[1:]
    nameRoom = "r{}{}".format(servAbrev, nameRoom_end)
    dicRooms[dicCorridors[cKey].rooms[ind].id].description = nameRoom



def setRooms_v2(nRows, nColumns, gridAreas, listRooms):
    indRooms = 0
    for i in range(nRows):
        for j in range(nColumns):
            area = gridAreas[i][j]  

            match area.type:
                case "A0":
                    listRoomsRes, indRooms = setRoomsToListRooms(7, listRooms, indRooms)
                    setRooms_A0(listRoomsRes, area.corridorsHoriz, area.corridorsVert)
                
                case "J0":
                    if j in [3,4]:
                        listRoomsRes, indRooms = setRoomsToListRooms_ER_IC(2, listRooms, indRooms)
                        setRooms_J0J1_ER_IC(listRoomsRes, area.corridorsHoriz)
                    else:
                        listRoomsRes, indRooms = setRoomsToListRooms(8, listRooms, indRooms)
                        setRooms_J0(listRoomsRes, area.corridorsHoriz)
                case "J1":
                    if j in [3,4]:
                        listRoomsRes, indRooms = setRoomsToListRooms_ER_IC(2, listRooms, indRooms)
                        setRooms_J0J1_ER_IC(listRoomsRes, area.corridorsHoriz)
                    else:
                        listRoomsRes, indRooms = setRoomsToListRooms(10, listRooms, indRooms)
                        setRooms_J1(listRoomsRes, area.corridorsHoriz)
                
def setRooms_J0J1_ER_IC(listRooms, corridorsHoriz):    # TODO
    p = corridorsHoriz[0]
    for i in range(2):
        r = listRooms[i]
        desc = "r{}_{}".format(i,p.description)
        r.description = desc
        r.parent = p.id
        p.rooms.append(r)   

    # Border rooms
    corridorsHoriz[0].roomsBorder['leftTop'] = listRooms[0]
    corridorsHoriz[0].roomsBorder['leftBottom'] = listRooms[1]
    corridorsHoriz[0].roomsBorder['rightTop'] = listRooms[0]
    corridorsHoriz[0].roomsBorder['rightBottom'] = listRooms[1] 
 
    # Opposite
    listRooms[0].opposite.append(listRooms[1].id)
    listRooms[1].opposite.append(listRooms[0].id)

    # Internal neighbours   ->  NOTHING


def setRoomsToListRooms_ER_IC(nRoomsType, listRooms, indRooms):
    if len(listRooms[indRooms].beds) == 0:   # La primera Room es la que se ha creado generica con el id de la entrada
        indRooms += 1
    
    return setRoomsToListRooms(nRoomsType, listRooms, indRooms)


def deleteAuxiliarRooms_ER_IC(dicRooms, dicServices, dicHospUnits):
    roomsToDeleteER = []
    roomsToDeleteIC = []
    for r in dicRooms.values():
        if len(r.beds)==0:
            if r.description=='er':
                roomsToDeleteER.append(r.id)
            elif r.description=='icu':
                roomsToDeleteIC.append(r.id)
        
    for s in dicServices.values():
        if s.abrev == "ER":
            for r in roomsToDeleteER:
                s.rooms.remove(r)
        if s.abrev == "ICU":
            for r in roomsToDeleteIC:
                s.rooms.remove(r)

    for hu in dicHospUnits.values():
        if hu.abrev == "ERU":
            for r in roomsToDeleteER:
                hu.rooms.remove(r)
        if hu.abrev == "ICUU":
            for r in roomsToDeleteIC:
                hu.rooms.remove(r)    

    for rId in roomsToDeleteER:
        dicRooms.pop(rId)
    for rId in roomsToDeleteIC:
        dicRooms.pop(rId)