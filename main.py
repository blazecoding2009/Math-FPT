import os
from dotenv import load_dotenv, dotenv_values
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


def display_question(question):
    print("\n" + question)


def get_user_answer():
    return input("Your answer: ")


def process_math_problems(math_problems):
    score = 0

    for problem in math_problems:
        display_question(problem['question'])
        user_answer = get_user_answer()

        if is_answer_correct(problem['answer'], user_answer):
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Incorrect. 😔 The correct answer was: {problem['answer']}")

    return score


def display_bonus_question(special_problem, mistake, corrected_problem):
    print(f"\nBonus Question!\nFind the mistake in the following equation:\n{special_problem}")
    print(f"A) {mistake}")
    print(f"B) {corrected_problem}")


def get_user_choice():
    return input("Your choice (A/B): ")


def process_bonus_question(user_choice, corrected_problem):
    if user_choice.upper() == 'B':
        print(f"Correct! 🎉 The mistake was in option A, and the corrected equation is: {corrected_problem}")
        return 1
    else:
        print("Incorrect. 😔 The correct answer was option B.")
        return 0


def main():
    os.system("cls")
    print(asciiart.main)
    print("Welcome to the Math Game! Please wait while we get your questions...")

    client = OpenAI(api_key=env["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Provide math equations of varying difficulty levels, ensuring they are suitable for a ninth-grade level. Exclude problems involving division by zero and repeating decimals. Include a few 'find the problem' equations. Focus only on algebra, arithmetic, and graphing questions. Please include equations like y=mx+b and finding the slope, but avoid questions that involve graphing lines. Ensure there's only one 'find the problem' question. REMEMBER TO USE BEDMAS TO SOLVE THEM. Return the information in JSON format, following this structure: \"math_equations\": {\"question\": \"what is 2+2\", \"answer\": \"4\"}, \"find_the_problem\": {\"question_1\": {\"original_equation\": \"2(x + 3) = 7x + 1\",\"incorrect_equation\": \"2(x - 3) = 7x - 1\",\"corrected_equation\": \"2(x + 3) = 7x - 1\",\"solution\": \"x = 4\"}}"
            },
        ],
    )

    reply = eval(response.choices[0].message.content)
    math_problems = reply["math_equations"]
    find_the_problem = reply["find_the_problem"]

    math_score = process_math_problems(math_problems)

    special_question_key = 'question_1'
    special_problem = find_the_problem[special_question_key]['original_equation']
    mistake = find_the_problem[special_question_key]['incorrect_equation']
    corrected_problem = find_the_problem[special_question_key]['corrected_equation']

    display_bonus_question(special_problem, mistake, corrected_problem)

    user_choice = get_user_choice()

    bonus_score = process_bonus_question(user_choice, corrected_problem)

    total_score = math_score + bonus_score

    print(f"\nGame Over! Your score: {total_score}/{len(math_problems) + 1}")


if __name__ == "__main__":
    main()
