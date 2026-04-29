import tkinter as tk
from tkinter import ttk
from services.monitorManager import MonitorManagerService


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

        # título
        titleLabel = tk.Label(
            self.window,
            text="Escolha o monitor do relógio",
            font=("Arial", 12)
        )
        titleLabel.pack(pady=(0, 20))

        # buscar monitores
        self.monitors = MonitorManagerService.getMonitors()

        # montar lista de exibição
        monitorOptions = []

        for monitor in self.monitors:
            label = (
                f'Monitor {monitor["index"] + 1} '
                f'- {monitor["width"]}x{monitor["height"]}'
            )
            monitorOptions.append(label)

        # variável do combobox
        self.selectedMonitor = tk.StringVar()

        # combobox
        self.monitorCombobox = ttk.Combobox(
            self.window,
            textvariable=self.selectedMonitor,
            values=monitorOptions,
            state="readonly",
            width=35
        )
        self.monitorCombobox.pack(pady=10)

        # selecionar primeiro monitor por padrão
        if monitorOptions:
            self.monitorCombobox.current(0)

        # botão salvar
        saveButton = tk.Button(
            self.window,
            text="Salvar",
            command=self.saveSettings
        )
        saveButton.pack(pady=20)

    def saveSettings(self):
        selectedIndex = self.monitorCombobox.current()

        selectedMonitor = self.monitors[selectedIndex]

        x = selectedMonitor["x"] + selectedMonitor["width"] - 200
        y = selectedMonitor["y"] + 20

        self.root.geometry(f"+{x}+{y}")

    
    def loadMonitors(self):
        self.monitors = MonitorManagerService.getMonitors()

        monitorLabels = []

        for monitor in self.monitors:
            label = (
                f"Monitor {monitor['index'] + 1} | "
                f"{monitor['width']}x{monitor['height']} | "
                f"{monitor['name']}"
            )

            if monitor["isPrimary"]:
                label += " (Principal)"

            monitorLabels.append(label)

        self.monitorSelect["values"] = monitorLabels

        if monitorLabels:
            self.monitorSelect.current(0)