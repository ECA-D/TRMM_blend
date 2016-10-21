# =============================================
# Remove all sea points from all TRMM data

# Author: I.Stepanov
#	  	: KNMI
# 		: 16.08.2016.
# =============================================

# Load python modules
import netCDF4
import pylab as pl
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from pylab import *
import math as m
from mpl_toolkits.basemap import Basemap, cm



in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/"
in_path_lsmsk_TRMM="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"
in_path_rr_SACA="/nobackup/users/stepanov/SACA/final/"

# Files
#===========================================================================================

# Precip TRMM
file_name='3B42_daily.2014_georef_SACA.nc'    
# ncks -d latitude,-24.875,25.125 -d longitude,80.125,179.875 3B42_daily.2015.12.29.7.nc 3B42_daily.2015.12.29.7_georef_SACA.nc

# Precip SACA rr
file_r_SACA='rr_0.25deg_regular.nc'

# Land Sea Maks TRMM specific
file_lsm_TRMM='TMPA_mask_georef_SACA_match_TRMM_grid.nc'
#ncks -d lat,-24.875,25.250 -d lon,80.125,179.875 TMPA_mask.nc TMPA_mask_georef_SACA_match_TRMM_grid.nc

#===========================================================================================

# Precip and elevation (Land Sea Mask)
nc_trmm        = Dataset(in_path+file_name,'r')                  # [latitude, longitude][201x400]
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM,'r')   # [lat,lon][201x400]
nc_SACA_rr     = Dataset(in_path_rr_SACA+file_r_SACA,'r')        # [longitude, latitude][400x201]

# Coordinates for TRMM
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# Coordinates for SACA
lons_saca = nc_SACA_rr.variables['longitude']
lats_saca = nc_SACA_rr.variables['latitude']

#===========================================================================================


# Extract the actual variable
# For TRMM data go from 1-365 in ncview, but python counts 0-364
trmm_precip = nc_trmm.variables['r'][0,:,:]                # [time, lat, lon], 0= 01.01.2014 (python)
trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:,:] # [time, latitude, longitude]   
saca_precip = nc_SACA_rr.variables['rr'][12053,:,:]        # 12053 = 01.Jan.2014. (python)  7030 = 31.03.2000. (panoply)
# 1-12418 in ncview, but python counts 0-12417



# Some data pre-processing
#===========================================================================================

fill_value=-999.9

# Python replacing syntax
# arr[arr > 255] = x

# All land points convert to 1
trmm_lsmask[trmm_lsmask!=100]=1.

# All sea points convert to 0
trmm_lsmask[trmm_lsmask==100]=fill_value

# New mask should now be: 1=land, 0=sea
# Multiply with TRMM data when plotting

print 'TRMM land sea mask',trmm_lsmask
print
print "TRMM precip is: ", trmm_precip
print


# Create netCDF files
sweep_xy = Dataset(in_path_lsmsk_TRMM+'NASA_lsmask_binary.nc','w', format='NETCDF4_CLASSIC') 
# level = dataset.createDimension('level', 10) 
# sweep_xy = binary_LS_MASK_TRMM.createGroup('sweep_xy')

# Dimensions
lat = sweep_xy.createDimension('latitude', 201)
lon = sweep_xy.createDimension('longitude', 400) 
time = sweep_xy.createDimension('time', None ) 

# variable
ls_mask_trmm = sweep_xy.createVariable('ls_mask_trmm','f4', ('latitude','longitude'))

ls_mask_trmm[:,:] = trmm_lsmask


# import netCDF4
# rootgrp = netCDF4.Dataset('test.nc', 'w', format='NETCDF4')
# sweep_xy = rootgrp.createGroup('sweep_xy')
# dim_azimuth = sweep_xy.createDimension('azimuth', None)
# dim_range = sweep_xy.createDimension('range', None)


# azimuths_var = sweep_xy.createVariable('azimuths','i4',('azimuth',))
# ranges_var = sweep_xy.createVariable('ranges','f4',('range',))
# dBZ_var = sweep_xy.createVariable('dBZ','f4',('azimuth','range',))


# azimuths_var[:] = np.arange(0,360)
# ranges_var[:] = np.arange(0, 128000., 1000.)
# dBZ_var[:] = data


quit()




