import tkinter as tk
from src.components.effects.explosion import Explosion
from src.components.interfaces.missed_shots_sensor import MissedShotsSensor
from src.components.interfaces.points_sensor import PointsSensor
from src.components.tanks.computer_tank import ComputerTank
from src.components.tanks.user_tank import UserTank
from src.components.utilities.air_defense.air_defense import AirDefense
from src.components.utilities.medicine_pack.medicine_pack import MedicinePack
from src.components.utilities.walls.movable_wall import MovableWall
from src.components.utilities.radar.radars import Radars
from src.components.utilities.walls.wall import Wall

class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.wall = None

    def start_game(self, root, screen_width, screen_height):
        canvas = tk.Canvas(self, width=screen_width, height=screen_height)
        canvas.pack(fill="both", expand=True)

        Explosion(canvas)
        Radars(canvas, screen_width, screen_height)
        self.wall = Wall(canvas, screen_width, screen_height)

        canvas.create_rectangle(5, screen_height - 165,
                                                  screen_width - 10, screen_height - 140,
                                                  fill="lightgray")

        AirDefense(canvas, screen_width, screen_height)

        canvas.create_line(0, 50, screen_width - 10, 50, width=1)
        canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

        tool_panel = canvas.create_rectangle(250, screen_height - 75,
                                             400, screen_height - 30,
                                             fill="lightgray")

        medicine_pack = MedicinePack(canvas, screen_width, screen_height, tool_panel)
        movable_wall = MovableWall(canvas, screen_width, screen_height, tool_panel)

        MissedShotsSensor(canvas, screen_width, screen_height)
        PointsSensor(canvas, screen_width, screen_height)

        computer_tank = ComputerTank(canvas, screen_width, screen_height)
        user_tank = UserTank(canvas, screen_width, screen_height)

        root.after(100, computer_tank.move_to_new_position)

        root.bind("<Left>", user_tank.move_tank_left)
        root.bind("<Right>", user_tank.move_tank_right)
        root.bind("<Key>", user_tank.shot_letter)
        root.bind("<KeyPress-Up>", user_tank.show_sight)
        root.bind("<KeyRelease-Up>", user_tank.hide_sight)

        canvas.tag_bind("drag_medicine_pack", "<ButtonPress-1>", medicine_pack.on_drag_start)
        canvas.tag_bind("drag_medicine_pack", "<B1-Motion>", medicine_pack.on_drag_move)
        canvas.tag_bind("drag_medicine_pack", "<ButtonRelease-1>", medicine_pack.on_drag_release)

        canvas.tag_bind("drag_movable_wall", "<ButtonPress-1>", movable_wall.on_drag_start)
        canvas.tag_bind("drag_movable_wall", "<B1-Motion>", movable_wall.on_drag_move)
        canvas.tag_bind("drag_movable_wall", "<ButtonRelease-1>", movable_wall.on_drag_release)
