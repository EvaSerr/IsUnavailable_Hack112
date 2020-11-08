from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  
canvas = Canvas(root, width = 250, height = 250)  
canvas.pack()  
img = Image.open("eserre.jpg")
image = img.resize((250, 250), Image.ANTIALIAS)  
myImg = ImageTk. PhotoImage(image)
canvas.create_image(0, 0, anchor=NW, image=myImg) 
root.mainloop() 


'''python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow'''