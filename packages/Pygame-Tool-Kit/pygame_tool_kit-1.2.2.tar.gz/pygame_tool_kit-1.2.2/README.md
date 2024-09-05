<h1 align = "center">
	<img alt = "Pygame Tool Kit" src = "img/logo.png"/>
	<br/>
	Pygame Tool Kit
</h1>
<br/>

A powerful and flexible toolkit to simplify game development with Pygame.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
	- [Configuration](#configuration)
	- [Event Management](#events-management)
	- [Storage Management](#storage-management)
- [Examples](#examples)
- [License](#license)
- [Contact](#contact)

---

## Description

`Pygame Tool Kit` is a library designed to simplify game development in Python using Pygame. It provides a range of tools and utilities covering events management, storage handling, and more, allowing developers to focus on what really matters: creating great games!

---

## Features

- **Events Management**: Subscribe, emit, and manage events efficiently.
- **Storage Management**: Save and load game settings and data in JSON format.
- **Flexible Configuration**: Configure the library from anywhere in your project.
- **Easy to Use**: Intuitive interfaces that are easy to integrate with your project.

---

## Installation

You can easily install it by using `pip`:

```bash
pip install Pygame_Tool_Kit
```

---

## Usage

### Configuration

Before using Pygame Tool Kit, you need to configure some basic parameters such as screen resolutions and the initial scale. This configuration can be done from anywhere in your project. Example of a game_config.json file:

```json

{
	"font_path": "Pygame_Tool_Kit/assets/font/Gloack_Font.ttf",
	"assets_path": "Pygame_Tool_Kit/assets/GUI/",
	"icon_path": "Pygame_Tool_Kit/assets/GUI/icon.png",
	"storage_path": "Pygame_Tool_Kit/storage/",
	"game_title": "Simple Game",
	"resolutions": [
		[384, 216],
		[768, 432],
		[1152, 648],
		[1536, 864],
		[1920, 1080]
	],
	"init_scale": 1
}

```

---

### Events Management

Manage in-game events using the constant `EVENTS_MANAGER`. You can subscribe to events, emit them, and process them with ease.

```python

from pygame_tool_kit.constants import EVENTS_MANAGER

# Funcion to call when the "quit" event is emitted
def on_quit ():
	print ("The game is closing")

EVENTS_MANAGER.subscribe ("quit", on_quit)

# Emit the "quit" event
EVENTS_MANAGER.emit ("quit")

```

---

### Storage Management

Storage_Manager allows you to save and load game data from JSON files in a structured way. It distinguishes between static and dynamic data.

- Static Data: Stored in a single static.json file.
- Dynamic Data: Each piece of data is stored in its own JSON file within a dynamic directory.

#### Saving Data

To save dynamic game data (such as game progress or user settings):

```python

from pygame_tool_kit.constants import STORAGE_MANAGER

data : dict[str, int] = { "level" : 3, "score" : 1500 }
STORAGE_MANAGER.save ("current_game", data)

```

This will save the data to a file located at STORAGE_PATH/dynamic/current_game.json.

---

#### Loading Data

To load either static or dynamic data:

```python

# Loading dynamic data
current_game = STORAGE_MANAGER.load ("current_game", static = False)
print (current_game)

# Loading static data
static_data = STORAGE_MANAGER.load ("game_settings", static = True)
print (static_data)

```

- If `static=True`, it will look for the data in STORAGE_PATH/static.json.
- If `static=False`, it will load the data from STORAGE_PATH/dynamic/{at}.json.

---

## License

This project is licensed under the MIT License.

---

Thank you for using Pygame Tool Kit! I hope it helps you create amazing games with Python!
Additional Notes:













