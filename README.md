# Merging WRF Daily Output NetCDF Files

This script merges multiple daily WRF output NetCDF files into a single file for easier analysis. 

## Installation

1. Install the required libraries:
    ```bash
    pip install xarray pandas matplotlib glob
    ```

## Usage

1. **Set the `data_dir` variable** to the directory containing your WRF daily output files. 
2. **Set the `output_path` variable** to the desired location for the merged NetCDF file.
3. **Run the script.**

## Script

```python
# installing required libraries for analysis
# pip install xarray pandas matplotlib glob

# importing downloaded libraries
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Set the directory containing your NetCDF files
data_dir = "E:/jupyter/DATA/wrf MAM/daily_output/"

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
output_path = "E:/jupyter/DATA/wrf MAM/merged_wrf_data.nc"

# Save the merged dataset to NetCDF format
merged_ds.to_netcdf(output_path)

print(f"Merged dataset saved to {output_path}")

##############################################################################################################3
Explanation
Import Libraries: The code imports necessary libraries:
xarray for handling NetCDF data.
pandas for data manipulation.
matplotlib.pyplot for plotting.
glob for finding files with wildcards.
Set Directories: The code defines:
data_dir: Path to the directory containing WRF daily output files.
output_path: Path where the merged NetCDF file will be saved.
Get File Paths: glob.glob(data_dir + "*.nc") finds all NetCDF files within the data directory.
Load Datasets: The code iterates through the found files, opening each NetCDF file using xr.open_dataset. This creates a list of xarray.Dataset objects.
Concatenate Datasets: xr.concat(datasets, dim='time') merges the datasets along the 'time' dimension, creating a single xarray.Dataset representing all the data.
Sort by Time: The code ensures the 'time' dimension is sorted correctly using merged_ds.sortby('time').
Select Data: The script selects data from the first day of the first week to the last day of the fourth week. This can be customized to select the desired time period.
Save Merged Dataset: merged_ds.to_netcdf(output_path) saves the merged dataset to the specified output path in NetCDF format.
Print Message: The code prints a message confirming the file has been saved.
Modifications
You can adjust the start_date and end_date variables to select a different time period.
Modify the output_path variable to change the destination for the merged file.
You can customize the data selection and analysis further using xarray's powerful capabilities.
