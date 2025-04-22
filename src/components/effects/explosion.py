from PIL import Image, ImageTk

class Explosion:
    _explosion_image = None

    def __init__(self, canvas):
        self.canvas = canvas

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        if Explosion._explosion_image is None:
            Explosion._explosion_image = ImageTk.PhotoImage(
                Image.open("../assets/effects/explosion.png")
            )

    def show(self, x, y, disappear_after_ms = 600):
        image_id = self.canvas.create_image(x, y, image=Explosion._explosion_image)
        self.canvas.after(disappear_after_ms, lambda: self.canvas.delete(image_id))