# installing required libraries for analysis
# pip install xarray pandas matplotlib glob

# importing downloaded libraries
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Set the directory containing your NetCDF files
data_dir = "test_data_set/"

# Get a list of all NetCDF files in the directory
file_paths = glob.glob(data_dir + "*.nc")

# Load all datasets into a list
datasets = [xr.open_dataset(file_path) for file_path in file_paths]

# Concatenate the datasets along the 'time' dimension
merged_ds = xr.concat(datasets, dim='time')


# Sort the 'time' dimension
merged_ds = merged_ds.sortby('time')

# Select data from the first day of the first week to the last day of the fourth week
start_date = merged_ds['time'][0].values
end_date = merged_ds['time'][-1].values  

merged_ds = merged_ds.sel(time=slice(start_date, end_date))

# Set the output file path
output_path = "E:/merged_wrf_data.nc"

# Save the merged dataset to NetCDF format
merged_ds.to_netcdf(output_path)

print(f"Merged dataset saved to {output_path}")

# Load the merged data
ds = xr.open_dataset('E:/merged_wrf_data.nc')

print(ds)

# Get latitude and longitude values
latitudes = ds.lat.values
longitudes = ds.lon.values

# Calculate the resolution
lat_res = abs(latitudes[1] - latitudes[0])
lon_res = abs(longitudes[1] - longitudes[0])

# Print the resolution
print(f"Latitude Resolution: {lat_res} degrees")
print(f"Longitude Resolution: {lon_res} degrees")

# Filter for the time period between February 1st and May 30th
ds = ds.sel(time=slice('2024-04-01', '2024-04-30'))

# Define the approximate latitude and longitude boundaries of Kenya
min_latitude = -4.0
max_latitude = 4.0
min_longitude = 34.0
max_longitude = 42.0

# Select data for Kenya using 'where' - corrected to use 'lat' and 'lon'
kenya_data = ds.where((ds.lat >= min_latitude) & (ds.lat <= max_latitude) & 
                       (ds.lon >= min_longitude) & (ds.lon <= max_longitude), drop=True)

# Convert to a pandas DataFrame
df = kenya_data.to_dataframe()

# Reset index to create separate columns for lon, lat, and time
df = df.reset_index()

# Rename columns to lon, lat, and rain
df = df.rename(columns={'lon': 'lon', 'lat': 'lat', 'dailyrain': 'rain'})

# Save to a CSV file in your E drive
df.to_csv('E:/wrf_data1.csv', index=False)
