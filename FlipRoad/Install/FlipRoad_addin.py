import arcpy
import pythonaddins
import ctypes

class ToolClass4(object):
    """Implementation for FlipRoad_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 4
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift): 
        self.mxd = arcpy.mapping.MapDocument("CURRENT")         
        pointGeom = arcpy.PointGeometry(arcpy.Point(x, y), self.mxd.activeDataFrame.spatialReference)
        self.polylineLayers = []
        self.selectedLayers = []
        self.currentOBJECTID = ""
        for lyr in arcpy.mapping.ListLayers(self.mxd, "", self.mxd.activeDataFrame):
            try:
                if arcpy.Describe(lyr).featureClass.shapeType == "Polyline" and lyr.visible:
                    self.polylineLayers.append(lyr)
            except:
                continue
        if len(self.polylineLayers) == 0:
            print ("No visible polyline layers were found.\nPlease add a road layer or make one visible.")
            return
        for lyr in self.polylineLayers:
            arcpy.SelectLayerByLocation_management(lyr.name, "INTERSECT", pointGeom, "3 Meters")
            result = arcpy.GetCount_management(lyr.name)
            selectedFeatures = int(result.getOutput(0))
            if selectedFeatures > 0:
                self.selectedLayers.append((selectedFeatures,lyr))
        
        if len(self.selectedLayers) > 1:
            print ("Only one visible polyline layer must be clicked.\nTurn all unnecessary polyline layers off.")
            return
        elif len(self.selectedLayers) == 0:
            print ("One visible polyline layer must be clicked.")
            return
        elif len(self.selectedLayers) == 1: 
            if self.selectedLayers[0][0] > 1:
                print ("Select one feature only.")                
                return
            else:
                fields = ["FRADDL", "TOADDL", "FRADDR", "TOADDR", "OBJECTID", "MUNICIPALITY_LEFT", "MUNICIPALITY_RIGHT"]
                with arcpy.da.UpdateCursor(self.selectedLayers[0][1], fields) as updateValueCursor:                    
                    for row in updateValueCursor:
                        FRADDL = row[fields.index("FRADDL")]
                        TOADDL = row[fields.index("TOADDL")]
                        FRADDR = row[fields.index("FRADDR")]
                        TOADDR = row[fields.index("TOADDR")]
                        MUNIC_LFT = row[fields.index("MUNICIPALITY_LEFT")]
                        MUNIC_RGHT = row[fields.index("MUNICIPALITY_RIGHT")]
                        self.currentOBJECTID = str(row[fields.index("OBJECTID")])
                        row[fields.index("FRADDL")] = TOADDR
                        row[fields.index("TOADDL")] = FRADDR
                        row[fields.index("FRADDR")] = TOADDL
                        row[fields.index("TOADDR")] = FRADDL
                        row[fields.index("MUNICIPALITY_LEFT")] = MUNIC_RGHT
                        row[fields.index("MUNICIPALITY_RIGHT")] = MUNIC_LFT
                        updateValueCursor.updateRow(row)                   
                arcpy.FlipLine_edit(self.selectedLayers[0][1])
                print ("Flipped " + self.selectedLayers[0][1].name + " segment with OBJECTID of " + self.currentOBJECTID)
                
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass
        
        
        
        

        
