"""
@Author: ZHHENG.
@Email: 2906023654@qq.com
@DateTime: 2024/9/6 18:53
@FileName: test21.py

"""
import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player_x_score = 0
        self.player_o_score = 0
        self.current_player = 'X'
        self.win_threshold = 4  # 设置胜利阈值为 4

        self.buttons = {}
        self.create_buttons()
        self.create_status_label()

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=' ', font=('Arial', 20), height=3, width=6,
                                   command=lambda i=i, j=j: self.button_click(i, j))
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[(i, j)] = button

    def create_status_label(self):
        self.status_label = tk.Label(self.root, text="", font=('Arial', 20))
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew")

    def button_click(self, i, j):
        if self.buttons[(i, j)]['text'] == ' ':
            self.buttons[(i, j)]['text'] = self.current_player
            if self.check_winner(i, j):
                self.status_label.config(text=f"Player {self.current_player} wins!")
                self.update_score(self.current_player)
                if self.player_x_score == self.win_threshold or self.player_o_score == self.win_threshold:
                    response = messagebox.askyesno("Game Over", f"Player {self.current_player} reaches 4 wins. Play again?")
                    if response:
                        self.reset_game()
                    else:
                        self.root.quit()
                else:
                    self.reset_game()
            elif self.check_draw():
                self.status_label.config(text="Draw!")
                self.reset_game(draw=True)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, i, j):
        player = self.buttons[(i, j)]['text']
        # Check row, column, and diagonals
        if (all(self.buttons[(i, k)]['text'] == player for k in range(3)) or
                all(self.buttons[(k, j)]['text'] == player for k in range(3)) or
                (i == j and all(self.buttons[(k, k)]['text'] == player for k in range(3))) or
                (i + j == 2 and all(self.buttons[(k, 2 - k)]['text'] == player for k in range(3)))):
            return True
        return False

    def check_draw(self):
        return all(self.buttons[(i, j)]['text']!= ' ' for i in range(3) for j in range(3))

    def update_score(self, player):
        if player == 'X':
            self.player_x_score += 1
        else:
            self.player_o_score += 1
        self.status_label.config(text=f"Player X: {self.player_x_score} - Player O: {self.player_o_score}")

    def reset_game(self, draw=False):
        response = messagebox.askyesno("Game Over", "Play again?")
        if response:
            self.reset_board()
        else:
            self.root.quit()

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)]['text'] = ' '
        self.current_player = 'X'
        self.status_label.config(text="")


def main():
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()