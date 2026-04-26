from datetime import datetime
from PIL import Image

class TrayIconManager:
    def __init__(self):
        self.iconFrames = []
        self.loadIcons()

    def loadIcons(self):
        for i in range(1, 65):
            fileName = f"icons/{i:02}.png"
            image = Image.open(fileName)
            self.iconFrames.append(image)

    def getCurrentFrame(self):
        now = datetime.now()

        hour = now.hour
        minute = now.minute

        # converte horário atual para minutos totais
        totalMinutes = (hour * 60) + minute

        # desloca o relógio para começar ao meio-dia
        shiftedMinutes = (totalMinutes - 720) % 1440

        frameIndex = int(shiftedMinutes / 22.5)

        if frameIndex >= 64:
            frameIndex = 63

        return self.iconFrames[frameIndex]