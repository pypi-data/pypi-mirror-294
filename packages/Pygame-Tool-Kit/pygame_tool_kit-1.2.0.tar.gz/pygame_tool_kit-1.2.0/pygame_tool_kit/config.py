"""
Contains the configuration data for the Pygame Tool Kit.

The configuration data is loaded from a 'game_config.json' file in the current working directory or any subdirectory.
The file should contain the following properties:
- 'font_path': The path to the font file to use for rendering text.
- 'assets_path': The path to the folder containing the assets for the game.
- 'icon_path': The path to the icon file for the game window.
- 'storage_path': The path to the folder where the game data will be saved.
- (Optional) 'game_title': The title of the game to display in the window title.
- (Optional) 'resolutions': A list of tuples containing the resolutions that the game can run at.
- (Optional) 'init_scale': The index of the resolution to use as the initial resolution.
"""

from json import load
from os import walk, getcwd, path

def load_config () -> dict:
	"""
	Loads the configuration data from a 'game_config.json' file in the current working directory or any subdirectory.

	Raises:
		FileNotFoundError: If the file is not found.
	"""

	for root, dirs, files in walk (getcwd ()):
		if ("game_config.json" in files):
			with open (path.join (root, "game_config.json"), "r") as file:
				return load (file)

	raise FileNotFoundError (f"The config file 'game_config.json' was not found in {getcwd ()} or any subdirectory.")

def load_config_required_path (data: str) -> str:
	"""
	Loads a required path from the configuration data.

	Args:
		data (str): The property name of the path to load.

	Raises:
		FileNotFoundError: If the property is not found in the configuration data.
	"""

	if (config_data.get (data + "_path", False)):
		return config_data[data + "_path"]

	else:
		raise FileNotFoundError (f"The config file 'game_config.json' does not contain the property '{data}_path'.")

config_data = load_config()

FONT_PATH : str = load_config_required_path ("font")
ASSETS_PATH : str = load_config_required_path ("assets")
STORAGE_PATH : str = load_config_required_path ("storage")

ICON_PATH : str = config_data["icon_path"] if (config_data.get ("icon_path", False)) else None
GAME_TITLE : str = config_data["game_title"] if (config_data.get ("game_title", False)) else "Game"

if (config_data.get ("resolutions", False)):
	RESOLUTIONS : tuple[tuple[int]] = tuple (tuple (resolution) for resolution in config_data["resolutions"])

else:
	RESOLUTIONS : tuple[tuple[int]] = ((384, 216), (768, 432), (1152, 648), (1536, 864), (1920, 1080))

INIT_SCALE : int = config_data["init_scale"] if (config_data.get ("init_scale", False)) else 0
RESOLUTION_SURFACE : tuple[int] = RESOLUTIONS[0]
RESOLUTION_CENTER : tuple[int] = (RESOLUTION_SURFACE[0] // 2, RESOLUTION_SURFACE[1] // 2)

