# Get officer's information from officers.txt
def GetOfficerDetails(officers_FullFilePath):
    lstMumStation = list()
    lstRank =  list()
    lstbHP_rider = list()
    lstOfficerName =  list()
    try:
        with open(officers_FullFilePath, 'r') as fp:
            ids = [s.strip() for s in fp.readlines() if s]
            for officerItems in ids:                

                #for cntStations in listOfStations:
                if officerItems != '':    
                    # Mum Station 
                    intMumStationEndIdx = officerItems.find(' ')                                                                                
                    lstMumStation.append(officerItems[0:intMumStationEndIdx])                    
                                            
                    # Rank: e.g. StnO
                    strTemp = (officerItems[intMumStationEndIdx: len(officerItems)]).strip()                    
                    delimiter = 'tnO'
                    intRankEndIdx = strTemp.find(delimiter)    
                    strRank = strTemp[0:intRankEndIdx + len(delimiter)]
                    lstRank.append(strRank)
                   
                    # Officer's name
                    strOfficerName = (strTemp[intRankEndIdx+ len(delimiter)+1:]).strip()
                    lstOfficerName.append(strOfficerName)
                
                    if (strRank=='SStnO' or strRank=='StnO'):
                        lstbHP_rider.append(True)
                    elif (strRank=='PStnO'):
                        if (strOfficerName.find('(HP)') > -1):
                            lstbHP_rider.append(True)
                        else:
                            lstbHP_rider.append(False)
                    else:
                        lstbHP_rider.append(False)                    
        fp.close()                                 
        return lstMumStation, lstRank, lstbHP_rider, lstOfficerName

    except OSError:
        print('Error in reading data from ', officers_FullFilePath)
    else:
        print('** Officers file closed **')
        fp.close()       

# Get application's information from application.txt        
def GetApplianceDetails(Appliances_FullFilePath):
    # lstMumStation, lstAppliances, lstPotentialOIC, lstAvailableOfficers
    lstMumStation = list()
    lstAppliances =  list()
    lstPotentialOIC = list()    
    try:
        with open(Appliances_FullFilePath, 'r') as fp:
            ids = [s.strip() for s in fp.readlines() if s]
            for ApplianceItems in ids:                

                #for cntStations in listOfStations:
                if ApplianceItems != '':                        
                    
                    intMumStationAppliancesEndIdx = ApplianceItems.find(' ')                                                                                                    
                    strMumStationAppliances = ApplianceItems[0:intMumStationAppliancesEndIdx]

                    intMumStationEndIdx = strMumStationAppliances.find('/')                                                                                                    
                    if intMumStationEndIdx==-1: raise Exception('Cannot find delimiter /')                            
                        
                    strMumStation = strMumStationAppliances[0:intMumStationEndIdx]
                    lstMumStation.append(strMumStation) 
                    
                    strAppliance = strMumStationAppliances[intMumStationEndIdx+1:]
                    lstAppliances.append(strAppliance) 

                    strPotentialOIC = (ApplianceItems[intMumStationAppliancesEndIdx:]).strip()                    
                    intPotentialOICIdx = strPotentialOIC.find('OIC:')
                    if intPotentialOICIdx==-1: raise Exception('Cannot find delimiter OIC')                        
                    strPotentialOIC = (strPotentialOIC[intPotentialOICIdx+len('OIC')+1:]).strip()
                    lstPotentialOIC.append(strPotentialOIC)                                                           
        return lstMumStation, lstAppliances, lstPotentialOIC

    except OSError:
        print('Error in reading data from ', Appliances_FullFilePath)
    else:
        print('** Appliances file closed **')
        fp.close()            
        
def GetOfficer(officers_FullFilePath):        
    lstMumStation, lstRank, lstbHP_rider, lstOfficerName = GetOfficerDetails(officers_FullFilePath)
    for cnt in range(len(lstRank)):
        OfficerDict[cnt] = dict(rank= lstRank[cnt], name = lstOfficerName[cnt], \
                                HP_rider = lstbHP_rider[cnt], mum_station=lstMumStation[cnt])    
    return OfficerDict

def GetAppliance(Appliances_FullFilePath):    
    lstMumStation, lstAppliances, lstPotentialOIC = GetApplianceDetails(Appliances_FullFilePath)
    for cnt in range(len(lstMumStation)):
        ApplianceDict[cnt] = dict(mum_station= lstMumStation[cnt], appliance = lstAppliances[cnt], \
                                  Potential_OIC = lstPotentialOIC[cnt], available_officers=[])    
    return ApplianceDict

def get_OfficerDict(searchWhat, returnWhat, OfficerDict): 
    #print(OfficerDict[0].items())
    for cntOfficer in range(len(OfficerDict)):    
        if (OfficerDict[cntOfficer]['name'] == searchWhat):
            if (returnWhat == 'rank'):
                return OfficerDict[cntOfficer]['rank']
            elif (returnWhat == 'HP_rider'):
                return OfficerDict[cntOfficer]['HP_rider']
            elif (returnWhat == 'mum_station'):
                return OfficerDict[cntOfficer]['mum_station']
    return ''

# for each Appliance's record, find it's home officer
def findHomeOfficer(AD_mum_station , AD_Potential_OIC, OfficerDict):
    lstOfficerName = list()
    for cntOfficer in range(len(OfficerDict)): 

        if (AD_mum_station == OfficerDict[cntOfficer]['mum_station']):
            if (AD_mum_station== 'TLW'):
                #print('>' + OfficerDict[cntOfficer]['rank'] in AD_Potential_OIC)            
                print('xxx')
                print(OfficerDict[cntOfficer]['rank'])
                print(AD_Potential_OIC)
                
            if (OfficerDict[cntOfficer]['rank'] in AD_Potential_OIC):
                return OfficerDict[cntOfficer]['name']
    return ''

# Currently Homing will stop once find an appropriate officer.
def Homing(OfficerDict, ApplianceDict): 
    # Create a list of officer names
    lstOfficerName = list()
    for cntOfficer in range(len(OfficerDict)):                
        lstOfficerName.append(OfficerDict[cntOfficer]['name'])
    print(lstOfficerName)       

    lstAppliance = list()
    for cntAppliance in range(len(ApplianceDict)):                   
        # for each Appliance's record, find it's home officer
        strHomeOfficer = findHomeOfficer(ApplianceDict[cntAppliance]['mum_station'] , \
                                         ApplianceDict[cntAppliance]['Potential_OIC'], \
                                        OfficerDict)         
        lstAppliance.append(ApplianceDict[cntAppliance]['mum_station'] + ' | ' + ApplianceDict[cntAppliance]['appliance'] + \
                            ' : ' + strHomeOfficer)
        
    print('************')
    for i in range(len(lstAppliance)):
        print(lstAppliance[i])
   
    
    
officers_FullFilePath = 'data/officers.txt'
appliances_FullFilePath = 'data/appliances.txt'

OfficerDict = {}
OfficerDict = GetOfficer(officers_FullFilePath)

ApplianceDict = {}
ApplianceDict = GetAppliance(appliances_FullFilePath)

Homing(OfficerDict, ApplianceDict)        
print('complete')    
