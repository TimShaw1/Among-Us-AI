import time
import vgamepad as vg

gamepad = vg.VX360Gamepad()
time.sleep(1)

gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
gamepad.update()
time.sleep(0.5)
gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
gamepad.update()