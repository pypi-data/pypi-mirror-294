from pygame import Rect, draw, SRCALPHA
from pygame.surface import Surface
from pygame.sprite import Sprite, Group
from pygame.image import load
from pygame.font import Font

from .config import ASSETS_PATH, FONT_PATH, RESOLUTION_CENTER

class Image (Sprite):

	def __init__ (self, path : str, size : tuple[int] = None, pos : tuple[int] = (0, 0), frame : tuple[int] = (0, 0)) -> None:

		super ().__init__ ()

		if (size):
			self.image : Surface = Surface (size)
			self.image.blit (load (f"{ASSETS_PATH}{path}.png").convert_alpha (), (0, 0), ((frame[0] * size[0]), (frame[1] * size[1]), size[0], size[1]))
		
		else:
			self.image : Surface = load (f"{ASSETS_PATH}{path}.png").convert_alpha ()

		self.image.set_colorkey ((0, 0, 0))
		self.rect : Rect = self.image.get_rect (center = pos)

class Image_Collection (Sprite):

	def __init__ (self, path : str, size : tuple[int], pos : tuple[int] = (0, 0), frame : int = 0) -> None:

		super ().__init__ ()

		sheet : Surface = load (f"{ASSETS_PATH}{path}.png").convert_alpha ()

		images : list[Surface] = []
		for i in range (sheet.get_rect ().height // size[1]):
			image : Surface = Surface (size)
			image.blit (sheet, (0, 0), ((frame * size[0]), (i * size[1]), size[0], size[1]))
			image.set_colorkey ((0, 0, 0))
			images.append (image)

		self.images : tuple[Surface] = tuple (images)
		self.set_image ()
		self.rect : Rect = image.get_rect (center = pos)

	def set_image (self, frame : int = 0) -> None:

		self.image : Surface = self.images[frame]

class Text (Sprite):

	def __init__ (self, text : str, pos : tuple[int] = (0, 0), align : str = "center", size : int = 6, color : tuple[int] = (5, 5, 5)) -> None:

		super ().__init__ ()

		self.rect : Rect = Rect (pos, (0, 0))

		def set_text (self, text : str) -> None:

			last_rect : Rect = self.rect

			self.image : Surface = Font (FONT_PATH, size).render (str (text), False, color)
			self.rect : Rect = Rect ((0, 0), (self.image.get_width (), size))

			match (align):
				case ("center") : self.rect.center : tuple[int] = last_rect.center

				case ("left") : self.rect.topleft : tuple[int] = last_rect.topleft

				case ("right") : self.rect.topright : tuple[int] = last_rect.topright
		
		self.set_text : callable = lambda text : set_text (self, text)
		self.set_text (text)

class Paragraph (Sprite):

	def __init__ (self, text : str, length : int, pos : tuple[int] = (0, 0), align : str = "left", size : int = 6) -> None:

		super ().__init__ ()

		self.rect : Rect = Rect (pos, (0, 0))

		def set_text (self, text : str) -> None:

			words : list[str] = text.split ()

			temp_group : Group = Group ()

			render_lines : list[Text] = []
			temp : str = ""
			i : int = 0

			for word in words:

				text : Text = Text (((temp + " ") if (temp != "") else "") + word, pos = (0, i * size), size = size)
				if (text.rect.width < length):
					temp += f" {word}" if (temp != "") else word

				elif (text.rect.width == length):
					render_lines.append (text)
					i += 1
					temp : str = ""

				else:
					render_lines.append (Text (temp, pos = (0, i * size), size = size))
					i += 1
					temp : str = word
			
			render_lines.append (Text (temp, pos = (0, i * size), size = size))

			width = 0
			for line in (render_lines):
				if (line.rect.width > width):
					width = line.rect.width

			self.image : Surface = Surface ((width, len (render_lines) * size)).convert_alpha ()

			match (align):
				case ("center") :
					for line in (render_lines):
						self.image.blit (line.image, (((width - line.rect.width) // 2), line.rect.y + (line.rect.height // 2)))
					
					self.image.set_colorkey ((0, 0, 0))
					self.rect : Rect = self.image.get_rect (center = self.rect.center)

				case ("left") :
					for line in (render_lines):
						self.image.blit (line.image, (0, line.rect.y + (line.rect.height // 2)))
					
					self.image.set_colorkey ((0, 0, 0))
					
					self.rect : Rect = self.image.get_rect (topleft = self.rect.topleft)

				case ("right") :
					for line in (render_lines):
						self.image.blit (line.image, (width, line.rect.y + (line.rect.height // 2)))
					
					self.image.set_colorkey ((0, 0, 0))
					self.rect : Rect = self.image.get_rect (topright = self.rect.topright)

		self.set_text : callable = lambda text : set_text (self, text)
		self.set_text (text)

class Mask (Sprite):

	def __init__ (self, size : tuple[int], pos : tuple[int] = (0, 0), color : tuple[int] = (95, 95, 95), opacity : int = 100) -> None:

		super ().__init__ ()

		self.image : Surface = Surface (size, SRCALPHA)
		draw.rect (self.image, (color[0], color[1], color[2], opacity), [0, 0, size[0], size[1]])
		self.rect : Rect = self.image.get_rect (center = pos)

class Container (Group):

	def __init__ (self, *sprites : tuple, pos : tuple[int] = RESOLUTION_CENTER) -> None:

		super ().__init__ ()

		self.pos : tuple[int] = pos

		self.add_sprites (*sprites)

	def add_sprites (self, *sprites : tuple) -> None:

		for sprite in sprites:
			sprite.rect.center : tuple[int] = ( sprite.rect.center[0] + self.pos[0], sprite.rect.center[1] + self.pos[1] )
			self.add (sprite)