import customtkinter as ctk
from tkinter import filedialog, messagebox
from textblob import TextBlob
from collections import Counter
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AIWritingAssistant(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Writing Assistant")
        self.geometry("1400x850")
        self.minsize(1200, 750)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="AI Writing Assistant",
            font=("Segoe UI", 32, "bold")
        )

        title.pack(pady=15)

        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.score_card = ctk.CTkFrame(
            self.dashboard_frame
        )

        self.score_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.score_title = ctk.CTkLabel(
            self.score_card,
            text="Quality Score"
        )

        self.score_title.pack(pady=(15, 5))

        self.score_value = ctk.CTkLabel(
            self.score_card,
            text="0",
            font=("Segoe UI", 28, "bold")
        )

        self.score_value.pack(pady=(0, 15))

        self.sentiment_card = ctk.CTkFrame(
            self.dashboard_frame
        )

        self.sentiment_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.sentiment_title = ctk.CTkLabel(
            self.sentiment_card,
            text="Sentiment"
        )

        self.sentiment_title.pack(pady=(15, 5))

        self.sentiment_value = ctk.CTkLabel(
            self.sentiment_card,
            text="Neutral",
            font=("Segoe UI", 28, "bold")
        )

        self.sentiment_value.pack(
            pady=(0, 15)
        )

        self.keyword_card = ctk.CTkFrame(
            self.dashboard_frame
        )

        self.keyword_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.keyword_title = ctk.CTkLabel(
            self.keyword_card,
            text="Keywords"
        )

        self.keyword_title.pack(
            pady=(15, 5)
        )

        self.keyword_value = ctk.CTkLabel(
            self.keyword_card,
            text="-",
            wraplength=250
        )

        self.keyword_value.pack(
            pady=(0, 15)
        )

        self.editor_frame = ctk.CTkFrame(self)

        self.editor_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.left_panel = ctk.CTkFrame(
            self.editor_frame
        )

        self.left_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.right_panel = ctk.CTkFrame(
            self.editor_frame
        )

        self.right_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            self.left_panel,
            text="Original Text",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        self.input_text = ctk.CTkTextbox(
            self.left_panel
        )

        self.input_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.right_panel,
            text="Corrected Text",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        self.output_text = ctk.CTkTextbox(
            self.right_panel
        )

        self.output_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(
            fill="both",
            expand=False,
            padx=15,
            pady=10
        )

        self.stats_frame = ctk.CTkFrame(
            self.bottom_frame
        )

        self.stats_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="""
Words: 0
Characters: 0
Sentences: 0
Reading Time: 0 min
Corrections: 0
""",
            justify="left",
            font=("Segoe UI", 14)
        )

        self.stats_label.pack(
            padx=15,
            pady=15,
            anchor="w"
        )

        self.correction_frame = ctk.CTkFrame(
            self.bottom_frame
        )

        self.correction_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            self.correction_frame,
            text="Corrections Made",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        self.correction_box = ctk.CTkTextbox(
            self.correction_frame,
            height=180
        )

        self.correction_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.correct_btn = ctk.CTkButton(
            self.button_frame,
            text="Correct Text",
            height=40,
            command=self.correct_text
        )

        self.correct_btn.pack(
            side="left",
            padx=10
        )

        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Report",
            height=40,
            command=self.save_report
        )

        self.save_btn.pack(
            side="left",
            padx=10
        )

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            height=40,
            command=self.clear_all
        )

        self.clear_btn.pack(
            side="left",
            padx=10
        )

    def extract_keywords(self, text):

        words = re.findall(
            r'\b[a-zA-Z]{4,}\b',
            text.lower()
        )

        common = Counter(words).most_common(5)

        return ", ".join(
            [word for word, count in common]
        )

    def get_changes(
        self,
        original,
        corrected
    ):

        old_words = re.findall(
            r'\b\w+\b',
            original
        )

        new_words = re.findall(
            r'\b\w+\b',
            corrected
        )

        changes = []

        for old, new in zip(
            old_words,
            new_words
        ):

            if old.lower() != new.lower():

                changes.append(
                    (old, new)
                )

        return changes

    def calculate_score(
        self,
        text,
        corrections
    ):

        words = len(text.split())

        score = 100

        score -= corrections * 3

        if words < 20:
            score -= 10

        if words > 100:
            score += 5

        return max(
            0,
            min(100, score)
        )
    def correct_text(self):

        text = self.input_text.get(
            "1.0",
            "end"
        ).strip()

        if not text:

            messagebox.showwarning(
                "Input Required",
                "Please enter some text."
            )

            return

        corrected = str(
            TextBlob(text).correct()
        )

        self.output_text.delete(
            "1.0",
            "end"
        )

        self.output_text.insert(
            "1.0",
            corrected
        )

        changes = self.get_changes(
            text,
            corrected
        )

        self.correction_box.delete(
            "1.0",
            "end"
        )

        if len(changes) == 0:

            self.correction_box.insert(
                "end",
                "No spelling mistakes detected."
            )

        else:

            self.correction_box.insert(
                "end",
                "SPELLING CORRECTIONS\n"
            )

            self.correction_box.insert(
                "end",
                "=" * 50 + "\n\n"
            )

            for old, new in changes:

                self.correction_box.insert(
                    "end",
                    f"❌ {old}\n"
                )

                self.correction_box.insert(
                    "end",
                    f"✅ {new}\n\n"
                )

        words = len(
            text.split()
        )

        characters = len(text)

        sentences = len(
            re.findall(
                r'[.!?]',
                text
            )
        )

        if sentences == 0:
            sentences = 1

        reading_time = round(
            words / 200,
            2
        )

        polarity = TextBlob(
            text
        ).sentiment.polarity

        if polarity > 0:

            sentiment = "Positive"

        elif polarity < 0:

            sentiment = "Negative"

        else:

            sentiment = "Neutral"

        self.sentiment_value.configure(
            text=sentiment
        )

        keywords = self.extract_keywords(
            text
        )

        if keywords == "":
            keywords = "No keywords"

        self.keyword_value.configure(
            text=keywords
        )

        score = self.calculate_score(
            text,
            len(changes)
        )

        self.score_value.configure(
            text=f"{score}/100"
        )

        self.stats_label.configure(
            text=
            f"""
Words: {words}
Characters: {characters}
Sentences: {sentences}
Reading Time: {reading_time} min
Corrections: {len(changes)}
"""
        )

    def save_report(self):

        corrected_text = self.output_text.get(
            "1.0",
            "end"
        ).strip()

        if corrected_text == "":

            messagebox.showwarning(
                "No Output",
                "Generate corrected text first."
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if file_path:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "AI WRITING ASSISTANT REPORT\n"
                )

                file.write(
                    "=" * 50 + "\n\n"
                )

                file.write(
                    corrected_text
                )

            messagebox.showinfo(
                "Saved",
                "Report saved successfully."
            )

    def clear_all(self):

        self.input_text.delete(
            "1.0",
            "end"
        )

        self.output_text.delete(
            "1.0",
            "end"
        )

        self.correction_box.delete(
            "1.0",
            "end"
        )

        self.score_value.configure(
            text="0"
        )

        self.sentiment_value.configure(
            text="Neutral"
        )

        self.keyword_value.configure(
            text="-"
        )

        self.stats_label.configure(
            text="""
Words: 0
Characters: 0
Sentences: 0
Reading Time: 0 min
Corrections: 0
"""
        )


if __name__ == "__main__":

    app = AIWritingAssistant()

    app.mainloop()