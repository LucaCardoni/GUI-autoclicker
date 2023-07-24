from tkinter import *
from tkinter import ttk
import pynput.keyboard as keyboard
import pynput.mouse as mouse
import threading
import time
from tkinter import filedialog
import json
import webbrowser

def get_mouse_position():
    global listener, k_listener
    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left and keyboard.Key.ctrl_l in current_keys:
            nonlocal X, Y
            X, Y = x, y
            listener.stop()
            k_listener.stop()

    def on_press(key):
        if key == keyboard.Key.ctrl_l:
            current_keys.add(key)

    def on_release(key):
        try:
            current_keys.remove(key)
        except KeyError:
            pass

    current_keys = set()
    X, Y = None, None

    with mouse.Listener(on_click=on_click) as listener, keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener:
        listener.join()
        k_listener.join()

    return X, Y

def close():
    try:
        listener.stop()
        k_listener.stop()
    except:
        pass
    root.destroy()

root = Tk()
root.title("Autoclicker")
root.geometry("230x380")
root.resizable(False, False)
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW", close)

def currentposition():
    root.geometry("230x380")

def choosepositions():
    root.geometry("378x380")

on = False

def getpositions():
    global on
    on = not on
    if on:
        posbtn.config(text="Stop recording")
        threading.Thread(target=append_mouse_position, daemon=True).start()
    else:
        listener.stop()
        k_listener.stop()
        on = False
        posbtn.config(text="Record positions")

def append_mouse_position():
    global on, n

    n = 1 if len(Lb.get(0, END)) == 0 else int(Lb.get(0,END)[-1].split(" ")[0])+1
    while on:
        x, y = get_mouse_position()
        text = f"{n}      X:{x}   Y:{y}"
        if on == True:
            Lb.insert(n, text)
            n += 1
    on = False

def start(interval, btn, clicks, crpt, posopt):
    if crpt == 'repeat':
        rpts = int(repetitions.get())
        for i in range(rpts):
            if state == False:
                break
            if posopt == 'currentposition':
                mouse.Controller().click(btn, clicks)
            if posopt == 'choosepositions':
                for pos in Lb.get(0, END):
                    if interval > 0.0040:
                        time.sleep(interval)
                    x = int(pos.split("X:")[1].split(" ")[0])
                    y = int(pos.split("Y:")[1])
                    mouse.Controller().position = (x, y)
                    mouse.Controller().click(btn, clicks)
        startbtn["state"] = "normal"
        stopbtn["state"] = "disabled"

    elif crpt == 'repeatuntilstopped':
        while state == True:
            if posopt == 'currentposition':
                mouse.Controller().click(btn, clicks)
            if posopt == 'choosepositions':
                for pos in Lb.get(0, END):
                    if interval > 0.0040:
                        time.sleep(interval)
                    x = int(pos.split("X:")[1].split(" ")[0])
                    y = int(pos.split("Y:")[1])
                    mouse.Controller().position = (x, y)
                    mouse.Controller().click(btn, clicks)
        startbtn["state"] = "normal"
        stopbtn["state"] = "disabled"

state = False
def togglestate():
    global state
    state = not state
    if state:
        state = True
        interval = (int(Millisecs.get(1.0, "end-1c"))/1000) + int(Secs.get(1.0, "end-1c"))
        btn = mousebtn.get().lower()
        if btn == 'left':
            btn = mouse.Button.left
        elif btn == 'middle':
            btn = mouse.Button.middle
        elif btn == 'right':
            btn = mouse.Button.right
        if clicktype.get() == 'Single':
            clicks = 1
        elif clicktype.get() == 'Double':
            clicks = 2
        crpt = sceltaclick.get()
        posopt = sceltaposition.get()
        threading.Thread(target=start, args=(interval, btn, clicks, crpt, posopt), daemon=True).start()
        startbtn["state"] = "disabled"
        stopbtn["state"] = "normal"
    else:
        state = False
        startbtn["state"] = "normal"
        stopbtn["state"] = "disabled"

