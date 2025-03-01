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
radars = []
small_rocket = ""
big_rocket = ""

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

    # listeners for air defence
    canvas.tag_bind(letter, "<Button-1>", lambda event: left_mouse_click(event, letter, is_uppercase))
    canvas.tag_bind(letter, "<Button-3>", lambda event: right_mouse_click(event, letter, is_uppercase))

    falling_letters.append(letter)
    move_failing_letter(letter)

def move_failing_letter(letter):
    letter_x, letter_y = canvas.coords(letter)

    # hit the radar
    for radar in radars:
        if radar["hp"] != 0:
            radar_x, radar_y, _, _ = canvas.coords(radar["radar"])

            if abs(letter_x - radar_x) <= 100 and abs(letter_y - radar_y) < 15:
                damaged_radar = radar["radar"]
                radar["hp"] -= 1

                if radar["hp"] == 0:
                    canvas.delete(damaged_radar)
                if radar["hp"] == 1:
                    canvas.itemconfig(damaged_radar, fill="yellow")

                canvas.delete(letter)
                falling_letters.remove(letter)
                return

    # hit the wall
    for wall_cell in wall_cells:
        wall_cell_x, wall_cell_y, _, _ = canvas.coords(wall_cell)

        if abs(letter_x - wall_cell_x) < 15 and abs(letter_y - wall_cell_y) < 15:
            canvas.delete(wall_cell)
            wall_cells.remove(wall_cell)

            canvas.delete(letter)
            falling_letters.remove(letter)
            return

    if abs(letter_y - screen_height) < 100:
        canvas.delete(letter)
        falling_letters.remove(letter)
    else:
        canvas.move(letter, 0, 10)
        canvas.after(500, move_failing_letter, letter)

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
        if canvas.itemcget(fired_letter, "text") == canvas.itemcget(falling_letter, "text"):
            if abs(current_x - falling_x) < 20 and abs(current_y - falling_y) < 20:
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
    user_tank_x0 = canvas.coords(user_tank)[0]
    user_tank_y0 = canvas.coords(user_tank)[1]
    user_tank_x1 = canvas.coords(user_tank)[3]

    line_top_y1 = screen_height * 0.09

    # check status of the nearest radar
    for radar in radars:
        radar_range_start, radar_range_end = radar["action_range"]

        if user_tank_x0 >= radar_range_start and user_tank_x1 <= radar_range_end:
            radar_hp = radar["hp"]

            if radar_hp == 2:
                print("full line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))

            elif radar_hp == 1:
                line_top_y1 = screen_height / 2
                print("divided line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))
            else:
                print("no line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))
                return

    global sight_line
    sight_line = canvas.create_line(user_tank_x0 + 50,
                                    user_tank_y0 - 60,
                                    user_tank_x0 + 50,
                                    line_top_y1,
                                    width=1,
                                    dash=(1, 1))

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

        top_block = canvas.create_rectangle(current_x0, top_y0, current_x1, screen_height - 165, fill='orange', outline='black')
        middle_block = canvas.create_rectangle(current_x0, middle_y0, current_x1, screen_height - 150, fill='orange', outline='black')
        bottom_block = canvas.create_rectangle(current_x0, bottom_y0, current_x1, screen_height - 135, fill='orange', outline='black')

        wall_cells.append(top_block)
        wall_cells.append(middle_block)
        wall_cells.append(bottom_block)

        current_x0 += 15
        current_x1 += 15
create_wall()

# Radars
def create_radars():
    radar_block = screen_width / 4

    initial_x0 = radar_block / 2.5
    initial_x1 = initial_x0 + 100

    for x in range(4):
        new_radar = canvas.create_rectangle(initial_x0, screen_height - 200, initial_x1, screen_height - 185, fill="lightgreen")

        range_x0 = radar_block * x
        range_x1 = radar_block + range_x0

        global radars
        radars.append({
            "radar": new_radar,
            "action_range": [
                range_x0,
                range_x1
            ],
            "hp": 2
        })

        canvas.create_text(range_x0, screen_height - 50,  text=range_x0)
        canvas.create_text(range_x1, screen_height - 50, text=range_x1)

        initial_x0 += 480
        initial_x1 += 480

create_radars()

# Air defence
def create_air_defense():
    small_air_defence = canvas.create_rectangle(10, screen_height - 190, 30, screen_height - 210, fill='white', outline="blue")
    big_air_defence = canvas.create_rectangle(screen_width - 20, screen_height - 190, screen_width - 40, screen_height - 210, fill='white', outline="red")

    #setup rockets
    global small_rocket
    global big_rocket

    small_rocket = canvas.create_rectangle(18, screen_height - 195, 22, screen_height - 205, fill='blue', outline="black")
    big_rocket = canvas.create_rectangle(screen_width - 33, screen_height - 195, screen_width - 27, screen_height - 205, fill='red', outline="black")

create_air_defense()

def move_small_rocket(letter):
    global small_rocket

    letter_x, letter_y = canvas.coords(letter)
    small_rocket_x, small_rocket_y, _, _ = canvas.coords(small_rocket)

    if abs(small_rocket_x - letter_x) < 10 and abs(small_rocket_y - letter_y) < 10:
        canvas.delete(small_rocket)
        canvas.delete(letter)
        falling_letters.remove(letter)
        return

    if small_rocket_y < 10:
        canvas.delete(small_rocket)
    else:
        step_x = 10 if small_rocket_x < letter_x else -10  # Move 10 pixels towards the letter in X direction
        step_y = -10 if small_rocket_y > letter_y else 10  # Move 10 pixels towards the letter in Y direction

        canvas.move(small_rocket, step_x, step_y)
        canvas.after(100, move_small_rocket, letter)
def move_big_rocket(letter):
    global big_rocket

    letter_x, letter_y = canvas.coords(letter)
    big_rocket_x, big_rocket_y, _, _ = canvas.coords(big_rocket)

    if abs(big_rocket_x - letter_x) < 10 and abs(big_rocket_y - letter_y) < 10:
        canvas.delete(big_rocket)
        canvas.delete(letter)
        falling_letters.remove(letter)
        return

    if big_rocket_y < 10:
        canvas.delete(big_rocket)
    else:
        step_x = 10 if big_rocket_x < letter_x else -10  # Move 10 pixels towards the letter in X direction
        step_y = -10 if big_rocket_y > letter_y else 10  # Move 10 pixels towards the letter in Y direction

        canvas.move(big_rocket, step_x, step_y)
        canvas.after(100, move_big_rocket, letter)

def left_mouse_click(event, letter, is_uppercase):
    if is_uppercase is not True:
        move_small_rocket(letter)

def right_mouse_click(event, letter, is_uppercase):
    if is_uppercase:
        move_big_rocket(letter)

# Binders
root.after(1000, move_tank)
root.bind("<Left>", move_tank_left)
root.bind("<Right>", move_tank_right)
root.bind("<KeyPress-Up>", show_sight)
root.bind("<KeyRelease-Up>", hide_sight)
root.bind("<Key>", fire_letter)
root.mainloop()