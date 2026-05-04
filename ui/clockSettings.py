import tkinter as tk
from tkinter import ttk
from services.configManager import ConfigManager
from services.monitorManager import MonitorManagerService
from services.positionManager import ClockPositionManager
from services.colorManager import ColorManager


class ClockSettingsWindow:
    def __init__(self, root, selectedMonitorIndex, label):
        self.window = tk.Toplevel()
        self.window.title("Configurações do Relógio")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        self.root = root
        self.currentMonitorIndex = selectedMonitorIndex
        self.label = label

        self.buildLayout()

    def buildLayout(self):
        # container principal
        mainFrame = ttk.Frame(self.window)
        mainFrame.pack(fill="both", expand=True)

        # canvas
        canvas = tk.Canvas(mainFrame, borderwidth=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(
            mainFrame,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # frame interno (conteúdo)
        self.container = ttk.Frame(canvas, padding=20)

        # coloca frame dentro do canvas
        canvas.create_window((0, 0), window=self.container, anchor="n")

        def onCanvasConfigure(event):
            # Ajusta a largura da janela interna para ser igual à do canvas
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", onCanvasConfigure)
        # Armazene o ID da janela para referência:
        canvas_window = canvas.create_window((0, 0), window=self.container, anchor="nw")

        # ajusta scroll automático
        def onConfigure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.container.bind("<Configure>", onConfigure)

        def onMouseWheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", onMouseWheel)

        # =========================
        # MONITOR 
        # =========================
        monitorLabel = tk.Label(
            self.container,
            text="Monitor"
        )
        monitorLabel.pack(pady=(10, 5))

        self.monitorCombobox = ttk.Combobox(
            self.container,
            state="readonly",
            width=35
        )
        self.monitorCombobox.pack()

        self.loadMonitors()
        
        # =========================
        # POSITION
        # =========================
        positionLabel = tk.Label(
            self.container,
            text="Posição"
        )
        positionLabel.pack(pady=(10, 5))

        self.positionMap = {
            "Superior Esquerdo": "topLeft",
            "Superior Direito": "topRight",
            "Inferior Esquerdo": "bottomLeft",
            "Inferior Direito": "bottomRight"
        }

        self.positionCombobox = ttk.Combobox(
            self.container,
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
            self.container,
            text="Cor da fonte"
        )
        colorLabel.pack(pady=(10, 5))

        self.colorMap = {
            "Branco": "white",
            "Preto": "black",
            "Vermelho": "red",
            "Verde": "green",
            "Azul": "blue"
        }

        self.colorCombobox = ttk.Combobox(
            self.container,
            values=list(self.colorMap.keys()),
            state="readonly",
            width=35
        )
        self.colorCombobox.pack()
        self.colorCombobox.current(0)

        # cor de fundo
        bgColorLabel = tk.Label(
            self.container,
            text="Cor de fundo"
        )
        bgColorLabel.pack(pady=(10, 5))

        self.bgColorMap = {
            "None": None,
            "Preto": "black",
            "Branco": "white",
            "Cinza": "gray",
            "Azul Escuro": "#1e1e1e"
        }

        self.bgColorCombobox = ttk.Combobox(
            self.container,
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
            self.container,
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

        self.label.config(
            fg=appearance["fg"],
            bg=self.root["bg"] if appearance["transparent"] else appearance["bg"]
        )

        if appearance["transparent"]:
            self.root.attributes("-transparentcolor", self.root["bg"])
        else:
            self.root.attributes("-transparentcolor", "")

        # Salvar configurações
        ConfigManager.save({
            "monitorIndex": selectedMonitorIndex,
            "position": selectedPosition,
            "bgColor": selectedBgColor,
            "fgColor": selectedFgColor
        })

    
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