from PIL import Image
import time

class Converter:

    def __init__(self):
        self.image = None
        self.name = ""
        self.grayscale = None
        self.final = None
        self.threshold = 0
        self.bg_color = (0, 0, 0, 0)

    def load_image(self, filename):
        self.image = Image.open(filename)
        self.name = filename.split(".")[0]
        self.grayscale = self.image.convert("L")

    def convert_image_to_png(self):
        gs = self.grayscale
        th = self.threshold
        im = self.image
        width, height = self.image.size
        new_image = Image.new("RGBA", (width, height), color=self.bg_color)
        start = time.time()
        for x in range(width):
            for y in range(height):
                grey = gs.getpixel((x, y))
                if im.mode in ("L", "P", "RGBA"):
                    im = im.convert("RGB")
                r, g, b = im.getpixel((x, y))
                if grey < 255 - th:
                    new_image.putpixel((x, y), (r, g, b, 255))
                #arr = np.array(gs)
                #ima = np.array(im)
                #print(ima[150][0][1])
                #RGB = np.where(arr < 255 - th, ima, 0)
                #A = np.where(arr < 255 - th, 255, 0)
                #pixels = np.dstack((RGB, A))
                #new_image = Image.fromarray(np.uint8(pixels))
        end = time.time()
        print(end-start)
        self.final = new_image

    def save_image(self, filename):
        self.final.save(filename)
