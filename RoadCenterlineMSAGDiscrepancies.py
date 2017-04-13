print "importing"
import arcpy
from itertools import groupby
from operator import itemgetter
def main():
    print "started"
    roads = "N:\ArcMap_Projects\NG911 Analysis\Gecoding4_7\Geocoding4_7.gdb\Roads_4_7"
    roadFields = [ 'FRADDL','TOADDL','FRADDR','TOADDR',"FULL_ROAD_NAME", "OBJECTID","MUNICIPALITY_LEFT","MUNICIPALITY_RIGHT","COMMUNITY"]
    ##                 0        1      2          3           4              5              6               7
    roadDict = {}

    msag = "N:\ArcMap_Projects\NG911 Analysis\Gecoding4_7\Geocoding4_7.gdb\MSAG_4_3"
    msagFields = [ "Low", "High", "O_E", "Dir", "Street", "Community", "OBJECTID" ]   
    ##                0      1       2      3       4           5           6
    msagDict = {}
    
    result = arcpy.GetCount_management(roads)
    totalRoads = int(result.getOutput(0))
    with arcpy.da.SearchCursor(roads, roadFields) as roadSearchCursor:
        print "Scanning Roads"
        for row in roadSearchCursor:
            roadName = row[roadFields.index("FULL_ROAD_NAME")].strip()        
            objectID = row[roadFields.index("OBJECTID")]
            communityLeft = row[roadFields.index("COMMUNITY")]
            communityRight = row[roadFields.index("COMMUNITY")]
            try:
                FRADDL = (int(row[roadFields.index("FRADDL")].strip()))
            except:
                FRADDL = None
            try:
                TOADDL = (int(row[roadFields.index("TOADDL")].strip()))
            except:
                TOADDL = None
            try:
                FRADDR = (int(row[roadFields.index("FRADDR")].strip()))
            except:
                FRADDR = None
            try:
                TOADDR = (int(row[roadFields.index("TOADDR")].strip()))
            except:
                TOADDR = None
                
            if communityLeft not in roadDict:            
                roadDict[communityLeft] = {}            
            if roadName not in roadDict[communityLeft]:
                roadDict[communityLeft][roadName] = set()      
            if FRADDL is not None and TOADDL is not None:
                if FRADDL%2 == TOADDL%2:                  
                    for i in xrange(min(FRADDL,TOADDL),max(FRADDL,TOADDL) + 2,2):
                        if i == 0:
                            continue
                        roadDict[communityLeft][roadName].add(i)                       
                    
                else:                   
                    for i in xrange(min(FRADDL,TOADDL),max(FRADDL,TOADDL) + 1):
                        if i == 0:
                            continue
                        roadDict[communityLeft][roadName].add(i)

            if communityRight not in roadDict:            
                roadDict[communityRight] = {}
            if roadName not in roadDict[communityRight]:
                roadDict[communityRight][roadName] = set()

            if FRADDR is not None and TOADDR is not None:
                if FRADDR%2 == TOADDR%2:                  
                    for i in xrange(min(FRADDR,TOADDR),max(FRADDR,TOADDR) + 2,2):
                        if i == 0:
                            continue
                        roadDict[communityRight][roadName].add(i)                       
                    
                else:                   
                    for i in xrange(min(FRADDR,TOADDR),max(FRADDR,TOADDR) + 1):
                        if i == 0:
                            continue
                        roadDict[communityRight][roadName].add(i)

    with arcpy.da.SearchCursor(msag, msagFields) as msagSearchCursor:
        print "Scanning MSAG"
        for row in msagSearchCursor:        
            roadName = str(str(row[msagFields.index("Dir")].strip()) + " " + str(row[msagFields.index("Street")].strip())).strip()
            community = row[msagFields.index("Community")].strip()
            oE = row[msagFields.index("O_E")].strip()
            objectID = row[msagFields.index("OBJECTID")]
            try:
                low = (int(row[msagFields.index("Low")]))
            except:
                print "MSAG blank at: " + str(objectID)
                low = None
            try:
                high = (int(row[msagFields.index("High")]))
            except:
                print "MSAG blank at: " + str(objectID)
                high = None            
            if oE == "EVEN" and (low%2 != 0 or high%2 != 0):
                print str(objectID) + " is not even"
            if oE == "ODD" and (low%2 != 1 or high%2 != 1):
                print str(objectID) + " is not odd"
            if community not in msagDict:            
                msagDict[community] = {}
            if roadName not in msagDict[community]:
                msagDict[community][roadName] = set()                
            if low is not None and high is not None:
                if oE == "EVEN" or oE == "ODD":
                    for i in xrange(low,high + 2,2):
                        if i == 0:
                            continue                    
                        msagDict[community][roadName].add(i)                        
                else:
                    for i in xrange(low,high + 1):
                        if i == 0:
                            continue                        
                        msagDict[community][roadName].add(i)
    roadCommunitiesNotInMSAG = set()
    roadNamesNotInMSAG = set()
    for roadCommunity in roadDict:
        if roadCommunity not in msagDict:
            roadCommunitiesNotInMSAG.add(roadCommunity)
        else:
            for roadRoadName in roadDict[roadCommunity]:                
                if roadRoadName not in msagDict[roadCommunity]:
                    roadNamesNotInMSAG.add(roadRoadName + ", " + roadCommunity)
                else:
                    addressNumberDifference = roadDict[roadCommunity][roadRoadName].difference(msagDict[roadCommunity][roadRoadName])
                    if len(addressNumberDifference) > 0:
                        addressNumberDifference = sorted(addressNumberDifference)
                        rangeLists = []
                        for k, g in groupby(enumerate(addressNumberDifference), lambda (i, x): i-x):                              
                            rangeLists.append(map(itemgetter(1), g)) 
                        singles = []
                        for element in rangeLists:
                            if len(element) > 1:
                                print str(min(element)) + "-" + str(max(element)) + " " + roadRoadName + ", " + roadCommunity + " in roads table but not MSAG"                                
                            else:
                                singles.append(element[0])
                        if len(singles)>0:                            
                            groups = [[singles[0]]]

                            for x in singles[1:]:
                                if x - groups[-1][-1] == 2:
                                    groups[-1].append(x)
                                else:
                                    groups.append([x])
                            for run in groups:
                                if len(run) == 1:
                                   print str(run[0]) + " " + roadRoadName + ", " + roadCommunity + " in roads table but not MSAG"
                                   continue
                                if min(run)%2 == 0:
                                    oe = '(Even)'
                                else:
                                    oe = '(Odd)'
                                print str(min(run)) + "-" + str(max(run)) + " " + oe + " " + roadRoadName + ", " + roadCommunity + " in roads table but not MSAG"
    print('\n' * 2) 
    for community in roadCommunitiesNotInMSAG:
        print community + " community found in roads table but not in MSAG table"
    print('\n' * 2) 
    for road in roadNamesNotInMSAG:
        print road + " found in roads table but not in MSAG table"
    print('\n' * 2) 

        

    msagCommunitiesNotInRoads = set()
    msagRoadNamesNotInRoads = set()
    for msagCommunity in msagDict:
        if msagCommunity not in roadDict:
            msagCommunitiesNotInRoads.add(msagCommunity)
        else:
            for msagRoadName in msagDict[msagCommunity]:                
                if msagRoadName not in roadDict[msagCommunity]:
                    msagRoadNamesNotInRoads.add(msagRoadName + ", " + msagCommunity)
                else:
                    addressNumberDifference = msagDict[msagCommunity][msagRoadName].difference(roadDict[msagCommunity][msagRoadName])
                    if len(addressNumberDifference) > 0:
                        addressNumberDifference = sorted(addressNumberDifference)
                        rangeLists = []
                        for k, g in groupby(enumerate(addressNumberDifference), lambda (i, x): i-x):                              
                            rangeLists.append(map(itemgetter(1), g)) 
                        singles = []
                        for element in rangeLists:
                            if len(element) > 1:
                                print str(min(element)) + "-" + str(max(element)) + " " + msagRoadName + ", " + msagCommunity + " in MSAG table but not roads table"                                
                            else:
                                singles.append(element[0])
                        if len(singles)>0:                            
                            groups = [[singles[0]]]

                            for x in singles[1:]:
                                if x - groups[-1][-1] == 2:
                                    groups[-1].append(x)
                                else:
                                    groups.append([x])
                            for run in groups:
                                if len(run) == 1:                                    
                                   print str(run[0]) + " " + msagRoadName + ", " + msagCommunity + " in MSAG table but not roads table"
                                   continue
                                if min(run)%2 == 0:
                                    oe = '(Even)'
                                else:
                                    oe = '(Odd)'
                                print str(min(run)) + "-" + str(max(run)) + " " + oe + " " + msagRoadName + ", " + msagCommunity + " in MSAG table but not roads table"
    print('\n' * 2) 
    for community in msagCommunitiesNotInRoads:
        print community + " community found in MSAG table but not in roads table"
    print('\n' * 2) 
    for road in msagRoadNamesNotInRoads:
        print road + " found in MSAG table but not in roads table"
                           
    print('\n' * 2)   

    print "Done"
if __name__ == "__main__":
    main()
        
