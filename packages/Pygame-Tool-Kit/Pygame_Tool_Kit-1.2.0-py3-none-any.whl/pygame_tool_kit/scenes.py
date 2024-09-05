"""
The module contains the Scene class, which is used to manage a scene in the game.

A scene is used to organize sprites, containers and buttons in the game.
"""

from .constants import DISPLAY

from .buttons import Button
from .sources import Container

class Scene ():
	"""
	Class for managing a scene in the game.
	
	Scenes are used to organize sprites, containers and buttons in the game.
	A scene is composed of a main container, which contains all the sprites
	and buttons in the scene.
	"""
	
	def __init__ (self, pos : tuple[int, int] = None) -> None:
		
		self.main_container : Container = Container (pos = pos) if (pos) else Container ()
		self.buttons : list = []

	def add_sprites (self, *sprites : tuple) -> None:
		
		self.main_container.add_sprites (*sprites)

	def add_containers (self, *containers : tuple[Container]) -> None:
		
		for container in containers:
			self.main_container.add (container.sprites ())

	def remove_containers (self, *containers : tuple[Container]) -> None:
		
		for container in containers:
			self.main_container.remove (container)

	def add_button (self, *args : tuple, **kwargs : dict) -> None:
		
		self.buttons.append (Button (*args, self.main_container, **kwargs))

	def update (self) -> None:
		
		for button in self.buttons:
			button.update ()

	def draw (self) -> None:
		
		self.main_container.draw (DISPLAY.surface)
