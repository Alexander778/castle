from tkinter import *

from src.components.interfaces.missed_shots_sensor import MissedShotsSensor
from src.components.tanks.computer_tank import ComputerTank
from src.components.tanks.user_tank import UserTank
from src.components.utilities.air_defense import AirDefense
from src.components.utilities.movable_wall import MovableWall
from src.components.utilities.radars import Radars
from src.components.utilities.wall import Wall
from src.components.utilities.radar import Radar
from src.components.utilities.repairing_key import RepairingKey

#root
root = Tk()

# Screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.state('zoomed')
root.resizable(False, False)

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width, height=screen_height)
canvas.grid(column=0, row=0)

# Storages
falling_letters = []

# Radars
radars = Radars(canvas, screen_width, screen_height)

# Wall
wall = Wall(canvas, screen_width, screen_height)

# Air defence
air_defense = AirDefense(canvas, screen_width, screen_height)

# Divider lines
canvas.create_line(0, 50, screen_width - 10, 50, width=1)
canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

# Tool panel
tool_panel = canvas.create_rectangle(screen_width / 2 - 100, screen_height - 60,
                                     screen_width / 2 + 300, screen_height - 35,
                                     fill="green")
# Repairing
repairing_key = RepairingKey(canvas, screen_width, screen_height, tool_panel)

# Movable wall
movable_wall = MovableWall(canvas, tool_panel)

# Missed shots sensor
sensor = MissedShotsSensor(canvas, screen_width, screen_height)

# Tanks
computer_tank = ComputerTank(canvas, screen_width, screen_height)
user_tank = UserTank(canvas, screen_width, screen_height, sensor)

# Binders
root.after(1000, computer_tank.move_to_new_position(), None)

root.bind("<Left>", user_tank.move_tank_left)
root.bind("<Right>", user_tank.move_tank_right)
root.bind("<Key>", user_tank.shot_letter)
root.bind("<KeyPress-Up>", user_tank.show_sight)
root.bind("<KeyRelease-Up>", user_tank.hide_sight)

canvas.tag_bind(tagOrId="draggable", sequence="<ButtonPress-1>", func=repairing_key.on_drag_start)
canvas.tag_bind(tagOrId="draggable", sequence="<B1-Motion>", func=repairing_key.on_drag_move)
canvas.tag_bind(tagOrId="draggable", sequence="<ButtonRelease-1>", func=repairing_key.on_drag_release)

canvas.tag_bind(tagOrId="drag_movable_wall", sequence="<ButtonPress-1>", func=movable_wall.on_drag_start)
canvas.tag_bind(tagOrId="drag_movable_wall", sequence="<B1-Motion>", func=movable_wall.on_drag_move)
canvas.tag_bind(tagOrId="drag_movable_wall", sequence="<ButtonRelease-1>", func=movable_wall.on_drag_release)

root.mainloop()