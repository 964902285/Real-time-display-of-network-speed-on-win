#!/usr/bin/env python
# coding: utf-8
import tkinter
from time import sleep
from threading import Thread
from psutil import net_io_counters
from PIL import Image, ImageTk, ImageDraw

width, height = 160, 80

root = tkinter.Toplevel()  # 不能使用Tk()
root.geometry(f'{width}x{height}+1300+650')  # x是小写字母x
root.resizable(False, False)
root.overrideredirect(True)
root.attributes('-transparentcolor', 'white')
root.attributes('-topmost', True)
image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
draw  = ImageDraw.Draw(image)
# 画一个椭圆
draw.ellipse((0, 0, width, height), fill = (200, 200, 200, 30))
image_tk = ImageTk.PhotoImage(image)
lbTraffic = tkinter.Label(
    root,
    text='',
    font=('楷体',14),
    foreground = 'red',
    bg = '#ffffff',
    compound = tkinter.CENTER,
    anchor = 'center', 
    image = image_tk)
lbTraffic.place(x=0, y=0, width=width, height=height)

canMove = tkinter.BooleanVar(root, False)
X = tkinter.IntVar(root, value=0)
Y = tkinter.IntVar(root, value=0)

def onLeftButtonDown(event):
    X.set(event.x)
    Y.set(event.y)
    canMove.set(True)
    
root.bind('<Button-1>', onLeftButtonDown)

def onLeftButtonUp(event):
    canMove.set(False)
    
root.bind('<ButtonRelease-1>', onLeftButtonUp)

def onLeftButtonMove(event):
    if not canMove.get():
        return
    newX = root.winfo_x() + (event.x - X.get())
    newY = root.winfo_y() + (event.y - Y.get())
    g = f'{width}x{height}+{newX}+{newY}'
    root.geometry(g)
    
root.bind('<B1-Motion>', onLeftButtonMove)

def onRightButtonUp(event):
    running.set(False)
    root.destroy()
    
root.bind('<ButtonRelease-3>', onRightButtonUp)

def compute_traffic():
    traffic_io = net_io_counters()[:2]
    while running.get():
        sleep(0.5)
        traffic_ioNew = net_io_counters()[:2]
        diff = tuple(map(lambda x, y: (x - y) * 2 / 1024,
                        traffic_ioNew,
                        traffic_io))
        msg = '↑:{:.2f} KB/s\n↓:{:.2f} KB/s'.format(*diff)
        lbTraffic['text'] = msg
        traffic_io = traffic_ioNew

running = tkinter.BooleanVar(root, True)
Thread(target=compute_traffic).start()
root.mainloop()
