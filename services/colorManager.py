class ColorManager:
    @staticmethod
    def getColors(bgColor, fgColor):
        return {
            "bg": bgColor,
            "fg": fgColor,
            "transparent": bgColor is None
        }