import tkinter as tk
from time import strftime
from screeninfo import get_monitors
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# =================== UTILS =====================

def updateTime():
    time_string = strftime('%H:%M:%S')
    label.config(text=time_string)
    label.after(1000, updateTime)

def showHideWindow(icon, menuItem):
    # verifica se a janela está escondida
    if root.state() == "withdrawn":
        root.deiconify()  # mostra novamente
    else:
        root.withdraw()   # esconde

def quitApp(icon, menuItem):
    icon.stop()
    root.quit()
    root.destroy()

def createTrayIcon():
    # ícone simples preto com quadrado branco
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")

    trayIcon = pystray.Icon(
        "Clock",
        image,
        "Digital Clock",
        menu=pystray.Menu(
            item("Mostrar / Esconder", showHideWindow),
            item("Sair", quitApp)
        )
    )

    trayIcon.run()

# ==========================================================

# janela
root = tk.Tk()
root.title("Clock")

# pegar o monitor 1 (DISPLAY1)
monitors = get_monitors()
monitor1 = next(m for m in monitors if m.name == '\\\\.\\DISPLAY1')

x = monitor1.x + monitor1.width - 200
y = monitor1.y + 20

# remove borda
root.overrideredirect(True)

# sempre no topo
root.attributes("-topmost", True)

# posição (ajuste aqui)
root.geometry(f"+{x}+{y}")

label = tk.Label(root, font=("Arial", 30), bg="black", fg="white")
label.pack()


# inicia atualização da hora
updateTime()

# inicia tray em thread separada
trayThread = threading.Thread(
    target=createTrayIcon,
    daemon=True
)
trayThread.start()

root.mainloop()