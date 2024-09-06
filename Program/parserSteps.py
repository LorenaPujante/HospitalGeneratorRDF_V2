from classes import *
from datetime import datetime, timedelta
import random
from random import randrange
import math

import sys

def parseSteps(dicPatients):

    step = 0

    with open(".\\Input\\movements.csv") as file:
        for lineString in file:
            
            lineString = str(lineString)
            line = lineString.split(';')
            
            step = int(line[0])

            i = 1
            places = False
            while i<len(line) and not places:
                # line[i]      ->  patient_id
                # line[i+1]    ->  patient_state
                # line[i+2]    ->  locationId
                # line[i+3]    ->  location_infected   :   Don't used
                if line[i]=='places' or line[i+1]=='places' or line[i+2]=='places' or line[i+3]=='places':
                    places = True
                else:
                    patientId = int(line[i])
                    seirdState = int(line[i+1])
                    if seirdState == 4:    # DEATH Event
                        i += 3
                    else:
                        locationId = int(line[i+2])

                        patient = dicPatients[patientId]
                        patient.stepLocations[step] = locationId
                        
                        i += 4 

                        # It is ONLY intended for PATIENTS WITH 1 EPISODE
                    if patient.seird[seirdState] is None:
                            patient.seird[seirdState] = step

                    

    file.close()

    return step



###################################
# CREATION OF EPISODES AND EVENTS #
###################################

def createEpisode(nEpisode, idPatient, start, end, events, index):
    description = "ep{}_p{}".format(nEpisode,idPatient)
    ep = Episode(index, description, start, end)
    ep.events = events
    
    index += 1
    nEpisode += 1
    
    return ep, nEpisode, index

def createEvent(nEvent, nEpisode, idPatient, start, end, location, index, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, events):
    
    if location in dicBeds:
        ev, nEvent, index = createEvent_Bed(nEvent, nEpisode, idPatient, start, end, location, index, dicBeds, dicHospUnits, husSurgery, events)
    elif location in dicRooms:
        ev, nEvent, index = createEvent_Room(nEvent, nEpisode, idPatient, start, end, location, index, dicBeds, dicRooms, dicHospUnits, events)
    elif location in dicServices:
        ev, nEvent, index = createEvent_Service(nEvent, nEpisode, idPatient, start, end, location, index, dicBeds, dicRooms, dicHospUnits, dicServices, events)
     
    return ev, nEvent, index

def createEvent_Bed(nEvent, nEpisode, idPatient, start, end, bedId, index, dicBeds, dicHospUnits, husSurgery, events):
         
    if dicBeds[bedId].type is TypeBed.Surgery:
        type = TypeEvent.Surgery
        # Asignarle la HU de su último evento (siempre que este no fuera de Radiology)
        lastHU = getLastHUNotRadSurg(events)
        if lastHU is None:
            # Si este es el primer Evento (o no hay otros Eventos distintos a Rad/Surg antes), le ponemos una HU dummy y dejamos marcado el Evento para asignarle la HU más tarde
            hu = -1
        else:
            # Se obtiene la HU Surgery del mismo servicio que la hu encontrada
            hu = getHUSurgery(lastHU, dicHospUnits, husSurgery)
            
    else:
        if dicBeds[bedId].type is TypeBed.Radiology:
            type = TypeEvent.Radiology
        else:
            type = TypeEvent.Hospitalization
        # HU
        hu = dicBeds[bedId].hospUnit
    

    # CREAR EVENTO
    description = "ev{}_ep{}_p{}".format(nEvent, nEpisode, idPatient)
    ev = Event(index, description, start, end, bedId, hu, type)

    tupla = (start, end)
    dicBeds[bedId].busy.append(tupla)
    dicBeds[bedId].busy.sort(key = lambda x: x[0]) 

    index += 1
    nEvent += 1

    return ev, nEvent, index


