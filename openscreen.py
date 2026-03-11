import arcade
import arcade.gui
import login
import register

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Finance Simulation"

class WelcomeView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # כותרת
        title = arcade.gui.UILabel(text="Welcome to the Finance Simulation", text_color=arcade.color.WHITE,
                                   font_size=24)
        self.v_box.add(title)

        # כפתור מעבר למסך התחברות
        sign_in_button = arcade.gui.UIFlatButton(text="Sign In", width=200)
        sign_in_button.on_click = self.on_click_sign_in
        self.v_box.add(sign_in_button)

        # כפתור מעבר למסך הרשמה
        register_button = arcade.gui.UIFlatButton(text="Register", width=200)
        register_button.on_click = self.on_click_register
        self.v_box.add(register_button)

        # מיקום במרכז
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_click_sign_in(self, event):
        # מעבר למסך ההתחברות
        login_view = login.LoginView()
        self.window.show_view(login_view)

    def on_click_register(self, event):
        # מעבר למסך ההרשמה
        register_view = register.RegisterView()
        self.window.show_view(register_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()
