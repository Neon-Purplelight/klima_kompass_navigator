# Import necessary library
import pandas as pd
import netCDF4 as nc
import numpy as np

################################################################################
# Data processing
################################################################################
# => dataManager dm 
# Here, all classes and functions for data processing 
    # Load data (once, to improve performance)

# For temp rolling-average: Skip 
# def preprocess_temperature_data(df_temp):
#     df_temp['mov_avg'] = df_temp['JJA'].rolling(20).mean()
#     return df_temp

def read_co2_data(pathToFile: str):
    # Read CO2 data
    df_co2 = pd.read_csv(pathToFile)

    return df_co2

def preprocess_co2_data(df_co2):
    # Preprocess CO2 data
    world_df = df_co2[df_co2['country'] == 'World']
    world_df = world_df[world_df['year'] >= 1880]

    new_columns = ['Entity', 'Year', 'Annual CO₂ emissions']
    df_co2 = pd.DataFrame(columns=new_columns)

    df_co2['Entity'] = world_df['country']
    df_co2['Year'] = world_df['year']
    df_co2['Annual CO₂ emissions'] = world_df['co2']
    df_co2.reset_index(drop=True, inplace=True)

    return df_co2

def read_continental_data(pathToFile: str):
    # Read the continental data
    df_continents = pd.read_csv(pathToFile)

    return df_continents

def read_temp_data(pathToFile: str):
    # Read temperature data
    df_temp = pd.read_csv(pathToFile, skiprows=1)

    return df_temp

# ------------------------------------------------------------------------------
# pedo_1
# ------------------------------------------------------------------------------
# Read netCDF4 structure
# import netCDF4 as nc

# # Öffnen der NetCDF-Datei
# file_path = 'SMI_Gesamtboden_monatlich.nc'
# dataset = nc.Dataset(file_path, 'r')

# # Auflisten aller Dimensionen
# print("Dimensionen:", dataset.dimensions.keys())

# # Auflisten aller Variablen und deren Attribute
# print("Variablen:")
# for var in dataset.variables:
#     print(var, dataset.variables[var])

# # Schließen der Datei
# dataset.close()

def preprocess_netcdf_data(pathToFile: str):
    dataset = nc.Dataset(pathToFile, 'r')
    lats = dataset.variables['lat'][:]
    lons = dataset.variables['lon'][:]
    data = dataset.variables['SMI'][:]
    time_var = dataset.variables['time']
    time_data = time_var[:]
    units = time_var.units
    date_values = nc.num2date(time_data, units)
    # Setze das Datum auf den ersten Tag jedes Monats
    date_values = [date.replace(day=1) for date in date_values]
    dataset.close()
    return lats, lons, data, date_values

# def remove_months(input_file, output_file):
#     with nc.Dataset(input_file, 'r') as src, nc.Dataset(output_file, 'w', format='NETCDF4') as dst:
#         # Zeitvariable extrahieren
#         time_var = src['time']
#         time_units = time_var.units
#         time_calendar = time_var.calendar

#         # Konvertieren der Zeittage in tatsächliche Daten
#         dates = nc.num2date(time_var[:], units=time_units, calendar=time_calendar)

#         # Bestimme die Indizes der zu behaltenden Daten (April bis Oktober)
#         keep_indices = [i for i, date in enumerate(dates) if 4 <= date.month <= 10]

#         # Kopieren der Dimensionen (außer 'time')
#         for name, dimension in src.dimensions.items():
#             if name == 'time':
#                 dst.createDimension(name, len(keep_indices))
#             else:
#                 dst.createDimension(name, len(dimension))

#         # Kopieren der Variablen mit Komprimierung
#         for name, variable in src.variables.items():
#             # Attribute kopieren, außer _FillValue
#             attrs = {k: variable.getncattr(k) for k in variable.ncattrs() if k != '_FillValue'}

#             # Erstellen der Variablen mit Komprimierung
#             if 'time' in variable.dimensions:
#                 new_var = dst.createVariable(name, variable.datatype, variable.dimensions, zlib=True, complevel=4)
#                 if name == 'time':
#                     # Weise die gefilterten Datumswerte direkt zu
#                     new_var[:] = time_var[keep_indices]
#                 else:
#                     # Für alle anderen Variablen, die Zeit enthalten, die gefilterten Daten anwenden
#                     new_var[:] = variable[keep_indices]
#             else:
#                 # Keine Komprimierung notwendig, wenn die Variable nicht zeitabhängig ist
#                 new_var = dst.createVariable(name, variable.datatype, variable.dimensions)
#                 new_var[:] = variable[:]

#             # Attribute zuweisen, nachdem die Daten zugewiesen wurden
#             new_var.setncatts(attrs)

#     print(f'Gefilterte NetCDF-Datei gespeichert als: {output_file}')

# # Pfade zur ursprünglichen und zur neuen Datei
# #input_file = 'SMI_Gesamtboden_monatlich.nc'   # Pfad zur ursprünglichen Datei
# #output_file = 'filtered_SMI_Gesamtboden_monatlich.nc'   # Pfad zur neuen gefilterten Datei

# input_file = 'SMI_Oberboden_monatlich.nc'   # Pfad zur ursprünglichen Datei
# output_file = 'filtered_SMI_Oberboden_monatlich.nc'   # Pfad zur neuen gefilterten Datei

# # Ausführen der Funktion
# remove_months(input_file, output_file)

def translate_month(date):
    english_to_german_months = {
    "January": "Januar",
    "February": "Februar",
    "March": "März",
    "April": "April",
    "May": "Mai",
    "June": "Juni",
    "July": "Juli",
    "August": "August",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Dezember"
}
    english_month = date.strftime("%B")
    german_month = english_to_german_months[english_month]
    return date.strftime("%d. ") + german_month + date.strftime(" %Y")

