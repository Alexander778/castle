from PIL import Image, ImageTk

class BigExplosion:
    _image = None

    def __init__(self, canvas):
        self.canvas = canvas

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        if BigExplosion._image is None:
            BigExplosion._image = ImageTk.PhotoImage(
                Image.open("assets/effects/big_explosion.png")
            )

    def show(self, x, y, disappear_after_ms = 600):
        image_id = self.canvas.create_image(x, y, image=BigExplosion._image)
        self.canvas.after(disappear_after_ms, lambda: self.canvas.delete(image_id))