import os
from dotenv import load_dotenv, dotenv_values
import tkinter as tk
from tkinter import simpledialog, messagebox
from openai import OpenAI
import asciiart

load_dotenv()

env = dotenv_values(".env")

def is_answer_correct(correct_answer, user_answer):
    try:
        return user_answer.replace(" ", "") == correct_answer.replace(" ", "") or user_answer.lower() in correct_answer.lower()
    except Exception as e:
        print(f"Error in is_answer_correct: {e}")
        return False

class MathGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Math Game")

        self.score = 0
        self.current_problem_index = 0

        self.client = OpenAI(api_key=env["OPENAI_API_KEY"])

        self.get_questions()

        self.title_label = tk.Label(master, text="Welcome to the Math Game!", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.problem_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.problem_label.pack(pady=10)

        self.answer_entry = tk.Entry(master, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)

        self.next_problem_button = tk.Button(master, text="Next Problem", command=self.process_problem, font=("Helvetica", 14))
        self.next_problem_button.pack(pady=10)

        self.display_problem()

    def get_questions(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Provide math equations of varying difficulty levels, ensuring they are suitable for a ninth-grade level. Exclude problems involving division by zero and repeating decimals. Include a few 'find the problem' equations. Focus only on algebra, arithmetic, and graphing questions. Please include equations like y=mx+b and finding the slope, but avoid questions that involve graphing lines. Ensure there's only one 'find the problem' question. REMEMBER TO USE BEDMAS TO SOLVE THEM. Return the information in JSON format, following this structure: \"math_equations\": {\"question\": \"what is 2+2\", \"answer\": \"4\"}, \"find_the_problem\": {\"question_1\": {\"original_equation\": \"2(x + 3) = 7x + 1\",\"incorrect_equation\": \"2(x - 3) = 7x - 1\",\"corrected_equation\": \"2(x + 3) = 7x - 1\",\"solution\": \"x = 4\"}}"
                },
            ],
        )

        reply = eval(response.choices[0].message.content)
        self.math_problems = reply["math_equations"]
        self.find_the_problem = reply["find_the_problem"]

    def display_problem(self):
        if self.current_problem_index < len(self.math_problems):
            problem = self.math_problems[self.current_problem_index]
            self.problem_label.config(text=f"\n{problem['question']}")
            self.answer_entry.delete(0, tk.END)  # Clear the entry for the new problem
        else:
            self.display_bonus_question()

    def process_problem(self, event=None):
        if self.current_problem_index < len(self.math_problems):
            problem = self.math_problems[self.current_problem_index]
            user_answer = self.answer_entry.get()

            if is_answer_correct(problem['answer'], user_answer):
                messagebox.showinfo("Correct!", "Well done! 🎉")
                self.score += 1
            else:
                messagebox.showinfo("Incorrect", f"Sorry, the correct answer was: {problem['answer']}")

            self.current_problem_index += 1
            self.display_problem()
        else:
            self.display_bonus_question()

    def display_bonus_question(self):
        special_question_key = 'question_1'
        special_problem = self.find_the_problem[special_question_key]['original_equation']
        mistake = self.find_the_problem[special_question_key]['incorrect_equation']
        corrected_problem = self.find_the_problem[special_question_key]['corrected_equation']

        user_choice = messagebox.askyesno("Bonus Question", f"\nBonus Question!\nFind the mistake in the following equation:\n{special_problem}\nA) {mistake}\nB) {corrected_problem}\n\nSelect 'Yes' if option B is correct, and 'No' otherwise.")

        if user_choice:
            messagebox.showinfo("Correct!", f"Correct! 🎉 The mistake was in option A, and the corrected equation is: {corrected_problem}")
            self.score += 1
        else:
            messagebox.showinfo("Incorrect", f"Incorrect. 😔 The correct answer was option B.")

        final_message = f"Game Over! Your score: {self.score}/{len(self.math_problems) + 1}"
        messagebox.showinfo("Game Over", final_message)

        # Exit the game after showing the final message
        self.master.destroy()

def main():
    root = tk.Tk()
    app = MathGameGUI(root)
    root.bind("<Return>", app.process_problem)  # Bind the 'Enter' key to process the problem
    root.mainloop()

if __name__ == "__main__":
    main()
