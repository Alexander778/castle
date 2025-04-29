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
from src.states.state import State


class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = None
        self.wall = None
        self.is_pause = False
        self.pause_button = None
        self.pause_overlay = None

        self.air_defense_left_rocket_add_btn = None
        self.air_defense_right_rocket_add_btn = None

    def start_game(self, root, screen_width, screen_height):
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        MissedShotsSensor(self.canvas, screen_width, screen_height)
        PointsSensor(self.canvas, screen_width, screen_height)

        Explosion(self.canvas)
        Radars(self.canvas, screen_width, screen_height)
        self.wall = Wall(self.canvas, screen_width, screen_height)

        air_defense = AirDefense(self.canvas, screen_width, screen_height)

        self.canvas.create_rectangle(5, screen_height - 165,
                                                  screen_width - 10, screen_height - 140,
                                                  fill="lightgray")

        self.canvas.create_line(0, 50, screen_width - 10, 50, width=1)
        self.canvas.create_line(0, screen_height - 80, screen_width - 10, screen_height - 80, width=1)

        tool_panel = self.canvas.create_rectangle(250, screen_height - 75,
                                             400, screen_height - 30,
                                             fill="lightgray")

        self.pause_button = tk.Button(self, text="Pause", font=("Arial", 14, "bold"), command=self.on_pause)
        self.pause_button.place(x=screen_width - 100, y=screen_height - 75)

        medicine_pack = MedicinePack(self.canvas, screen_width, screen_height, tool_panel)
        movable_wall = MovableWall(self.canvas, screen_width, screen_height, tool_panel)

        computer_tank = ComputerTank(self.canvas, screen_width, screen_height)
        user_tank = UserTank(self.canvas, screen_width, screen_height)

        # Left button for adding air defense rocket
        self.air_defense_left_rocket_add_btn = tk.Button(self, text="+", font=("Arial", 14, "bold"),
                                                         command=air_defense.left_device.setup_rocket)
        self.air_defense_left_rocket_add_btn.place(x=32, y=screen_height - 162, height=20, width=20)

        # Right button for adding air defense rocket
        self.air_defense_right_rocket_add_btn = tk.Button(self, text="+", font=("Arial", 14, "bold"),
                                                          command=air_defense.right_device.setup_rocket)
        self.air_defense_right_rocket_add_btn.place(x=screen_width - 65, y=screen_height - 162, height=20, width=20)

        root.after(100, computer_tank.move_to_new_position)

        root.bind("<Left>", user_tank.move_tank_left)
        root.bind("<Right>", user_tank.move_tank_right)
        root.bind("<Key>", user_tank.shot_letter)
        root.bind("<KeyPress-Up>", user_tank.show_sight)
        root.bind("<KeyRelease-Up>", user_tank.hide_sight)

        self.canvas.tag_bind("drag_medicine_pack", "<ButtonPress-1>", medicine_pack.on_drag_start)
        self.canvas.tag_bind("drag_medicine_pack", "<B1-Motion>", medicine_pack.on_drag_move)
        self.canvas.tag_bind("drag_medicine_pack", "<ButtonRelease-1>", medicine_pack.on_drag_release)

        self.canvas.tag_bind("drag_movable_wall", "<ButtonPress-1>", movable_wall.on_drag_start)
        self.canvas.tag_bind("drag_movable_wall", "<B1-Motion>", movable_wall.on_drag_move)
        self.canvas.tag_bind("drag_movable_wall", "<ButtonRelease-1>", movable_wall.on_drag_release)

    def on_pause(self):
        self.is_pause = not self.is_pause
        self.pause_button.config(text="Resume" if self.is_pause else "Pause")
        State().append("pause_game", self.is_pause)

        if self.is_pause:
            self.show_pause_overlay()
        else:
            self.hide_pause_overlay()

    def show_pause_overlay(self):
        self.pause_overlay = tk.Frame(self.canvas, bg='black', width=self.canvas.winfo_width(),
                                      height=self.canvas.winfo_height())
        self.pause_overlay.place(relx=0.5, rely=0.5, anchor='center')
        self.pause_overlay.attributes = {}

        pause_label = tk.Label(self.pause_overlay, text="Game Paused", font=("Arial", 40), fg="white", bg="black")
        pause_label.pack(expand=True)

        self.pause_overlay.lift()  # Bring it to the front

    def hide_pause_overlay(self):
        if hasattr(self, 'pause_overlay') and self.pause_overlay:
            self.pause_overlay.destroy()
            self.pause_overlay = None