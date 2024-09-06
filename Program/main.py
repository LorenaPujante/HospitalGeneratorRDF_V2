from datetime import datetime
from mainAuxFunctions import *
from readInputParams import *
from parserHospital import *
from parserPatients import parsePatients
from parserSteps import *
from makerFloors import *
from makerFloor0 import *
from makerLogicZones import *
from writerCSV import *
from writerRDF import *
from writerRDF_star import *
from writerSummary import *
from writerUnion import unionFiles


############
##  MAIN  ##
############

def main(index, huPerService, nFloors, huPerFloor, nRows, nColumns, startDateTime, optionFloorHU):

    # Input of index to start numbering the objects that are created
    #index = readIndex()
    
    # Input of HospitalizationUnits per Service
    #huPerService = readHospitalizationUnitsPerServicio()
    
    # Create vanilla Services and HospUnits
    dicServices, dicHospUnits, index = createServicesAndHospUnits_Vanilla_v2(index)
    
    # Dictionary where each ordinary Service has a list with the number of Rooms of each HU
    dicServsHusRooms = getNumHUsAndRoomsPerOrdService()
    
    # PARSE OF THE INPUT
    dicBeds, dicRooms, roomsER, roomsIC, index = parseHospital(dicHospUnits, dicServices, huPerService, dicServsHusRooms, index)

    # CREATE SURGERY UNITS FOR ALL THE SERVICES EXCEPT RADIOLOGY (AND SURGERY)
    husSurgery, index = createSurgeryHUs(dicHospUnits, dicServices, index)
    
    # The Service Rooms are distributed equally among its HospUnits
    # The Beds in each Room belong to its HospUnit
    setRooms_In_HospitalizationUnit_v2(dicServsHusRooms, dicServices, dicHospUnits, dicRooms, dicBeds)
    

    # Create Building
    dicBuildings, index = createBuilding(index)

    # Filter HUs that are not [ICUU, ERU, RadU, Surgerys]
    list_Ord_HU = getOrd_HU(dicHospUnits)
    n_ord_HU = len(list_Ord_HU)


    # Request number of Hospitalization Units per Floor
    if huPerFloor>n_ord_HU:
        raise ReadHUPerFloorError(None)


    # Create and populate Floor_0
    dicFloors0, dicUnits0, dicBlocks0, dicAreas0, dicCorridors0, index = createFloor0_v2(index, dicBuildings, dicHospUnits, dicRooms, dicBeds, roomsER, roomsIC)

    # NEW
    # CREATE LOGIC ZONES FOR OPERATING ROOMS, X-RAY ROOMS, ICU ROOMS AND EMERGENCY ROOMS
    dicLogicZones, index = createLogicZones(dicAreas0, index)
    
    # Create Ordinary Floors and associate their HospUnits with them 
    dicOrdFloors, index = createOrdFloors_v2(nFloors-1, huPerFloor, list_Ord_HU, index, dicBuildings)


    # Populate Ord Floors
    dicOrdUnits, dicOrdBlocks, dicOrdAreas, dicOrdCorridors, index = populateOrdFloors(dicOrdFloors, nRows, nColumns, dicBuildings, dicRooms, dicBeds, index)

    # Se puede eliminar las Rooms auxiliares creadas para ER e IC con los id de hospital.txt
    deleteAuxiliarRooms_ER_IC(dicRooms, dicServices, dicHospUnits) 


    # Join the elements of Ord Floors with those of Floor 0
    dicFloors = {}
    appendDictionarys(dicFloors0, dicFloors)
    appendDictionarys(dicOrdFloors, dicFloors)
    dicUnits = {}
    appendDictionarys(dicUnits0, dicUnits)
    appendDictionarys(dicOrdUnits, dicUnits)
    dicBlocks = {}
    appendDictionarys(dicBlocks0, dicBlocks)
    appendDictionarys(dicOrdBlocks, dicBlocks)
    dicAreas = {}
    appendDictionarys(dicAreas0, dicAreas)
    appendDictionarys(dicOrdAreas, dicAreas)
    dicCorridors = {}
    appendDictionarys(dicCorridors0, dicCorridors)
    appendDictionarys(dicOrdCorridors, dicCorridors)

    
    # PATIENTS 
    dicPatients = parsePatients()
    
    # MICROORGANISMS
    # A dummy Microorganism is created, since only one will be detected
    dicMicroorganisms = {}
    microorg = Microorganism(index, "Microorg1") 
    dicMicroorganisms[microorg.id] = microorg
    index += 1

    
    # STEPS
    lastStep = parseSteps(dicPatients)
    index = createEpisodesAndEventsPerPacient(dicPatients, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, startDateTime, index)
        # TestMicro
    #index = createTestMicro_positive_StartInfectious(dicPatients, dicMicroorganisms, startDateTime, index)     # TestMicro happens at the step in which the Patient becomes Infectious 
    index = createTestMicro_positive_DuringInfectious(dicPatients, dicMicroorganisms, startDateTime, index)
    #index = createTestMicro_negative_StartRecovered(dicPatients, dicMicroorganisms, startDateTime, index)
    index = createTestMicro_negative_During24HoursRecovered(dicPatients, dicMicroorganisms, startDateTime, index)
    


    keysPatients = list(dicPatients.keys())
    keysPatients.sort()
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("First patient: {}".format(keysPatients[0]))
    print("Last patient: {}".format(keysPatients[len(keysPatients)-1]))

    print("Range Steps: [0, {}] \n".format(lastStep))
    

    
    # PRINT SUMMARIES
    setFolderSummary(".\\OutputSummary")
    printSummaryHospital(nFloors, dicFloors, dicBeds)
    printEpisodeSummary(dicPatients, startDateTime)
    print(" * Summary Files : Completed")
    
    
    # PRINT CSV
    setFolderOutputCSV(".\\OutputCSV")
    printCSV(dicServices, dicHospUnits, dicBuildings, dicFloors, dicUnits, dicBlocks, dicAreas, dicCorridors, dicRooms, dicBeds, dicLogicZones, dicPatients, dicMicroorganisms)
    print(" * CSV Files : Completed")

    # PRINT NT
    dirNT = ".\\OutputRDF"
    setFolderOutputRDF(dirNT)
    printRDF(dicServices, dicHospUnits, dicBuildings, dicFloors, dicUnits, dicBlocks, dicAreas, dicCorridors, dicRooms, dicBeds, dicLogicZones, dicPatients, dicMicroorganisms)
    print(" * RDF Files : Completed")
            # File union
    unionFiles(dirNT, False)


    # PRINT NT-Star
    dirNT_star = ".\\OutputRDF_star"
    setFolderOutputRDFstar(dirNT_star)
    printRDF_star(dicServices, dicHospUnits, dicBuildings, dicFloors, dicUnits, dicBlocks, dicAreas, dicCorridors, dicRooms, dicBeds, dicLogicZones, dicPatients, dicMicroorganisms)
    print(" * RDF-star Files : Completed")
        # File union
    unionFiles(dirNT_star, True)
    
    print("\nDONE!")



if __name__ == '__main__':
    
    ''' MAIN '''

    print("Last id Hospital Input: {}\n".format(getLastIndexHospital()))


    # PARAMS
            # The folders where the result files are created are not parameters     
    index = 1200
    huPerService = 2
    nFloors = 4
    huPerFloor = 13
    nRows = 2
    nColumns = 4
    startDateTime = datetime(2023,1,1,8,0,0)    # 01-01-2023 08:00:00   # dd/mm/yyyy HH:MM:SS
    optionFloorUH = 2 #None    # If None, then the option will be asked by terminal

    params = []
    paramsLinea = []
    paramsLinea.append(index)
    paramsLinea.append(huPerService)
    paramsLinea.append(nFloors)
    paramsLinea.append(huPerFloor)
    paramsLinea.append(nRows)
    paramsLinea.append(nColumns)
    paramsLinea.append(startDateTime)
    paramsLinea.append(optionFloorUH)
    params.append(paramsLinea)

    main(params[0][0], params[0][1], params[0][2], params[0][3], params[0][4], params[0][5], params[0][6], params[0][7])    



