# NG911-Scripts
A collection of scripts and tools for analyzing GIS data for NG911. Please contact me at dylan.olin@gallatin.mt.gov if you would like help in setting any of these up for your own use.

## OverlappingRoadRanges.py
This script will review a road centerline feature class for overlapping road range attributes for roads with the same name in the same community. It has been configured for a dataset with to and from, left and right ranges. 

## RoadCenterlineMSAGDiscrepancies.py
This script reviews an msag table and road centerline feature class for discrepancies. It currently does not factor in ESN, but will in the near future. The resulting list includes community, road, and address range discrepancies. 

## MSAGsyncStructures.py
Same as RoadCenterlineMSAGDiscrepancies, but with structures instead of centerline data. Every structure listed does not fall within the MSAG.

## FlipRoad
This is an [ArcGIS add-in](http://desktop.arcgis.com/en/arcmap/latest/analyze/python-addins/sharing-and-installing-add-ins.htm) for flipping the orientation of a road segment, but keeping the to/from, left/right address ranges and other orientation dependent fields, like left/right municipality in the correct spatial location. The default line flip tool in ArcGIS requires you to go back and edit these fields manually. Because I'm a moron, I can't figure out how to print messages to he Results window in ArcMap, so it prints to the Python window. You can edit the following lines in FlipRoad_addin.py file to reflect whatver fields you want to have swapped.
![Field Values](/images/FlipRoadFields.png?raw=true "Fields")
