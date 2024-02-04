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

# ------------------------------------------------------------------------------
# start_page_2
# ------------------------------------------------------------------------------

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
        "Republic of the Congo":"Congo",
        "Democratic Republic of the Congo": "Democratic Republic of Congo",
        "United Republic of Tanzania": "Tanzania",
        "Somaliland" :"Somalia",
        "Swaziland": "Eswatini",
        "Republic of Serbia": "Serbia",
        "Macedonia": "North Macedonia",
        "Ivory Coast": "Cote d'Ivoire"
    }

    # Remove the feature with the id '-99' (which represents Somaliland)
    world_geo["features"] = [
        feature for feature in world_geo["features"]
        if feature.get("id") != "-99"
    ]

    # Optionally, if you want to merge it, set the 'id' of Somalia to 'SOM'
    for feature in world_geo["features"]:
        if feature["properties"]["name"] == "Somalia":
            feature['id'] = 'SOM'
        # Apply any other name replacements
        if feature["properties"]["name"] in country_replacements:
            feature["properties"]["name"] = country_replacements[feature["properties"]["name"]]

    # Save the processed GeoJSON to the output file
    with open(output_json_path, "w") as json_out_file:
        json.dump(world_geo, json_out_file)

def extract_country_names(json_path):
    with open(json_path, "r") as json_file:
        world_geo = json.load(json_file)
        country_names = [feature["properties"]["name"] for feature in world_geo["features"]]
    return country_names

def process_and_save_csv(input_file_path, output_file_path, country_names):
    # Read the original CSV file
    df = pd.read_csv(input_file_path)
    df_continents = pd.read_csv("data/originalData/klima_1/continents-according-to-our-world-in-data.csv")

    # Replace the ISO code for South Sudan from 'SSD' to 'SDS'
    df['iso_code'] = df['iso_code'].replace('SSD', 'SDS')

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

# ------------------------------------------------------------------------------
# pedo_1
# ------------------------------------------------------------------------------
# Datensatz vor Upload vorprozessiert, da ansonsten zu groß für github   
def read_netCDF4_structure(pathToFile: str):
    import netCDF4 as nc

    # Öffnen der NetCDF-Datei
    file_path = 'SMI_Gesamtboden_monatlich.nc'
    dataset = nc.Dataset(file_path, 'r')

    # Auflisten aller Dimensionen
    print("Dimensionen:", dataset.dimensions.keys())

    # Auflisten aller Variablen und deren Attribute
    print("Variablen:")
    for var in dataset.variables:
        print(var, dataset.variables[var])

    # Schließen der Datei
    dataset.close()

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

def remove_months(input_file, output_file):
    with nc.Dataset(input_file, 'r') as src, nc.Dataset(output_file, 'w', format='NETCDF4') as dst:
        # Zeitvariable extrahieren
        time_var = src['time']
        time_units = time_var.units
        time_calendar = time_var.calendar

        # Konvertieren der Zeittage in tatsächliche Daten
        dates = nc.num2date(time_var[:], units=time_units, calendar=time_calendar)

        # Bestimme die Indizes der zu behaltenden Daten (April bis Oktober)
        keep_indices = [i for i, date in enumerate(dates) if 4 <= date.month <= 10]

        # Kopieren der Dimensionen (außer 'time')
        for name, dimension in src.dimensions.items():
            if name == 'time':
                dst.createDimension(name, len(keep_indices))
            else:
                dst.createDimension(name, len(dimension))

        # Kopieren der Variablen mit Komprimierung
        for name, variable in src.variables.items():
            # Attribute kopieren, außer _FillValue
            attrs = {k: variable.getncattr(k) for k in variable.ncattrs() if k != '_FillValue'}

            # Erstellen der Variablen mit Komprimierung
            if 'time' in variable.dimensions:
                new_var = dst.createVariable(name, variable.datatype, variable.dimensions, zlib=True, complevel=4)
                if name == 'time':
                    # Weise die gefilterten Datumswerte direkt zu
                    new_var[:] = time_var[keep_indices]
                else:
                    # Für alle anderen Variablen, die Zeit enthalten, die gefilterten Daten anwenden
                    new_var[:] = variable[keep_indices]
            else:
                # Keine Komprimierung notwendig, wenn die Variable nicht zeitabhängig ist
                new_var = dst.createVariable(name, variable.datatype, variable.dimensions)
                new_var[:] = variable[:]

            # Attribute zuweisen, nachdem die Daten zugewiesen wurden
            new_var.setncatts(attrs)

    print(f'Gefilterte NetCDF-Datei gespeichert als: {output_file}')

# Pfade zur ursprünglichen und zur neuen Datei
#input_file = 'SMI_Gesamtboden_monatlich.nc'   # Pfad zur ursprünglichen Datei
#output_file = 'filtered_SMI_Gesamtboden_monatlich.nc'   # Pfad zur neuen gefilterten Datei

