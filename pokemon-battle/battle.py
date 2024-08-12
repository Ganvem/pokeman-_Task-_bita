import uuid

class Pokemon:
    def __init__(self, pokeman_data):
        self.name = pokeman_data['name']
        self.type1 = pokeman_data['type1']
        self.type2 = pokeman_data.get('type2', None)
        self.attack = pokeman_data['attack']
        self.hp = pokeman_data['hp']
        self.defense = pokeman_data['defense']
        self.speed = pokeman_data['speed']
        self.against = pokeman_data['against']
        self.is_legendary = pokeman_data['is_legendary']

    def calculate_damage(self, opponent):
        print(opponent)
        print("+++++++++++++++++++++++++++++")
        # against_type1 = opponent.against[f"against_{self.type1}"]
        # against_type2 = opponent.against[f"against_{self.type2}"] if self.type2 else 1
        print(opponent)
        damage = (self.attack / 200) * 100 - (((2 / 4) * 100) + ((6 / 4) * 100))
        return max(0, damage)

class Battle:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.result = None
        self.battle_id = str(uuid.uuid4())

    def simulate(self):
        damage_to_pokemon2 = self.pokemon1.calculate_damage(self.pokemon2)
        damage_to_pokemon1 = self.pokemon2.calculate_damage(self.pokemon1)

        if damage_to_pokemon2 > damage_to_pokemon1:
            self.result = {'winner': self.pokemon1.name, 'won_by_margin': damage_to_pokemon2}
        elif damage_to_pokemon1 > damage_to_pokemon2:
            self.result = {'winner': self.pokemon2.name, 'won_by_margin': damage_to_pokemon1}
        else:
            self.result = {'winner': 'draw', 'won_by_margin': 0}

        return self.result
