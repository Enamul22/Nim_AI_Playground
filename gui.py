import tkinter as tk
from tkinter import simpledialog, messagebox
from nim import Nim, train

class NimGUI:
    def __init__(self, master):
        self.master = master
        master.title("Nim Game")

        self.nim = Nim()
        self.ai = train(10000)  # Train the AI for 10,000 games

        # Create a label to display instructions and the current player
        self.label = tk.Label(master, text="Your Turn", height=2)
        self.label.pack()

        # Label to display the last move made
        self.last_move_label = tk.Label(master, text="", height=2)
        self.last_move_label.pack()

        # Create a frame to hold the pile buttons
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Create buttons for each pile
        self.pile_buttons = []
        for i, pile in enumerate(self.nim.piles):
            button = tk.Button(self.frame, text=f'Pile {i}: {pile}', command=lambda i=i: self.remove_items(i))
            button.pack(side=tk.LEFT)
            self.pile_buttons.append(button)

        # Restart button
        self.restart_button = tk.Button(master, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()

    def remove_items(self, pile):
        if self.nim.winner is not None:
            messagebox.showinfo("Game Over", "The game has already ended. Please restart the game.")
            return

        count = simpledialog.askinteger("Choose Count", f"How many to remove from pile {pile}?", parent=self.master, minvalue=1, maxvalue=self.nim.piles[pile])
        if count is None:  # The user cancelled the input dialog
            return

        # Make the player's move
        self.nim.move((pile, count))
        self.update_piles()

        # Check if the game has ended
        if self.nim.winner is not None:
            self.end_game()
            return

        # AI's turn
        self.label.config(text="AI's Turn")
        self.master.update_idletasks()

        ai_action = self.ai.choose_action(self.nim.piles, epsilon=False)
        self.nim.move(ai_action)
        self.last_move_label.config(text=f"AI removed {ai_action[1]} from pile {ai_action[0]}")
        self.update_piles()

        # Check if the game has ended again
        if self.nim.winner is not None:
            self.end_game()
            return

        self.label.config(text="Your Turn")
        self.master.update_idletasks()

    def update_piles(self):
        for i, pile in enumerate(self.nim.piles):
            self.pile_buttons[i].config(text=f'Pile {i}: {pile}')

    def end_game(self):
        winner = "You" if self.nim.winner == 0 else "AI"
        self.last_move_label.config(text=f"{winner} won the game!")
        messagebox.showinfo("Game Over", f"{winner} won the game!")
        self.label.config(text=f"{winner} won the game!")

    def restart_game(self):
        self.nim = Nim()  # Reset the game state
        self.ai = train(10000)  # Retrain the AI
        self.update_piles()
        self.label.config(text="Your Turn")
        self.last_move_label.config(text="")

def main():
    root = tk.Tk()
    gui = NimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
