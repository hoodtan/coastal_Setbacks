

# Purpose: This script mosaics DEM rasters, creates a 0m contour from the mosaic, buffers a user defined distance from the 0m contour, and produces a feature class of buildings
# that fall within the buffer zone. 
# The script is intended to be used as a tool within an ArcGIS toolbox.
# I have included a screenshot on how to properly set up the parameters to run this script.
# Programmer: Jacob Albury
# Date: January 30, 2023


import arcpy 
arcpy.env.overwriteOutput = True 

# Creating variables for input  
rasters = arcpy.GetParameter(0) # get this to automatically insert all rasters as default 
workspace = arcpy.GetParameterAsText(1)
#out_file = arcpy.GetParameter(2)
coord = arcpy.GetParameter(2) 

# Allowing for default values with if statements
cell_Default = '5'
cell_size = arcpy.GetParameterAsText(3) # not required. if blank then 5
if cell_size == "":
    cell_size = cell_Default    

bands_Default = '1'
bands = arcpy.GetParameterAsText(4) # not required. if blank then 1 
if bands == "":
    bands = bands_Default 
outfile = arcpy.GetParameterAsText(5)
buffer_output = arcpy.GetParameter(6)
buffer_value = arcpy.GetParameter(7)

#variables
buildings = arcpy.GetParameter(8) # optional #

####################
# Geoprocessing ####
####################

# mosaicing input rasters (DEM)
mosaic = arcpy.management.MosaicToNewRaster(rasters, workspace, "mosaic", coord, '16_BIT_SIGNED', cell_size, bands) # create cell size input 
arcpy.AddMessage(f'{rasters} mosaiced DEM sucessfully')

#removing the erroneous -1 
mosaic_Tidy = arcpy.sa.ExtractByAttributes("mosaic", "Value > -1 " )
#mosaic_Tidy.save("C:\\Users\\jacob\\OneDrive - Nova Scotia Community College\\HP_Laptop\\Documents\\ArcGIS\\Projects\\coastal_Setback\\coastal_Setback.gdb\\please")


mosaic_Tidy.save(workspace +'/' + outfile)


# deriving contour from the mosaic DEM
contours = arcpy.sa.Contour("mosaic", "intermediate_Contours",  5, 0, 1, "CONTOUR", None ) # create contour inputs 
arcpy.AddMessage(f'creating intermediate contour layer...')

# selecting only 0m contours
contour_selection = arcpy.management.SelectLayerByAttribute(contours, "NEW_SELECTION", "Contour = 0", None)
arcpy.AddMessage(f'selecting only 0m contour...')

# writing the selection to a new feature class 
arcpy.management.CopyFeatures( contour_selection, "zerom_Contour")
arcpy.AddMessage(f'copying selection to new feature layer...')

# delete full contour layer 
arcpy.Delete_management(contours)
arcpy.AddMessage(f'deleting the intermediate contour layer...')

# buffering from line 
buffer = arcpy.analysis.Buffer("zerom_Contour", buffer_output, buffer_value,  "FULL", "ROUND", "ALL", "", "PLANAR" )
arcpy.AddMessage(f'buffering {buffer_value}m from 0m contour...')

#selecting where buffer and buildings intersect
arcpy.AddMessage(f'finding where {buildings} and the {buffer} layer intersect...')

failed = arcpy.management.SelectLayerByLocation(buildings, "INTERSECT", buffer, '0 meters',  "NEW_SELECTION", "NOT_INVERT")

arcpy.AddMessage(f'creating a point layer containing buildings that are within 100m of the coastline...')
# creating the intersecting features layer

arcpy.FeatureClassToFeatureClass_conversion(failed, workspace,  "intersecting_Buildings") # create outpath paramter

# delete untidy mosaic layer 
arcpy.Delete_management("mosaic")
#arcpy.AddMessage(f'deleting the intermediate mosaic layer...')

arcpy.AddMessage(f'Done!')




