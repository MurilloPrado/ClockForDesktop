from screeninfo import get_monitors

class MonitorManagerService:
    @staticmethod
    def getMonitors():
        monitors = get_monitors()
        result = []

        for index, monitor in enumerate(monitors):
            result.append({
                "index": index,
                "name": monitor.name,
                "width": monitor.width,
                "height": monitor.height,
                "x": monitor.x,
                "y": monitor.y,
                "isPrimary": monitor.is_primary
            })

        return result