import arcade

import openscreen
from openscreen import WelcomeView, SCREEN_WIDTH
from login import LoginView
from register import RegisterView

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, openscreen.SCREEN_HEIGHT, openscreen.SCREEN_TITLE)
    # מתחילים תמיד ממסך הפתיחה
    welcome_view = openscreen.WelcomeView()
    window.show_view(welcome_view)
    arcade.run()