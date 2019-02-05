import json
import csv
from pprint import pprint

class Constants:
    def __init__(self, data):
        self.game_constants()
        self.map()
        self.hero_constants()
        self.ability_constants()

    def game_constants(self):
        self.game_cs = data[0]['gameConstants']  # game constants

    def map(self):
        self.map_row_num = data[0]['map']['rowNum']
        self.map_column_num = data[0]['map']['columnNum']
        self.map_cells = data[0]['map']['cells']

    def hero_constants(self):
        self.hero_cs = {}  # hero constants
        for hero in data[0]['heroConstants']:
            self.hero_cs[hero['name']] = hero

    def ability_constants(self):
        self.ability_cs = {}  # ability constants
        for ability in data[0]['abilityConstants']:
            self.ability_cs[ability['name']] = ability


class Hero_IDs:
    def __init__(self, data):
        self.id = {}
        for i in range(2):
            for player in data[1]['heroes'][i]:
                #for hero in player:
                self.id[player['id']] = player
        pprint(self.id)

class _Parser:
    def __init__(self, data):
        self.constants = Constants(data)
        self.hero_IDs = Hero_IDs(data)  # call self.hero_IDs.id[j] where j is id of the hero. It returns a hero dict.

    def parse(self, f):
        writer = csv.writer(f, delimiter=',')
        writer.writerow(
            ['index', 'game_name', 'player', 'hero_ID', 'hero_name', 'turn', 'phase', 'action', 'action_AP', 'ability',
             'ability_cast', 'ability_target', 'current_HP', 'current_location', 'move_action', 'targeted_by', 'score',
             'obj_zone', 'cooldown_per_ability', 'target_location', 'ability_location', 'is_lobbing', 'is_piercing',
             'area_effect', 'is_wall', 'is_in_respawn_zone', 'game_type'])
        for i in range(2, len(data)):
            row = data[i]
            self.index = i
            self.game_name = None   #todo handle fucking game name
            for j in range(len(row['players'])):
                self.player = j  # player could be 0 or 1

            writer.writerow([])


if __name__ == "__main__":
    with open('server_view.log') as f:
        data = json.load(f)
    with open('server_view.csv', mode='w') as f:
        _Parser(data).parse(f)
