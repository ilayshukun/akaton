import arcade
import arcade.gui
import requests



def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json()["response"]
    except Exception as e:
        return f"Error connecting to Ollama: {e}"


class QuestionsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.ARMY_GREEN)

        # המכולה הראשית
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # תצוגת השאלה מה-AI
        # השתמשנו ב-UITextArea כי שאלות של AI יכולות להיות ארוכות
        self.question_text = arcade.gui.UITextArea(
            text="טוען סיטואציה פיננסית מ-Ollama...",
            width=500,
            height=200,
            text_color=arcade.color.WHITE
        )
        self.v_box.add(self.question_text)

        # תיבת טקסט לתשובה של הנער/ה
        self.answer_input = arcade.gui.UIInputText(
            width=500,
            height=50,
            text=""
        )
        self.v_box.add(self.answer_input.with_background(color=arcade.color.DARK_GRAY))

        # כפתור שליחה
        submit_button = arcade.gui.UIFlatButton(text="שלח תשובה וקבל סיטואציה חדשה", width=300)
        self.v_box.add(submit_button)

        @submit_button.event("on_click")
        def on_click_submit(event):
            self.send_answer_and_get_next()

        # מיקום הכל במרכז
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        # קבלת השאלה הראשונה מיד עם פתיחת המסך


    def get_new_situation(self):
        prompt = "Give me one short finance situation for teenagers and ask a question about it. Be concise."
        ai_response = ask_ollama(prompt)
        self.question_text.text = ai_response

    def send_answer_and_get_next(self):
        user_reply = self.answer_input.text
        if not user_reply.strip():
            return

        # כאן אנחנו שולחים ל-AI את התשובה שלנו ומבקשים פידבק + סיטואציה חדשה
        prompt = f"The user answered: '{user_reply}' to the previous situation. Give a very brief feedback and then provide a new finance situation for a teenager with a question."

        self.question_text.text = "ה-AI חושב..."
        self.answer_input.text = ""  # איפוס התיבה

        new_ai_response = ask_ollama(prompt)
        self.question_text.text = new_ai_response

    def on_show_view(self):
        """נקרא כשהמסך מוצג"""
        self.manager.enable()
        self.get_new_situation()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


