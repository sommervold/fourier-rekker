
# Importing required modules
from tkinter import *
from reader import Reader
from PIL import ImageGrab
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np

class Fourier:
    def __init__(self, n, file):

        self.path_width = 4 # Width of the paths drawn on screen (px)
        self.n = n # Number of circles
        self.upr = 100 # Updates per rotation, for upr=50, it takes 50 updates to reach a full rotation
        self.t = 0 # 'time' passed since start.
        self.width, self.height = 1920, 1080 # Width and height of screen shown on screen/video
        self.fullscreen = True

        self.video_mode = False # Video mode creates a video of the drawing
        self.fps = 40 # Frames per second in video
        self.video_length = 200 # Number of frames in video
        self.finished = False
        self.framecount = 0
        if self.video_mode:
            fourcc = VideoWriter_fourcc(*'MP42')
            self.video = VideoWriter('C:\\Koding\\Scripts\\Python\\Fourier Series\\Videoer\\' +file+ '_' +str(self.n)+ '.avi', fourcc, float(self.fps), (self.width, self.height))

        self.root = Tk() # Main window
        if self.fullscreen:
            self.root.attributes("-fullscreen", True) # set fullscreen
        else:
            self.root.geometry(str(self.width) + "x" + str(self.height)) # Setting width and height of video

        self.root.bind("<Escape>", self.close) # Pressing escape closes the window
        self.canvas = Canvas(self.root, width=self.width, height=self.height) # Canvas to draw on
        self.canvas.pack()
        self.canvas.create_text(100,100,text="n="+str(n),font="Times 50 italic bold")

        self.reader = Reader(self.n, self.upr, self.width, self.height, self.path_width)
        self.paths = self.reader.read_svg(file + ".svg") # Read SVG file and calculate vectors
        for path in self.paths: # Draw startposition of all vectors on the canvas
            for vector in path.vectors:
                vector.create(self.canvas)
        self.root.after(1, self.frame) # Run first frame after 1ms
        self.root.mainloop() # Start window

    def frame(self):
        """
            One frame/calculation. Calculates next position of each vector in each path,
            and draws new positions / tracelines
        """
        self.t += (1/self.upr)

        for path in self.paths:
            path.calculate(self.t)
            path.draw(self.canvas, self.upr)

        if self.video_mode:
            self.save_frame() # Save frames to a video, if video mode is enabled
        if not self.finished:
            self.root.after(1, self.frame) # Run new frame after 1ms

    def save_frame(self):
        """
            Takes a screencapture of the drawing, and saves the frame to the video
        """
        x=self.root.winfo_rootx()+self.canvas.winfo_x()
        y=self.root.winfo_rooty()+self.canvas.winfo_y()
        x1=x+self.canvas.winfo_width()
        y1=y+self.canvas.winfo_height()
        img = np.array(ImageGrab.grab().crop((x,y,x1,y1)))
        img = np.flip(img, axis=2) # colors are in reversed order for some reason (BGR), flip back to RGB
        self.video.write(img) # Save to video object
        self.framecount += 1
        if self.framecount >= self.video_length: # Check if the video has reached its end
            self.finished = True
            self.video.release() # Save the video
            self.close(0) # Exit

    def close(self, event):
        self.root.destroy() # close and exit

Fourier(25, "ntg3")
#for n in range(1, 103, 2):
#    Fourier(n, "ntg3")
