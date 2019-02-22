import json
import csv
from pprint import pprint

class total:
	def __init__(self,data):
		pass
	def parse(self,f):
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['index',
						 'game_name',
						 'player',
						 'hero_ID',
						 'hero_name',
						 'turn',
						 'phase',
						 'ability',
						 'ability_cast',
						 'ability_target',
						 'current_HP',
						 'current_location',
						 'score',
						 'ability_location',
						 'is_lobbing',
						 'is_piercing',
						 'area_effect'])
		#TODO game_type, action, action_ap, move_action, targeted_by, cooldown_per_ability, obj_zone, target_location, is_wall, is_in_respawn_zone
		for i in range(2, len(data)):
			row = data[i]
			self.index = i
			self.game_name = "game"
			self.turn = row['currentTurn']
			self.phase = row['currentPhase']
			if self.phase == 'ACTION':
				for hero in row['castAbilities']:
					self.ability = hero["abilityName"]
					self.AOE = find_ability_property(data[0]['abilityConstants'],self.ability)[0]
					self.ability_cost = find_ability_property(data[0]['abilityConstants'],self.ability)[3]
					#TODO underStanding what it is
					self.ability_location = hero['endCell']
					self.caster_hero_id = hero['casterId']
					self.player = (self.caster_hero_id%2 +1)
					self.score = row['players'][self.caster_hero_id%2]['score']
					self.hero_name = find_hero_name(data[1]['heroes'][self.caster_hero_id%2],self.caster_hero_id)
					self.current_hp = find_hp(row['players'][self.caster_hero_id%2]['heroes'],self.caster_hero_id)
					self.current_location = find_location(row['players'][self.caster_hero_id%2]['heroes'],self.caster_hero_id)
					self.is_lobbing = find_ability_property(data[0]['abilityConstants'],self.ability)[1]
					self.is_piercing = find_ability_property(data[0]['abilityConstants'],self.ability)[2]
					self.ability_target = find_ability_target(self.AOE,self.ability_location,row['players'][self.caster_hero_id%2]['heroes'])
					writer.writerow([
						self.index,
						self.game_name,
						self.player,
						self.caster_hero_id,
						self.hero_name,
						self.turn,
						self.phase,
						self.ability,
						self.ability_cost,#thisone
						self.ability_target,
						self.current_hp,
						self.current_location,
						self.score,
						self.ability_location,
						self.is_lobbing,
						self.is_piercing,
						self.AOE
					])
			elif self.phase == 'MOVE':
				for j in range(len(row['players'])):
					for hero in row['players'][j]['heroes']:
						self.player = j+1
						self.caster_hero_id = hero['id']
						self.current_hp = hero['currentHP']
						self.current_location = hero['currentCell']
						self.hero_name = hero['type']
						self.score = row['players'][j]['score']
						writer.writerow([
							self.index,
							self.game_name,
							self.player,
							self.caster_hero_id,
							self.hero_name,
							self.turn,
							self.phase,
							'-',
							'-',  # thisone
							'-',
							self.current_hp,
							self.current_location,
							self.score,
							'-',
							'-',
							'-',
							'-'
						])

def find_ability_target(AOE,location,data):
	row = location['row']
	col = location['column']
	col -= AOE
	heroes = []
	i = 0
	while(True):
		for j in range(i*(-1),i+1):
			if row+j <=31 and row+j>0:
				x = find_hero_from_cell(row+j,col,data)
				if x != None:
					heroes.append((x['type'],x['id']))
		col += 1
		if col>location['column']+AOE:
			break
		else:
			if i>=AOE:
				i-=1
			else:
				i+=1
	return heroes


def find_hero_from_cell(i,j,data):
	for hero in data:
		if hero['currentCell']['row'] == i and hero['currentCell']['column']==j:
			return hero
	return None

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
