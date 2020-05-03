from KeyHardwareInput import *
from time import *
from Enderecos import *
class keyController(object):

    def __init__(self):
        pass


    def pressionar(self,tecla,tempo):

        if (tecla==0):
            self.pressKey(S)
            sleep(tempo)
            self.releaseKey(S)
        if (tecla==1):
            self.pressKey(A)
            sleep(tempo)
            self.releaseKey(A)
        if (tecla==2):
            self.pressKey(F4)
            sleep(tempo)
            self.releaseKey(F4)


    def pressKey(self,hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def releaseKey(self,hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                            ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
