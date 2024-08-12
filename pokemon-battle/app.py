from flask import Flask, jsonify, request
import pandas as pd
from utils import load_pokemon_data, normalize_name
from battle import Pokemon, Battle
import threading

app = Flask(__name__)

# Dataset is Loading 
pokemon_df = load_pokemon_data()

# To store ongoing battles in-memory
active_battles = {}

def retrieve_pokemon_data(pokemon_name):
    filtered_data = pokemon_df[pokemon_df['name'] == pokemon_name]
    
    pokemon_info = {
        'name': pokemon_name,
        'type1': filtered_data['type1'].values[0],
        'type2': filtered_data['type2'].values[0],
        'hp': filtered_data['hp'].values[0],
        'attack': filtered_data['attack'].values[0],
        'defense': filtered_data['defense'].values[0],
        'speed': filtered_data['speed'].values[0],
        'against': {
            f"against_{filtered_data['type1'].values[0]}": filtered_data[f"against_{filtered_data['type1'].values[0]}"].values[0]
        },
        'is_legendary': filtered_data['is_legendary'].values[0]
    }
    
    # if it's not NaN then add only second type.
    secondary_type = filtered_data['type2'].values[0]
    if pd.notna(secondary_type):
        pokemon_info['against'][f"against_{secondary_type}"] = filtered_data[f"against_{secondary_type}"].values[0]
    
    return pokemon_info


def battle_simulation_thread(battle_instance):
    battle_result = battle_instance.simulate()
    active_battles[battle_instance.battle_id] = {'status': 'BATTLE_COMPLETED', 'result': battle_result}

@app.route('/api/pokemon', methods=['GET'])
def get_pokeman_list():
    current_page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('per_page', 10))

    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page

    pokemon_subset = pokemon_df.iloc[start_index:end_index].to_dict(orient='records')
    return jsonify(pokemon_subset)

@app.route('/api/battle', methods=['POST'])
def start_battle():
    request_data = request.get_json()
    pokemon_1_name = request_data.get('pokemon1')
    pokemon_2_name = request_data.get('pokemon2')


    print("+++++++++=============+++++++++++++++")
    print(pokemon_1_name)

    try:
        pokemon_1_info = retrieve_pokemon_data(pokemon_1_name)
        pokemon_2_info = retrieve_pokemon_data(pokemon_2_name)


        pokemon_1 = Pokemon(pokemon_1_info)
        pokemon_2 = Pokemon(pokemon_2_info)

        print("______________________________")
        print(pokemon_1)
        battle_instance = Battle(pokemon_1, pokemon_2)
        active_battles[battle_instance.battle_id] = {'status': 'BATTLE_INPROGRESS'}
        print(active_battles)

        threading.Thread(target=battle_simulation_thread, args=(battle_instance,)).start()

        return jsonify({'battle_id': battle_instance.battle_id})

    except ValueError as error:
        return jsonify({'error': str(error)}), 400

@app.route('/api/battle/<battle_id>', methods=['GET'])
def check_battle_status(battle_id):
    battle_status = active_battles.get(battle_id)

    if not battle_status:
        return jsonify({'error': 'Battle not found'}), 404

    return jsonify(battle_status)


if __name__ == '__main__':
    app.run(debug=True)
