from tkinter import *
from src.pages.game_page import GamePage
from src.pages.start_page import StartPage

#root
root = Tk()

# Screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("The Castle")
root.geometry("800x600")
root.resizable(False, False)

# Container for "pages"
container = Frame(root)
container.pack(fill="both", expand=True)

# Page instances
game_page = GamePage(container)
start_page = StartPage(container, show_game_callback=lambda u, d: switch_to(game_page, u, d))
def switch_to(page, username=None, difficulty=None):
    start_page.pack_forget()
    game_page.pack_forget()

    if isinstance(page, GamePage) and username and difficulty:
        root.state("normal")
        page.start_game(root, screen_width, screen_height - 50)
        root.geometry(f"{screen_width}x{screen_height - 50}")
        root.resizable(True, True)
    else:
        root.state("zoomed")
        root.resizable(False, False)
    page.pack(fill="both", expand=True)

# Show start page by default
start_page.pack(fill="both", expand=True)

root.mainloop()