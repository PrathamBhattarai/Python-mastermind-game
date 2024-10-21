import tkinter as tk
import random

# Possible colors
COLORS = ["Red", "Green", "Blue", "Yellow", "White", "Orange"]

# Number of colors in the secret code
CODE_LENGTH = 4

# Maximum number of attempts allowed
MAX_ATTEMPTS = 10

def generate_secret_code():
    return random.choices(COLORS, k=CODE_LENGTH)

# Game state variables
secret_code = generate_secret_code()
current_guess = []
attempts = 0
game_over = False

# Initialize the main window
window = tk.Tk()
window.title("Mastermind Game")
window.geometry("600x600")

# Instructions label
instructions_label = tk.Label(window, text="Welcome to Mastermind! Guess the secret code.", font=("Helvetica", 16))
instructions_label.pack(pady=10)

# Feedback label to display messages
feedback_label = tk.Label(window, text="", font=("Helvetica", 12))
feedback_label.pack(pady=5)

# Label to display the current guess
guess_label = tk.Label(window, text="Current Guess: []", font=("Helvetica", 12))
guess_label.pack(pady=5)

# Frame to display previous attempts
attempts_frame = tk.Frame(window)
attempts_frame.pack(pady=10)

# Label for previous attempts
attempts_label = tk.Label(attempts_frame, text="Previous Attempts:", font=("Helvetica", 14))
attempts_label.pack()

# Text widget to display the list of attempts
attempts_text = tk.Text(attempts_frame, height=10, width=50, state='disabled')
attempts_text.pack()

# Frame to hold color buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=10)

# Dictionary to hold the color buttons
color_buttons = {}

# Function to add a color to the current guess
def add_color(color):
    global current_guess
    if not game_over and len(current_guess) < CODE_LENGTH:
        current_guess.append(color)
        guess_label.config(text=f"Current Guess: {current_guess}")
    if len(current_guess) == CODE_LENGTH:
        submit_button.config(state='normal')

# Create buttons for each color
for color in COLORS:
    btn = tk.Button(buttons_frame, text=color, bg=color.lower(), fg="black", width=10,
                    command=lambda c=color: add_color(c))
    btn.pack(side='left', padx=5)
    color_buttons[color] = btn

# Submit button
submit_button = tk.Button(window, text="Submit Guess", state='disabled', command=lambda: submit_guess())
submit_button.pack(pady=10)

def check_guess(guess, code):
    # Make copies to avoid modifying originals
    guess_copy = guess.copy()
    code_copy = code.copy()
    correct_positions = 0
    correct_colors = 0

    # First pass: check for correct color and position
    for i in range(len(guess_copy)):
        if guess_copy[i] == code_copy[i]:
            correct_positions += 1
            # Mark the positions so they are not reused
            guess_copy[i] = None
            code_copy[i] = None

    # Second pass: check for correct color but wrong position
    for i in range(len(guess_copy)):
        if guess_copy[i] and guess_copy[i] in code_copy:
            correct_colors += 1
            # Remove the color to prevent duplicate counting
            code_copy[code_copy.index(guess_copy[i])] = None

    return correct_positions, correct_colors

def submit_guess():
    global attempts, current_guess, game_over
    if game_over:
        return
    attempts += 1
    correct_positions, correct_colors = check_guess(current_guess, secret_code)
    update_attempts_text(current_guess, correct_positions, correct_colors)
    if correct_positions == CODE_LENGTH:
        feedback_label.config(text="Congratulations! You've cracked the code!")
        game_over = True
        disable_buttons()
    elif attempts >= MAX_ATTEMPTS:
        feedback_label.config(text=f"Game Over! The secret code was: {secret_code}")
        game_over = True
        disable_buttons()
    else:
        feedback_label.config(text=f"Attempt {attempts}: {correct_positions} correct position(s), {correct_colors} correct color(s)")
    # Reset for next guess
    current_guess = []
    guess_label.config(text="Current Guess: []")
    submit_button.config(state='disabled')

def update_attempts_text(guess, correct_positions, correct_colors):
    attempts_text.config(state='normal')
    attempts_text.insert('end', f"Attempt {attempts}: {guess} | Positions: {correct_positions}, Colors: {correct_colors}\n")
    attempts_text.config(state='disabled')

def disable_buttons():
    for btn in color_buttons.values():
        btn.config(state='disabled')
    submit_button.config(state='disabled')

def restart_game():
    global secret_code, current_guess, attempts, game_over
    secret_code = generate_secret_code()
    current_guess = []
    attempts = 0
    game_over = False
    feedback_label.config(text="")
    guess_label.config(text="Current Guess: []")
    attempts_text.config(state='normal')
    attempts_text.delete('1.0', 'end')
    attempts_text.config(state='disabled')
    for btn in color_buttons.values():
        btn.config(state='normal')
    submit_button.config(state='disabled')

# Restart button
restart_button = tk.Button(window, text="Restart Game", command=restart_game)
restart_button.pack(pady=10)

# Start the main loop
window.mainloop()
