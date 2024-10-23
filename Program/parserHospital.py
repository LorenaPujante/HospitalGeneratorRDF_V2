from classes import *
from alphabets import *


def parseHospital(dicHospUnits, dicServices, dicServsHusRooms, index):

    # Results
    dicRooms = {}
    dicBeds = {}

    # Control parameters
    parent = False
    children = False
    neighbours = False
    nService = 0   # For the name of the new Services
    currentId = -1
    currentType = -1
    
    listHospUnitsIds = list(dicHospUnits.keys())
    listServicesIds = list(dicServices.keys())
    
    indHURad_Room = 0
    nRoomsRad = 0
    indHURad_Bed = 0
    nBedsRad = 0
    nRoomSurg = 0

    roomsER = []
    indRoomER = 0
    nBedsER = 0
    roomsIC = []
    indRoomICU = 0
    nBedsICU = 0
    
    '''Open hospital.txt'''
    with open(".\\Input\\hospital.txt") as file:
        for line in file:
            
            line = str(line)

            # Read file with input hospital layout 
            if (not parent and not children and not neighbours):
                if (line == "children\n"):
                    children = True
                elif (line == "neighbours\n"):
                    neighbours = True  
                elif (line == "parent\n"):
                    parent = True
                else:
                    line = line.split('\n')
                    line = line[0]
                    words = line.split(",")
                    id = int(words[0])
                    type = int(words[1])
                    
                    currentType = type
                    currentId = id

                    if (type==6):    # Create Service
                        s = Service(id, "Service {}".format(nService), "S{}".format(nService))
                            
                            # Hospitalization Units are created and associated with the Service 
                        hospUnitsServ = []
                        
                        nHUs = len(dicServsHusRooms[nService])
                        for i in range(nHUs):
                        #for i in range(huPerService):
                            index += 1
                            letter = abcCap[i]
                            u = HospUnit(index, "HospUnit {}{}".format(nService, letter), "HU{}{}".format(nService, letter))
                            u.service = s
                            dicHospUnits[u.id] = u
                            hospUnitsServ.append(u.id)

                        s.hospUnits = hospUnitsServ
                        
                        dicServices[id] = s
                        nService += 1

                    elif (type==1 or type==4 or type==5 or type==3):   # Create Rooms (without name)
                        r = Room(id,"")

                        if (type==1):    # The ER HospUnit and Service are associated with the Room
                            # Creamos 1 Room auxilar con el id leído en hospital.txt
                            r.description = 'er'
                            r.type = TypeBed.ER
                            r.hospUnit = listHospUnitsIds[0]
                            dicHospUnits[listHospUnitsIds[0]].rooms.append(id)
                            dicServices[listServicesIds[0]].rooms.append(r.id)

                            # Creamos 4 Rooms
                            for i in range(4):
                                index += 1
                                rAux = Room(index,"")
                                rAux.description = "er"
                                rAux.type = TypeBed.ER
                                rAux.hospUnit = listHospUnitsIds[0]
                                
                                dicHospUnits[listHospUnitsIds[0]].rooms.append(rAux.id)
                                dicServices[listServicesIds[0]].rooms.append(rAux.id)
                                dicRooms[rAux.id] = rAux

                                roomsER.append(rAux.id)

                        elif (type==5):  # The ICU HospUnit and Service are associated with the Room
                            # Creamos 1 Room auxilar con el id leído en hospital.txt
                            r.description = "icu"
                            r.type = TypeBed.ICU
                            r.hospUnit = listHospUnitsIds[1]
                            dicHospUnits[listHospUnitsIds[1]].rooms.append(id)
                            dicServices[listServicesIds[1]].rooms.append(r.id)

                            # Creamos 4 Rooms
                            for i in range(4):
                                index += 1
                                rAux = Room(index,"")
                                rAux.description = "icu"
                                rAux.type = TypeBed.ICU
                                rAux.hospUnit = listHospUnitsIds[1]

                                dicHospUnits[listHospUnitsIds[1]].rooms.append(rAux.id)
                                dicServices[listServicesIds[1]].rooms.append(rAux.id)
                                dicRooms[rAux.id] = rAux

                                roomsIC.append(rAux.id)
                        
                        elif (type==3): # The Radiology HospUnit and Service are associated with the Room
                            r.description = "rad"
                            r.type = TypeBed.Radiology
                            # RADIOLOGY
                            # 6 HUs:
                            # - 1 HU con 8 Rooms
                            # - 3 HUs con 4 Rooms
                            # - 2 HUs con 2 Rooms
                            if indHURad_Room == 0:
                                
                                r.hospUnit = listHospUnitsIds[2+indHURad_Room]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Room]].rooms.append(id)
                                dicServices[listServicesIds[2]].rooms.append(id)

                                if nRoomsRad == 7:
                                    nRoomsRad = 0
                                    indHURad_Room += 1
                                else:
                                    nRoomsRad += 1

                            elif indHURad_Room in [1,2,3]:
                                r.hospUnit = listHospUnitsIds[2+indHURad_Room]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Room]].rooms.append(id)
                                dicServices[listServicesIds[2]].rooms.append(id)

                                if nRoomsRad == 3:
                                    nRoomsRad = 0
                                    indHURad_Room += 1
                                else:
                                    nRoomsRad += 1

                            elif indHURad_Room in [4,5]:
                                r.hospUnit = listHospUnitsIds[2+indHURad_Room]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Room]].rooms.append(id)
                                dicServices[listServicesIds[2]].rooms.append(id)

                                if nRoomsRad == 1:
                                    nRoomsRad = 0
                                    indHURad_Room += 1
                                else:
                                    nRoomsRad += 1

                            
                        dicRooms[id] = r

                    elif (type==2 or type==7):     # Create Beds (no name)    
                        b = Bed(id,"")
                            
                        if (type==2):       # SURGERY
                                # Create Surgery Room for the the Bed  
                            index += 1
                            r = Room(index, "surgery {}".format(nRoomSurg))
                            r.type = TypeBed.Surgery
                            nRoomSurg += 1
                            dicRooms[index] = r
                            r.beds.append(b.id)
                            b.parent = r.id

                            b.type = TypeBed.Surgery
                            
                        dicBeds[id] = b


            # line with the parent
            elif (parent):      
                if (currentType == 7): # Beds. They have as a parent: Room, ER(Room), ICU(Room), RAD(Room)
                    line = line.split('\n')
                    line = line[0]
                    words = line.split(",")
                    idParent = int(words[0])
                    typeParent = int(words[1])

                    if typeParent in [1,5]: # ER o ICU
                        
                        if typeParent == 1:   # ER   
                            # 4 ROOMS CON 4 BEDS CADA UNA
                            b.type = TypeBed.ER  
                            dicBeds[currentId].hospUnit = listHospUnitsIds[0] 

                            idParentv2 = roomsER[indRoomER]
                            dicBeds[currentId].parent = idParentv2
                            dicRooms[idParentv2].beds.append(currentId)

                            nBedsER += 1
                            if nBedsER == 5:
                                nBedsER = 0
                                indRoomER += 1

                        elif typeParent == 5:     # ICU
                            # 4 ROOMS CON 5 BEDS CADA UNA
                            b.type = TypeBed.ICU
                            dicBeds[currentId].hospUnit = listHospUnitsIds[1]

                            idParentv2 = roomsIC[indRoomICU]
                            dicBeds[currentId].parent = idParentv2
                            dicRooms[idParentv2].beds.append(currentId)

                            nBedsICU += 1
                            if nBedsICU == 4:
                                nBedsICU = 0
                                indRoomICU += 1
                    else:
                        dicBeds[currentId].parent = idParent
                        dicRooms[idParent].beds.append(currentId)

                        if typeParent == 3:   # RAD
                            # RADIOLOGY
                                # 6 HUs:
                                # - 1 HU con 8 Rooms
                                # - 3 HUs con 4 Rooms
                                # - 2 HUs con 2 Rooms
                            if indHURad_Bed == 0:
                                b.type = TypeBed.Radiology
                                dicBeds[currentId].hospUnit = listHospUnitsIds[2+indHURad_Bed]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Bed]].beds.append(b.id) 

                                if nBedsRad == 7:
                                    nBedsRad = 0
                                    indHURad_Bed += 1
                                else:
                                    nBedsRad += 1

                            elif indHURad_Bed in [1,2,3]:
                                b.type = TypeBed.Radiology
                                dicBeds[currentId].hospUnit = listHospUnitsIds[2+indHURad_Bed]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Bed]].beds.append(b.id) 

                                if nBedsRad == 3:
                                    nBedsRad = 0
                                    indHURad_Bed += 1
                                else:
                                    nBedsRad += 1

                            elif indHURad_Bed in [4,5]:
                                b.type = TypeBed.Radiology
                                dicBeds[currentId].hospUnit = listHospUnitsIds[2+indHURad_Bed]
                                dicHospUnits[listHospUnitsIds[2+indHURad_Bed]].beds.append(b.id) 

                                if nBedsRad == 1:
                                    nBedsRad = 0
                                    indHURad_Bed += 1
                                else:
                                    nBedsRad += 1
                        
                elif (currentType == 4):  # Rooms. They have as a parent: Service -> Not their parent
                    line = line.split('\n')
                    line = line[0]
                    words = line.split(",")
                    idParent = int(words[0])

                    dicServices[idParent].rooms.append(currentId)

                parent = False
                

            # With these types of lines we do NOTHING
            elif (children):
                if (line == "children_end\n"):
                    children = False
            elif (neighbours):
                if (line == "neighbours_end\n"):
                    neighbours = False
                

    '''Close hospital.txt'''
    file.close()


    return dicBeds, dicRooms, roomsER, roomsIC, index 



