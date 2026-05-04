import tkinter as tk
from tkinter import ttk
from services.monitorManager import MonitorManagerService
from services.positionManager import ClockPositionManager
from services.colorManager import ColorManager


class ClockSettingsWindow:
    def __init__(self, root, selectedMonitorIndex):
        self.window = tk.Toplevel()
        self.window.title("Configurações do Relógio")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        self.root = root
        self.currentMonitorIndex = selectedMonitorIndex

        self.buildLayout()

    def buildLayout(self):
        container = ttk.Frame(
            self.window,
            padding=20
        )
        container.pack(fill="both", expand=True)

        # =========================
        # MONITOR 
        # =========================
        monitorLabel = tk.Label(
            self.window,
            text="Monitor"
        )
        monitorLabel.pack(pady=(20, 5))

        self.monitorCombobox = ttk.Combobox(
            self.window,
            state="readonly",
            width=35
        )
        self.monitorCombobox.pack()

        self.loadMonitors()
        
        # =========================
        # POSITION
        # =========================
        positionLabel = tk.Label(
            self.window,
            text="Posição"
        )
        positionLabel.pack(pady=(20, 5))

        self.positionMap = {
            "Superior Esquerdo": "topLeft",
            "Superior Direito": "topRight",
            "Inferior Esquerdo": "bottomLeft",
            "Inferior Direito": "bottomRight"
        }

        self.positionCombobox = ttk.Combobox(
            self.window,
            values=list(self.positionMap.keys()),
            state="readonly",
            width=35
        )
        self.positionCombobox.pack()

        self.positionCombobox.current(1)  # Superior Direito

        # =========================
        # COLORS
        # =========================
        # cor da fonte
        colorLabel = tk.Label(
            self.window,
            text="Cor da fonte"
        )
        colorLabel.pack(pady=(20, 5))

        self.colorMap = {
            "Branco": "white",
            "Preto": "black",
            "Vermelho": "red",
            "Verde": "green",
            "Azul": "blue"
        }

        self.colorCombobox = ttk.Combobox(
            self.window,
            values=list(self.colorMap.keys()),
            state="readonly",
            width=35
        )
        self.colorCombobox.pack()
        self.colorCombobox.current(0)

        # cor de fundo
        bgColorLabel = tk.Label(
            self.window,
            text="Cor de fundo"
        )
        bgColorLabel.pack(pady=(20, 5))

        self.bgColorMap = {
            "None": None,
            "Preto": "black",
            "Branco": "white",
            "Cinza": "gray",
            "Azul Escuro": "#1e1e1e"
        }

        self.bgColorCombobox = ttk.Combobox(
            self.window,
            values=list(self.bgColorMap.keys()),
            state="readonly",
            width=35
        )
        self.bgColorCombobox.pack()
        self.bgColorCombobox.current(0)

        # =========================
        # SAVE BUTTON
        # =========================
        saveButton = tk.Button(
            self.window,
            text="Salvar",
            command=self.saveSettings
        )
        saveButton.pack(pady=30)


    def saveSettings(self):
        # Monitor e posição
        selectedMonitorIndex = self.monitorCombobox.current()

        selectedPositionLabel = self.positionCombobox.get()
        selectedPosition = self.positionMap[selectedPositionLabel]
        selectedMonitor = self.monitors[selectedMonitorIndex]

        x, y = ClockPositionManager.getClockPosition(
            selectedMonitor,
            selectedPosition
        )

        self.root.geometry(f"+{x}+{y}")

        # Colors
        selectedBgColor = self.bgColorMap[self.bgColorCombobox.get()]
        selectedFgColor = self.colorMap[self.colorCombobox.get()]

        appearance = ColorManager.getColors(
            selectedBgColor,
            selectedFgColor
        )

        self.root.children['!label'].config(
            fg=appearance["fg"],
            bg=self.root["bg"] if appearance["transparent"] else appearance["bg"]
        )

        if appearance["transparent"]:
            self.root.attributes("-transparentcolor", self.root["bg"])
        else:
            self.root.attributes("-transparentcolor", "")

    
    def loadMonitors(self):
        self.monitors = MonitorManagerService.getMonitors()

        monitorOptions = []

        for monitor in self.monitors:
            label = (
                f'Monitor {monitor["index"] + 1} '
                f'- {monitor["width"]}x{monitor["height"]}'
            )

            if monitor["isPrimary"]:
                label += " (Principal)"

            monitorOptions.append(label)

        self.monitorCombobox["values"] = monitorOptions

        if monitorOptions:
            self.monitorCombobox.current(self.currentMonitorIndex)