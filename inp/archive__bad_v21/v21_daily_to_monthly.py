import calendar
import glob
import xarray as xr

months = list(calendar.month_name)[1:]
months = [i.lower() for i in months]
# print(months)

def num_to_month(num):
    j=int(num)
    return months[j-1]

x = glob.glob('gldas__v21__clip__daily/*.nc')
x0 = [i[-11:-5] for i in x]
x1 = sorted(list(set(x0)))

arr = []
for i in x1:
    arr1 = []
    for jdj,j in enumerate(x):
        if i == j[-11:-5]:
            arr1.append(jdj)
    arr.append(arr1)

for idx,i in enumerate(arr):
    for jdj,j in enumerate(i):
        if jdj == 0:
            w0 = xr.open_dataset(x[j])
            w1 = w0.Rainfall
            u = xr.Dataset(
            data_vars={
            "Rainfall":(["lat","lon"],w1.data,{"units": "mm"})}

            ,

            coords={
                "lon":(["lon"],w0.lon.data),
                "lat":(["lat"],w0.lat.data)}

            ,

            attrs={
                "timeframe of observation" : f"{num_to_month(x[j][-7:-5])} {str(x[j][-11:-7])}"}
            )
            
        else:
            v0 = xr.open_dataset(x[j])
            v1 = v0.Rainfall
            w1.data += v1.data
    
    u.to_netcdf(f"gldas__v21__clip__monthly/ksa_gld_v21_monthly_{str(x[j][-11:-7])}_{x[j][-7:-5]}.nc")   