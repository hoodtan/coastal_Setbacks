Coastal Setbacks

I have included a python script that:  
-Mosaics LiDAR derived DEM's from Nova Scotia's Elevation explorer. 
-Tidy's the resulting DEM mosaic by eliminating No Data (representing water) values.
-Derives a 0m contour of the coastline.
-Creates a buffer layer of a user specified distance from the 0m coastline contour.
-Creates a feature class of buildings from GeoNova that fall inside of the buffer. 

The script is ready for use in your own toolbox in the Esri environment. I have included a screenshot of how to properly set up the parameters for this tool as well.
