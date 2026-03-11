import arcade
import arcade.gui
import openscreen
users_db = {}

class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)

        # כותרת
        self.title = arcade.gui.UILabel(text="Sign In", text_color=arcade.color.WHITE, font_size=24)
        self.v_box.add(self.title)

        # שדות קלט
        self.email_input = arcade.gui.UIInputText(width=300, height=40, text="Email")
        self.v_box.add(self.email_input.with_background(color=arcade.color.DARK_GRAY))

        self.password_input = arcade.gui.UIInputText(width=300, height=40, text="Password")
        self.v_box.add(self.password_input.with_background(color=arcade.color.DARK_GRAY))

        # הודעות שגיאה/הצלחה
        self.message_label = arcade.gui.UILabel(text="", text_color=arcade.color.YELLOW, font_size=14)
        self.v_box.add(self.message_label)

        # כפתור ביצוע התחברות
        login_button = arcade.gui.UIFlatButton(text="Submit Sign In", width=200)
        login_button.on_click = self.on_click_login
        self.v_box.add(login_button)

        # כפתור חזרה למסך הראשי
        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        back_button.on_click = self.on_click_back
        self.v_box.add(back_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_click_login(self, event):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        # בודקים אם האימייל קיים במילון וגם אם הסיסמה תואמת
        if email in users_db and users_db[email] == password:
            self.message_label.text = "Login successful!"
            self.message_label.text_color = arcade.color.GREEN
            print(f"User {email} logged in successfully!")
            # כאן תוכל להוסיף את המעבר למסך המשחק

        # אם אחד מהם לא נכון - שגיאה
        else:
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

