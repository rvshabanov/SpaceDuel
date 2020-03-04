"""
Space Duel v.1.0a

Single / Two player game using single keyboard.
The goal is to control your spacecraft, to avoid obstacles and shoot down enemy spacecraft

Graphics used:
https://opengameart.org/
MillionthVector, visit his/her blog at http://millionthvector.blogspot.de.
Some non-copyrighted space backgrounds used.

"""
import arcade
import menus
import constants


"""
Main - create arcade windows, set some window parameters
and run arcade 
"""


def main():
    """ Main method """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

    # Don't show the mouse cursor and set update rate
    window.set_mouse_visible(False)
    window.set_update_rate(1 / 60)
    if constants.SCREEN_FULLSCREEN:
        window.set_fullscreen(True)
        constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT = window.get_size()

    menu_view = menus.MenuView()
    window.show_view(menu_view)
    arcade.run()


"""
Entry point - call main() 
"""
if __name__ == "__main__":
    main()
