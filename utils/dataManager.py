# Import necessary library
import pandas as pd

################################################################################
# Data processing
################################################################################
# => dataManager dm 
# Here, all classes and functions for data processing 
    # Load data (once, to improve performance)

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

# For temp rolling-average: Skip 
# def preprocess_temperature_data(df_temp):
#     df_temp['mov_avg'] = df_temp['JJA'].rolling(20).mean()
#     return df_temp
