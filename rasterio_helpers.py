import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.merge import merge
from rasterio.fill import fillnodata
from rasterio.io import MemoryFile
import os
import numpy as np
from arosics import COREG_LOCAL
from geoarray import GeoArray

def get_ds(np_in, profile):
  with MemoryFile() as memfile:
    with memfile.open(**profile) as ds:
        ds.write(np_in)
    ds = memfile.open()
  return ds


def mask_ds(ds, maskfile, masklayer=None, nodata=None):
  print("maskfile", maskfile, "layer", masklayer)
  
  if masklayer is None:
    masklayer = os.path.splitext(os.path.basename(maskfile))[0]

  with fiona.open(maskfile, layer=masklayer) as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

  out_np, out_transform = rasterio.mask.mask(ds, shapes, nodata=nodata, crop=True)
  out_profile = ds.profile

  out_profile.update({"driver": "GTiff",
                   "height": out_np.shape[1],
                   "width": out_np.shape[2],
                   "transform": out_transform})

  return get_ds(out_np, out_profile)

def merge_ds(ds_list):
  merge_np, merge_transform = merge(ds_list)
  merge_profile = ds_list[0].profile
  merge_profile.update({"driver": "GTiff",
                   "height": merge_np.shape[1],
                   "width": merge_np.shape[2],
                   "transform": merge_transform})
  
  return get_ds(merge_np, merge_profile)

def save_ds(ds, outfile):
  ds_profile = ds.profile
  ds_np = ds.read()
  with rasterio.open(outfile, "w", **ds_profile) as dest:
      dest.write(ds_np)

def align_rasters(ref_tiff, tgt_tiff, out_tiff, arosic_args=None):
    work_dir = f'{os.path.dirname(out_tiff)}/working'
    base_fn = os.path.splitext(os.path.basename(out_tiff))[0]
    proj_dir =  f'{work_dir}/{base_fn}' 
    vect_fig_file = f'{proj_dir}/{base_fn}_vect.png'
    ang_fig_file = f'{proj_dir}/{base_fn}_ang.png'
    mag_fig_file = f'{proj_dir}/{base_fn}_mag.png'
    tiepoint_file = f'{proj_dir}/{base_fn}.shp'
    tiepoint_table_file = f'{proj_dir}/{base_fn}.csv'

    print(f'Aligning Rasters')
    print(f'Target:    {tgt_tiff}')
    print(f'Reference: {ref_tiff}')
    print(f'Output:    {out_tiff}')    
    
    if not os.path.exists(proj_dir):
        os.makedirs(proj_dir)

    with rasterio.open(ref_tiff) as ds:
        ref_band = ds.count

    with rasterio.open(tgt_tiff) as ds:
        tgt_band = ds.count
            
    print(f'Using Ref Band: {ref_band}')
    print(f'Using Tgt Band: {tgt_band}')
            
    kwargs = {
        'grid_res'     : 100,
        'path_out'     : out_tiff,
        'fmt_out'      : 'GTIFF',
        'r_b4match'    : ref_band,
        's_b4match'    : tgt_band,
        'tieP_filter_level' : 2,       
        'min_reliability' : 20,
        'CPUs'         : 6,
        'nodata'       : (0,0)
    }
       
    
    if arosic_args is not None: 
        kwargs.update(arosic_args)

    CRL = COREG_LOCAL(ref_tiff, tgt_tiff, **kwargs)

    print("Generating: ", tiepoint_table_file)                
    CRL.CoRegPoints_table.to_csv(tiepoint_table_file)

    #Some of these outputs are undocument, but cool.
    #The cool vector plot
    print("Generating: ", ang_fig_file)        
    CRL.view_CoRegPoints(figsize=(20,20), savefigPath=vect_fig_file, shapes2plot='vectors', vector_scale=15)
    #Plotting cool stuff

    print("Generating: ", vect_fig_file)
    CRL.view_CoRegPoints(figsize=(20,20), savefigPath=ang_fig_file,  attribute2plot='ANGLE')

    print("Generating: ", mag_fig_file)        
    CRL.view_CoRegPoints(figsize=(20,20), savefigPath=mag_fig_file )

    print("Generating: ", out_tiff)                
    CRL.correct_shifts()
    
    return CRL

