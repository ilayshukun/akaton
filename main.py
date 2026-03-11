import arcade
import openscreen
from openscreen import  SCREEN_WIDTH


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, openscreen.SCREEN_HEIGHT, openscreen.SCREEN_TITLE)
    welcome_view = openscreen.WelcomeView()
    window.show_view(welcome_view)
    arcade.run()