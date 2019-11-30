from tkinter import filedialog as df
import Converter
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image


class UI:

	def __init__(self):
		self.conv = Converter.Converter()
		self.root = Tk()
		self.root.title("JPG background remover")
		self.frame = Frame(self.root)
		self.frame.grid(column=0, row=0, sticky=(N, E, W, S))

		self.in_filename = StringVar()
		self.in_image = None
		self.out_filename = StringVar()
		self.out_image = None
		self.last_out_filename = ""
		self.threshold = IntVar()
		self.use_color = IntVar()
		self.conv_image = None
		self.color = (255, 105, 180, 255)

		ttk.Label(self.frame, text="Input file").grid(row=1, column=1, sticky=N)
		ttk.Entry(self.frame, textvariable=self.in_filename, width=50).grid(row=3, column=1, sticky=N)
		ttk.Button(self.frame, command=self.get_path, text="Open file").grid(row=4, column=1, sticky=N)
		self.cnv_in_image = Canvas(self.frame, width=300, height=300)
		self.cnv_in_image.grid(row=2, column=1, sticky=N)

		ttk.Label(self.frame, text="Output file").grid(row=1, column=2, sticky=N)
		ttk.Entry(self.frame, textvariable=self.out_filename, width=50).grid(row=3, column=2, sticky=N)
		ttk.Button(self.frame, command=self.get_output_filename, text="Set output file").grid(row=4, column=2, sticky=N)
		self.cnv_out_image = Canvas(self.frame, width=300, height=300)
		self.cnv_out_image.grid(row=2, column=2, sticky=N)

		ttk.Label(self.frame, text="Filter threshold").grid(row=5, column=1, sticky=N)
		ttk.Scale(self.frame, from_=0, to=254, orient=HORIZONTAL, length=280, variable=self.threshold)\
			.grid(row=5, column=2, sticky=N)

		ttk.Button(self.frame, command=self.convert, text="Convert image").grid(row=6, column=1, sticky=N)
		ttk.Button(self.frame, command=self.save, text="Save as png").grid(row=6, column=2, sticky=N)

		ttk.Checkbutton(self.frame, text="Color Background", variable=self.use_color).grid(row=7, column=1, sticky=N)
		ttk.Button(self.frame, command=self.get_color, text="Choose Color").grid(row=7, column=2, sticky=N)

		self.frame.mainloop()

	def get_path(self):
		self.in_filename.set(df.askopenfilename())
		self.in_image = Image.open(self.in_filename.get())
		self.in_image = self.in_image.resize((300, 300), Image.ANTIALIAS)
		self.in_image = ImageTk.PhotoImage(self.in_image)
		self.cnv_in_image.create_image((0, 0), anchor=NW, image=self.in_image)

	def get_output_filename(self):
		self.out_filename.set(df.asksaveasfilename(defaultextension="png"))

	def convert(self):
		self.conv.load_image(self.in_filename.get())
		self.conv.threshold = self.threshold.get()
		if self.use_color.get():
			self.conv.bg_color = self.color
		else:
			self.conv.bg_color = (0, 0, 0, 0)
		self.conv.convert_image_to_png()

		self.conv_image = self.conv.final
		# width, height = self.conv_image.size
		oi = Image.new("RGB", (300, 300), color=self.color)

		conv_im = self.conv_image.resize((300, 300), Image.ANTIALIAS)
		for x in range(300):
			for y in range(300):
				r, g, b, a = conv_im.getpixel((x, y))
				if a != 0:
					oi.putpixel((x, y), (r, g, b))

		self.out_image = oi
		self.out_image = ImageTk.PhotoImage(self.out_image)
		self.cnv_out_image.create_image((0, 0), anchor=NW, image=self.out_image)

	def save(self):
		if self.out_filename.get() == self.last_out_filename:
			self.get_output_filename()
			"""out_filename gets set in get_output filename
				We set last_out_filename to avoid overriding the last converted image"""
			self.last_out_filename = self.out_filename.get()
		self.conv.save_image(self.out_filename.get())

	def get_color(self):
		lcl = askcolor()
		if lcl[0] is not None:
			lcl = list(lcl[0])
			lcl[0] = int(lcl[0])
			lcl[1] = int(lcl[1])
			lcl[2] = int(lcl[2])
			lcl.append(255)
			lcl = tuple(lcl)
			self.color = lcl
