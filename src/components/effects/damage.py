from PIL import Image, ImageTk

class Damage:
    _image = None

    def __init__(self, canvas):
        self.canvas = canvas

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        if Damage._image is None:
            Damage._image = ImageTk.PhotoImage(Image.open("../assets/effects/damage.png"))

    def show(self, x, y):
        return self.canvas.create_image(x, y, image=Damage._image)

    def hide(self, image_id):
        self.canvas.after(0, lambda: self.canvas.delete(image_id))