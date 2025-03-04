from tkinter import *
from src.components.tanks.computer_tank import ComputerTank
from src.components.tanks.user_tank import UserTank
from src.components.utilities.wall import Wall
from src.components.utilities.radar import Radar
from src.components.utilities.repairing_key import RepairingKey

#root
root = Tk()

# Screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 150
root.geometry(f"{screen_width}x{screen_height}")

# Globals
falling_letters = []
air_defenses = []

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width, height=screen_height)
canvas.grid(column=0, row=0)

# Divider lines
canvas.create_line(0, 50, screen_width - 10, 50, width=1)
canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

# Tool panel
tool_panel = canvas.create_rectangle(screen_width / 2 - 100, screen_height - 30,
                                     screen_width / 2 + 300, screen_height - 75,
                                     fill="lightgreen")
# Tanks
computer_tank = ComputerTank(canvas, screen_width, screen_height)
user_tank = UserTank(canvas, screen_width, screen_height)

# Wall
wall = Wall(canvas, screen_width, screen_height)

# Repairing
repairing_key = RepairingKey(canvas, screen_width, screen_height, wall.cells)

# Radars
radars = [
    Radar(canvas, screen_width, screen_height, 1).radar,
    Radar(canvas, screen_width, screen_height, 2).radar,
    Radar(canvas, screen_width, screen_height, 3).radar,
    Radar(canvas, screen_width, screen_height, 4).radar
]

# Air defence
def create_air_defense():
    small_air_defence = canvas.create_rectangle(50, screen_height - 190, 80, screen_height - 210, fill='white', outline="blue")
    big_air_defence = canvas.create_rectangle(screen_width - 20, screen_height - 190, screen_width - 40, screen_height - 210, fill='white', outline="red")

    small_rocket = canvas.create_rectangle(18, screen_height - 195, 22, screen_height - 205, fill='blue', outline="black")
    big_rocket = canvas.create_rectangle(screen_width - 33, screen_height - 195, screen_width - 27, screen_height - 205, fill='red', outline="black")

    air_defenses.append({ "item": small_air_defence, "hp": 2, "rocket": small_rocket})
    air_defenses.append({ "item": big_air_defence, "hp": 2, "rocket": big_rocket })

create_air_defense()

def move_small_rocket(letter):
    small_rocket = air_defenses[0].rocket

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
    big_rocket = air_defenses[1].rocket

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
root.after(1000, computer_tank.move_to_new_position())

root.bind("<Left>", user_tank.move_tank_left)
root.bind("<Right>", user_tank.move_tank_right)
root.bind("<Key>", user_tank.shot_letter)
root.bind("<KeyPress-Up>", user_tank.show_sight)
root.bind("<KeyRelease-Up>", user_tank.hide_sight)

canvas.tag_bind(tagOrId="draggable", sequence="<ButtonPress-1>", func=repairing_key.on_drag_start)
canvas.tag_bind(tagOrId="draggable", sequence="<B1-Motion>", func=repairing_key.on_drag_move)
canvas.tag_bind(tagOrId="draggable", sequence="<ButtonRelease-1>", func=repairing_key.on_drag_release)

root.mainloop()