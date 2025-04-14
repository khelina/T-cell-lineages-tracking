import tkinter as tk
from PIL import Image, ImageTk

class ImageZoomApp:
    def __init__(self, master, image_path):
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

        # Load the image
        self.original_image = Image.open(image_path)
        self.current_image = self.original_image
        self.photo = ImageTk.PhotoImage(self.current_image)

        # Display the image
        self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        # Scale factors
        self.scale_factor = 1.0
        self.zoom_step = 0.1

        # Buttons to zoom in and out
        zoom_in_button = tk.Button(master, text="Zoom In", command=self.zoom_in)
        zoom_in_button.pack(side='left', padx=5)

        zoom_out_button = tk.Button(master, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.pack(side='left', padx=5)

    def zoom_in(self):
        self.scale_factor += self.zoom_step
        self.update_image()

    def zoom_out(self):
        if self.scale_factor > self.zoom_step:
            self.scale_factor -= self.zoom_step
            self.update_image()

    def update_image(self):
        # Resize the image based on the current scale factor
        new_size = (int(self.original_image.width * self.scale_factor), 
                    int(self.original_image.height * self.scale_factor))
        self.current_image = self.original_image.resize(new_size, Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.current_image)
        
        # Update the image on the canvas
        self.canvas.itemconfig(self.image_id, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))  # Update scroll region if needed

# Create the main application window
root = tk.Tk()
root.title("Image Zoom Example")

# Path to the image file (use a valid image path)
image_path = r"C:\Users\helina\Desktop\zoom.tif"
        
app = ImageZoomApp(root, image_path)

root.mainloop()