from tkinter import *

from src.components.storage.air_defense_storage import AirDefenseStorage
from src.components.storage.falling_letter_storage import FallingLetterStorage
from src.components.storage.radar_storage import RadarStorage
from src.components.storage.wall_storage import WallStorage
from src.components.tanks.computer_tank import ComputerTank
from src.components.tanks.user_tank import UserTank
from src.components.utilities.air_defense_device import AirDefenseDevice
from src.components.utilities.wall import Wall
from src.components.utilities.radar import Radar
from src.components.utilities.repairing_key import RepairingKey
from src.constants import small_letter_color, big_letter_color

#root
root = Tk()

# Screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 150
root.geometry(f"{screen_width}x{screen_height}")

#Canvas
canvas = Canvas(root)
canvas.config(width=screen_width, height=screen_height)
canvas.grid(column=0, row=0)

# Storages
letter_storage = FallingLetterStorage()

radar_storage = RadarStorage()
radar_storage.append_range([
    Radar(canvas, screen_width, screen_height, 1),
    Radar(canvas, screen_width, screen_height, 2),
    Radar(canvas, screen_width, screen_height, 3),
    Radar(canvas, screen_width, screen_height, 4)
])

wall_storage = WallStorage()
wall = Wall(canvas, screen_width, screen_height)
wall_storage.append_range(wall.cells)

# Air defence
air_defense_storage = AirDefenseStorage()
air_defense_storage.append_range([
    AirDefenseDevice(canvas,
                     coordinates=(screen_width - 20, screen_height - 190, screen_width - 40, screen_height - 210),
                     colors={ "fill": "white", "outline": big_letter_color }),
    AirDefenseDevice(canvas,
                     coordinates=(50, screen_height - 190, 80, screen_height - 210),
                     colors={ "fill": "white", "outline": small_letter_color })
])

# Divider lines
canvas.create_line(0, 50, screen_width - 10, 50, width=1)
canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

# Tool panel
tool_panel = canvas.create_rectangle(screen_width / 2 - 100, screen_height - 30,
                                     screen_width / 2 + 300, screen_height - 75,
                                     fill="lightgreen")
# Repairing
repairing_key = RepairingKey(canvas, screen_width, screen_height)

# Tanks
computer_tank = ComputerTank(canvas, screen_width, screen_height)
user_tank = UserTank(canvas, screen_width, screen_height)

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