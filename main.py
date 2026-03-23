import arcade
import openscreen

def main():
    window = arcade.Window(800, 600, "Finance Sim")
    welcome = openscreen.WelcomeView()
    window.show_view(welcome)
    arcade.run()

if __name__ == "__main__":
    main()