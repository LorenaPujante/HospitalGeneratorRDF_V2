
from classes import *

def createLogicZones(dicAreas0, index):
    dicLogicZones = {}
    index = createLogicZone("LogicZone_ICU", TypeBed.ICU, dicAreas0, dicLogicZones, index)
    index = createLogicZone("LogicZone_ER", TypeBed.ER, dicAreas0, dicLogicZones, index)
    index = createLogicZone("LogicZone_Surgery", TypeBed.Surgery, dicAreas0, dicLogicZones, index)
    index = createLogicZone("LogicZone_Radiology", TypeBed.Radiology, dicAreas0, dicLogicZones, index)
    
    return dicLogicZones, index
    


def createLogicZone(name, type, dicAreas0, dicLogicZones, index):

    lz = LogicZone(index, name)
    index += 1

    for area in dicAreas0.values():
        # Como  en la Floor_0 no hay Areas con distintos tipos de habitaciones, se puede hacer esto
        corridors = []
        if len(area.corridorsHoriz) != 0:
            corridors = area.corridorsHoriz
        else:
            corridors = area.corridorsVert
        c0 = corridors[0]
        r0 = c0.rooms[0]
        if r0.type == type:
            lz.areas.append(area.id)

    dicLogicZones[lz.id] = lz
    
    return index

