#!/usr/bin/env python3

"""
@Title : HUCT - HTB University Completion Tracker
@Desc : A simple python script to track the completion of challenges, boxs and fortresses of universities on HackTheBox website.
@Author : Drahoxx (https://twitter.com/50mgDrahoxx)
@Date : 4 dec. 2023
"""

import logging
from requests import get
import argparse
from time import sleep

# Configure logging
logger = logging.getLogger(__name__)

"""
Global lists of all machines, challenges and fortess that exist on HTB
"""
MACHINES 	= 	[]
CHALLENGES 	= 	[]
FORTRESS 	= 	[]


class HTB_Player():
	"""
	@Desc : Defines a player.
	@Functions :
		- flag_challenge(challenge_id : int) -> void
		- flag_machine(machine_id : int) -> void
		- flag_fortress(fortress_id : int) -> void
		- get_name() -> str
		- get_id() -> int
	@Input :
		- id : int (player's id in htb database)
		- name : str (player's username)
	"""
	def __init__(self, id: int, name: str):
		self.id = id
		self.name = name
		self.flags = []
	def flag_challenge(self, challenge_id : int) -> None:
		flag = HTB_Challenge.get_challenge_by_id(challenge_id)
		if flag not in self.flags and flag != None:
			self.flags.append(flag)
			flag.add_flagger(self)
	def flag_machine(self, machine_id : int) -> None:
		flag = HTB_Machine.get_machine_by_id(machine_id)
		if flag not in self.flags and flag != None:
			self.flags.append(flag)
			flag.add_flagger(self)
	def flag_fortress(self, fortress_id : int) -> None:
		flag = HTB_Fortress.get_fortress_by_id(fortress_id)
		if flag not in self.flags and flag != None:
			self.flags.append(flag)
			flag.add_flagger(self)
	def get_name(self) -> str:
		return self.name
	def get_id(self) -> int:
		return self.id
	def __str__(self) -> str:
		return self.get_name()
	def __repr__(self) -> str:
		return self.get_name()


class _HTB_BaseObject():
	"""
	@Desc : Defines the base object for challenges, machines and fortress (anything that can be flagged).
	@Functions :
		- add_flagger(player : HTB_Player) -> void
		- flag_machine(machine_id : int) -> void
		- get_name() -> str
		- get_id() -> int
		- get_objtype() -> str
		- is_flagged
		- is_retired() -> bool
		- get_difficulty() -> str
	@Input :
		- id : int (id of the object in htb database)
		- name : str (name of the object in htb database)
		- retired : bool (if the object is retired or not)
		- difficulty : str (difficulty of the object)
	@Warnings :
		- Protected -- Should not be called as it is. Use its children.
	"""
	def __init__(self, id: int, name: str, retired: bool, difficulty: str):
		self.id = id
		self.name = name
		self.retired = retired
		self.difficulty = difficulty
		self.is_flagged_by_uni = False
		self.flagged_by = []

	def add_flagger(self, player : HTB_Player) -> None:
		"""
		@Title : add_flagger
		@Desc : Add a player to the list of people who flagged the challenge, alse switch is_flagged to true.
		@Input : HTB_Player
		@Output : void
		"""
		self.flagged_by.append(player)
		self.is_flagged_by_uni = True
	def get_id(self) -> int:
		return self.id
	def get_name(self) -> str:
		return self.name
	def get_objtype(self) -> str:
		if type(self) is HTB_Challenge:
			return "Challenge"
		if type(self) is HTB_Machine:
			return "Machine"
		if type(self) is HTB_Fortress:
			return "Fortress"
		return None
	def is_retired(self) -> bool:
		return self.retired
	def is_flagged(self) -> bool:
		return self.is_flagged_by_uni
	def get_difficulty(self) -> str:
		return self.difficulty
	def __str__(self):
		return self.get_name()
	def __repr__(self):
		return self.get_name()

