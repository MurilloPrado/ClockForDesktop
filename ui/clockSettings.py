import tkinter as tk
from tkinter import ttk
from services.monitorManager import MonitorManager


class ClockSettingsWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Configurações do Relógio")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        self.buildLayout()

    def buildLayout(self):
        container = ttk.Frame(
            self.window,
            padding=20
        )
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Tela de Configurações do Relógio",
            font=("Arial", 14)
        ).pack(pady=(0, 20))

        ttk.Label(
            container,
            text="Aqui ficarão as opções de monitor, tamanho e posição."
        ).pack()