#input_file = 'SMI_Oberboden_monatlich.nc'   # Pfad zur ursprünglichen Datei
#output_file = 'filtered_SMI_Oberboden_monatlich.nc'   # Pfad zur neuen gefilterten Datei

# Ausführen der Funktion
#remove_months(input_file, output_file)

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

def merge_schadholz_niederschlag_and_save(schadholz_path, niederschlag_path):
    # Laden der Schadholz-Daten mit Semikolon als Trennzeichen
    schadholz_df = pd.read_csv(schadholz_path, sep=';')
    
    # Laden der Niederschlagsdaten, Umwandlung des Dezimaltrennzeichens und Umbenennung der Spalte
    niederschlag_df = pd.read_csv(niederschlag_path, sep='\t', encoding='utf-8')
    niederschlag_df['Niederschlag'] = niederschlag_df['Niederschlag'].str.replace(',', '.').astype(float)
    niederschlag_df = niederschlag_df.rename(columns={'Niederschlag': 'Durchschnittsniederschlag'})
    
    # Zusammenführen der Datensätze basierend auf "Jahr"
    merged_df = pd.merge(schadholz_df, niederschlag_df, on='Jahr', how='left')
    
    # Ausgabepfad festlegen
    output_path = 'data/processedData/hydro_2/merged_schadholz_niederschlag.csv'
    
    # Speichern des zusammengeführten Datensatzes als CSV-Datei mit Semikolon als Trennzeichen
    merged_df.to_csv(output_path, sep=';', index=False, encoding='utf-8')
    
    return output_path

# Pfade der Eingabedateien
schadholz_path = 'data/processedData/hydro_2/processed_schadholz.csv'
niederschlag_path = 'data/originalData/hydro_2/niederschlag_gebietsmittel.txt'

# Ausführen der Funktion und Speichern des neuen Datensatzes
#output_path = merge_schadholz_niederschlag_and_save(schadholz_path, niederschlag_path)

def process_dataset(file_path, output_path):
    data = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1')
    
    filtered_data = data[(data['3_Auspraegung_Label'] == 'Insgesamt') & (data['4_Auspraegung_Label'] == 'Insgesamt')].copy()
    
    filtered_data['HES002__Schadholzeinschlag__1000_cbm'] = filtered_data['HES002__Schadholzeinschlag__1000_cbm'].str.replace(',', '.').astype(float)
    
    aggregated_data = filtered_data.pivot_table(index='Zeit', columns='2_Auspraegung_Label', values='HES002__Schadholzeinschlag__1000_cbm', aggfunc='sum')
    
    expected_columns = ['Trockenheit', 'Sonstiges', 'Schnee/Duft', 'Wind/Sturm', 'Insekten']
    for column in expected_columns:
        if column not in aggregated_data.columns:
            aggregated_data[column] = float('nan')
    aggregated_data = aggregated_data.rename(columns={'Sonstiges': 'Sonstige Ursachen'})
    
    final_data_columns = ['Jahr', 'Trockenheit', 'Sonstige Ursachen', 'Schnee/Duft', 'Wind/Sturm', 'Insekten']
    aggregated_data.reset_index(inplace=True)
    aggregated_data = aggregated_data.rename(columns={'Zeit': 'Jahr'})
    final_data = aggregated_data[final_data_columns]
    
    # Anpassung des Formats: Korrekte Formatierung für das europäische Zahlenformat
    for col in final_data_columns[1:]:
        final_data[col] = final_data[col].apply(lambda x: format_european_decimal(x/1000) if pd.notnull(x) else '')

    with open(output_path, 'w', encoding='ISO-8859-1') as f:
        f.write('"' + '";"'.join(final_data_columns) + '"\n')
        final_data.to_csv(f, sep=';', index=False, header=False)

def format_european_decimal(x):
    """Formatiert eine Zahl im europäischen Stil mit Komma als Dezimaltrennzeichen und behält vier Nachkommastellen bei."""
    # Umwandlung in String mit Tausenderpunkt und Komma als Dezimalzeichen
    num_str = f"{x:.4f}".replace('.', ',')
    # Split bei Komma für separate Bearbeitung von Ganzzahl- und Dezimalteil
    parts = num_str.split(',')
    integer_part = parts[0].replace(',', '.')
    # Kombinieren der Teile mit europäischen Trennzeichen
    european_formatted = integer_part + ',' + parts[1]
    return european_formatted

file_path = 'data/originalData/hydro_2/41261-0003_flat.csv'
output_path = 'data/processedData/hydro_2/processed_schadholz.csv'

#process_dataset(file_path, output_path)

def process_logging_data(csv_file_path):
    data = pd.read_csv(csv_file_path, delimiter=';', decimal=',', na_values=[''])
    data = data.apply(pd.to_numeric, errors='coerce')
    return data