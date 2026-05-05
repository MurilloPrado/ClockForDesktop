import tkinter as tk
from time import strftime
import time
import threading
import pystray
from pystray import MenuItem as item

from services.colorManager import ColorManager
from services.trayIconManager import TrayIconManager
from ui.clockSettings import ClockSettingsWindow
from services.monitorManager import MonitorManagerService
from services.positionManager import ClockPositionManager
from services.configManager import ConfigManager

# =================== UTILS =====================

config = ConfigManager.load()

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
    ClockSettingsWindow(root, selectedMonitorIndex, label)

# ==========================================================

# janela
root = tk.Tk()
root.title("Clock")

# configurações iniciais
selectedMonitorIndex = config["monitorIndex"]
selectedPosition = config["position"]
selectedBgColor = config["bgColor"]
selectedFgColor = config["fgColor"]

# pegar lista de monitores
monitors = MonitorManagerService.getMonitors()

# escolher monitor pelo índice
selectedMonitor = next(
    (monitor for monitor in monitors if monitor["index"] == selectedMonitorIndex),
    monitors[0]
)

# posição do relógio
x, y = ClockPositionManager.getClockPosition(   
    selectedMonitor,
    selectedPosition
)

# sempre no topo
root.attributes("-topmost", True)

# posição da janela
root.geometry(f"+{x}+{y}")

appearance = ColorManager.getColors(
    selectedBgColor,
    selectedFgColor,
)

# remove borda
root.overrideredirect(True)

root.configure(bg="black")

# transparência
if appearance["transparent"]:
    root.attributes("-transparentcolor", "black")

label = tk.Label(
    root,   
    font=("Arial", 30),
    bg="black" if appearance["transparent"] else appearance["bg"],
    fg=appearance["fg"]
)

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