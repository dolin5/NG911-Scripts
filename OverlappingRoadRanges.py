print "started"
import arcpy
def main():
    roads = "N:\ArcMap_Projects\NG911 Analysis\Gecoding4_7\Geocoding4_7.gdb\Roads_4_7"
    fields = [ 'FRADDL','TOADDL','FRADDR','TOADDR',"FULL_ROAD_NAME","MUNICIPALITY_LEFT","MUNICIPALITY_RIGHT","COMMUNITY","OBJECTID"]
    ##             0       1        2        3            4                5                     6              7             8
    roadDict = {}
    with arcpy.da.SearchCursor(roads, fields) as searchCursor:
        for row in searchCursor:
            roadName = row[fields.index("FULL_ROAD_NAME")].strip()        
            objectID = row[fields.index("OBJECTID")]
            communityLeft = row[fields.index("COMMUNITY")]
            communityRight = row[fields.index("COMMUNITY")]
            
         
            if communityLeft not in roadDict:            
                roadDict[communityLeft] = {}
            try:
                FRADDL = (int(row[fields.index("FRADDL")].strip()))
            except:
                FRADDL = None
            try:
                TOADDL = (int(row[fields.index("TOADDL")].strip()))
            except:
                TOADDL = None
            if FRADDL is not None and TOADDL is not None:
                if roadName not in roadDict[communityLeft]:            
                    roadDict[communityLeft][roadName] = set()
                if FRADDL%2 == TOADDL%2:
                    minRange = maxRange = None                    
                    for i in xrange(min(FRADDL,TOADDL),max(FRADDL,TOADDL) + 2,2):
                        if i == 0:
                            continue
                        if i in roadDict[communityLeft][roadName]:
                            if minRange == None:
                                minRange = i
                            else:
                                maxRange = i                            
                        else:
                            roadDict[communityLeft][roadName].add(i)
                    if minRange != None and maxRange != None:
                        print str(minRange) + " - " + str(maxRange) + " " + roadName + ", " + communityLeft 
                    elif minRange != None and maxRange == None:
                        print str(minRange) + " " + roadName + ", " + communityLeft 
                    
                else:
                    minRange = maxRange = None                    
                    for i in xrange(min(FRADDL,TOADDL),max(FRADDL,TOADDL) + 1):
                        if i == 0:
                            continue
                        if i in roadDict[communityLeft][roadName]:
                            if minRange == None:
                                minRange = i
                            else:
                                maxRange = i                            
                        else:
                            roadDict[communityLeft][roadName].add(i)
                    if minRange != None and maxRange != None:
                        print str(minRange) + " - " + str(maxRange) + " " + roadName + ", " + communityLeft 
                    elif minRange != None and maxRange == None:
                        print str(minRange) + " " + roadName + ", " + communityLeft



            if communityRight not in roadDict:            
                roadDict[communityRight] = {}
            try:
                FRADDR = (int(row[fields.index("FRADDR")].strip()))
            except:
                FRADDR = None
            try:
                TOADDR = (int(row[fields.index("TOADDR")].strip()))
            except:
                TOADDR = None
            if FRADDR is not None and TOADDR is not None:
                if roadName not in roadDict[communityRight]:            
                    roadDict[communityRight][roadName] = set()
                if FRADDR%2 == TOADDR%2:
                    minRange = maxRange = None                  
                    for i in xrange(min(FRADDR,TOADDR),max(FRADDR,TOADDR) + 2,2):
                        if i == 0:
                            continue
                        if i in roadDict[communityRight][roadName]:
                            if minRange == None:
                                minRange = i
                            else:
                                maxRange = i                            
                        else:
                            roadDict[communityRight][roadName].add(i)
                    if minRange != None and maxRange != None:
                        print str(minRange) + " - " + str(maxRange) + " " + roadName + ", " + communityLeft 
                    elif minRange != None and maxRange == None:
                        print str(minRange) + " " + roadName + ", " + communityLeft 
                else:
                    minRange = maxRange = None                  
                    for i in xrange(min(FRADDR,TOADDR),max(FRADDR,TOADDR) + 1):
                        if i == 0:
                            continue
                        if i in roadDict[communityRight][roadName]:
                            if minRange == None:
                                minRange = i
                            else:
                                maxRange = i                            
                        else:
                            roadDict[communityRight][roadName].add(i)
                    if minRange != None and maxRange != None:
                        print str(minRange) + " - " + str(maxRange) + " " + roadName + ", " + communityLeft 
                    elif minRange != None and maxRange == None:
                        print str(minRange) + " " + roadName + ", " + communityLeft 
    print "Done"
if __name__ == "__main__":
    main()

        
