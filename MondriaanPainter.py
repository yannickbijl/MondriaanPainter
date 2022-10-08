import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
from random import randrange, random


class MondrianPainter:

    def __init__(self):
        self.painter = tk.Tk()
        self.painter.state('normal')
        self.painter.attributes("-fullscreen", True)
        self.set_fixed_settings()
        self.paint_art()


    def set_fixed_settings(self):
        self.WIDTH = self.painter.winfo_screenwidth()
        self.HEIGHT = self.painter.winfo_screenheight()
        self.frame = tk.Canvas(self.painter, width=self.WIDTH, height=self.HEIGHT)
        self.frame.pack()
        self.sub_menu()
        self.painter.bind("<Escape>", self.end_program)
        self.painter.bind("<Button-1>", self.paint_art)
        self.painter.bind("<Button-2>", self.paint_art)
        self.painter.bind("<Button-3>", self.do_popup)

    def sub_menu(self):
        self.submenu = tk.Menu(self.painter, tearoff = 0)
        self.submenu.add_command(label="Save",command=self.save_as_png)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=self.end_program)

    def set_variable_settings(self):
        self.SPLIT_LOW = randrange(100, 250)
        self.SPLIT_PENALTY = randrange(10, 30) / 10
        self.THICKNESS = randrange(3,20)
        self.COLORS = [["red", "blue", "yellow", "white"],
                       ["green", "cyan", "magenta", "white"],
                       ["spring green", "steel blue", "plum", "white"],
                       ["tomato", "turquoise", "gold", "white"],
                       ["dark violet", "dark orange", "dark green", "white"],
                       ["pale turquoise", "pale violet red", "pale green", "white"],
                       ["aquamarine", "peach puff", "light coral", "white"]]
        self.COLORS = self.COLORS[randrange(0, len(self.COLORS))]
        self.COLOR_CHANCE = [randrange(10, 20), randrange(15, 30), randrange(30, 50), randrange(60, 80)]
        self.COLOR_CHANCE = sorted([number / sum(self.COLOR_CHANCE) for number in self.COLOR_CHANCE])


    def end_program(self, event=None):
        self.painter.quit()

    def paint_art(self, event=None):
        self.set_variable_settings()
        self.mondriaan(0, 0, self.WIDTH, self.HEIGHT, self.frame)

    def do_popup(self, event=None):
        try:
            self.submenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.submenu.grab_release()

    def save_as_png(self):
        self.file = filedialog.asksaveasfilename(initialdir="C:/", filetypes=(("PNG File", ".PNG"), ("PNG File", ".png")))
        self.file = self.file + ".png"
        ImageGrab.grab().save(self.file)


    def randomColor(self):
        color_chance = random()
        if color_chance < self.COLOR_CHANCE[0]:
            return self.COLORS[0]
        elif color_chance < self.COLOR_CHANCE[1]:
            return self.COLORS[1]
        elif color_chance < self.COLOR_CHANCE[2]:
            return self.COLORS[2]
        else:
            return self.COLORS[3]

    def split_both(self, x, y, width, height, canvas):
        horizontal_split = randrange(25, 76) / 100
        vertical_split = randrange(25, 76) / 100
        left_width = round(horizontal_split * width)
        right_width = width - left_width
        top_height = round(vertical_split * height)
        bottom_height = height - top_height
        self.mondriaan(x, y, left_width, top_height, canvas)
        self.mondriaan((x + left_width), y, right_width, top_height, canvas)
        self.mondriaan(x, (y + top_height), left_width, bottom_height, canvas)
        self.mondriaan((x + left_width), (y + top_height), right_width, bottom_height, canvas)

    def split_horizontal(self, x, y, width, height, canvas):
        horizontal_split = randrange(25, 76) / 100
        left_width = round(horizontal_split * width)
        right_width = width - left_width
        self.mondriaan(x, y, left_width, height, canvas)
        self.mondriaan((x + left_width), y, right_width, height, canvas)

    def split_vertical(self, x, y, width, height, canvas):
        vertical_split = randrange(25, 76) / 100
        top_height = round(vertical_split * height)
        bottom_height = height - top_height
        self.mondriaan(x, y, width, top_height, canvas)
        self.mondriaan(x, (y + top_height), width, bottom_height, canvas)


    def mondriaan(self, x, y, width, height, canvas):
        # Splits based on the size of the region
        if width > self.WIDTH / 2 and height > self.HEIGHT / 2:
            self.split_both(x, y, width, height, canvas)
        elif width > self.WIDTH / 2:
            self.split_horizontal(x, y, width, height, canvas)
        elif height > self.HEIGHT / 2:
            self.split_vertical(x, y, width, height, canvas)
        else:
            # Splits based on random chance
            hsplit = randrange(self.SPLIT_LOW, max(round(self.SPLIT_PENALTY * width) + 1, self.SPLIT_LOW + 1))
            vsplit = randrange(self.SPLIT_LOW, max(round(self.SPLIT_PENALTY * height) + 1, self.SPLIT_LOW + 1))
            if hsplit < width and vsplit < height:
                self.split_both(x, y, width, height, canvas)
            elif hsplit < width:
                self.split_horizontal(x, y, width, height, canvas)
            elif vsplit < height:
                self.split_vertical(x, y, width, height, canvas)
            # No split therefore fill the region with a color.
            else:
                color = self.randomColor()
                canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="black", width=self.THICKNESS)



if __name__ == '__main__':
    app = MondrianPainter()
    app.painter.mainloop()
