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

# Globals
falling_letters = []
wall_cells = []

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
    falling_letters.append(letter)
    move_letter(letter)

def find_closest_tuple(arr, target1, target2):
    return min(arr, key=lambda x: abs(x[0] - target1) + abs(x[1] - target2))

def move_letter(letter):
    current_x, current_y = canvas.coords(letter)

    for wall_cell in wall_cells:
        wall_cell_x, wall_cell_y, _, _ = canvas.coords(wall_cell)

        if abs(current_x - wall_cell_x) < 15 and abs(current_y - wall_cell_y) < 15:
            canvas.delete(wall_cell)
            wall_cells.remove(wall_cell)

            canvas.delete(letter)
            falling_letters.remove(letter)
            return

    if abs(current_y - screen_height) < 100:
        canvas.delete(letter)
        falling_letters.remove(letter)
    else:
        canvas.move(letter, 0, 10)
        canvas.after(200, move_letter, letter)

# User tank
user_tank = canvas.create_rectangle(screen_width / 2, screen_height - 130, screen_width / 2 + 100, screen_height - 85, fill='brown')

def move_tank_left(event):
    user_tank_x = canvas.coords(user_tank)[0]

    if user_tank_x > 0:
        canvas.move(user_tank, -10, 0)

def move_tank_right(event):
    user_tank_x = canvas.coords(user_tank)[0]

    if user_tank_x < screen_width - 100:
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
def move_fired_letter(fired_letter):
    current_x, current_y = canvas.coords(fired_letter)

    for falling_letter in falling_letters:
        falling_x, falling_y = canvas.coords(falling_letter)
        if abs(current_x - falling_x) < 20 and abs(current_y - falling_y) < 20:
            if canvas.itemcget(fired_letter, "text") == canvas.itemcget(falling_letter, "text"):
                canvas.delete(fired_letter)
                canvas.delete(falling_letter)
                falling_letters.remove(falling_letter)
                return

    if current_y < 10:
        canvas.delete(fired_letter)
    else:
        canvas.move(fired_letter, 0, -10)
        canvas.after(100, move_fired_letter, fired_letter)

#Sight
sight_line = ""
def show_sight(event):
    print("show_sight")
    current_x = canvas.coords(user_tank)[0]
    current_y = canvas.coords(user_tank)[1]

    global sight_line
    sight_line = canvas.create_line(current_x + 50, current_y - 10, current_x + 50, 55, width=1, dash=(1, 1))

def hide_sight(event):
    global sight_line
    canvas.delete(sight_line)

# User panel line
canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

# Wall
def create_wall():
    max_x1 = screen_width - 10
    current_x0 = 5
    current_x1 = 20

    while current_x1 <= max_x1:
        global wall_cells

        top_y0 = screen_height - 180
        middle_y0 = screen_height - 165
        bottom_y0 = screen_height - 150

        top_block = canvas.create_rectangle(current_x0, top_y0, current_x1, screen_height - 165, fill='red')
        middle_block = canvas.create_rectangle(current_x0, middle_y0, current_x1, screen_height - 150, fill='yellow')
        bottom_block = canvas.create_rectangle(current_x0, bottom_y0, current_x1, screen_height - 135, fill='green')

        wall_cells.append(top_block)
        wall_cells.append(middle_block)
        wall_cells.append(bottom_block)

        current_x0 += 15
        current_x1 += 15

create_wall()

root.after(1000, move_tank)

# Binders
root.bind("<Left>", move_tank_left)
root.bind("<Right>", move_tank_right)
root.bind("<KeyPress-Up>", show_sight)
root.bind("<KeyRelease-Up>", hide_sight)
root.bind("<Key>", fire_letter)

root.mainloop()