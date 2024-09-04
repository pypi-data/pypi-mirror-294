"""
Module for managing the mouse in the game.

Contains the Mouse class, which manages the mouse events and position.
"""

from pygame import mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from .events_manager import EVENTS_MANAGER
from .display import DISPLAY
from .sources import Image

MOUSE_MAPPING : tuple[str] = (
	"left",
	"middle",
	"right",
	"scroll_up",
	"scroll_down"
)

class Mouse ():

	"""
	Class for managing the mouse in the game.
	
	Manages the mouse events and position.
	"""

	def __init__ (self) -> None:

		self.pos : tuple[int] = (0, 0)
		self.image : Image = Image ("mouse")

		self.buttons_pressed : dict[str, bool] = { "left" : False, "middle" : False, "right" : False, "scroll_up" : False, "scroll_down" : False }
		self.buttons_held : dict[str, bool] = { "left" : False, "middle" : False, "right" : False, "scroll_up" : False, "scroll_down" : False }
		self.buttons_released : dict[str, bool] = { "left" : False, "middle" : False, "right" : False, "scroll_up" : False, "scroll_down" : False }

		EVENTS_MANAGER.subscribe (MOUSEBUTTONDOWN, lambda event : self.button_down_event (event.button), context = "input")
		EVENTS_MANAGER.subscribe (MOUSEBUTTONUP, lambda event : self.button_up_event (event.button), context = "input")
	
	def button_down_event (self, button : int) -> None:

		self.buttons_pressed[MOUSE_MAPPING[button - 1]] : bool = True
		self.buttons_held[MOUSE_MAPPING[button - 1]] : bool = True

	def button_up_event (self, button : int) -> None:

		self.buttons_released[MOUSE_MAPPING[button - 1]] : bool = True
		self.buttons_held[MOUSE_MAPPING[button - 1]] : bool = False

	def button_pressed (self, button_name : str = "left") -> bool:

		return self.buttons_pressed[button_name]

	def button_held (self, button_name : str = "left") -> bool:

		return self.buttons_held[button_name]

	def button_released (self, button_name : str = "left") -> bool:

		return self.buttons_released[button_name]

	def update (self) -> None:

		pos : tuple[int] = mouse.get_pos ()

		if (DISPLAY.scaled_display_surface_rect.collidepoint (pos)):
			mouse.set_visible (False)

			self.buttons_pressed : dict[str, bool] = { "left" : False, "middle" : False, "right" : False }
			self.buttons_released : dict[str, bool] = { "left" : False, "middle" : False, "right" : False }

			self.pos = ((pos[0] - ((DISPLAY.window_size[0] - DISPLAY.scaled_display_surface_rect.width) // 2)) // (DISPLAY.scale + 1), (pos[1] - ((DISPLAY.window_size[1] - DISPLAY.scaled_display_surface_rect.height) // 2)) // (DISPLAY.scale + 1))

			self.image.rect.center : tuple[int] = self.pos
			DISPLAY.surface.blit (self.image.image, self.image.rect)

		else:
			mouse.set_visible (True)
			self.pos : tuple[int] = pos

MOUSE = Mouse ()

