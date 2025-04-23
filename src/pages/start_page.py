import tkinter as tk

from src.states.state import State


class StartPage(tk.Frame):
    def __init__(self, parent, show_game_callback):
        super().__init__(parent)
        self.configure(bg="lightblue")
        self.show_game_callback = show_game_callback
        self.load_game_callback = show_game_callback #load_game_callback

        tk.Label(self, text="🏰 Welcome to The Castle 🏰", font=("Arial", 32, "bold"), bg="lightblue").pack(pady=40)

        # Username
        tk.Label(self, text="Enter your name:", font=("Arial", 16), bg="lightblue").pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        # --- New Game Section ---
        tk.Label(self, text="Start a New Game:", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=(30, 10))

        self.difficulty = tk.StringVar(value="Medium")
        difficulties = ["Easy", "Medium", "Hard"]

        for level in difficulties:
            tk.Radiobutton(self, text=level, variable=self.difficulty, value=level, bg="lightblue",
                           font=("Arial", 14)).pack()

        tk.Button(self, text="Start Game", font=("Arial", 14, "bold"),
                  command=self.on_start).pack(pady=20)

        # --- Upload Saved Game Section ---
        tk.Label(self, text="Or", font=("Arial", 14, "italic"), bg="lightblue").pack(pady=10)

        tk.Button(self, text="Upload Saved Game", font=("Arial", 14),
                  command=self.on_start).pack()

    def on_start(self):
        username = self.username_entry.get()
        difficulty = self.difficulty.get()

        State().append("difficulty", difficulty.lower())

        if not username.strip():
            #tk.Message.showwarning("Input Required", "Please enter your name.")
            return

        # Call main screen with collected data
        self.show_game_callback(username, difficulty)
