from tkinter import *
from PIL import ImageTk,Image
from datetime import datetime
import json

def getSignal(rssi):
    if 0 <= abs(rssi) <= 10: return ''  # 5 bars
    elif 11 <= abs(rssi) <= 20: return ''  # 4 bars
    elif 21 <= abs(rssi) <= 30: return ''  # 3 bars
    elif 31 <= abs(rssi) <= 40: return ''  # 2 bars
    elif 41 <= abs(rssi) <= 50: return ''  # 1 bar
    else: return ''

backgroundColor = '#303339'
foregroundColor = '#dbdbdb'
secondaryColor = '#b2b2b2'
tertiaryColor = '#efcb15'
defaultValue = '----'

# Initialize window
root = Tk()
root.wm_title("PiPlane")
root.geometry("800x480")
root.configure(bg=backgroundColor)
root.resizable(False, False)
root.attributes('-fullscreen',True)
root.config(cursor="none")

# Statusbar
Label(root, text='', fg=foregroundColor, bg=backgroundColor, font=('Font Awesome 5 Pro Solid', 30)).place(x=725, y=25)
timeLabel = Label(root, text=str(datetime.now().strftime("%H:%M:%S")), fg=foregroundColor, bg=backgroundColor, font=('arial', 30))
signalLabel = Label(root, text=getSignal(999), fg=foregroundColor, bg=backgroundColor, font=('Font Awesome 5 Pro Solid', 30))

# Label
Label(root, text='CALL SIGN', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=25, y=25)
Label(root, text='ALTITUDE', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=25, y=175)
Label(root, text='VERTICAL SPEED', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=250, y=175)
Label(root, text='AIRSPEED', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=25, y=275)
Label(root, text='HEADING', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=250, y=275)
Label(root, text='HITS', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=25, y=375)
Label(root, text='SQUAWK', fg=secondaryColor, bg=backgroundColor, font=('arial', 15)).place(x=250, y=375)

# Value
callSignLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 60))
altitudeLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))
vsLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))
airspeedLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))
headingLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))
hitsLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))
squawkLabel = Label(root, text=defaultValue, fg=foregroundColor, bg=backgroundColor, font=('arial', 50))

# Placing mutable labels
signalLabel.place(x=655, y=25)
timeLabel.place(x=475, y=25)
callSignLabel.place(x=25, y=50)
altitudeLabel.place(x=25, y=200)
vsLabel.place(x=250, y=200)
airspeedLabel.place(x=25, y=300)
headingLabel.place(x=250, y=300)
hitsLabel.place(x=25, y=400)
squawkLabel.place(x=250, y=400)

# Compass
compassImage = ImageTk.PhotoImage(Image.open("assets/compass.gif").resize((300, 300), Image.ANTIALIAS).convert('RGBA').rotate(0))
compass = Label(root, bg=backgroundColor, image=compassImage)
compass.place(x=450, y=125)

pointerImage = ImageTk.PhotoImage(Image.open("assets/A1.gif").resize((100, 100), Image.ANTIALIAS).convert('RGBA'))
pointer = Label(root, bg=backgroundColor, image=pointerImage)
pointer.image = pointerImage
pointer.place(x=550, y=225)

def update():
    timeLabel.config(text=str(datetime.now().strftime("%H:%M:%S")))

    aircraft = []
    with open('/var/run/dump1090-mutability/aircraft.json') as json_file:
        rawData = json.load(json_file)
        aircraft = rawData['aircraft']
        # print(aircraft)
    try:
        if 'flight' in aircraft[0]:
            callSignLabel.config(text=aircraft[0]['flight'])
        else:
            callSignLabel.config(text=defaultValue)
        if 'altitude' in aircraft[0]:
            altitudeLabel.config(text=aircraft[0]['altitude'])
        else:
            altitudeLabel.config(text=defaultValue)
        if 'vert_rate' in aircraft[0]:
            vsLabel.config(text=aircraft[0]['vert_rate'])
        else:
            vsLabel.config(text=defaultValue)
        if 'speed' in aircraft[0]:
            airspeedLabel.config(text=aircraft[0]['speed'])
        else:
            airspeedLabel.config(text=defaultValue)
        if 'track' in aircraft[0]:
            headingLabel.config(text=str(aircraft[0]['track']) + 'º')
            compassImage = ImageTk.PhotoImage(Image.open("assets/compass.gif").resize((300, 300), Image.ANTIALIAS).convert('RGBA').rotate(aircraft[0]['track']))
            compass.configure(image=compassImage)
            compass.image = compassImage
        else:
            headingLabel.config(text=defaultValue)
            compassImage = ImageTk.PhotoImage(Image.open("assets/compass.gif").resize((300, 300), Image.ANTIALIAS).convert('RGBA').rotate(0))
            compass.configure(image=compassImage)
            compass.image = compassImage
        if 'messages' in aircraft[0] and 'altitude' in aircraft[0]:
            hitsLabel.config(text=aircraft[0]['messages'])
        else:
            hitsLabel.config(text=defaultValue)
        if 'squawk' in aircraft[0]:
            squawkLabel.config(text=aircraft[0]['squawk'])
        else:
            squawkLabel.config(text=defaultValue)
        if 'rssi' in aircraft[0]:
            signalLabel.config(text=getSignal(aircraft[0]['rssi']))
        else:
            signalLabel.config(text=getSignal(999))
        if 'category' in aircraft[0]:
            try:
                pointerImage = ImageTk.PhotoImage(Image.open('assets/' + str(aircraft[0]['category']) + ".gif").resize((100, 100), Image.ANTIALIAS).convert('RGBA'))
                pointer.configure(image=pointerImage)
                pointer.image = pointerImage
            except Exception as e:
                pointerImage = ImageTk.PhotoImage(Image.open("assets/default.gif").resize((100, 100), Image.ANTIALIAS).convert('RGBA'))
                pointer.configure(image=pointerImage)
                pointer.image = pointerImage
    except Exception as e:
        pass
    root.after(250, update)

update()
root.mainloop()
