from PIL import Image, ImageTk

class Damage:
    _image = None

    def __init__(self, canvas):
        self.canvas = canvas

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        if Damage._image is None:
            Damage._image = ImageTk.PhotoImage(
                Image.open("C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/damage.png") # TODO replace with relative path
            )

    def show(self, x, y, is_disappear = False):
        image_id = self.canvas.create_image(x, y, image=Damage._image)

        if is_disappear:
            self.canvas.after(0, lambda: self.canvas.delete(image_id))