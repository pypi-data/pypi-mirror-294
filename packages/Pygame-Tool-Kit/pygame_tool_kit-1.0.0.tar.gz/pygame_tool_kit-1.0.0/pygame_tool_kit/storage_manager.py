from json import load, dump

from .config import STORAGE_PATH

class Storage_Manager ():

	def load (self, at : str, static : bool = True) -> dict:

		if (static):
			with open (f"{STORAGE_PATH}/static.json", "r") as file:
				return load (file)[at]
		
		else:
			with open (f"{STORAGE_PATH}/dynamic/{at}.json", "r") as file:
				return load (file)[at]

	def save (self, at : str, data : any) -> None:

		with open (f"{STORAGE_PATH}/dynamic/{at}.json", "w") as file:
			dump ({at : data}, file, indent = 4)

STORAGE_MANAGER = Storage_Manager ()