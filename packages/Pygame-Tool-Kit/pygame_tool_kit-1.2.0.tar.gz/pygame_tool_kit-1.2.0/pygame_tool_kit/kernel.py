"""
Class for managing the game kernel.

This class is used to manage the game scenes and switch between them.
"""

from pygame import init, QUIT
from pygame import quit as close

from .constants import EVENTS_MANAGER, KEYBOARD, DISPLAY, MOUSE, DELTA_TIME
from .config import RESOLUTION_CENTER, RESOLUTION_SURFACE

from .sources import Mask

class Kernel ():

	"""
	Initializes the game kernel.

	Args:
		scenes (tuple[type]): Tuple of scene classes to load.
		background (type): Optional background class to use.
	"""

	def __init__ (self, *scenes : tuple[type], background : type = None) -> None:

		init ()

		self.running : bool = True
		self.mask : Mask = Mask (RESOLUTION_SURFACE, pos = RESOLUTION_CENTER)

		if (background):
			self.background : background = background ()
			self.display_background : callable = lambda : self.background.display ()

		else:
			self.display_background : callable = lambda : DISPLAY.surface.fill ((0, 0, 0))

		self.load_scenes (*scenes)

		EVENTS_MANAGER.subscribe (QUIT, lambda event : self.quit_event (), context = "input")
		EVENTS_MANAGER.subscribe ("switch_scene", self.switch)
		EVENTS_MANAGER.subscribe ("remove_scene", self.remove)
		EVENTS_MANAGER.subscribe ("overlay_scene", self.overlay)
		EVENTS_MANAGER.subscribe ("print_scene", self.print_scene)

		self.run ()

	def quit_event (self) -> None:

		self.running : bool = False

	def load_scenes (self, *scenes : tuple[type]) -> None:

		self.scenes_collection : dict = {}

		for scene in scenes:
			self.scenes_collection[scene.__name__] : scene = scene ()

		self.scenes : list = [ self.scenes_collection[scenes[0].__name__] ]

	def switch (self, scene_name : str) -> None:

		self.scenes[-1] = self.scenes_collection[scene_name]

	def overlay (self, scene_name : str) -> None:

		self.scenes[-1].update ()
		self.scenes.append (self.scenes_collection[scene_name])

	def remove (self) -> None:

		self.scenes.pop ()

		if (not self.scenes):
			self.quit_event ()

	def print_scene (self, scene : any) -> None:

		self.scenes.append (scene)

	def run (self) -> None:

		DELTA_TIME.init_delta_time ()
		while (self.running):
			DELTA_TIME.update ()

			self.display_background ()

			if (len (self.scenes) > 1):
				for i in range (len (self.scenes) - 1):
					self.scenes[i].draw ()

				DISPLAY.surface.blit (self.mask.image, self.mask.rect)

			self.scenes[-1].update ()
			self.scenes[-1].draw ()

			MOUSE.update ()
			KEYBOARD.update ()

			DISPLAY.update ()
			EVENTS_MANAGER.process_inputs ()
			EVENTS_MANAGER.process_lazy_events ()

		close ()
