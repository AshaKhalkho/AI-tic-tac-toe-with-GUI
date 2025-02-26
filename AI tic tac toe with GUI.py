import tkinter as tk
import math

# Initialize the game board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Function to check for a winner
def check_winner():
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    return None  # No winner yet

# Function to check if the board is full
def is_full():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Minimax algorithm for AI
def minimax(is_maximizing):
    winner = check_winner()
    if winner == 'X': return -10
    if winner == 'O': return 10
    if is_full(): return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(False)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(True)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
        return best_score

# Function for AI to find the best move
def best_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Function to update the board when a player clicks a button
def player_move(i, j):
    if board[i][j] == ' ' and check_winner() is None:
        board[i][j] = 'X'
        buttons[i][j].config(text='X', state=tk.DISABLED, fg="blue")

        if check_winner() == 'X':
            status_label.config(text="🎉 You Win! 🎉")
            disable_all_buttons()
            return

        if is_full():
            status_label.config(text="🤝 It's a Draw! 🤝")
            return

        # AI's turn
        ai_move = best_move()
        if ai_move:
            board[ai_move[0]][ai_move[1]] = 'O'
            buttons[ai_move[0]][ai_move[1]].config(text='O', state=tk.DISABLED, fg="red")

        if check_winner() == 'O':
            status_label.config(text="💻 AI Wins! 💻")
            disable_all_buttons()
            return

        if is_full():
            status_label.config(text="🤝 It's a Draw! 🤝")

# Disable all buttons when the game is over
def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

# Function to restart the game
def restart_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state=tk.NORMAL)
    status_label.config(text="Your Turn!")

# Creating the main GUI window
root = tk.Tk()
root.title("Tic-Tac-Toe with AI")

# Create the game board buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i, column=j)

# Status label
status_label = tk.Label(root, text="Your Turn!", font=('Arial', 16))
status_label.grid(row=3, column=0, columnspan=3)

# Restart button
restart_button = tk.Button(root, text="Restart Game", font=('Arial', 14), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3)

# Run the Tkinter main loop
root.mainloop()
