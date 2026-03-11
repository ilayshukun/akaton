import arcade
import arcade.gui
import openscreen

# מסד הנתונים הגלובלי (כדאי לוודא שהוא מוגדר בקובץ הראשי שלך כדי שגם ה-Login וגם ה-Register יראו אותו)
users_db = {}


class RegisterView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.DARK_OLIVE_GREEN)

        # התיבה הראשית שמסדרת הכל אנכית
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # כותרת המסך
        self.title = arcade.gui.UILabel(text="Register", text_color=arcade.color.WHITE, font_size=30, bold=True)
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

        # --- הודעות שגיאה/הצלחה ---
        self.message_label = arcade.gui.UILabel(text="", text_color=arcade.color.YELLOW, font_size=14)
        self.v_box.add(self.message_label)

        # --- כפתורים ---
        # שים לב: שיניתי את on_click ל-on_click_register כדי שיתאים לשם הפונקציה למטה
        register_button = arcade.gui.UIFlatButton(text="Submit Register", width=200)
        register_button.on_click = self.on_click_register
        self.v_box.add(register_button)

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        back_button.on_click = self.on_click_back
        self.v_box.add(back_button)

        # עיגון למרכז המסך
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_click_register(self, event):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        # בדיקה 1: האם השדות ריקים?
        if email == "" or password == "":
            self.message_label.text = "Error: Fields cannot be empty."
            self.message_label.text_color = arcade.color.RED

        # בדיקה 2: האם המשתמש כבר קיים במערכת?
        elif email in users_db:
            self.message_label.text = "Error: User already exists!"
            self.message_label.text_color = arcade.color.RED

        # אם הכל תקין - הצלחה!
        else:
            users_db[email] = password
            self.message_label.text = "Success! Account created."
            self.message_label.text_color = arcade.color.GREEN
            print("Users in system:", users_db)

    def on_click_back(self, event):
        welcome_view = openscreen.WelcomeView()
        self.window.show_view(welcome_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()