def createEvent_Room(nEvent, nEpisode, idPatient, start, end, roomId, index, dicBeds, dicRooms, dicHospUnits, events):
    if dicRooms[roomId].type is TypeBed.Service:
        type = TypeEvent.Hospitalization
    elif dicRooms[roomId].type is TypeBed.Radiology:
        type = TypeEvent.Radiology
    elif dicRooms[roomId].type is TypeBed.Surgery:
        type = TypeEvent.Surgery

        sys.exit('-1')
    else:
        sys.exit('-2')
    
    # Asignar Bed y HU
    if type.name == "Hospitalization":
        # Comprobar si ha estado en una Bed de la misma Room en algun Evento pasado, estando esta Bed libre
        idBed = isThereSomeFreeBed_InRoom_FromPast(events, dicBeds, roomId, start, end)
        if idBed is None:
            # Comprobar si hay alguna Bed de la misma HU que esté libre
            rHU = dicRooms[roomId].hospUnit
            idBed = isThereSomeFreeBed_InHU(dicHospUnits[rHU], start, end)
            if idBed is None:
                # Comprobar si hay alguna Bed del mismo Servicio que esté libre
                service = dicHospUnits[rHU].service
                idBed = isThereSomeFreeBed_InService(dicBeds, dicRooms, service, start, end)
                if idBed is None:
                    print("createEvent_Room - NO BED EN SERVICIO")
                    sys.exit('-3')
        
        if not isinstance(idBed, int):
            idBed = idBed.id
    
        hu = dicBeds[idBed].hospUnit
                
    elif type.name == "Radiology":
        # Las habitaciones de Radiology solo tienen una Bed     (Si esa está siendo usada... A tomar por culo)
        idBed = dicRooms[roomId].beds[0]
        hu = dicBeds[idBed].hospUnit

    elif type.name == "Surgery":
        sys.exit('-4')

    # DON'T TODO: NO TIENE PINTA DE QUE EN MOVEMENTS.CSV LA GENTE SE HOSPITALICE DIRECTAMENTE EN 'ER' O 'IC'    ->  NO HACE FALTA PONER 2 CASOS PARA ESTE TIPO DE HABITACIONES


    # CREAR EVENTO
    description = "ev{}_ep{}_p{}".format(nEvent, nEpisode, idPatient)
    ev = Event(index, description, start, end, idBed, hu, type)

    tupla = (start, end)
    dicBeds[idBed].busy.append(tupla)
    dicBeds[idBed].busy.sort(key = lambda x: x[0]) 

    index += 1
    nEvent += 1

    return ev, nEvent, index


def createEvent_Service(nEvent, nEpisode, idPatient, start, end, servId, index, dicBeds, dicRooms, dicHospUnits, dicServices, events):
    
    
    if dicServices[servId].description.startswith("Service"):
        type = TypeEvent.Hospitalization
    elif dicServices[servId].abrev.startswith("RAD"):
        type = TypeEvent.Radiology
    elif dicServices[servId].abrev.startswith("SURG"):
        type = TypeEvent.Surgery
        sys.exit('-5')
    else:
        sys.exit('-6')
    

    # Asignar Bed y HU
    if type.name == "Hospitalization":
        # Comprobar si ha estado en una Bed del mismo Servicio en algun Evento pasado, estando esta Bed libre
        idBed = isThereSomeFreeBed_InService_FromPast(events, dicBeds, dicHospUnits, servId, start, end)
        if idBed is None:
            # Comprobar si hay alguna Bed del mism Servicio que esté libre
            idBed = isThereSomeFreeBed_InService(dicBeds, dicRooms, dicServices[servId], start, end)
            if idBed is None:
                print("createEvent_Service - HOSPITALIZATION - NO BED EN SERVICIO")
                sys.exit('-7')
            
        if not isinstance(idBed, int):
            idBed = idBed.id

        hu = dicBeds[idBed].hospUnit
                
    elif type.name == "Radiology":
        # Buscar una Bed del Servicio
        idBed = isThereSomeFreeBed_InService(dicBeds, dicRooms, dicServices[servId], start, end)
        if idBed is None:
            print("createEvent_Service - RADIOLOGY - NO BED EN SERVICIO")
            sys.exit('-8')
        
        if not isinstance(idBed, int):
            idBed = idBed.id

        hu = dicBeds[idBed].hospUnit

    elif type.name == "Surgery":
        sys.exit('-9')


    # CREAR EVENTO
    description = "ev{}_ep{}_p{}".format(nEvent, nEpisode, idPatient)
    ev = Event(index, description, start, end, idBed, hu, type)

    tupla = (start, end)
    dicBeds[idBed].busy.append(tupla)
    dicBeds[idBed].busy.sort(key = lambda x: x[0]) 

    index += 1
    nEvent += 1

    return ev, nEvent, index


def isBedFree(bed, start, end):
    if len(bed.busy) == 0:
        return True
    
    i = 0
    free = False
    while not free and i<len(bed.busy):
        evPeriod = bed.busy[i]
        # El Evento a insetar es anterior
        if end <= evPeriod[0]:
            # Es el primer Evento
            if i == 0:
                free = True
            else:
                # El evento empieza despues de que termine el anterior en la lista
                evAntPeriod = bed.busy[i-1]
                if start >= evAntPeriod[1]:
                    free = True
        
        # El Evento a insetar es posterior    
        elif start >= evPeriod[1]:
            # Es el ultimo Evento
            if i == len(bed.busy)-1:
                free = True
            else:
                # El evento termina ante de que empiece el siguiente en la lista
                evSigPeriod = bed.busy[i+1]
                if end <= evSigPeriod[0]:
                    free = True
            
        i += 1

    return free
        
