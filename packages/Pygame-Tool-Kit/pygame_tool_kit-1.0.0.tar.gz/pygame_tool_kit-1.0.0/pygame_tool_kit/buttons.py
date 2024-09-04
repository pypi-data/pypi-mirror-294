from .constants import *
from .sources import Image, Image_Collection, Text, Paragraph, Mask, Container

class Button ():

	def __init__ (self, image_collection : Image_Collection, container : Container, commands : tuple[callable] = (), text : str = "", unlock : bool = True, lock_image : str = None) -> None:

		self.state : int = 0
		self.image_collection : Image_Collection = image_collection
		container.add_sprites (self.image_collection)

		self.commands : tuple[callable] = commands

		self.text : Paragraph = Paragraph (text, self.image_collection.rect.width - 10, pos = self.image_collection.rect.center, align = "center")
		container.add (self.text)

		if (not unlock):
			self.mask : Mask = Mask ((self.image_collection.rect.width - 4, self.image_collection.rect.height - 4), pos = self.image_collection.rect.center)
			container.add (self.mask)
			if (lock_image):
				self.lock_image : Image = Image (f"buttons/locks/{lock_image}", pos = self.image_collection.rect.center)
				container.add (self.lock_image)

			self.update = lambda : None

		else:
			def update (self) -> None:

				if (self.image_collection.rect.collidepoint (MOUSE.pos)):
					if (MOUSE.button_pressed ()):
						self.state = 2
						for command in self.commands:
							command ()

					else:
						self.state = 1
				else:
					self.state = 0

				self.image_collection.set_image (self.state)

			self.update = lambda : update (self)

		def unlock (self) -> None:
			
			container.remove (self.mask)
			if (self.lock_image):
				container.remove (self.lock_image)
	
			def update (self) -> None:

				if (self.image_collection.rect.collidepoint (MOUSE.pos)):
					if (MOUSE.button_pressed ()):
						self.state = 2
						for command in self.commands:
							command ()

					else:
						self.state = 1
				else:
					self.state = 0

				self.image_collection.set_image (self.state)

			self.update = lambda : update (self)

		self.unlock = lambda : unlock (self)

	def set_commands (self, *commands : tuple[callable]) -> None:

		self.commands : tuple[callable] = commands

	def set_text (self, text : str) -> None:

		self.text.set_text (text)

class Selection_Button ():

	def __init__ (self, image_collection : Image_Collection, container : Container, selection : int = 0, text : str = "", unlock : bool = True, lock_image : str = None) -> None:

		self.state : int = 0
		self.selection : int = selection
		self.image_collection : Image_Collection = image_collection
		container.add (self.image_collection)

		self.text : Paragraph = Paragraph (text, self.image_collection.rect.width - 10, pos = self.image_collection.rect.center, align = "center")
		container.add (self.text)

		if (not unlock):
			self.mask : Mask = Mask ((self.image_collection.rect.width - 4, self.image_collection.rect.height - 4), pos = self.image_collection.rect.center)
			container.add (self.mask)
			if (lock_image):
				self.lock_image : Image = Image (f"buttons/locks/{lock_image}", pos = self.image_collection.rect.center)
				container.add (self.lock_image)

			self.update = lambda selection : None

		else:
			def update (self, selection : int) -> bool:

				output : bool = False
				if (self.image_collection.rect.collidepoint (MOUSE.pos)):
					if (MOUSE.button_pressed ()):
						self.state : int = 3
						output : bool = True

					else:
						self.state : int = 1
				else:
					if (self.selection == selection):
						self.state : int = 2

					else:
						self.state : int = 0

				self.image_collection.set_image (self.state)

				return output

			self.update = lambda selection : update (self, selection)

		def unlock (self) -> None:
			
			container.remove (self.mask)
			if (self.lock_image):
				container.remove (self.lock_image)

			def update (self, selection : int) -> bool:

				output : bool = False
				if (self.image_collection.rect.collidepoint (MOUSE.pos)):
					if (MOUSE.button_pressed ()):
						self.state : int = 3
						output : bool = True

					else:
						self.state : int = 1
				else:
					if (self.selection == selection):
						self.state : int = 2

					else:
						self.state : int = 0

				self.image_collection.set_image (self.state)

				return output

			self.update = lambda selection : update (self, selection)

		self.unlock = lambda : unlock (self)

	def set_text (self, text : str) -> None:

		self.text.set_text (text)

class Hover ():

	def __init__ (self, hover_image : Image, dropdown_image : Image, container : Container, hover_text : Text = None, dropdown_texts : tuple[Text] = ()) -> None:
		
		self.hover : bool = False

		self.hover_image : Image = hover_image
		container.add_sprites (self.hover_image)

		self.hover_texts_container : Container = Container (hover_text, pos = self.hover_image.rect.center) if (self.hover_image.rect.center != (0, 0)) else Container (hover_text)
		
		self.dropdown_image : Image = dropdown_image
		self.dropdown_image.rect.center : tuple[int] = ( self.dropdown_image.rect.center[0] + container.pos[0], self.dropdown_image.rect.center[1] + container.pos[1] )
		
		self.dropdown_container : Container = Container (pos = self.dropdown_image.rect.center) if (self.dropdown_image.rect.center != (0, 0)) else Container ()
		self.dropdown_container.add (self.dropdown_image)
		self.dropdown_container.add_sprites (*dropdown_texts)

	def update (self):

		if (self.hover):
			self.hover : bool = True if self.dropdown_image.rect.collidepoint (MOUSE.pos) else False
			if (not self.hover):
				self.hover : bool = True if self.hover_image.rect.collidepoint (MOUSE.pos) else False

		else:
			self.hover : bool = True if self.hover_image.rect.collidepoint (MOUSE.pos) else False

	def draw (self):

		if (self.hover):
			self.dropdown_container.draw (DISPLAY.surface)

		else:
			self.hover_texts_container.draw (DISPLAY.surface)


def command (function : callable, *args : tuple, **kwargs : dict) -> callable:

	return lambda : function (*args, **kwargs)

def scene_command (event : callable, *args : tuple) -> callable:

	return command (EVENTS_MANAGER.emit, f"{event}_scene", *args, lazy = True)