hk = 'Key.f7'
recnhk = False
def get_new_hotkey():
    global hk, Klistener, recnhk
    recnhk = True
    def on_press(key):
        global hk
        hk = str(key)
        hklbl.config(text=hk.replace("Key.", "").replace("'", "").upper())
        startbtn.config(text=f"""Start ({hk.replace('Key.', '').replace("'", "").upper()})""")
        stopbtn.config(text=f"""Stop ({hk.replace('Key.', '').replace("'", "").upper()})""")

    with keyboard.Listener(on_press=on_press) as Klistener:
        Klistener.join()

def check_hotkey():
    def on_press(key):
        global state
        if str(key).replace("'", "") == hk.replace("'", "") and recnhk == False:
            togglestate()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


threading.Thread(target=check_hotkey, daemon=True).start()

ciFrame = LabelFrame(root, text="Click interval", width=210, height=50)
ciFrame.place(x=10, y=10)

Secs = Text(ciFrame, height=1, width=5)
Secs.insert("1.0", "0")
Secs.place(x=5, y=3)
ttk.Label(ciFrame, text="Secs").place(x=55, y=3)

Millisecs = Text(ciFrame, height=1, width=5)
Millisecs.insert("1.0", "100")
Millisecs.place(x=100, y=3)
ttk.Label(ciFrame, text="Millisecs").place(x=145, y=3)

coFrame = LabelFrame(root, text="Click options", width=210, height=85)
coFrame.place(x=10, y=65)

mousebtn = StringVar(value="Left")
clicktype = StringVar(value="Single")

ttk.Label(coFrame, text="Mouse button: ").place(x=5, y=3)
ttk.Combobox(coFrame, textvariable=mousebtn, width=8, values=["Left", "Middle", "Right"], state="readonly").place(x=125, y=3)

ttk.Label(coFrame, text="Click type: ").place(x=5, y=33)
ttk.Combobox(coFrame, textvariable=clicktype, width=8, values=["Single", "Double"], state="readonly").place(x=125, y=33)

crFrame = LabelFrame(root, text="Click repeat", width=210, height=80)
crFrame.place(x=10, y=155)

sceltaclick = StringVar(value="repeatuntilstopped")
repetitions = StringVar(root)
repetitions.set("0")

ttk.Radiobutton(crFrame, text="Repeat", variable=sceltaclick, value="repeat").place(x=5, y=3)
repsbox = Spinbox(crFrame, from_=0, to=9999, increment=1, width=8,  textvariable=repetitions)
repsbox.place(x=75, y=3)
ttk.Label(crFrame, text="times").place(x=150, y=3)

ttk.Radiobutton(crFrame, text="Repeat until stopped", variable=sceltaclick, value="repeatuntilstopped").place(x=5, y=33)

moFrame = LabelFrame(root, text="Mouse options", width=210, height=80)
moFrame.place(x=10, y=240)

sceltaposition = StringVar(value="currentposition")

ttk.Radiobutton(moFrame, text="Follow cursor position", variable=sceltaposition, value="currentposition",  command=currentposition).place(x=5, y=3)

ttk.Radiobutton(moFrame, text="Choose coordinates", variable=sceltaposition, value="choosepositions", command=choosepositions).place(x=5, y=33)

posbtn = Button(root, text="Record positions", command=getpositions, width=17)
posbtn.place(x=234, y=25)

Lb = Listbox(root, width=22, height=18)
Lb.place(x=230, y=72)

startbtn = Button(root, text=f"Start ({hk.replace('Key.', '').upper()})", command=togglestate, width=13, height=2)
startbtn.place(x=11, y=330)

stopbtn = Button(root, text=f"Stop ({hk.replace('Key.', '').upper()})", command=togglestate, width=13, height=2)
stopbtn.place(x=117, y=330)
stopbtn["state"] = "disabled"