def getNumHUsAndRoomsPerOrdService():

    dicServsHusRooms = {}

    '''Open roomsHU.txt'''
    with open(".\\Input\\roomsHU.txt") as file:
        for line in file:
            line = str(line)

            line = line.split('\n')
            line = line[0]
            words = line.split(",")
            serv = int(words[0])
            nRooms = int(words[2])

            if serv not in dicServsHusRooms:
                dicServsHusRooms[serv] = []
            dicServsHusRooms[serv].append(nRooms)

    '''Close hospital.txt'''
    file.close()

    return dicServsHusRooms

def createSurgeryHUs(dicHospUnits, dicServices, index):
    husSurgery = {}
    for s in dicServices.values():
        if not s.abrev.startswith('RAD') and not s.abrev.startswith('SURG'):

            # Create a Unit for the surgeries
            u = HospUnit(index, "Surgery Unit {}".format(s.abrev), "SURGU_{}".format(s.abrev))
            u.service = s
            dicHospUnits[u.id] = u
            index += 1
            s.hospUnits.append(u.id)

            husSurgery[s.id] = u.id

    return husSurgery, index




def getLastIndexHospital():

     # Control parameters
    parent = False
    children = False
    neighbours = False

    biggestId = 0

    '''Open hospital.txt'''
    with open(".\\Input\\hospital.txt") as file:
        for line in file:
            line = str(line)

            if (not parent and not children and not neighbours):
                if (line == "children\n"):
                    children = True
                elif (line == "neighbours\n"):
                    neighbours = True  
                elif (line == "parent\n"):
                    parent = True
                
                else:
                    line = line.split('\n')
                    line = line[0]
                    words = line.split(",")
                    id = int(words[0])
                    if biggestId < id:
                        biggestId = id


            # With these types of lines we do NOTHING
            elif (parent):      
                parent = False
            elif (children):
                if (line == "children_end\n"):
                    children = False
            elif (neighbours):
                if (line == "neighbours_end\n"):
                    neighbours = False
    
    '''Close hospital.txt'''
    file.close()
    
    return id
