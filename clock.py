import tkinter as tk
from time import strftime
import time
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

from trayIconManager import TrayIconManager
from ui.clockSettings import ClockSettingsWindow
from services.monitorManager import MonitorManagerService

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
    trayIcon = pystray.Icon("Clock")

    trayManager = TrayIconManager()

    trayIcon.menu = pystray.Menu(
        item("Mostrar / Esconder", showHideWindow),
        item("Configurações", openSettings),
        item("Sair", quitApp)
    )

    def updateTrayIcon():
        while True:
            trayIcon.icon = trayManager.getCurrentFrame()
            time.sleep(60)

    threading.Thread(
        target=updateTrayIcon,
        daemon=True
    ).start()

    trayIcon.run()

def openSettings():
    ClockSettingsWindow(root, selectedMonitorIndex)

# ==========================================================

# janela
root = tk.Tk()
root.title("Clock")

# monitor selecionado
selectedMonitorIndex = 0

# pegar lista de monitores
monitors = MonitorManagerService.getMonitors()

# escolher monitor pelo índice
selectedMonitor = next(
    (monitor for monitor in monitors if monitor["index"] == selectedMonitorIndex),
    monitors[0]
)

x = selectedMonitor["x"] + selectedMonitor["width"] - 200
y = selectedMonitor["y"] + 20

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