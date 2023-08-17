from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import json,os

root = Tk()
root.title("Tileset creator")
img_w,img_h = 112,112

sprites = []
sockets = {}
rots = {}
spritesdir = os.listdir("sprites")
count = 0
for sp_name in spritesdir:
    sprite = Image.open("sprites/"+sp_name).resize((img_w,img_h))
    sprites.append(ImageTk.PhotoImage(sprite))
    sockets[count] = ["","","",""]
    rots[count] = 0
    count += 1
cur_img = 0

def OPEN():
    tilesetname = filedialog.askopenfilename(title="tilesets",filetypes=(("json files","*.json"),))
    if tilesetname != '':
        with open(tilesetname,'r') as file:
            tileset = json.load(file)
        if len(tileset) != len(sockets):
            messagebox.showinfo("Error","Tileset does not match\n the sprites in sprites folder")
        else:
            for tile in tileset:
                sockets[int(tile)] = tileset[tile][0]
                rots[int(tile)] = tileset[tile][1]
            updatedisplay()
def SAVE():
    tileset = {}
    for count in sockets:
        tileset[count] = [sockets[count],rots[count]]
    with open("tileset.json",'w') as file:
        json.dump(tileset, file, indent=4)
        
def FORWARD():
    updatedata()
    global cur_img
    if cur_img == 0:
        backward_button.config(state=NORMAL)
    cur_img += 1
    if cur_img == len(sockets)-1:
        forward_button.config(state=DISABLED)
    updatedisplay()
        
def BACKWARD():
    updatedata()
    global cur_img
    if cur_img == len(sockets)-1:
        forward_button.config(state=NORMAL)
    cur_img -= 1
    if cur_img == 0:
        backward_button.config(state=DISABLED)
    updatedisplay()
    
def updatedata():
    socket = (t_val.get(),r_val.get(),b_val.get()[-1::-1],l_val.get()[-1::-1])
    sockets[cur_img] = socket
    rots[cur_img] = rot_val.get()
def updatedisplay():
    socket = sockets[cur_img]
    t_val.delete(0,END)
    r_val.delete(0,END)
    b_val.delete(0,END)
    l_val.delete(0,END)
    t_val.insert(0,socket[0])
    r_val.insert(0,socket[1])
    b_val.insert(0,socket[2])
    l_val.insert(0,socket[3])
    rot_val.set(rots[cur_img])
    img_lbl.config(image = sprites[cur_img])
    
open_button = Button(root, text="Open", command=OPEN)
save_button = Button(root, text="Save", command=SAVE)
forward_button = Button(root, text=">>", command=FORWARD)
backward_button = Button(root, text="<<", command=BACKWARD, state=DISABLED)
t_val = Entry(root)
r_val = Entry(root)
b_val = Entry(root)
l_val = Entry(root)
rot_val = IntVar()
rot_val.set(0)
sing_rot = Radiobutton(root, text="Single Rotation", variable=rot_val, value=0)
dual_rot = Radiobutton(root, text="Dual Rotation", variable=rot_val, value=1)
quad_rot = Radiobutton(root, text="Quad Rotation", variable=rot_val, value=2)
img_lbl = Label(root, image= sprites[cur_img])

backward_button.grid(row=0, column=0)
forward_button.grid(row=0, column=2)
open_button.grid(row=2, column=0)
save_button.grid(row=2, column=2)
t_val.grid(row=0, column=1)
r_val.grid(row=1, column=2)
b_val.grid(row=2, column=1)
l_val.grid(row=1, column=0)
img_lbl.grid(row=1, column=1)
sing_rot.grid(row=3, column=0)
dual_rot.grid(row=3, column=1)
quad_rot.grid(row=3, column=2)

mainloop()
