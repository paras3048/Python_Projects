import tkinter as tk
from tkinter import messagebox
import random
import time
import statistics


TEXTS = {
    "Easy": [
        "Python is easy to learn and fun to use.",
        "Practice makes programming better.",
        "Learning Python takes time and patience.",
        "Small projects help build programming skills."
    ],

    "Medium": [
        "Python provides powerful libraries for data analysis and visualization.",
        "Writing code regularly is one of the best ways to improve programming skills.",
        "Data can be transformed into useful information using Python and different libraries.",
        "Good programming requires practice, logical thinking, and attention to detail."
    ],

    "Hard": [
        "Python can be used to automate repetitive tasks, analyze large datasets, and build intelligent applications.",
        "Efficient programming requires developers to understand algorithms, data structures, debugging techniques, and software design.",
        "Data analysis involves collecting information, cleaning datasets, identifying patterns, and communicating meaningful insights."
    ]
}


class TypingSpeedTester:

    def __init__(self, root):

        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x600")

        self.start_time = None
        self.test_running = False
        self.current_text = ""
        self.results = []

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Typing Speed Tester",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=10)

        tk.Label(
            difficulty_frame,
            text="Difficulty:"
        ).pack(side=tk.LEFT, padx=5)

        self.difficulty = tk.StringVar(value="Medium")

        difficulty_menu = tk.OptionMenu(
            difficulty_frame,
            self.difficulty,
            "Easy",
            "Medium",
            "Hard"
        )

        difficulty_menu.pack(side=tk.LEFT)

        self.text_display = tk.Label(
            self.root,
            text="Click 'Start Test' to begin.",
            wraplength=700,
            justify="left",
            font=("Arial", 14),
            padx=20,
            pady=20
        )

        self.text_display.pack(pady=20)

        self.input_box = tk.Text(
            self.root,
            height=6,
            width=80,
            font=("Arial", 12),
            state=tk.DISABLED
        )

        self.input_box.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start Test",
            command=self.start_test,
            width=15
        )

        self.start_button.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(
            button_frame,
            text="Submit",
            command=self.finish_test,
            width=15,
            state=tk.DISABLED
        )

        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_test,
            width=15
        )

        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(
            self.root,
            text="Time: 0.00 seconds",
            font=("Arial", 12)
        )

        self.timer_label.pack(pady=10)

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 13),
            justify="left"
        )

        self.result_label.pack(pady=10)

    def start_test(self):

        difficulty = self.difficulty.get()

        self.current_text = random.choice(
            TEXTS[difficulty]
        )

        self.text_display.config(
            text=self.current_text
        )

        self.input_box.config(
            state=tk.NORMAL
        )

        self.input_box.delete(
            "1.0",
            tk.END
        )

        self.input_box.focus()

        self.start_button.config(
            state=tk.DISABLED
        )

        self.submit_button.config(
            state=tk.NORMAL
        )

        self.difficulty_menu_state(False)

        self.result_label.config(
            text=""
        )

        self.start_time = time.time()
        self.test_running = True

        self.update_timer()

    def update_timer(self):

        if not self.test_running:
            return

        elapsed = time.time() - self.start_time

        self.timer_label.config(
            text=f"Time: {elapsed:.2f} seconds"
        )

        self.root.after(
            100,
            self.update_timer
        )

    def finish_test(self):

        if not self.test_running:
            return

        end_time = time.time()

        typed_text = self.input_box.get(
            "1.0",
            tk.END
        ).strip()

        elapsed_time = end_time - self.start_time

        self.test_running = False

        accuracy = self.calculate_accuracy(
            self.current_text,
            typed_text
        )

        wpm = self.calculate_wpm(
            typed_text,
            elapsed_time
        )

        characters = len(typed_text)

        errors = self.calculate_errors(
            self.current_text,
            typed_text
        )

        result = {
            "wpm": wpm,
            "accuracy": accuracy,
            "time": elapsed_time,
            "errors": errors
        }

        self.results.append(result)

        self.display_result(
            wpm,
            accuracy,
            elapsed_time,
            characters,
            errors
        )

        self.input_box.config(
            state=tk.DISABLED
        )

        self.submit_button.config(
            state=tk.DISABLED
        )

        self.start_button.config(
            state=tk.NORMAL
        )

        self.difficulty_menu_state(True)

    def calculate_accuracy(self, original, typed):

        if not typed:
            return 0

        correct_characters = 0

        for i in range(
            min(len(original), len(typed))
        ):

            if original[i] == typed[i]:
                correct_characters += 1

        accuracy = (
            correct_characters /
            max(len(original), len(typed))
        ) * 100

        return accuracy

    def calculate_errors(self, original, typed):

        errors = abs(
            len(original) - len(typed)
        )

        for i in range(
            min(len(original), len(typed))
        ):

            if original[i] != typed[i]:
                errors += 1

        return errors

    def calculate_wpm(self, typed_text, elapsed_time):

        if elapsed_time <= 0:
            return 0

        words = len(typed_text.split())

        minutes = elapsed_time / 60

        return words / minutes

    def display_result(
        self,
        wpm,
        accuracy,
        elapsed_time,
        characters,
        errors
    ):

        result = (
            f"WPM: {wpm:.2f}\n"
            f"Accuracy: {accuracy:.2f}%\n"
            f"Time: {elapsed_time:.2f} seconds\n"
            f"Characters Typed: {characters}\n"
            f"Errors: {errors}"
        )

        self.result_label.config(
            text=result
        )

        if accuracy < 70:
            messagebox.showwarning(
                "Typing Result",
                "Your accuracy is low. Focus on typing carefully."
            )

    def difficulty_menu_state(self, enabled):

        # The OptionMenu is not directly stored,
        # so this method is intentionally kept simple.
        pass

    def reset_test(self):

        self.test_running = False
        self.start_time = None
        self.current_text = ""

        self.input_box.config(
            state=tk.NORMAL
        )

        self.input_box.delete(
            "1.0",
            tk.END
        )

        self.input_box.config(
            state=tk.DISABLED
        )

        self.text_display.config(
            text="Click 'Start Test' to begin."
        )

        self.timer_label.config(
            text="Time: 0.00 seconds"
        )

        self.result_label.config(
            text=""
        )

        self.start_button.config(
            state=tk.NORMAL
        )

        self.submit_button.config(
            state=tk.DISABLED
        )


def main():

    root = tk.Tk()

    app = TypingSpeedTester(root)

    root.mainloop()


if __name__ == "__main__":
    main()