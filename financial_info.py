import arcade
import arcade.gui
import user_manger
import openscreen


class FinancialInfoView(arcade.View):
    def __init__(self, email, temp_details):
        super().__init__()
        self.email = email
        self.temp_details = temp_details
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.v_box = arcade.gui.UIBoxLayout(space_between=10)

        # כותרת
        self.v_box.add(arcade.gui.UILabel(text="Financial Details", font_size=20, bold=True))

        # שדות קלט
        self.money = self.add_input("Current Money:")
        self.social = self.add_input("Social Meetings (per week):")
        self.working = self.add_input("Working? (Yes/No):")
        self.job_type = self.add_input("Job Type:")
        self.income = self.add_input("Monthly Income:")
        self.goal = self.add_input("Financial Goal:")

        # כפתור סיום
        submit_btn = arcade.gui.UIFlatButton(text="Finish & Save", width=200)
        submit_btn.on_click = self.on_finish
        self.v_box.add(submit_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def add_input(self, label_text):
        row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        row.add(arcade.gui.UILabel(text=label_text, width=200))
        input_field = arcade.gui.UIInputText(width=200, height=30, text="")
        row.add(input_field.with_background(color=arcade.color.DARK_GRAY))
        self.v_box.add(row)
        return input_field

    def on_finish(self, event):
        # איסוף הנתונים החדשים
        fin_data = {
            "money": self.money,
            "social_meetings": self.social.text,
            "is_working": self.working.text,
            "job_type": self.job_type.text,
            "monthly_income": self.income.text,
            "goal": self.goal.text
        }

        # הרשמה סופית ל-JSON דרך ה-Manager
        user_manger.register_user(
            self.email,
            self.temp_details['password'],
            self.temp_details['first_name'],
            self.temp_details['last_name'],
            self.temp_details['birth_date']
        )

        # עדכון הנתונים הפיננסיים בתוך הקובץ
        users = user_manger.load_users()
        users[self.email]["financial_info"] = fin_data
        user_manger.save_users(users)

        # חזרה למסך הראשי
        self.window.show_view(openscreen.WelcomeView())

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()