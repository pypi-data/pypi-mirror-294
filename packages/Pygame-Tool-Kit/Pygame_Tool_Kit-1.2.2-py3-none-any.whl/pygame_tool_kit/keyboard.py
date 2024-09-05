"""
This module contains the Keyboard class which handles keyboard events.
"""

from pygame import key, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SPACE, K_BACKSPACE, K_RETURN, K_ESCAPE, K_TAB, K_F11, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, KEYUP

from .events_manager import EVENTS_MANAGER

KEYBOARD_MAPPING : dict[str, int] = {
	"a" : K_a, "b" : K_b, "c" : K_c, "d" : K_d, "e" : K_e, "f" : K_f,
	"g" : K_g, "h" : K_h, "i" : K_i, "j" : K_j, "k" : K_k, "l" : K_l,
	"m" : K_m, "n" : K_n, "o" : K_o, "p" : K_p, "q" : K_q, "r" : K_r,
	"s" : K_s, "t" : K_t, "u" : K_u, "v" : K_v, "w" : K_w, "x" : K_x,
	"y" : K_y, "z" : K_z, "0" : K_0, "1" : K_1, "2" : K_2, "3" : K_3,
	"4" : K_4, "5" : K_5, "6" : K_6, "7" : K_7, "8" : K_8, "9" : K_9,
	"space" : K_SPACE, "backspace" : K_BACKSPACE, "return" : K_RETURN, "scape" : K_ESCAPE, "tab" : K_TAB,
	"F11" : K_F11, "up" : K_UP, "down" : K_DOWN, "left" : K_LEFT, "right" : K_RIGHT
}


class Keyboard ():

	"""
	This class handles keyboard events.
	"""

	def __init__ (self) -> None:

		self.keys_pressed : dict[str, bool] = {}
		self.keys_held : dict[str, bool] = {}
		self.keys_released : dict[str, bool] = {}

		EVENTS_MANAGER.subscribe (KEYDOWN, lambda event : self.key_down_event (event.key), context = "input")
		EVENTS_MANAGER.subscribe (KEYUP, lambda event : self.key_up_event (event.key), context = "input")

	def key_down_event (self, key) -> None:

		self.keys_held[key] = True

	def key_up_event (self, key) -> None:

		self.keys_released[key] = True

	def key_pressed (self, key_name : str) -> bool:

		return self.keys_pressed[KEYBOARD_MAPPING[key_name]]

	def key_held (self, key_name : str) -> bool:

		return self.keys_held.get (KEYBOARD_MAPPING[key_name], False)

	def key_released (self, key_name : str) -> bool:

		return self.keys_released.get (KEYBOARD_MAPPING[key_name], False)

	def update (self) -> None:

		self.keys_pressed : dict[str, bool] = key.get_pressed ()
		self.keys_held : dict[str, bool] = {}
		self.keys_released : dict[str, bool] = {}

KEYBOARD = Keyboard ()
