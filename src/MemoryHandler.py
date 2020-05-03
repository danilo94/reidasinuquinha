from ctypes import *
from ctypes.wintypes import *
import psutil


PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ  = 0x0010
PROCESS_ALL_ACCESS = 0x001F0FFF

class MemoryHandler(object):

    pid= 0
    openProcess = None
    readProcessMemory = None
    CloseHandle = None
    gerenciadorProcesso = None

    def __init__(self,nomeProcesso):
        for processo in psutil.process_iter():
            if processo.name() == nomeProcesso:
                self.pid = processo.pid
                print("Processo encontrado, inicializando coleta de dados")
                print(self.pid)
                self.conectarProcesso()
                pass

    def conectarProcesso(self):
        self.abrirProcesso = windll.kernel32.OpenProcess
        self.lerMemoriaProcesso = windll.kernel32.ReadProcessMemory
        self.escreverMemoriaProcesso = windll.kernel32.WriteProcessMemory
        self.fecharGerenciador = windll.kernel32.CloseHandle
        self.gerenciadorProcesso = self.abrirProcesso(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ | PROCESS_ALL_ACCESS,False,self.pid)



    def lerPalavra(self,endereco):
        if (self.gerenciadorProcesso!= None):
            buffer = ctypes.c_uint16()
            bytread = ctypes.c_uint16()
            self.lerMemoriaProcesso(self.gerenciadorProcesso,endereco, ctypes.byref(buffer),ctypes.sizeof(buffer),ctypes.byref(bytread))
            return buffer.value
        else:
            print("Gerenciador de processo não foi inicializado, abortando código")
            exit(0)

    def lerByte(self,endereco):
        if (self.gerenciadorProcesso!= None):
            buffer = ctypes.c_ubyte()
            bytread = ctypes.c_ubyte()
            self.lerMemoriaProcesso(self.gerenciadorProcesso,endereco, ctypes.byref(buffer),ctypes.sizeof(buffer),ctypes.byref(bytread))
            return buffer.value
        else:
            print("Gerenciador de processo não foi inicializado, abortando código")
            exit(0)

    def escreverByte(self,endereco,valor):
        if(self.gerenciadorProcesso!=None):
            buffer = ctypes.c_ubyte()
            bytread = ctypes.c_ubyte()
            self.escreverMemoriaProcesso(self.gerenciadorProcesso,endereco,valor,ctypes.sizeof(buffer),ctypes.byref(bytread))
        else:
            print("Gerenciador de processo não foi inicializado, abortando código")
            exit(0)
