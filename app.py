import sys
from openai import OpenAI

client = OpenAI(api_key="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")

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

ETHICAL_GUIDELINES = (
    "Always be respectful, avoid harmful or misleading content, "
    "do not promote discrimination, and protect user privacy. Also do not talk about weapons of any sort, do not swear, and be appropriate."
)

PERSONALITIES = {
    "Batman": f"Respond like Batman. Be disciplined, focused, and stoic. {ETHICAL_GUIDELINES}",
    "Albert Einstein": f"Respond like Albert Einstein. Be curious, thoughtful, and slightly whimsical. Use analogies from physics and math to explain ideas, and encourage deep thinking and imagination. {ETHICAL_GUIDELINES}",
    "Serena Williams": f"Respond like Serena Williams. Be powerful, poised, and determined. Speak with confidence, resilience, and pride in overcoming adversity. Encourage excellence through perseverance. {ETHICAL_GUIDELINES}",
    "Sherlock Holmes": f"Respond like Sherlock Holmes. Be analytical, precise, and logical. Use deductive reasoning and a sharp, observational tone. Keep responses crisp and intelligent. {ETHICAL_GUIDELINES}",
    "Bob Ross": f"Respond like Bob Ross. Be calm, positive, and nurturing. Use gentle encouragement and peaceful imagery. Speak like you're painting a happy little idea in the user’s mind. {ETHICAL_GUIDELINES}",
    "Tony Stark": f"Respond like Tony Stark. Be witty, genius-level smart, and a bit arrogant. Mix humor with insight. Reference tech, innovation, and always make it feel like you're the smartest person in the room—but still charming. {ETHICAL_GUIDELINES}"
}

class AICompanionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Companion")
        self.setFixedSize(350, 600)
        self.setStyleSheet("background-color: #121212; color: white;")
        self.chat_history_stack = []  
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit()
        send_button = QPushButton("Send")
        clear_button = QPushButton("Clear Chat")
        undo_button = QPushButton("Undo")  

        self.personality_box = QComboBox()
        self.personality_box.addItems(PERSONALITIES.keys())
        self.personality_box.setStyleSheet("background-color: #333333; color: white;")

        send_button.setStyleSheet("background-color: #007BFF; color: white;")
        clear_button.setStyleSheet("background-color: #DC3545; color: white;")
        undo_button.setStyleSheet("background-color: #6C757D; color: white;")  

        send_button.clicked.connect(self.send_message)
        clear_button.clicked.connect(self.clear_chat)
        undo_button.clicked.connect(self.undo_last)  

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_button)

        button_layout.addWidget(clear_button)
        button_layout.addWidget(undo_button)  

        layout.addWidget(self.personality_box)
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        personality = self.personality_box.currentText()
        system_prompt = PERSONALITIES[personality]

        
        self.chat_history_stack.append(self.chat_display.toHtml())  

        self.chat_display.append(f"You: {user_input}")
        self.input_field.clear()

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150
            )

            reply = response.choices[0].message.content.strip()
            self.chat_display.append(f"{personality}: {reply}\n")

        except Exception as e:
            self.chat_display.append(f"Error: {e}")

    def clear_chat(self):
        self.chat_display.clear()
        self.chat_history_stack.clear()  

    def undo_last(self):  
        if self.chat_history_stack:
            last_state = self.chat_history_stack.pop()
            self.chat_display.setHtml(last_state)
        else:
            self.chat_display.append("Nothing to undo.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AICompanionApp()
    window.show()
    sys.exit(app.exec_())
