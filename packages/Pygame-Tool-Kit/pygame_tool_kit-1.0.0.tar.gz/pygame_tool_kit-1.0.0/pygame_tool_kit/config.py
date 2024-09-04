from json import load
from os import walk, getcwd, path

for root, dirs, files in walk (getcwd ()):
	if ("game_config.json" in files):
		with open (path.join (root, "game_config.json"), "r") as file:
			config_data : dict = load (file)

		break
	
else:
	raise FileNotFoundError (f"No se encontró el archivo de configuración game_config.json en {getcwd ()} o subdirectorios.")

def load_config_required_path (data : str) -> str:

	if (config_data.get (data + "_path", False)):
		return config_data[data + "_path"]

	else:
		raise FileNotFoundError (f"El archivo de configuración game_config.json no contiene la propiedad '{data}_path'.")

FONT_PATH : str = load_config_required_path ("font")
ASSETS_PATH : str = load_config_required_path ("assets")
ICON_PATH : str = load_config_required_path ("icon")
STORAGE_PATH : str = load_config_required_path ("storage")

GAME_TITLE: str = config_data["game_title"] if (config_data.get ("game_title", False)) else "Game"

if (config_data.get ("resolutions", False)):
	RESOLUTIONS : tuple[tuple[int]] = tuple (tuple (resolution) for resolution in config_data["resolutions"])

else:
	RESOLUTIONS : tuple[tuple[int]] = ((384, 216), (768, 432), (1152, 648), (1536, 864), (1920, 1080))

INIT_SCALE : int = config_data["init_scale"] if (config_data.get ("init_scale", False)) else 0
RESOLUTION_SURFACE : tuple[int] = RESOLUTIONS[0]
RESOLUTION_CENTER : tuple[int] = (RESOLUTION_SURFACE[0] // 2, RESOLUTION_SURFACE[1] // 2)
