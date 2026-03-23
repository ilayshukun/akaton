import arcade
import arcade.gui
import requests
import json
import openscreen


def ask_ollama(prompt, is_json=True):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.8}
    }
    if is_json:
        payload["format"] = "json"
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json()["response"]
    except:
        return None


class QuestionsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.history = []
        self.questions_answered = 0

        self.topics = [
            "Emergency savings for unexpected events",
            "Social pressure and expensive lifestyle",
            "Building a side business or hobby income",
            "Smart comparison shopping and discounts",
            "Managing recurring monthly subscriptions",
            "Long-term compound interest basics",
            "Lending money and financial boundaries",
            "Budgeting for major social celebrations"
        ]
        self.current_data = {}

        arcade.set_background_color(arcade.color.BLACK)

        self.main_box = arcade.gui.UIBoxLayout(space_between=15)

        self.progress_label = arcade.gui.UILabel(text="", font_size=14, bold=True, text_color=arcade.color.LIGHT_BLUE)
        self.main_box.add(self.progress_label)

        # תיבת שאלה גדולה במיוחד לסיפורים ארוכים (גובה 220)
        self.question_area = arcade.gui.UITextArea(text="Generating a complex scenario...", width=620, height=220,
                                                   font_size=15)
        self.main_box.add(self.question_area)

        self.options_box = arcade.gui.UIBoxLayout(space_between=10)
        self.main_box.add(self.options_box)

        # Feedback Popup
        self.popup_layer = arcade.gui.UIAnchorLayout()
        self.feedback_box = arcade.gui.UIBoxLayout(space_between=15)

        self.feedback_text = arcade.gui.UITextArea(text="", width=520, height=180, font_size=14)
        self.next_btn = arcade.gui.UIFlatButton(text="I Understand", width=160)
        self.next_btn.on_click = self.advance_to_next

        self.feedback_box.add(self.feedback_text)
        self.feedback_box.add(self.next_btn)

        self.popup_layer.add(child=self.feedback_box.with_background(color=arcade.color.DARK_SLATE_GRAY),
                             anchor_x="center_x", anchor_y="center_y")
        self.popup_layer.visible = False

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.main_box, anchor_x="center_x", anchor_y="center_y")
        anchor.add(child=self.popup_layer)
        self.manager.add(anchor)

    def on_show_view(self):
        self.get_new_situation()

    def get_new_situation(self):
        self.progress_label.text = f"MISSION {self.questions_answered + 1} / 10"
        topic = self.topics[self.questions_answered % len(self.topics)]

        # פרומפט שדורש סיפור ארוך ומפורט (5 משפטים) ותשובות ברורות (עד 7 מילים)
        prompt = (f"Act as a financial coach. Write a detailed 5-sentence story for a teenager about {topic}. "
                  "Describe a realistic situation with names and a specific financial dilemma. "
                  "End with a clear question: 'What is your best financial move?'. "
                  "Provide 4 options. IMPORTANT: Each option must be 4 to 7 words. "
                  "Return ONLY JSON: {'scenario': '...', 'options': ['...', '...', '...', '...'], 'correct_index': 0}")

        raw = ask_ollama(prompt)
        if raw:
            try:
                data = json.loads(raw)
                if all(key in data for key in ['scenario', 'options', 'correct_index']):
                    self.current_data = data
                    self.question_area.text = data['scenario']
                    self.display_options(data['options'])
                else:
                    self.get_new_situation()
            except:
                self.get_new_situation()

    def display_options(self, options):
        self.options_box.clear()
        for i, opt in enumerate(options):
            # התאמה ויזואלית לטקסט ארוך יותר בכפתורים
            btn = arcade.gui.UIFlatButton(text=opt, width=600, height=55)
            btn.index = i
            btn.on_click = self.on_answer_selected
            self.options_box.add(btn)

    def on_answer_selected(self, event):
        idx = event.source.index
        selected_text = event.source.text
        correct_idx = self.current_data.get('correct_index', 0)
        is_correct = (idx == correct_idx)

        self.history.append({"q": self.current_data.get('scenario', ''), "a": selected_text})

        # משוב עמוק ומנומק
        prompt = (f"In this scenario: '{self.current_data['scenario']}', the user chose: '{selected_text}'. "
                  f"Explain in 3 detailed sentences why this is {'a great strategic' if is_correct else 'a risky or poor'} decision. "
                  "Use very simple English and explain the long-term impact on their wallet.")

        feedback = ask_ollama(prompt,
                              is_json=False) or "This choice directly affects your ability to save for future goals."
        self.feedback_text.text = f"{'EXCELLENT!' if is_correct else 'CAUTION:'}\n\n{feedback}"

        self.popup_layer.visible = True
        self.main_box.visible = False

    def advance_to_next(self, event):
        self.questions_answered += 1
        self.popup_layer.visible = False
        self.main_box.visible = True
        if self.questions_answered >= 10:
            self.show_final_summary()
        else:
            self.get_new_situation()

    def show_final_summary(self):
        self.main_box.clear()

        # סיכום מקיף ומקצועי בשפה פשוטה
        summary_prompt = (f"Review these 10 detailed decisions: {json.dumps(self.history)}. "
                          "Write a professional 5-sentence financial report for this teenager. "
                          "Sentence 1: Their overall relationship with money. "
                          "Sentence 2: Their biggest strength. "
                          "Sentence 3: Their biggest weakness or risk. "
                          "Sentence 4: A specific strategy they should use starting tomorrow. "
                          "Sentence 5: A motivational closing. No intro, start immediately.")

        final_advice = ask_ollama(summary_prompt,
                                  is_json=False) or "You have completed the financial simulation successfully."

        self.main_box.add(arcade.gui.UILabel(text="YOUR COMPREHENSIVE FINANCIAL REPORT", font_size=20, bold=True))
        self.main_box.add(arcade.gui.UITextArea(text=final_advice, width=620, height=260, font_size=15))

        btn = arcade.gui.UIFlatButton(text="Return to Menu", width=220)
        btn.on_click = lambda x: self.window.show_view(openscreen.WelcomeView())
        self.main_box.add(btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()