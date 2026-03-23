import arcade
import arcade.gui
import requests
import json


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

        self.history = []
        self.current_situation = ""
        self.questions_answered = 0
        self.questions_limit = 3

        self.topics = [
            "Peer pressure and spending",
            "Delayed gratification in purchasing",
            "Long-term savings management"
        ]

        self.question_box = arcade.gui.UIBoxLayout(space_between=20)

        self.question_text = arcade.gui.UITextArea(
            text="Preparing financial scenario...",
            width=500,
            height=200,
            text_color=arcade.color.WHITE
        )
        self.question_box.add(self.question_text)

        self.answer_input = arcade.gui.UIInputText(
            width=500,
            height=50,
            text=""
        )
        self.question_box.add(self.answer_input.with_background(color=arcade.color.DARK_GRAY))

        self.submit_button = arcade.gui.UIFlatButton(text="Submit Answer", width=300)
        self.question_box.add(self.submit_button)

        @self.submit_button.event("on_click")
        def on_click_submit(event):
            self.process_answer()

        self.feedback_box = arcade.gui.UIBoxLayout(space_between=20)

        self.feedback_text = arcade.gui.UITextArea(
            text="",
            width=500,
            height=200,
            text_color=arcade.color.WHITE
        )
        self.feedback_box.add(self.feedback_text)

        self.next_button = arcade.gui.UIFlatButton(text="Next Question", width=300)
        self.feedback_box.add(self.next_button)

        self.feedback_box.visible = False

        @self.next_button.event("on_click")
        def on_click_next(event):
            self.advance_to_next()

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.question_box, anchor_x="center_x", anchor_y="center_y")
        anchor.add(child=self.feedback_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        self.get_new_situation()

    def get_new_situation(self):
        current_topic = self.topics[self.questions_answered % len(self.topics)]

        prompt = (f"Create a short financial scenario for teenagers about: {current_topic}. "
                  f"At the end, ask one question about what they would do. Be concise and write in English.")

        self.current_situation = ask_ollama(prompt)
        self.question_text.text = self.current_situation

    def process_answer(self):
        user_reply = self.answer_input.text.strip()
        if not user_reply:
            return

        self.history.append({
            "question": self.current_situation,
            "user_answer": user_reply
        })

        with open("finance_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)

        feedback_prompt = (f"Scenario: {self.current_situation}\n"
                           f"User answered: {user_reply}\n"
                           f"Give a very brief feedback (up to 2 sentences) in English.")
        immediate_feedback = ask_ollama(feedback_prompt)

        self.question_box.visible = False
        self.feedback_text.text = f"--- Feedback ---\n\n{immediate_feedback}"
        self.feedback_box.visible = True

    def advance_to_next(self):
        self.questions_answered += 1
        self.answer_input.text = ""

        self.feedback_box.visible = False
        self.question_box.visible = True

        if self.questions_answered >= self.questions_limit:
            self.finalize_and_analyze()
        else:
            self.question_text.text = "Loading next question..."
            self.get_new_situation()

    def finalize_and_analyze(self):
        self.submit_button.visible = False
        self.answer_input.visible = False
        self.question_text.text = "Analyzing your responses... Final feedback will appear shortly."

        history_str = json.dumps(self.history, indent=2)
        analysis_prompt = (
            f"Here is a history of scenarios and answers: {history_str}. "
            f"Analyze the user's financial decision-making and provide a constructive summary in English, including points for improvement."
        )

        final_feedback = ask_ollama(analysis_prompt)
        self.question_text.text = f"--- Final Analysis ---\n\n{final_feedback}"

    def on_draw(self):
        self.clear()
        self.manager.draw()