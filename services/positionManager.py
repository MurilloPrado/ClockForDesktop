class ClockPositionManager:
    @staticmethod
    def getClockPosition(monitor, position):
        margin = 20
        clockWidth = 200
        clockHeight = 60

        if position == "topLeft":
            x = monitor["x"] + margin
            y = monitor["y"] + margin

        elif position == "topRight":
            x = monitor["x"] + monitor["width"] - clockWidth - margin
            y = monitor["y"] + margin

        elif position == "bottomLeft":
            x = monitor["x"] + margin
            y = monitor["y"] + monitor["height"] - clockHeight - margin

        elif position == "bottomRight":
            x = monitor["x"] + monitor["width"] - clockWidth - margin
            y = monitor["y"] + monitor["height"] - clockHeight - margin

        else:
            x = monitor["x"] + margin
            y = monitor["y"] + margin

        return x, y