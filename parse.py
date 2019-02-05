import json
import csv

class total:
	def __init__(self,data):
		pass
	def parse(self,f):
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['index', 'game_name', 'player', 'hero_ID', 'hero_name', 'turn', 'phase', 'action', 'action_AP', 'ability', 'ability_cast', 'ability_target', 'current_HP', 'current_location', 'move_action', 'targeted_by', 'score', 'obj_zone', 'cooldown_per_ability', 'target_location', 'ability_location', 'is_lobbing', 'is_piercing', 'area_effect', 'is_wall', 'is_in_respawn_zone', 'game_type'])
		for i in range(2, len(data)):
			self.ability_target = []
			row = data[i]
			self.index = i
			self.game_name = "game"
			self.turn = row['currentTurn']
			self.phase = row['currentPhase']
			for j in range(len(row['players'])):
				self.player = j+1 # player could be 1 or 2
				self.score = row['players']['score']
				for hero in row['castAbilities'][j]:
					self.ability = hero['abilityName']
					self.AOE = find_ability_property(data[0]['abilityConstants'],self.ability)[0]
					self.ability_cost = find_ability_property(data[0]['abilityConstants'],self.ability)[3]
					#TODO underStanding what it is
					self.ability_location = hero['endCell']
					self.caster_hero_id = hero['casterId']
					self.hero_name = find_hero_name(data[1]['heroes'],self.caster_hero_id)
					self.current_hp = find_hp(row['players'][j]['heroes'],self.caster_hero_id)
					self.current_location = find_location(row['players'][j]['heroes'],self.caster_hero_id)
					self.is_lobbing = find_ability_property(data[0]['abilityConstants'],self.ability)[1]
					self.is_piercing = find_ability_property(data[0]['abilityConstants'],self.ability)[2]
					self.ability_target = find_ability_target()
					writer.writerow([])

def find_ability_target():#TODO
	pass


def find_ability_property(abilities,name):
	for ability in abilities:
		if ability['name'] == name:
			return [ability['areaOfEffect'],ability['isLobbing'],ability['isPiercing'],ability['APCost']]


def find_hero_name(heroes,id):
	for hero in heroes:
		if hero['id'] == id:
			return hero['name']


def find_location(heroes,id):
	for hero in heroes:
		if hero['id'] == id:
			return hero['currentCell']

def find_hp(heroes,id):
	for hero in heroes:
		if hero['id'] == id:
			return hero['currentHP']

with open('server_view.log') as f:
	data = json.load(f)
with open('server_view.csv', mode='w') as f:
	total(data).parse(f)
