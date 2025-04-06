import tkinter as tk

def display_coordinates(event):
    screen_x = event.x  # X coordinate on the screen
    canvas_x = canvas.canvasx(event.x)  # Convert to canvas coordinates
    print(f"Screen Coordinates: {screen_x}, Canvas Coordinates: {canvas_x}")

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=300, bg='lightgray')
canvas.pack()

# Bind mouse click event to the canvas
canvas.bind("<Button-1>", display_coordinates)

root.mainloop()