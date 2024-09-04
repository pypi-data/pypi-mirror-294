from pygame.event import get as get_events

class Events_Manager ():

	def __init__ (self) -> None:

		self.listeners : dict[str, dict[str, list[callable]]] = { "game" : {}, "input" : {} }
		self.lazy_events : list[tuple[str, tuple, dict]] = []

	def subscribe (self, event : str, listener : callable, context : str = "game") -> None:

		if (event not in self.listeners[context]):
			self.listeners[context][event] : list[callable] = []

		self.listeners[context][event].append (listener)

	def unsubscribe (self, event : str, listener : callable, context : str = "game") -> None:

		if (event in self.listeners[context]):
			self.listeners[context][event].remove (listener)

	def emit (self, event : str, *args : tuple, lazy : bool = False, **kwargs : dict) -> None:

		if (lazy):
			self.lazy_events.append ((event, args, kwargs))

		else:
			if (event in self.listeners["game"]):
				for listener in self.listeners["game"][event]:
					listener (*args, **kwargs)

	def process_lazy_events (self) -> None:

		while self.lazy_events:
			event, args, kwargs = self.lazy_events.pop (0)
			if (event in self.listeners["game"]):
				for listener in self.listeners["game"][event]:
					listener (*args, **kwargs)

	def process_inputs (self) -> None:

		for event in get_events ():
			if (event.type in self.listeners["input"]):
				for listener in self.listeners["input"][event.type]:
					listener (event)

EVENTS_MANAGER = Events_Manager ()
