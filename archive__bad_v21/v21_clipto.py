import xarray as xr
import glob
from shapely.geometry import mapping
import geopandas as geo

def clip(rast,shp,name,yearmonthdotnc):
    basin = geo.read_file(shp)
    # rast = xr.open_dataset(raster)
    rast.rio.write_crs(4326,inplace=True)
    rast.rio.set_spatial_dims(x_dim="lon",y_dim="lat")
    r_clip = rast.rio.clip(basin.geometry.apply(mapping),basin.crs) ### !!! ###
#     plt.imshow(np.where(r_clip[0]<0,np.nan,r_clip[0]))
    r_clip.to_netcdf(f'v21_monthly_{name}/{name}_{yearmonthdotnc}')
    return r_clip

for x in glob.glob('gldas__v21__clip__monthly/*.nc'):
    # print(x[-10:-3])
    # break
    raster = xr.open_dataset(x)
    clip(raster,'umm/umm.shp','umm',x[-10:])
    clip(raster,'wasia/wasia.shp','wasia',x[-10:])
    clip(raster,'wajid/wajid.shp','wajid',x[-10:])