class HTB_Challenge(_HTB_BaseObject):
	"""
	@Desc : Defines the challenge object.
	@Inherits : _HTB_BaseObject
	@Functions :
		- (static) get_challenge_by_id(id : int) -> HTB_Challenge
		- get_categorie() -> str
		From parent
		- add_flagger(player : HTB_Player) -> void
		- flag_machine(machine_id : int) -> void
		- get_name() -> str
		- get_id() -> int
		- get_objtype() -> str
		- is_flagged
		- is_retired() -> bool
		- get_difficulty() -> str
	@Input :
		- id : int (id of the object in htb database)
		- name : str (name of the object in htb database)
		- retired : bool (if the object is retired or not)
		- difficulty : str (difficulty of the object)
		---
		- str_categorie : str (string representation of the challenge categorie)
		OR
		- categorie : int (id of the categorie)
	"""
	def __init__(self, id: int, name: str, retired: bool, difficulty: str, str_categorie=None, categorie=0):
		_HTB_BaseObject.__init__(self, id, name, retired, difficulty)
		if str_categorie==None:
			if not isinstance(categorie,int):
				raise Error("Categorie should be an integer of the categorie id")
			categories = ["Reverse","Crypto","","Pwn","Web","Misc","Forensic","Mobile","","Hardware","GamePwn","Blockchain","","","","","","","","","AI-ML", "Coding", "ICS"]
			if categorie < 1 or categorie > len(categories):
				self.categorie = "Unknown"
			else:
				self.categorie = categories[categorie-1]
		else:
			self.categorie = str_categorie
		CHALLENGES.append(self)
	def get_categorie(self) -> str:
		return self.categorie
	def get_challenge_by_id(id):
		for challenge in CHALLENGES:
			if challenge.get_id() == id:
				return challenge
		else:
			return None

class HTB_Machine(_HTB_BaseObject):
	"""
	@Desc : Defines the machine (box) object.
	@Inherits : _HTB_BaseObject
	@Functions :
		- (static) get_machine_by_id(id : int) -> HTB_Machine
		From parent
		- add_flagger(player : HTB_Player) -> void
		- flag_machine(machine_id : int) -> void
		- get_name() -> str
		- get_id() -> int
		- get_objtype() -> str
		- is_flagged
		- is_retired() -> bool
		- get_difficulty() -> str
	@Input :
		- id : int (id of the object in htb database)
		- name : str (name of the object in htb database)
		- retired : bool (if the object is retired or not)
		- difficulty : str (difficulty of the object)
	"""
	def __init__(self, id: int, name: str, retired: bool, difficulty: str):
		_HTB_BaseObject.__init__(self, id, name, retired, difficulty)
		MACHINES.append(self)
	def get_machine_by_id(id):
		for machine in MACHINES:
			if machine.get_id() == id:
				return machine
		else:
			return None

class HTB_Fortress(_HTB_BaseObject):
	"""
	@Desc : Defines the fortress object.
	@Inherits : _HTB_BaseObject
	@Functions :
		- (static) get_fortress_by_id(id : int) -> HTB_Fortress
		From parent
		- add_flagger(player : HTB_Player) -> void
		- flag_machine(machine_id : int) -> void
		- get_name() -> str
		- get_id() -> int
		- get_objtype() -> str
		- is_flagged
		- is_retired() -> bool
		- get_difficulty() -> str
	@Input :
		- id : int (id of the object in htb database)
		- name : str (name of the object in htb database)
	"""
	def __init__(self, id: int, name: str):
		_HTB_BaseObject.__init__(self, id, name, False,'')
		FORTRESS.append(self)
	def get_fortress_by_id(id):
		for fortress in FORTRESS:
			if fortress.get_id() == id:
				return fortress
		else:
			return None


