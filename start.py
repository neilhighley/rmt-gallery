import sys, configparser
from time import sleep
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk, ImageOps
from itertools import cycle

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.IMAGES = ["image2-pt.png", "image1.jpg"]
        self.delay = delay
        self.canvas = {}
        self.get_aspects()

    def get_aspects(self):
        root = self
        w,h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.focus_set()
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas = tkinter.Canvas(root, width=w, height=h)
        self.canvas.pack()
        self.canvas.configure(background='black')

    def show_image_resized_and_rotated(self, pilImage):
        #root = tkinter.Tk()
        root=self
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        imgWidth, imgHeight = pilImage.size
        imgaspect = 0 # 0= portrait
        scrnaspect = 0
        rot = 0
        print("image:" + str(imgWidth) + "," + str(imgHeight))
        print("Screen:" + str(w) + "," + str(h))
        if w > h:
            print("Screen aspect is landscape")
            scrnaspect=1
        if imgWidth > imgHeight:
            print("Image aspect is landscape")
            imgaspect=1

        if imgaspect != scrnaspect:
            if scrnaspect == 1:
                print("Rotate Image 90deg")
                rot = 90
            else:
                print("Rotate Image 270deg")
                rot = 270
            print("Rotate image")
            pilImage = pilImage.copy().rotate(rot, 1, 1)
            t = imgWidth
            imgWidth = imgHeight
            imgHeight = t
            print("image new:" + str(imgWidth) + "," + str(imgHeight))
        ratio = 1
        if imgWidth > w or imgHeight > h:
            ratio = min(w/imgWidth, h/imgHeight)

        if imgWidth < w and imgHeight < h:
            ratio = min(w/imgWidth, h/imgHeight)
        print("Ratio:"+str(ratio))
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        print("image upd to ratio:" + str(imgWidth) + "," + str(imgHeight))
        pilImage = ImageOps.fit(pilImage, (imgWidth, imgHeight))
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(w/2, h/2, image=image)
        self.mainloop()

    def refresh_images(self,imgArray):
        self.IMAGES= cycle((Image.open(image), image)
              for image in imgArray)

    def show_slides(self):
            img_object, img_name=next(self.IMAGES)
            print("load image:"+img_name)
            self.after(self.delay, self.show_image_resized_and_rotated(img_object))

    def run(self):
        self.mainloop()


delay = 5
app = App()
app.refresh_images(["image2-pt.png", "image1.jpg"])
app.show_slides()
app.run()

exit(0)