def isThereSomeFreeBed_InRoom_FromPast(events, dicBeds, rId, start, end):
    if len(events) == 0:
        return None
    
    i = len(events)-1
    bed = None
    while bed is None and i>=0:
        ev = events[i]
        if ev.type.name != "Surgery":
            bedAux = dicBeds[ev.location]
            if bedAux.parent == rId:
                if isBedFree(bedAux, start, end):
                    bed = ev.location
        
        i -= 1

    return bed

def isThereSomeFreeBed_InHU(hu, start, end): 
    i = 0
    huBeds = hu.beds
    bed = None
    while bed is None and i<len(huBeds):
        bedAux = huBeds[i]
        if isBedFree(bedAux, start, end):
            bed = bedAux

        i += 1

    return bed

def isThereSomeFreeBed_InService(dicBeds, dicRooms, serv, start, end):
    servBeds = []
    for rId in serv.rooms:
        servBeds.extend(dicRooms[rId].beds)
    
    i = 0
    bed = None
    while bed is None and i<len(servBeds):
        bedAuxId = servBeds[i]
        bedAux = dicBeds[bedAuxId]
        if isBedFree(bedAux, start, end):
            bed = bedAux

        i += 1
    return bed

def isThereSomeFreeBed_InService_FromPast(events, dicBeds, dicHospUnits, sId, start, end):
    if len(events) == 0:
        return None
    
    i = len(events)-1
    bed = None
    while bed is None and i>=0:
        ev = events[i]
        if ev.type.name != "Surgery":
            bedAux = dicBeds[ev.location]
            evHU = dicHospUnits[bedAux.hospUnit]
            evServ = evHU.service
            if evServ.id == sId:
                if isBedFree(bedAux, start, end):
                    bed = ev.location
        
        i -= 1

    return bed  # Se devuelve un objeto


def getLastHUNotRadSurg(events):
    if len(events) == 0:
        return None
    
    i = len(events)-1
    hu = None
    while hu is None and i>=0:
        ev = events[i]
        if ev.type.name != "Radiology"  and  ev.type.name != "Surgery":
            hu = ev.hospUnit

        i -= 1
    
    return hu

def getHUSurgery(huId, dicHospUnits, husSurgery):
    hu = dicHospUnits[huId]
    servId = hu.service.id
    HUSurgId = husSurgery[servId]

    return HUSurgId



def createEventDeath(nEpisode, idPatient, datetimeDeath, index):
    type = TypeEvent.Death     
    description = "death_ep{}_p{}".format(nEpisode, idPatient)
    ev = Event(index, description, datetimeDeath, datetimeDeath, None, None, type)

    index += 1

    return ev, index


# MAIN
def createEpisodesAndEventsPerPacient(dicPatients, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, startDateTime, index):

    for patient in dicPatients.values():
        path = patient.stepLocations
        steps = list(path.keys())
        if len(steps)>0:    # In case there is a Patient without Events
            i = 0
            
            lastStep = steps[0]-1
            startEp = getRandomDateTime(startDateTime, steps[0], 0, 240)    # The Episode starts between the FIRST 4 HOURS  ->  (0 ,     4*60=240)
            endEp = startEp
            nEpisode = 0
            events = []
            
            nEvent = 0
            startEv = startEp
            lastLoc = path[steps[0]]

            while i<len(steps):
                step = steps[i]

                # An Event is created when the Location (Bed) is changed
                location = path[step]
                if location != lastLoc:
                    if nEvent==0:
                        startEv = startEp
                    endEv = startDateTime + timedelta(hours=8*lastStep, minutes=479)    # 8*60-1 = 479
                    ev, nEvent, index = createEvent(nEvent, nEpisode, patient.id, startEv, endEv, lastLoc, index, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, events)
                    events.append(ev)
                    
                    startEv = startDateTime + timedelta(hours=8*step)

                # An Episode is created with the events up to the previous step
                if step != lastStep+1:
                    # The last Event of the Episode is created
                    if nEvent==0:
                        startEv = startEp
                    endEv = getRandomDateTime(startDateTime, lastStep, 240, 479)    # The Episode ends within the LAST 4 HOURS   ->  (4*60=240 ,     # 8*60-1 = 480-1 = 479)
                    ev, nEvent, index = createEvent(nEvent, nEpisode, patient.id, startEv, endEv, lastLoc, index, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, events)
                    events.append(ev)

                    # The Episode is created
                    endEp = endEv 
                    ep, nEpisode, index = createEpisode(nEpisode, patient.id, startEp, endEp, events, index)
                    patient.episodes.append(ep)

                    startEp = getRandomDateTime(startDateTime, step, 0, 240)    # The Episode starts between the FIRST 4 HOURS   ->  (0 ,     4*60=240)
                    events = []
                    nEvent = 0

                lastLoc = location
                lastStep = step
                i += 1  


            # Create last Event
            endEv = getRandomDateTime(startDateTime, lastStep, 240, 479)    # The Episode ends within the LAST 4 HOURS  ->  (4*60=240 ,     # 8*60-1 = 480-1 = 479)
            ev, nEvent, index = createEvent(nEvent, nEpisode, patient.id, startEv, endEv, lastLoc, index, dicBeds, dicRooms, dicHospUnits, dicServices, husSurgery, events)
            events.append(ev)

            # If the Patient dies, an Event is created for it
            if patient.death:
                ev, index = createEventDeath(nEpisode, patient.id, endEv, index) # The date and time of death is the 'end' of the last Episode/Event
                events.append(ev)

            # Create last Episode
            endEp = endEv
            ep, nEpisode, index = createEpisode(nEpisode, patient.id, startEp, endEp, events, index)
            patient.episodes.append(ep)        
        

            # Comprobar si hay Episodios con Surgeries a las que no se les ha asignado una HU
            setHUToSurgeriesWithoutIt(patient.episodes, dicHospUnits, husSurgery)

    return index     


