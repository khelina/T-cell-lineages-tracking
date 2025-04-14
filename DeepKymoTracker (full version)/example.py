import tkinter as tk
import random
from interface_functions import turn_image_into_tkinter
import cv2
root = tk.Tk()
pressed = False


def load_image():
        global canvas, xsb,ysb
        canvas = tk.Canvas(root, width=400, height=400, background="black")
        xsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
        ysb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        canvas.configure(scrollregion=(0,0,1000,1000))

        xsb.grid(row=1, column=0, sticky="ew")
        ysb.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
    
         
        
        global my_image,my_image_resized, tk_image , image_object
        my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
        my_image_resized=my_image.copy()
        my_image_resized= cv2.resize(my_image_resized,(400,400), cv2.INTER_LINEAR)      
        tk_image =  turn_image_into_tkinter(my_image_resized,400)
        image_object=canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                
        """
        for n in range(50):
            x0 = random.randint(0, 900)
            y0 = random.randint(50, 900)
            x1 = x0 + random.randint(50, 100)
            y1 = y0 + random.randint(50,100)
            color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
            self.canvas.create_rectangle(x0,y0,x1,y1, outline="black", fill=color, activefill="black", tags=n)
        #self.canvas.create_text(50,10, anchor="nw", text="Click and drag to move the canvas\nScroll to zoom.", font = ("Helvetica", int(self.fontSize)), tags="text")
        """
        # This is what enables using the mouse:
        canvas.bind("<ButtonPress-1>", move_start)
        canvas.bind("<B1-Motion>", move_move)

        #canvas.bind("<ButtonPress-2>", pressed2)
        #canvas.bind("<Motion>", move_move2)      
        canvas.bind("<MouseWheel>",zoomer)
        # Hack to make zoom work on Windows
        root.bind_all("<MouseWheel>",zoomer)
#move
def move_start(event):
        canvas.scan_mark(event.x, event.y)
def move_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

#move
def pressed2(event):
        global pressed
        pressed = not pressed
        canvas.scan_mark(event.x, event.y)
def move_move2( event):
        if pressed:
            canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
def zoomer(event):
        if (event.delta > 0):
            canvas.scale("all", event.x, event.y, 1.1, 1.1)
            #fontSize = fontSize * 1.1
        elif (event.delta < 0):
            canvas.scale("all", event.x, event.y, 0.9, 0.9)
            #fontSize = fontSize * 0.9
        #canvas.configure(scrollregion = canvas.bbox("all"))
        

load_image()    

root.mainloop()