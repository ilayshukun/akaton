import arcade
from openscreen import  *


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT, SCREEN_TITLE)
    welcome_view = WelcomeView()
    window.show_view(welcome_view)
    arcade.run()