def setHUToSurgeriesWithoutIt(episodes, dicHospUnits, husSurgery):
    for ep in episodes:
        for i in range(len(ep.events)):
            ev = ep.events[i]
            if ev.type.name == 'Surgery':
                if ev.hospUnit == -1:

                    j = i+1
                    HUSurgId = None
                    while HUSurgId is None and j<len(ep.events):
                        nextEv = ep.events[j]
                        if nextEv.type.name != 'Radiology' and nextEv.type.name != 'Surgery'  and  nextEv.hospUnit is not None:
                            HUSurgId = getHUSurgery(nextEv.hospUnit, dicHospUnits, husSurgery)
                        j += 1
                    
                    if HUSurgId is not None:
                        ep.events[i].hospUnit = HUSurgId
                    else:
                        # Se selecciona una HU random entre las HU de Surgery
                        randInd = random.randint(0, len(husSurgery)-1)
                        keysList = list(husSurgery.keys())
                        randKey = keysList[randInd]
                        randHU = husSurgery[randKey]
                        ep.events[i].hospUnit = randHU
                        
                    


# Time Functions
def getRandomMinutos(start,end):
    return random.randint(start, end)

def getRandomDateTime(startDateTime, steps, startMinutes, endMinutes):
    minutos = getRandomMinutos(startMinutes, endMinutes)
    datetimeRandom = startDateTime + timedelta(hours=8*steps, minutes=minutos)

    return datetimeRandom


##############
# TEST MICRO #
##############

def randomMDR():
    start = -1
    end = 1
    peak = -0.5
    mdr = random.triangular(start,end,peak)
    if mdr <= 0:
        return False
    return True

def createEventTestMicro_positive(idPatient, datetimeTest, microorg, index):
    type = TypeEvent.TestMicro     
    description = "testMicro_p{}_0".format(idPatient)
    ev = Event(index, description, datetimeTest, datetimeTest, None, None, type)
    ev.extra1 = microorg
    ev.extra2 = randomMDR()
    ev.extra3 = True

    index += 1

    return ev, index

def createEventTestMicro_negative(idPatient, datetimeTest, microorg, index):
    type = TypeEvent.TestMicro     
    description = "testMicro_p{}_1".format(idPatient)
    ev = Event(index, description, datetimeTest, datetimeTest, None, None, type)
    ev.extra1 = microorg
    ev.extra2 = False   # This information is not relevant since we just want to represent that the Patient is not longer infected
    ev.extra3 = False

    index += 1

    return ev, index

# Find at which Episode an Event belongs to
def getEpisodeFromEvent(patient, ev):
    found = False
    i = 0
    while not found and i<len(patient.episodes):
        episode = patient.episodes[i]
        if ev.start >= episode.start  and  ev.start <= episode.end:
            found = True
        else: 
            i += 1
    if found:
        patient.episodes[i].events.append(ev)


