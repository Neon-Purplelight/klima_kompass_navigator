# Import necessary library
import pandas as pd
import netCDF4 as nc
import numpy as np
import json

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
# klima_2
# ------------------------------------------------------------------------------
def process_and_save_json(input_json_path, output_json_path):
    # Load the original GeoJSON file
    with open(input_json_path, "r") as json_file:
        world_geo = json.load(json_file)

    # Define a mapping for country name replacements
    country_replacements = {
        "United States of America": "United States",
        "Guinea Bissau": "Guinea-Bissau",
        "The Bahamas": "Bahamas",
        "Czech Republic": "Czechia",
        "United Republic of Tanzania": "Tanzania",
        "Democratic Republic of the Congo": "Congo",
        "Swaziland": "Eswatini",
        "Republic of Serbia": "Serbia",
        "Macedonia": "North Macedonia",
        "Ivory Coast": "Cote d'Ivoire"
    }

    # Update the 'name' property for each feature in the GeoJSON
    for feature in world_geo["features"]:
        country_name = feature["properties"]["name"]
        if country_name in country_replacements:
            feature["properties"]["name"] = country_replacements[country_name]

    # Save the processed GeoJSON to the original file
    with open(output_json_path, "w") as json_out_file:
        json.dump(world_geo, json_out_file)

    # # Example usage
    # input_json_path = 'data/world-countries.json'
    # output_json_path = 'data/processed_world-countries.json'
    # process_and_save_json(input_json_path, output_json_path)

def extract_country_names(json_path):
    with open(json_path, "r") as json_file:
        world_geo = json.load(json_file)
        country_names = [feature["properties"]["name"] for feature in world_geo["features"]]
    return country_names

    # # Extract country names from the processed JSON
    # country_names = extract_country_names(output_json_path)

def process_and_save_csv(input_file_path, output_file_path, country_names):
    # Read the original CSV file
    df = pd.read_csv(input_file_path)
    df_continents = pd.read_csv("data/continents-according-to-our-world-in-data.csv")

    # Select and reorder columns
    selected_columns = ["country", "iso_code", "population", "gdp", "year", "co2", "coal_co2", 
                        "oil_co2", "gas_co2", "cement_co2", "flaring_co2", 
                        "other_industry_co2", "co2_per_capita", "cumulative_co2", 
                        "cumulative_coal_co2", "cumulative_oil_co2", 
                        "cumulative_gas_co2", "cumulative_cement_co2", 
                        "cumulative_flaring_co2", "cumulative_other_co2", 
                        "land_use_change_co2", "share_global_co2", 
                        "share_global_cumulative_co2", "temperature_change_from_co2", 
                        "total_ghg", "total_ghg_excluding_lucf"]
    df = df[selected_columns]

    # Set 'country' and 'year' as the index
    df = df.set_index(['country', 'year'])

    # Interpolate missing values using linear interpolation
    df['population'] = df['population'].interpolate(method='linear')

    # Reset the index to make 'country' and 'year' regular columns
    df = df.reset_index()

    # Merge the dataframes based on 'iso_code' and 'Code'
    merged_data = pd.merge(df, df_continents, left_on='iso_code', right_on='Code', how='left')

    # Rename columns to match the desired structure
    merged_data.rename(columns={'Continent': 'continent'}, inplace=True)

    # Drop unnecessary columns from the merged dataframe
    merged_data.drop(['Entity', 'Code', 'Year'], axis=1, inplace=True)

    # Reorder the columns
    column_order = ['country', 'continent'] + [col for col in merged_data.columns if col not in ['country', 'continent']]
    merged_data = merged_data[column_order]

    # Filter the dataframe to include only countries in the provided list
    merged_data = merged_data[merged_data['country'].isin(country_names)]

    # Filter rows to include only data from 1850 onwards
    merged_data = merged_data[merged_data['year'] >= 1850]

    # Save the processed DataFrame to the CSV file
    merged_data.to_csv(output_file_path, index=False)

    # # Process and save the CSV
    # input_file_path_csv = 'data/owid-co2-data.csv'
    # output_file_path_csv = 'data/processed_data.csv'
    # process_and_save_csv(input_file_path_csv, output_file_path_csv, country_names)

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

# ------------------------------------------------------------------------------
# hydro_2
# ------------------------------------------------------------------------------
# Datenbereinigungsfunktion
def process_logging_data(csv_file_path):
    data = pd.read_csv(csv_file_path, delimiter=';', decimal=',', na_values=[''])
    data = data.apply(pd.to_numeric, errors='coerce')
    return data