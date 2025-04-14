spaceship_texture = tk.PhotoImage(file=path + r'\spaceship_fast.png')

spaceship = tk.Label(root,image=spaceship_texture)

space.create_image(960,540,image=spaceship_texture, anchor="center", tag="ship")

space.tag_lower("ship")


#Here's the main part:


def moveshiptocursor(event):

print(event.x, event.y)

#space.coords("ship")[0] = event.x Did also try this, but didn't work

space.move("ship", event.x,event.y) #'ship' is the object I want to move (it's an image)


space.bind('<Motion>', moveshiptocursor) #'space' is my canvasdef moveshiptocursor(event):
   
    
   
    
   
def moveshiptocursor(event):
    space.coords("ship", event.x,event.y)