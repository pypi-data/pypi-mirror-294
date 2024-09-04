"""
A class to manage the time delta between the current frame and the previous frame.

The time delta is the time in seconds since the last frame.
"""

from time import time

class Delta_Time ():
	"""
	A class to manage the time delta between the current frame and the previous frame.
	"""

	def __init__ (self) -> None:

		self.previous_time : float = 0.0
		self.delta_time : float = 0.0

	def init_delta_time (self) -> None:

		self.previous_time = time ()

	def update (self) -> None:

		self.delta_time = time () - self.previous_time
		self.previous_time = time ()

DELTA_TIME = Delta_Time ()
