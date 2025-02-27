import random
from tkinter import *
import random

#root
root = Tk()

# Constants
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Fullscreen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 150
root.geometry(f"{screen_width}x{screen_height}")

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width, height=screen_height)
canvas.grid(column=0, row=0)

# Top line drawing
canvas.create_line(0, 50, screen_width - 10, 50, width=1)

# Computer tank
computer_tank = canvas.create_rectangle(0, 10, 100, 40, fill='gray')

# Computer tank movement
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

# Computer tank letter funcs
def shot_letter():
    current_x = canvas.coords(computer_tank)[0]
    is_uppercase = random.choice([True, False])
    letter_symbol = random.choice(alphabet)
    letter_symbol_color = "#0000FF" # small letter color

    if is_uppercase:
        letter_symbol = letter_symbol.upper()
        letter_symbol_color = "#FF0000" # big letter color

    # make letter coordinate dynamic, not hardcoded
    letter = canvas.create_text(current_x + 50, 60, text=letter_symbol, fill=letter_symbol_color)
    move_letter(letter)

def move_letter(letter):
    _, current_y = canvas.coords(letter)

    if abs(current_y - screen_height) < 10:
        canvas.delete(letter)
    else:
        canvas.move(letter, 0, 10)
        canvas.after(100, move_letter, letter)

# User tank
user_tank = canvas.create_rectangle(screen_width / 2, screen_height - 130, screen_width / 2 + 100, screen_height - 85, fill='brown')

def move_tank_left(event):
    user_tank_x = canvas.coords(user_tank)[0]

    if user_tank_x == 0:
        return

    canvas.move(user_tank, -10, 0)
def move_tank_right(event):
    user_tank_x = canvas.coords(user_tank)[0]

    if user_tank_x == screen_width - 100:
        return

    canvas.move(user_tank, 10, 0)
def fire_letter(event):
    letter = event.char
    letter_symbol_color = "#0000FF"  # small letter color

    if letter.isupper():
        letter_symbol_color = "#FF0000"  # big letter color

    current_x = canvas.coords(user_tank)[0]
    current_y= canvas.coords(user_tank)[1]

    letter = canvas.create_text(current_x + 50, current_y - 10, text=letter, fill=letter_symbol_color)
    move_fired_letter(letter)

def move_fired_letter(letter):
    _, current_y = canvas.coords(letter)

    if current_y < 10:
        canvas.delete(letter)
    else:
        canvas.move(letter, 0, -10)
        canvas.after(100, move_fired_letter, letter)

# User panel line
canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

root.after(1000, move_tank)
root.bind("<Left>", move_tank_left)
root.bind("<Right>", move_tank_right)
root.bind("<Key>", fire_letter)
root.mainloop()