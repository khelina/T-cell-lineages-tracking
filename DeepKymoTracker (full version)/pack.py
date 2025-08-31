import tkinter as tk

root = tk.Tk()

b1 = tk.Button(root, text='b1')
b2 = tk.Button(root, text='b2')
b3 = tk.Button(root, text='b3')
b4 = tk.Button(root, text='b4')
b5 = tk.Button(root, text='b5')
b5.pack(side=tk.BOTTOM)      
b4.pack(side=tk.BOTTOM)
b3.pack(side=tk.BOTTOM)
b1.pack(side=tk.LEFT)
b2.pack(side=tk.LEFT)      
root.mainloop()