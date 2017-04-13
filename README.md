# NG911-Scripts
A collection of scripts and tools for analyzing GIS data for NG911.

## OverlappingRoadRanges.py
This script will review a road centerline feature class for overlapping road range attributes for roads with the same name in the same community. It has been configured for a dataset with to and from, left and right ranges. 

## RoadCenterlineMSAGDiscrepancies.py
This script reviews an msag table and road centerline feature class for discrepancies. It currently does not factor in ESN, but will in the near future. The resulting list includes community, road, and address range discrepancies. 

## MSAGsyncStructures.py
Same as RoadCenterlineMSAGDiscrepancies, but with structures instead of centerline data. Every structure listed does not fall within the MSAG. 