# Add a positive TestMicro in the step in which the Patient's status becomes Infectious
def createTestMicro_positive_StartInfectious(dicPatients, dicMicroorganisms, startDateTime, index):
    keysMicroorg = list(dicMicroorganisms.keys())
    microorg = dicMicroorganisms[keysMicroorg[0]]   # Since there is only one Microorganism, it is taken directly from the dictionary
    
    for patient in dicPatients.values():
        
        if patient.seird[2] is not None:  # Patient is Infectious
            stepI = patient.seird[2]
            if patient.seird[1] is not None:  # Patient has gone from Exposed -> Infectious
                datetimeTest  = startDateTime + timedelta(hours=8*stepI)
            else:   # Patient has been directly admitted in an Infectious state
                datetimeTest  = patient.episodes[0].start
            ev, index = createEventTestMicro_positive(patient.id, datetimeTest, microorg, index)
            
            # Find which Episode the Event belongs to
            getEpisodeFromEvent(patient, ev)
    
    return index


# Add a positive TestMicro while the Patient is Infectious (from the first moment they are Infectious to half the time they are Infectious)
def createTestMicro_positive_DuringInfectious(dicPatients, dicMicroorganisms, startDateTime, index):
    keysMicroorg = list(dicMicroorganisms.keys()) 
    microorg = dicMicroorganisms[keysMicroorg[0]]   # Since there is only one Microorganism, it is taken directly from the dictionary
    
    for patient in dicPatients.values():
        
        if patient.seird[2] is not None:  # Patient is Infectious
            stepI = patient.seird[2]
            
            if patient.seird[1] is not None:  # Patient has gone from Exposed -> Infectious
                stepI_start  = startDateTime + timedelta(hours=8*stepI)
            else:   # Patient has been directly admitted in an Infectious state
                stepI_start  = patient.episodes[0].start
            startRandom = stepI_start.timestamp()

            if patient.seird[3] is not None: # Patient has gone from Infectious -> Recovered
                stepI_end  = startDateTime + timedelta(hours=8*patient.seird[3])
            else:   # Patient has left the hospital (alive or dead) in an Infectious state
                stepI_end = patient.episodes[0].end
            endI = stepI_end.timestamp()
            diffStartEnd = endI-startRandom
            mitadDiff = math.floor(diffStartEnd/2)  # As a limit, the test is carried out halfway through the period that the Patient is Infectious.
            endRandom = startRandom+mitadDiff
            randomSeconds = randrange(startRandom, endRandom)   
            datetimeTest = datetime.fromtimestamp(randomSeconds)
            ev, index = createEventTestMicro_positive(patient.id, datetimeTest, microorg, index)
            
            # Find which Episode the Event belongs to
            getEpisodeFromEvent(patient, ev)
    
    return index


# Add a negative TestMicro in the step in which the Patient's status becomes Recovered
def createTestMicro_negative_StartRecovered(dicPatients, dicMicroorganisms, startDateTime, index):
    keysMicroorg = list(dicMicroorganisms.keys()) 
    microorg = dicMicroorganisms[keysMicroorg[0]]   # Since there is only one Microorganism, it is taken directly from the dictionary

    for patient in dicPatients.values():
        if patient.seird[3] is not None:  # Patient is Recovered
            stepR = patient.seird[3]
            
            datetimeTest  = startDateTime + timedelta(hours=8*stepR)
            ev, index = createEventTestMicro_negative(patient.id, datetimeTest, microorg, index)
            getEpisodeFromEvent(patient, ev)

    return index


# Add a negative TestMicro within the 3 next steps the Patient got Recovered
def createTestMicro_negative_During24HoursRecovered(dicPatients, dicMicroorganisms, startDateTime, index):
    keysMicroorg = list(dicMicroorganisms.keys()) 
    microorg = dicMicroorganisms[keysMicroorg[0]]   # Since there is only one Microorganism, it is taken directly from the dictionary

    for patient in dicPatients.values():
        if patient.seird[3] is not None:  # Patient is Recovered
            stepR = patient.seird[3]
            
            startR  = startDateTime + timedelta(hours=8*stepR)
            endR_1 = startDateTime + timedelta(hours=8*(stepR+3))  # Step in which Patient has Recovered + 3 (total = 24 horus)
            endR_2 = patient.episodes[0].end   # Time Episode ends
            if endR_1 < endR_2:
                endR = endR_1
            else:
                endR = endR_2
            startR_timestamp = startR.timestamp()
            endR_timestamp = endR.timestamp()
            randomSeconds = randrange(startR_timestamp, endR_timestamp)
            datetimeTest = datetime.fromtimestamp(randomSeconds) 

            ev, index = createEventTestMicro_negative(patient.id, datetimeTest, microorg, index)
            getEpisodeFromEvent(patient, ev)

    return index