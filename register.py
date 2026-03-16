import arcade
import arcade.gui
import openscreen
import user_manger
# מסד הנתונים הגלובלי (כדאי לוודא שהוא מוגדר בקובץ הראשי שלך כדי שגם ה-Login וגם ה-Register יראו אותו)
users_db =user_manger.load_users()


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

        # --- שורת שם פרטי ---
        firstname_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        firstname_label = arcade.gui.UILabel(text="First Name:", text_color=arcade.color.WHITE, font_size=16, width=100)
        firstname_row.add(firstname_label)

        self.firstname_input = arcade.gui.UIInputText(width=250, height=40, text="")
        # שים לב לשינוי כאן למטה: self.firstname_input במקום self.password_input
        firstname_row.add(self.firstname_input.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(firstname_row)

        # --- Last Name שורת שם משפחה ---
        lastname_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        lastname_label = arcade.gui.UILabel(text="Last Name:", text_color=arcade.color.WHITE, font_size=16, width=100)
        lastname_row.add(lastname_label)

        self.lastname_input = arcade.gui.UIInputText(width=250, height=40, text="")
        lastname_row.add(self.lastname_input.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(lastname_row)

        # --- Birth Date שורת תאריך לידה ---
        birthdate_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        birthdate_label = arcade.gui.UILabel(text="Birth Date:", text_color=arcade.color.WHITE, font_size=16, width=100)
        birthdate_row.add(birthdate_label)

        self.birthdate_input = arcade.gui.UIInputText(width=250, height=40, text="DD/MM/YYYY")
        birthdate_row.add(self.birthdate_input.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(birthdate_row)

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
            user_manger.register_user(email,password)
            self.message_label.text = "Success! Account created."
            self.message_label.text_color = arcade.color.GREEN
            print("Users in system:", users_db)

    def on_click_back(self, event):
        new_db=users_db
        welcome_view = openscreen.WelcomeView()
        self.window.show_view(welcome_view)
        new_db=user_manger.load_users()


    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()