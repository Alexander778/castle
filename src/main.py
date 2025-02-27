import random
from tkinter import *
from random import *

root = Tk()

# Constants
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Fullscreen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 50
root.geometry(f"{screen_width}x{screen_height}")

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width)

# Top line drawing
canvas.create_line(0, 50, screen_width - 10, 50, width=1)
canvas.grid(column=0, row=1)

# Computer tank
computer_tank = canvas.create_rectangle(0, 10, 100, 40, fill='gray')
canvas.grid(column=0, row=0)


def move_tank():
    new_x = randrange(0, screen_width - 100)
    current_x = int(canvas.coords(computer_tank)[0])

    def animate():
        nonlocal current_x
        if abs(current_x - new_x) < 10:
            root.after(1000, move_tank) # move again
            return # Stop moving

        if current_x < new_x:
            current_x += 10
        else:
            current_x -= 10

        canvas.moveto(computer_tank, x=current_x, y=10)
        canvas.after(100, animate)

    animate()


root.after(1000, move_tank)
root.mainloop()