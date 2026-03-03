from mss import mss
from PIL import Image

class ScreenCapture:
    def __init__(self, monitor_index: int = 1):
        self.sct = mss()
        self.monitor_index = monitor_index

    def grab(self) -> Image.Image:
        mon = self.sct.monitors[self.monitor_index]  # 1 = primary
        shot = self.sct.grab(mon)
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        return img