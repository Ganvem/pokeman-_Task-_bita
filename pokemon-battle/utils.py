import pandas as pd

# Dataset is Loading 
def load_pokemon_data(filepath='pokemon.csv'):
    df = pd.read_csv(filepath)
    return df

# The Input Pokémon name is normalize
def normalize_name(name):
    return name.strip().lower()
