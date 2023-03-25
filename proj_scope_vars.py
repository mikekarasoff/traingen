epsg                        = 32610

layer_dir                   = '../layers'

temp_dir                    = '/dev/shm'

studyarea                   = f'{layer_dir}/study_area_land_mask.gpkg'
studyarealayer              = 'study_area_land_mask'

lidar_dir                   = '../lidar_dl'
lidar_process_dir           = f'{lidar_dir}/processed'
lidar_dl_dir                = f'{lidar_dir}/CA_NoCAL_3DEP_Supp_Funding_2018_D18_Laz'

lidar_dl_tif_dir            = '/dev/shm/lidar_tiffs'
#lidar_dl_tif_dir    = lidar_dl_dir + '/geotiffs'
lidar_height_merged_tif     = f'{lidar_dl_tif_dir}/CA_NoCAL_3DEP_Supp_Funding_2018_D18_SF_Height_Merged.tif'
height_map_tif              = f'{lidar_process_dir}/ca_3dep_2018_sf_height_map.tif'
height_map_max_tif          = f'{lidar_process_dir}/ca_3dep_2018_sf_height_map_max_height.tif'
height_map_dl_tif           = f'{lidar_process_dir}/ca_3dep_2018_sf_height_map_hag_delaunay.tif'
height_map_mask             = f'{layer_dir}/ca_3dep_2018_sf_height_map_mask.gpkg'

pscope_dir                          = '../pscope_analytic_tiffs'
pscope_processed_dir                = f'{pscope_dir}/processed'
pscope_intraband_aligned_dir        = f'{pscope_processed_dir}/intraband_aligned'
pscope_intraband_aligned_out_dir    = f'{pscope_intraband_aligned_dir}/output'
pscope_study_dir                    = f'{pscope_processed_dir}/study_area'

aligned_raster_dir          = f'../aligned'

skysat_dir                  = '../skysat_skycol_tiffs'
skysat_dl_dir               = f'{skysat_dir}/skysat_collect_dl'
skysat_processed_dir        = f'{skysat_dir}/processed'
skysat_basename             = f'sks_collect_sf_2022_04_23'
skysat_mask                 = f'{layer_dir}/{skysat_basename}_mask.gpkg'
skysat_dl_bands             = {1:'blue', 2:'green', 3:'red', 4:'nir'}
skysat_bands                = {**skysat_dl_bands, 5:'pan'}

training_area_mask          = f'{layer_dir}/training_area_mask.gpkg'
training_mask_dir           = '../training_tiffs'
training_work               = f'{training_mask_dir}/work'

