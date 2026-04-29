import tkinter as tk
from tkinter import ttk
from services.monitorManager import MonitorManagerService
from services.positionManager import ClockPositionManager


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
            text="Escolha o monitor"
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
            text="Escolha a posição"
        )
        positionLabel.pack(pady=(20, 5))

        self.positionMap = {
            "Topo Esquerdo": "topLeft",
            "Topo Direito": "topRight",
            "Baixo Esquerdo": "bottomLeft",
            "Baixo Direito": "bottomRight"
        }

        self.positionCombobox = ttk.Combobox(
            self.window,
            values=list(self.positionMap.keys()),
            state="readonly",
            width=35
        )
        self.positionCombobox.pack()

        self.positionCombobox.current(1)  # Topo Direito

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
        selectedMonitorIndex = self.monitorCombobox.current()

        selectedPositionLabel = self.positionCombobox.get()
        selectedPosition = self.positionMap[selectedPositionLabel]
        selectedMonitor = self.monitors[selectedMonitorIndex]

        print("Monitor:", selectedMonitorIndex)
        print("Position:", selectedPosition)

        x, y = ClockPositionManager.getClockPosition(
            selectedMonitor,
            selectedPosition
        )

        self.root.geometry(f"+{x}+{y}")

    
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