class HTB_Univ_Fetcher():
	"""
	@Desc : Defines the fetcher object to fetch the HTB database in the context of a university.
	@Functions :
		- __do_get(ENDPOINT : str) -> dict
		- get_university_members() -> list(HTB_Player)
		- update_challenges_own_by_player(player : HTB_Player) -> void
		- fetch_all_challenges() -> void
		- fetch_all_machines() -> void
		- fetch_all_fortress() -> void
	@Input :
		- KEY : str (HTB API key to request the database, can be obtained from https://app.hackthebox.com/profile/settings -> App Tokens)
		- UNIV_NUMBER : int (University id)
	"""
	def __init__(self,KEY: str, UNIV_NUMBER: int):
		self.KEY = KEY
		self.UNIV_NUMBER = UNIV_NUMBER

	def __do_get(self,ENDPOINT : str) -> dict:
		"""
		@Title : __do_get
		@Desc : Internal method to request HTB API endpoint, handles error in response.
		@Input : str
		@Output : dict
		@Todo : Remove recursion
		"""
		logger.debug(f"Fetching... {ENDPOINT}")
		g = get(ENDPOINT,headers={"Accept":"application/json","Authorization":f"Bearer {self.KEY}", "User-Agent":"ensibs/gcc"})
		res = g.json()
		if "message" in res and res["message"] == "Too Many Attempts.":
			logger.warning("Too Many Attempts. Sleeping for 20 seconds.")
			sleep(20) # Wait 20 secs and retry
			return self.__do_get(ENDPOINT)
		return res

	def get_university_members(self) -> list:
		"""
		@Title : get_university_members
		@Desc : List the members of a university (both active and pending / invited)
		@Output : list(HTB_Player)
		@Comments :
			- curl --location 'https://www.hackthebox.com/api/v4/university/members/518' -H "Accept: application/json" -H "Authorization: Bearer $(cat api_htb.sec)" | jq
		"""
		ENDPOINT = f"https://www.hackthebox.com/api/v4/university/members/{self.UNIV_NUMBER}"
		fetch_res = self.__do_get(ENDPOINT)
		univ_players = []
		for user_infos in fetch_res:
			player = HTB_Player(user_infos["id"],user_infos["name"])
			univ_players.append(player)
		return univ_players

	def update_challenges_own_by_player(self,player: HTB_Player) -> None:
		"""
		@Title : update_challenges_own_by_player
		@Desc : Update the challenges, fortress and machines a player has own (update the HTB_Challenge, ... and the HTB_Player)
		@Input : HTB_Player
		@Output : list(HTB_Player)
		"""
		ENDPOINT = f"https://www.hackthebox.com/api/v4/user/profile/activity/{player.id}"
		fetch_res = self.__do_get(ENDPOINT)
		for activity in fetch_res["profile"]["activity"]:
			if activity["object_type"] == "challenge":
				player.flag_challenge(activity["id"])
			elif activity["object_type"] == "machine":
				player.flag_machine(activity["id"])
			elif activity["object_type"] == "fortress":
				player.flag_fortress(activity["id"])
			else:
				logger.error(f'Unknown object_type: {activity["object_type"]}. An unknown object_type has been encountered in the update_challenges_own_by_player function. Maybe HackTheBox added a new type of challenge?')
				raise Exception('Unknown object_type', 'An unknown object_type has been encountered in the update_challenges_own_by_player function. Maybe HackTheBox added a new type of challenge ?')

	def fetch_all_challenges(self):
		"""
		List Active Challenges
		"""
		ENDPOINT = "https://www.hackthebox.com/api/v4/challenge/list"
		fetch_res = self.__do_get(ENDPOINT)
		logger.debug(f"Result for active challenge: {fetch_res}")
		for challenge in fetch_res["challenges"]:
			# Debug: log category ID if it's unexpected
			cat_id = challenge["challenge_category_id"]
			if cat_id < 1 or cat_id > 22:
				logger.warning(f"Unexpected category ID {cat_id} for challenge {challenge['name']}")
			HTB_Challenge(challenge['id'],challenge["name"],False,challenge["difficulty"], categorie=challenge["challenge_category_id"])
		"""
		List Retired Challenges
		"""
		ENDPOINT = "https://www.hackthebox.com/api/v4/challenge/list/retired"
		fetch_res = self.__do_get(ENDPOINT)
		logger.debug(f"Result for retired challenge: {fetch_res}")
		for challenge in fetch_res["challenges"]:
			# Debug: log category ID if it's unexpected
			cat_id = challenge["challenge_category_id"]
			if cat_id < 1 or cat_id > 22:
				logger.warning(f"Unexpected category ID {cat_id} for challenge {challenge['name']}")
			HTB_Challenge(challenge['id'],challenge["name"],True,challenge["difficulty"], categorie=challenge["challenge_category_id"])

	def fetch_all_machines(self):
		"""
		List Active Machines
		"""
		base_endoint = "https://www.hackthebox.com/api/v4/machine/paginated?page="
		page_index = 1
		while True:
			ENDPOINT = base_endoint+str(page_index)
			fetch_res = self.__do_get(ENDPOINT)
			logger.debug(f"Result for active machine: {fetch_res}")
			for machine in fetch_res["data"]:
				HTB_Machine(machine['id'],machine['name'],False,machine['difficultyText'])
			last_page = int(fetch_res["meta"]["last_page"])
			current_page = int(fetch_res["meta"]["current_page"])
			page_index+=1
			if last_page == current_page:
				break
		"""
		List Retired Machines
		"""
		base_endoint = "https://www.hackthebox.com/api/v4/machine/list/retired/paginated?page="
		page_index = 1
		while True:
			ENDPOINT = base_endoint+str(page_index)
			fetch_res = self.__do_get(ENDPOINT)
			logger.debug(f"Result for retired machine: {fetch_res}")
			for machine in fetch_res["data"]:
				HTB_Machine(machine['id'],machine['name'],True,machine['difficultyText'])
			last_page = int(fetch_res["meta"]["last_page"])
			current_page = int(fetch_res["meta"]["current_page"])
			page_index+=1
			if last_page == current_page:
				break

	def fetch_all_fortress(self):
		"""
		List fortresses
		"""
		ENDPOINT = "https://www.hackthebox.com/api/v4/fortresses"
		fetch_res = self.__do_get(ENDPOINT)
		logger.debug(f"Result for fortress: {fetch_res}")
		for fortress_pseudo_id in fetch_res["data"]:
			HTB_Fortress(int(fetch_res["data"][fortress_pseudo_id]['id']),fetch_res["data"][fortress_pseudo_id]["name"])