def Importconfig():
    global hk
    file = filedialog.askopenfilename()
    with open(file) as json_file:
        data = json.load(json_file)
    Scs = data['Scs']
    Mlscs = data['Mlscs']
    btn = data['btn']
    clicks = data['clicks']
    crpt = data['crpt']
    rpts = data['rpts']
    posopt = data['posopt']
    poss = data['poss']
    hk = data['hk']

    Secs.delete('1.0', 'end')
    Millisecs.delete('1.0', 'end')
    Lb.delete(0, END)
    Secs.insert(1.0, Scs)
    Millisecs.insert("1.0", Mlscs)
    mousebtn.set(btn)
    clicktype.set(clicks)
    sceltaclick.set(crpt)
    repetitions.set(rpts)
    sceltaposition.set(posopt)
    for item in poss:
        Lb.insert(END, item)
    startbtn.config(text=f"Start ({hk.replace('Key.', '').upper()})")
    stopbtn.config(text=f"Stop ({hk.replace('Key.', '').upper()})")

    exec(f"{posopt}()")

def Exportconfig():
    Scs = Secs.get(1.0,"end-1c")
    Mlscs = Millisecs.get(1.0, "end-1c")
    btn = mousebtn.get()
    clicks = clicktype.get()
    crpt = sceltaclick.get()
    rpts = int(repetitions.get())
    posopt = sceltaposition.get()
    poss = Lb.get(0, END)
    configdict = {"Scs" : Scs, "Mlscs" : Mlscs, "btn" : btn, "clicks" : clicks, "crpt" : crpt, "rpts" : rpts, "posopt": posopt, "poss" : poss, "hk" : hk}
    file = filedialog.asksaveasfile(filetypes = [('JSON Files', '*.json')], defaultextension = [('JSON Files', '*.json')])
    with open(file.name, "w") as f:
        json.dump(configdict, f)

def Resetconfig():
    global hk
    Secs.delete('1.0', 'end')
    Millisecs.delete('1.0', 'end')
    Lb.delete(0, END)
    Secs.insert(1.0, 0)
    Millisecs.insert("1.0", 100)
    mousebtn.set('Left')
    clicktype.set('Single')
    sceltaclick.set('repeatuntilstopped')
    repetitions.set(0)
    sceltaposition.set('currentposition')
    hk = 'Key.f7'
    currentposition()

def Hotkey():
    def save():
        global recnhk
        try:
            Klistener.stop()
        except:
            pass
        try:
            recnhk = False
        except:
            pass
        Hkw.destroy()
    global hklbl
    Hkw = Toplevel(root)
    Hkw.title("Hotkey settings")
    Hkw.geometry("200x81")
    Hkw.attributes("-topmost", True)
    Hkw.protocol("WM_DELETE_WINDOW", save)
    hkbtn = Button(Hkw, text="Start/Stop", command=threading.Thread(target=get_new_hotkey, daemon=True).start(), width=10, height=2)
    hkbtn.place(x=20, y=20)
    hkframe = LabelFrame(Hkw)
    hkframe.place(x=130, y=30)
    hklbl = Label(hkframe, text=hk.replace("Key.", "").replace("'", "").upper(), font=(15))
    hklbl.pack()

def About():
    webbrowser.open(url='https://github.com/Rickionee/GUI-autoclicker')

menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=False)
help_menu = Menu(menubar, tearoff=False)

file_menu.add_command(label='Import config', command=Importconfig)
file_menu.add_command(label='Export config', command=Exportconfig,)
file_menu.add_command(label='Reset config', command=Resetconfig,)

help_menu.add_command(label='Hotkey settings', command=Hotkey)
help_menu.add_command(label='About', command=About)

menubar.add_cascade(label='File', menu=file_menu, underline=0)
menubar.add_cascade(label='Help', menu=help_menu, underline=0)

mainloop()