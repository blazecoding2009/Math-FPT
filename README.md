# Math Grade 9 FPT Creation

Welcome to my Grade 9 Creation for the Math Final Performace task! This console-based game challenges players with math problems and a bonus question. The game retrieves math problems from OpenAI's GPT-3.5-turbo model and evaluates the player's responses.

## Features

- Diverse math problems suitable for a ninth-grade level.
- Bonus question involving finding a mistake in an equation.
- Utilizes OpenAI's GPT-3.5-turbo model for generating math problems.
- User-friendly interface with clear instructions.

## Prerequisites

- Python 3.x
- Required Python packages (install via `pip install -r requirements.txt`):
  - `openai`
  - `python-dotenv`

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/math-game.git
   cd math-game
   ```
2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```
3. **Create a .env file in the project root and add your OpenAI API key:**

    ```makefile
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage
Run the game by executing the following command:

    ```bash
    python math_game.py
    ```

Follow the on-screen instructions to play the game. Answer the math problems and the bonus question to earn a score.

## Contributing
If you'd like to contribute to the project, feel free to submit pull requests or open issues. Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
OpenAI for providing the powerful GPT-3.5-turbo model.
ASCII Art contributors for the cool ASCII art used in the game.
Have fun playing the Math Game! 🎮🧠