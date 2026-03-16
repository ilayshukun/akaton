import arcade
import arcade.gui
import openscreen
import user_manger
users_db = user_manger.load_users()


class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)

        # התיבה הראשית
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # כותרת המסך - הסרנו את with_space_around
        self.title = arcade.gui.UILabel(text="Sign In", text_color=arcade.color.WHITE, font_size=30, bold=True)
        self.v_box.add(self.title)

        # --- שורת אימייל ---
        email_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        email_label = arcade.gui.UILabel(text="Email:", text_color=arcade.color.WHITE, font_size=16, width=100)
        email_row.add(email_label)

        self.email_input = arcade.gui.UIInputText(width=250, height=40, text="")
        email_row.add(self.email_input.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(email_row)

        # --- שורת סיסמה ---
        password_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        password_label = arcade.gui.UILabel(text="Password:", text_color=arcade.color.WHITE, font_size=16, width=100)
        password_row.add(password_label)

        self.password_input = arcade.gui.UIInputText(width=250, height=40, text="")
        password_row.add(self.password_input.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(password_row)


        # --- הודעות שגיאה ---
        self.message_label = arcade.gui.UILabel(text="", text_color=arcade.color.YELLOW, font_size=14)
        self.v_box.add(self.message_label)

        # --- כפתורים ---
        login_button = arcade.gui.UIFlatButton(text="Submit Sign In", width=200)
        login_button.on_click = self.on_click_login
        self.v_box.add(login_button)

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        back_button.on_click = self.on_click_back
        self.v_box.add(back_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_click_login(self, event):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        #print(email in users_db)
        if email in users_db and users_db[email]['password'] == int(password):
            self.message_label.text = "Login successful!"
            self.message_label.text_color = arcade.color.GREEN
        else:
            print(email)
            print(users_db[email]["password"])
            self.message_label.text = "Error: Invalid email or password."
            self.message_label.text_color = arcade.color.RED

    def on_click_back(self, event):
        welcome_view = openscreen.WelcomeView()
        self.window.show_view(welcome_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()