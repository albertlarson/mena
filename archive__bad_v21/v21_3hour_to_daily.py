import glob
import xarray as xr

x = glob.glob('gldas__v21__clip/*.nc')
x = x[7:]
print(x[0])
print(len(x))
days = list(range(0,65000,8))

for day in days:
    o = xr.open_dataset(x[day])
    oo = xr.open_dataset(x[day+1])
    ooo = xr.open_dataset(x[day+2])
    oooo = xr.open_dataset(x[day+3])
    ooooo = xr.open_dataset(x[day+4])
    oooooo = xr.open_dataset(x[day+5])
    ooooooo = xr.open_dataset(x[day+6])
    oooooooo = xr.open_dataset(x[day+7])
    
    w0 = o.Rainf_tavg[0]+\
    oo.Rainf_tavg[0]+\
    ooo.Rainf_tavg[0]+\
    oooo.Rainf_tavg[0]+\
    ooooo.Rainf_tavg[0]+\
    oooooo.Rainf_tavg[0]+\
    ooooooo.Rainf_tavg[0]+\
    oooooooo.Rainf_tavg[0]
    
    z = xr.Dataset(
    
        data_vars={
        "Rain_f":(["lat","lon"],w0.data,{"units": "kg m-2 s-1"}),
        "Rainfall":(["lat","lon"],w0.data*24*60*60,{"units": "mm"})}

        ,

        coords={
            "lon":(["lon"],o.lon.data),
            "lat":(["lat"],o.lat.data)}

        ,

        attrs={
            "date" : f"{str(x[day][21:29])}"}
    )
    z.to_netcdf(f"gldas__v21__clip__daily/ksa_gld_v21_daily_{x[day][21:29] + x[day][-3:]}")
    # z.to_netcdf('gldas__v21__clip__daily/hey5.nc')