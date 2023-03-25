import importlib 

import pdal
import glob
import json
import os
from raserio_helpers import *
from proj_scope_vars import *

#This creates a TIF of the height above ground using the delaunay cal.
def laz_to_height(lazfile_in, tiffile_out):
    pdal_json = {
         "pipeline": [
             lazfile_in,
             {
                 "type":"filters.hag_nn"
             },
             {

                 "filename": tiffile_out,
                 "gdaldriver": "GTiff",
                 "output_type": "mean",
                 "dimension" : "HeightAboveGround",
                 "window_size" : 5,
                 "resolution": "1",
                 "type": "writers.gdal"
             }
         ]
     }
    print(1)
    pdal_json_str = json.dumps(pdal_json)
    pipeline = pdal.Pipeline(pdal_json_str)
    count = pipeline.execute()
    print(2, count)


lazfiles=glob.glob(lidar_dl_dir + '/*laz')
if not os.path.exists(lidar_dl_tif_dir):
    os.makedirs(lidar_dl_tif_dir)
count=0
for lazfile in lazfiles:
    filename = os.path.basename(lazfile)
    outfile = lidar_dl_tif_dir + '/' + os.path.splitext(filename)[0] + '_height.tif'
    print(count, "Infile:", filename)
    print("Outfile:", outfile)
    laz_to_height(lazfile, outfile)
    count += 1

print("Done with Lazfiles")
tiffiles=glob.glob(lidar_dl_tif_dir + '/*height.tif')
lidar_height_datasets=[]
for tiffile in tiffiles:
    ds = rasterio.open(tiffile)
    print(tiffile)
    print(ds.profile)
    lidar_height_datasets.append(ds)
    
lidar_height_merged_ds = merge_ds(lidar_height_datasets)
print(lidar_height_merged_ds.profile)
#show(lidar_height_merged_ds)

save_ds(lidar_height_merged_ds, lidar_height_merged_tif)
