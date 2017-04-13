import arcpy
structures = "N:\ArcMap_Projects\NG911 Analysis\Gecoding4_7\Geocoding4_7.gdb\Address_Points_4_7"
structureFields = [ "ADDRESS", "DIRPRE","ROADNAME","ROADTYPE","DIRSUF"]

msag = "N:\ArcMap_Projects\NG911 Analysis\Gecoding4_7\Geocoding4_7.gdb\MSAG_4_3"
msagFields = ["Low", "High", "O_E", "Dir", "Street","Community"]



print "Building MSAG List"
msagDict = {}
##msagDict Structures {"W MAIN ST":[[LOW,HIGH,oE],[LOW,HIGH,oE]]}
with arcpy.da.SearchCursor(msag, msagFields) as msagSearchCursor:
    for row in msagSearchCursor:
        roadName = str(str(row[msagFields.index("Dir")].strip()) + " " + str(row[msagFields.index("Street")].strip())).strip()
        oE = row[msagFields.index("O_E")].strip()
        try:
            LOW = (int(row[msagFields.index("Low")]))
        except:
            LOW = None
        try:
            HIGH = (int(row[msagFields.index("High")]))
        except:
            HIGH = None
        if roadName in msagDict:
            msagDict[roadName].append([LOW, HIGH, oE])
        else:
            msagDict[roadName] = []
            msagDict[roadName].append([LOW, HIGH, oE])

print "Scanning Structures"
totalStructures = arcpy.GetCount_management(structures).getOutput(0)
with arcpy.da.SearchCursor(structures, structureFields) as structuresSearchCursor:
    unmatchedAddresses = []
    for currentStructure in structuresSearchCursor:
        currentStructureRoadName = (currentStructure[structureFields.index("DIRPRE")].strip() + " " + currentStructure[structureFields.index("ROADNAME")].strip() + " " + currentStructure[structureFields.index("ROADTYPE")].strip() + " " + currentStructure[structureFields.index("DIRSUF")].strip()).strip()
        currentStructureNumber = currentStructure[structureFields.index("ADDRESS")].strip()
        try:
            currentStructureNumber = int(currentStructureNumber)
            if currentStructureNumber % 2 == 0:
                currentStructureNumberEO = "EVEN"
            else:
                currentStructureNumberEO = "ODD"            
        except:
            currentStructureNumber = None
            currentStructureNumberEO = None
        if currentStructureNumber == None:
            continue
        addressFound = False      
        if currentStructureRoadName in msagDict:            
            for msagRow in msagDict[currentStructureRoadName]:
                if (currentStructureNumber >= msagRow[0] and currentStructureNumber <= msagRow[1]):
                    if (msagRow[2] == "BOTH") or (msagRow[2] == currentStructureNumberEO):
                        addressFound = True                        
                        break
        if not addressFound:
            unmatchedAddresses.append((currentStructureNumber,currentStructureRoadName))
    sortedAddresses = sorted(unmatchedAddresses,key=lambda x:(x[1],x[0]))
    for address in sortedAddresses:
        print str(address[0]) + " " + address[1] + " not found in MSAG"
        

print "Done"

        
