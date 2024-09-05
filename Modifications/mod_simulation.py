
# ADD THIS IMPORT
import os


# ADD THESE FUNCTIONS AT THE BEGINNING OF THE FILE "simulation.py" (AFTER THE IMPORTS)
def setRandomNRooms(nServ, nHU):
    rand = random.uniform(1, 10)
    
    if rand <= 5:
        nRooms = 8
    elif rand <= 6:
        nRooms = 10
    elif rand <= 7:
        nRooms = 6
    elif rand <= 8.5:
        nRooms = 9
    else:
        nRooms = 7

    printRoomsPerHU(nServ, nHU, nRooms)
    return nRooms

def setRoomsMultipleHUs(nServ, nHUs):
    nRooms = 0
    for i in range(nHUs):
        nRooms += setRandomNRooms(nServ, i)

    return nRooms        

def printRoomsPerHU(nServ, nHU, nRooms):
    file = open('./roomsHU.txt', 'a')
    file.write("{},{},{}\n".format(nServ,nHU,nRooms))
    file.close()
# UNTIL HERE


# ADD THESE LINES AT THE BEGINNING OF THE FUNCTION initialize()
er_nbeds = 20
icu_nbeds = 16
nwards = 17 #18     # Wards = Services
# 7 #8 Services with 1 HU
# 3 Services with 2 HUs
# 4 Services with 3 HUs
# 1 Services with 4 HUs
# 1 Services with 5 HUs
# 1 Services with 6 HUs

# 1 HU [6-10] Rooms
# 50% 8 Rooms
# 10% 10 Rooms
# 10% 6 Rooms
# 15% 9 Rooms
# 15% 7 Rooms


# If the file exists, remove it
file_path = "./roomsHU.txt"
if os.path.exists(file_path):
    os.remove(file_path)

wards_nrooms = []
for i in range(nwards):
    
    if i in [0,1,5,10,11,12,13]:
        nRooms = setRandomNRooms(i,1)
    elif i in [2,6,8]:
        nRooms = setRoomsMultipleHUs(i, 2)
    elif i in [3,4,9,16]:
        nRooms = setRoomsMultipleHUs(i, 3)
    elif i == 7:
        nRooms = setRoomsMultipleHUs(i, 4)
    elif i == 15:
        nRooms = setRoomsMultipleHUs(i, 5)
    elif i == 14:
        nRooms = setRoomsMultipleHUs(i, 6)
    
    wards_nrooms.append(nRooms)

sx_nrooms = 27
rx_nrooms = 24
room_nbeds = 2
rx_nbeds = 1
L = initialize_hospital(er_nbeds, icu_nbeds, nwards, wards_nrooms, sx_nrooms, rx_nrooms, room_nbeds, rx_nbeds)


# COMMENT THE LINE: L = initialize_hospital(20, 10, 7, [36, 7, 6, 6, 6, 6, 24], 3, 5, 2, 4)