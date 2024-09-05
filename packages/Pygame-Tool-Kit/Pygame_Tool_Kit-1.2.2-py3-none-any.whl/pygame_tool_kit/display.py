"""
Module for managing the display of the game.

This module contains the Display class, which is used to manage the display
of the game. It provides methods for setting the display mode, getting the
current display size, and updating the display.

The display is managed by the Display class, which is a singleton class.
The instance of the class is stored in the DISPLAY constant.
"""

from pygame import display, transform, Rect, RESIZABLE, VIDEORESIZE, FULLSCREEN
from pygame.surface import Surface
from pygame.image import load

from .events_manager import EVENTS_MANAGER
from .storage_manager import STORAGE_MANAGER
from .keyboard import KEYBOARD

from .config import RESOLUTIONS, INIT_SCALE, RESOLUTION_SURFACE, GAME_TITLE, ICON_PATH


class Display ():
    """
    Class for managing the display of the game.

    This class is a singleton class, and the instance of the class is stored
    in the DISPLAY variable.

    The class provides methods for setting the display mode, getting the
    current display size, and updating the display.
    """

    def __init__ (self) -> None:

        self.window : Surface = display.set_mode (RESOLUTIONS[INIT_SCALE], RESIZABLE)
        self.window_size : tuple[int] = RESOLUTIONS[INIT_SCALE]
        self.window_center : tuple[int] = ((self.window_size[0] // 2), (self.window_size[1] // 2))
        self.full_scene : bool = False
        self.scale : int = 0

        self.surface : Surface = Surface (RESOLUTION_SURFACE)
        self.rescale (self.window_size[0], self.window_size[1])
        self.scaled_display_surface : Surface = transform.scale (self.surface, RESOLUTIONS[self.scale])
        self.scaled_display_surface_rect : Rect = self.scaled_display_surface.get_rect (center = self.window_center)

        EVENTS_MANAGER.subscribe (VIDEORESIZE, lambda event : self.rescale (event.w, event.h), context = "input")

        display.set_caption (GAME_TITLE)
        if (ICON_PATH):
            display.set_icon (load (ICON_PATH))

    def rescale (self, width : int, height : int) -> None:

        self.window_size : tuple[int] = (width, height)
        self.window_center : tuple[int] = (self.window_size[0] // 2, self.window_size[1] // 2)

        for i in range (len (RESOLUTIONS) - 1, -1, -1):
            if ((self.window_size[0] >= RESOLUTIONS[i][0]) and (self.window_size[1] >= RESOLUTIONS[i][1])):
                self.scale : int = i
                break

        self.window.fill ((0, 0, 0))

    def update (self) -> None:

        if (KEYBOARD.key_pressed ("F11")):
            self.full_scene : bool = not self.full_scene
            if (self.full_scene):
                self.window : Surface = display.set_mode (RESOLUTIONS[4], FULLSCREEN)
                self.rescale (RESOLUTIONS[4][0], RESOLUTIONS[4][1])

            else:
                self.window : Surface = display.set_mode (RESOLUTIONS[self.scale], RESIZABLE)
                self.rescale (RESOLUTIONS[self.scale][0], RESOLUTIONS[self.scale][1])

        self.scaled_display_surface : Surface = transform.scale (self.surface, RESOLUTIONS[self.scale])
        self.scaled_display_surface_rect : Rect = self.scaled_display_surface.get_rect (center = self.window_center)

        self.window.blit (self.scaled_display_surface, self.scaled_display_surface_rect)

        display.update ()

DISPLAY : Display = Display ()
