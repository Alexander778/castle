import random
from tkinter import *
import random

root = Tk()

# Constants
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Fullscreen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 50
root.geometry(f"{screen_width}x{screen_height}")

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width, height=screen_height)

# Top line drawing
canvas.create_line(0, 50, screen_width - 10, 50, width=1)
canvas.grid(column=0, row=1)

# Computer tank
computer_tank = canvas.create_rectangle(0, 10, 100, 40, fill='gray')
canvas.grid(column=0, row=0)


def move_tank():
    new_x = random.randrange(0, screen_width - 100)
    current_x = int(canvas.coords(computer_tank)[0])

    def animate_tank_movement():
        nonlocal current_x
        if abs(current_x - new_x) < 10:
            shot_letter()
            root.after(2000, move_tank) # move again
            return # Stop moving

        if current_x < new_x:
            canvas.move(computer_tank, 10, 0)
            current_x += 10
        else:
            canvas.move(computer_tank, -10, 0)
            current_x -= 10

        canvas.after(100, animate_tank_movement)

    animate_tank_movement()

def shot_letter():
    current_tank_position_x = canvas.coords(computer_tank)[0]
    is_uppercase = random.choice([True, False])
    letter_symbol = random.choice(alphabet)
    letter_symbol_color = "#0000FF" # small letter color

    if is_uppercase:
        letter_symbol = letter_symbol.upper()
        letter_symbol_color = "#FF0000" # big letter color

    # make letter coordinate dynamic, not hardcoded
    letter = canvas.create_text(current_tank_position_x + 50, 60, text=letter_symbol, fill=letter_symbol_color)
    move_letter(letter)

def move_letter(letter):
    _, current_y = canvas.coords(letter)

    if abs(current_y - screen_height) < 10:
        canvas.delete(letter)
    else:
        canvas.move(letter, 0, 10)
        canvas.after(1000, move_letter, letter)

root.after(1000, move_tank)
root.mainloop()