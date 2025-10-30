#!/usr/bin/env python3
"""
tictactoe_gui.py
Tkinter-based Tic-Tac-Toe with buttons.
Options:
 - Human vs Human
 - Human vs AI (Minimax)
Usage:
    python tictactoe_gui.py
"""

import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.resizable(False, False)
        self.board = [' '] * 9
        self.buttons = []
        self.current = 'X'
        self.human_is = 'X'
        self.ai_is = 'O'
        self.vs_ai = tk.BooleanVar(value=True)

        top = tk.Frame(self)
        top.pack(padx=10, pady=6)

        mode_frame = tk.Frame(top)
        mode_frame.pack(side=tk.LEFT, padx=6)
        tk.Label(mode_frame, text="Mode:").pack(anchor='w')
        tk.Radiobutton(mode_frame, text="Human vs AI", variable=self.vs_ai, value=True).pack(anchor='w')
        tk.Radiobutton(mode_frame, text="Human vs Human", variable=self.vs_ai, value=False).pack(anchor='w')

        control_frame = tk.Frame(top)
        control_frame.pack(side=tk.RIGHT, padx=6)
        tk.Button(control_frame, text="New Game", command=self.new_game).pack(fill='x')
        tk.Button(control_frame, text="Switch Sides", command=self.switch_sides).pack(fill='x', pady=(6,0))

        board_frame = tk.Frame(self)
        board_frame.pack(padx=10, pady=10)
        for i in range(9):
            b = tk.Button(board_frame, text=' ', width=6, height=3, font=('Helvetica', 20),
                          command=lambda idx=i: self.on_click(idx))
            b.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(b)

        self.status = tk.Label(self, text="X to move", anchor='w')
        self.status.pack(fill='x', padx=10, pady=(0,10))

        self.new_game()

    def switch_sides(self):
        # Switch which symbol human uses when vs AI
        self.human_is, self.ai_is = self.ai_is, self.human_is
        messagebox.showinfo("Switch Sides", f"You are now {self.human_is}.")
        self.new_game()

    def new_game(self):
        self.board = [' '] * 9
        self.current = 'X'
        for b in self.buttons:
            b.config(text=' ', state=tk.NORMAL)
        self.update_status()
        # If AI plays first and mode selected:
        self.after(100, self.maybe_ai_move)

    def update_status(self, text=None):
        if text:
            self.status.config(text=text)
        else:
            self.status.config(text=f"{self.current} to move")

    def on_click(self, idx):
        if self.board[idx] != ' ':
            return
        # If vs AI and it's human's turn, ensure symbol matches
        self.board[idx] = self.current
        self.buttons[idx].config(text=self.current)
        self.buttons[idx].config(state=tk.DISABLED)
        self.check_game_over()
        if self.is_game_over():
            return
        self.current = 'O' if self.current == 'X' else 'X'
        self.update_status()
        self.after(150, self.maybe_ai_move)

    def is_game_over(self):
        return winner(self.board) is not None

    def maybe_ai_move(self):
        if not self.vs_ai.get():
            return
        # If mode is vs AI and it's AI's turn:
        if self.current == self.ai_is:
            move = ai_move(self.board, self.ai_is, self.human_is)
            if move is not None:
                self.board[move] = self.ai_is
                self.buttons[move].config(text=self.ai_is)
                self.buttons[move].config(state=tk.DISABLED)
                self.check_game_over()
                if not self.is_game_over():
                    self.current = self.human_is
                    self.update_status()

    def check_game_over(self):
        w = winner(self.board)
        if w is not None:
            if w == 'Tie':
                self.update_status("It's a tie!")
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                self.update_status(f"{w} wins!")
                messagebox.showinfo("Game Over", f"Player {w} wins!")
            for b in self.buttons:
                b.config(state=tk.DISABLED)

# Shared helper functions (same logic as CLI)

def winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Tie'
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if v == ' ']

def minimax(board, current_player, ai_player, human_player):
    res = winner(board)
    if res == ai_player:
        return (1, None)
    elif res == human_player:
        return (-1, None)
    elif res == 'Tie':
        return (0, None)

    if current_player == ai_player:
        best_score = -math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = ai_player
            score, _ = minimax(board, human_player, ai_player, human_player)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)
    else:
        best_score = math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = human_player
            score, _ = minimax(board, ai_player, ai_player, human_player)
            board[move] = ' '
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)

def ai_move(board, ai_player, human_player):
    moves = available_moves(board)
    if not moves:
        return None
    # Random opening to avoid deterministic first move always same
    if len(moves) == 9:
        return random.choice(moves)
    _, move = minimax(board, ai_player, ai_player, human_player)
    return move

if __name__ == '__main__':
    app = TicTacToeGUI()
    app.mainloop()
