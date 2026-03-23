import arcade
import arcade.gui
import openscreen
import user_manger
import questions_screen


class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # החזרת הרקע המקורי
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # כותרת
        self.v_box.add(arcade.gui.UILabel(text="Sign In", font_size=30, bold=True))

        # שדות קלט בעיצוב המקורי (אפור כהה)
        self.email_input = arcade.gui.UIInputText(width=250, height=40, text="").with_background(
            color=arcade.color.DARK_GRAY)
        self.password_input = arcade.gui.UIInputText(width=250, height=40, text="").with_background(
            color=arcade.color.DARK_GRAY)

        self.v_box.add(arcade.gui.UILabel(text="Email:"))
        self.v_box.add(self.email_input)
        self.v_box.add(arcade.gui.UILabel(text="Password:"))
        self.v_box.add(self.password_input)

        self.message_label = arcade.gui.UILabel(text="", text_color=arcade.color.YELLOW)
        self.v_box.add(self.message_label)

        # כפתור התחברות
        login_btn = arcade.gui.UIFlatButton(text="Submit Sign In", width=200)
        login_btn.on_click = self.on_click_login
        self.v_box.add(login_btn)

        # כפתור חזרה (Back) - מעוצב באותו סגנון
        back_btn = arcade.gui.UIFlatButton(text="Back", width=200)
        back_btn.on_click = lambda x: self.window.show_view(openscreen.WelcomeView())
        self.v_box.add(back_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_click_login(self, event):
        users = user_manger.load_users()
        email = self.email_input.text.strip()
        pw = self.password_input.text.strip()

        # בדיקת תקינות פרטים
        if email in users and str(users[email]['password']) == pw:
            self.window.show_view(questions_screen.QuestionsView())
        else:
            self.message_label.text = "Invalid credentials"

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()