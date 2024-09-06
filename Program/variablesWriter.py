
prefixes_nt = {}
prefixes_nt['hospOnt'] = "http://www.semanticweb.org/spatiotemporalHospitalOntology"
prefixes_nt['rdf'] = "http://www.w3.org/1999/02/22-rdf-syntax-ns"
prefixes_nt['xmlSchema'] = "http://www.w3.org/2001/XMLSchema"

nameFiles_Classes = {}
nameFiles_Classes['patient'] = '\\patients'
nameFiles_Classes['episode'] = '\\episodes'
nameFiles_Classes['death'] = '\\eventsDeath'
nameFiles_Classes['hospitalization'] = '\\eventsHospitalization'
nameFiles_Classes['radiology'] = '\\eventsRadiology'
nameFiles_Classes['surgery'] = '\\eventsSurgery'
nameFiles_Classes['testMicro'] = '\\eventsTestMicro'
nameFiles_Classes['microorganism'] = '\\microorganisms'
nameFiles_Classes['uh'] = '\\hospUnits'
nameFiles_Classes['service'] = '\\services'
nameFiles_Classes['bed'] = '\\beds'
nameFiles_Classes['room'] = '\\rooms'
nameFiles_Classes['corridor'] = '\\corridors'
nameFiles_Classes['area'] = '\\areas'
nameFiles_Classes['unit'] = '\\units'
nameFiles_Classes['block'] = '\\blocks'
nameFiles_Classes['floor'] = '\\floors'
nameFiles_Classes['building'] = '\\buildings'
nameFiles_Classes['logicZone'] = '\\logicZones'

nameFiles_Rels = {}
nameFiles_Rels['ep_pat'] = '\\relEpisodePatient'
nameFiles_Rels['ev_ep'] = '\\relEventEpisode'
nameFiles_Rels['test_micro'] = '\\relTestMicroorg'
nameFiles_Rels['ev_bed'] = '\\relEventBed'
nameFiles_Rels['ev_uh'] = '\\relEventHospUnit'
nameFiles_Rels['serv_uh'] = '\\relServiceHospUnit'
nameFiles_Rels['bed_room'] = '\\relRoomBed'
nameFiles_Rels['room_corridor'] = '\\relCorridorRoom'
nameFiles_Rels['corridor_area'] = '\\relAreaCorridor'
nameFiles_Rels['area_block'] = '\\relAreaBlock'
nameFiles_Rels['area_unit'] = '\\relAreaUnit'
nameFiles_Rels['area_floor'] = '\\relFloorArea'
nameFiles_Rels['block_floor'] = '\\relFloorBlock'
nameFiles_Rels['unit_floor'] = '\\relFloorUnit'
nameFiles_Rels['floor_building'] = '\\relBuildingFloor'
nameFiles_Rels['bed_nt'] = '\\relBed_NextTo'
nameFiles_Rels['bed_ot'] = '\\relBed_Opposite'
nameFiles_Rels['room_nt'] = '\\relRoom_NextTo'
nameFiles_Rels['room_ot'] = '\\relRoom_Opposite'
nameFiles_Rels['corridor_nt'] = '\\relCorridor_NextTo'
nameFiles_Rels['area_nt'] = '\\relArea_nextTo'
nameFiles_Rels['block_nt'] = '\\relBlock_NextTo'
nameFiles_Rels['unit_nt'] = '\\relUnit_NextTo'
nameFiles_Rels['lz_area'] = '\\relLogicZoneArea'


def get01_FalseTrue(value):
    if value:
        return 1
    else:
        return 0