def sort_by_difficulty(c : _HTB_BaseObject) -> int:
	l = ["Very Easy","Easy","Medium","Hard","Insane"]
	return l.index(c.get_difficulty())



if __name__ == "__main__":
	"""
	Parsing args
	"""
	parser = argparse.ArgumentParser(prog='HUCT - HTB University Completion Tracker',\
					description='A simple python script to track the completion of challenges, boxs and fortresses of universities on HackTheBox website.',\
					epilog='Made with love for GCC-ENSIBS by Drahoxx 🫶')
	parser.add_argument("university_id", help="The university id you want to track the completion of.")
	parser.add_argument("api_key",help="The HTB api key (Profile -> Settings -> App Tokens). Tips: Use $(cat .api_key)")
	parser.add_argument("-q","--quiet",help="Set logging level to ERROR (only show errors)",action="store_true")
	parser.add_argument("-v","--verbose",help="Set logging level to DEBUG (show all debug information)",action="store_true")
	args = parser.parse_args()

	# Configure logging based on arguments
	if args.quiet:
		log_level = logging.ERROR
	elif args.verbose:
		log_level = logging.DEBUG
	else:
		log_level = logging.INFO

	logging.basicConfig(
		level=log_level,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)

	"""
	Fetching the database
	"""
	logger.info("Starting fetching data.")
	fetcher = HTB_Univ_Fetcher(args.api_key,args.university_id)
	fetcher.fetch_all_fortress()
	logger.info(f"{len(FORTRESS)} fortresses fetched.")
	fetcher.fetch_all_machines()
	logger.info(f"{len(MACHINES)} machines fetched.")
	fetcher.fetch_all_challenges()
	logger.info(f"{len(CHALLENGES)} challenges fetched.")
	logger.info("Now fetching the university members.")
	members=fetcher.get_university_members()
	logger.info(f"Members of the university are: {members}")
	for member in members:
		logger.info(f"Fetching {member.id} : {member.name}")
		fetcher.update_challenges_own_by_player(member)

	"""
	Printing results
	"""
	print("-"*40)
	print("MACHINES THAT AREN'T OWN BY UNIVERSITY")
	for m in sorted(MACHINES,key=sort_by_difficulty):
		if not m.is_flagged() and not m.is_retired():
			print(f"{m.id} -- {m.name} -- {m.difficulty}")
	print()
	print("-"*40)
	print("CHALLENGES THAT AREN'T FLAGGED BY UNIVERSITY")
	# To get output by category
	OUT_CHALLENGES = dict()
	for c in CHALLENGES:
		if not c.is_flagged() and not c.is_retired():
			if c.get_categorie() not in OUT_CHALLENGES:
				OUT_CHALLENGES[c.get_categorie()] = []
			OUT_CHALLENGES[c.get_categorie()].append(c)
	for key in OUT_CHALLENGES:
		for c in sorted(OUT_CHALLENGES[key],key=sort_by_difficulty):
			print(f"{c.categorie} -- {c.name} -- {c.difficulty}")
		print()
	print()
	print("-"*40)
	print("FORTRESS THAT AREN'T OWN BY UNIVERSITY")
	for f in FORTRESS:
		if not f.is_flagged():
			print(f"{f.id} -- {f.name}")
	print()