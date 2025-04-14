import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, master, image_path):
        self.master = master
        self.canvas = tk.Canvas(master, bg='white', width=719,height=719)
        self.scrollbar_x = tk.Scrollbar(master, orient='horizontal', command=self.canvas.xview)
        self.scrollbar_y = tk.Scrollbar(master, orient='vertical', command=self.canvas.yview)

        # Configure the canvas to work with scrollbars
        self.canvas.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x.pack(side='bottom', fill='x')
        self.scrollbar_y.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Load the image
        self.original_image = Image.open(image_path)
        self.image = self.original_image
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Store the image ID on the canvas
        self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        # Variables for zoom and panning
        self.scale_factor = 1.0
        self.zoom_step = 0.1
        self.canvas_width = 719
        self.canvas_height = 719
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Bind mouse events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows
        self.canvas.bind("<Button-1>", self.on_button_press)  # Left mouse button press
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)     # Mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)  # Release the mouse button
        
        # Initial pan coordinates
        self.start_x = None
        self.start_y = None

    def on_mouse_wheel(self, event):
        # Zoom in or out based on mouse wheel movement
        if event.delta > 0:
            self.scale_factor += self.zoom_step
        else:
            if self.scale_factor > self.zoom_step:
                self.scale_factor -= self.zoom_step
        
        self.update_image()

    def update_image(self):
        # Resize the image based on the current scale factor
        new_size = (int(self.original_image.width * self.scale_factor), 
                    int(self.original_image.height * self.scale_factor))
        self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Update the canvas with the new image
        self.canvas.itemconfig(self.image_id, image=self.photo)
        
        # Update canvas scroll region
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        # Record the mouse position for panning
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Calculate the distance moved
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        # Move the canvas view
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")

        # Update the starting position
        self.start_x = event.x
        self.start_y = event.y

    def on_button_release(self, event):
        # Reset the start position
        self.start_x = None
        self.start_y = None

# Create the main application window
root = tk.Tk()
root.title("Image Viewer with Zoom and Pan")

# Path to the image file (use a valid image path)
image_path = r"C:\Users\helina\Desktop\zoom.tif"  # Replace with your image path

app = ImageViewer(root, image_path)

root.mainloop()