import time
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

KEYMAP = {
    "ENTER": "enter",
    "TAB": "tab",
    "ESC": "esc",
    "BACKSPACE": "backspace",
    "SPACE": "space",
    "UP": "up",
    "DOWN": "down",
    "LEFT": "left",
    "RIGHT": "right",
}

def _press_combo(combo: str):
    keys = [k.strip().lower() for k in combo.split("+")]
    pyautogui.hotkey(*keys)

class ActionExecutor:
    """
    PRO executor:
    - clickdan oldin cursor move qiladi (ko‘rinadi)
    - clickdan oldin short focus click (optional) yoki wait
    - scroll direction fix
    """
    def execute(self, actions: list[dict]):
        for a in actions:
            t = a.get("type")

            if t in ("click", "double_click", "right_click"):
                x = int(a.get("x"))
                y = int(a.get("y"))

                # 1) Move first so user can SEE target
                pyautogui.moveTo(x, y, duration=0.15)
                time.sleep(0.05)

                if t == "click":
                    pyautogui.click(x, y)
                elif t == "double_click":
                    pyautogui.doubleClick(x, y)
                else:
                    pyautogui.rightClick(x, y)

            elif t == "type":
                txt = a.get("text", "")
                pyautogui.typewrite(txt, interval=0.01)

            elif t == "press":
                key = (a.get("key") or "").strip()
                if not key:
                    continue
                if "+" in key:
                    _press_combo(key)
                else:
                    pyautogui.press(KEYMAP.get(key.upper(), key.lower()))

            elif t == "scroll":
                dy = int(a.get("dy", 0))
                # model: positive = down, pyautogui: positive = up
                pyautogui.scroll(-dy)

            elif t == "wait":
                ms = int(a.get("ms", 250))
                time.sleep(ms / 1000.0)

            else:
                # unknown action
                pass