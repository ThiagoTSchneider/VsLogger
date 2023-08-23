from AppOpener import open
import keyboard
import os
import shutil
import winreg as reg
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#-------------------------------On_Spirit------------------------------#

class MyHandler(FileSystemEventHandler):
      def on_modified(self, event):
         if event.src_path.endswith(".py"):
            autorun()

def autorun():
   
   if not os.path.exists(r"C:\Users\Thiago Schneider\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/vslogger.pyw") or os.path.getmtime(__file__) > os.path.getmtime(r"C:\Users\Thiago Schneider\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/vslogger.pyw"):
      shutil.copy(__file__, r"C:\Users\Thiago Schneider\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/vslogger.pyw")
      print("Copiando Arquivo para o Startup!\n")
      update_register(r"C:\Users\Thiago Schneider\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/vslogger.pyw")
   else:
      print("Arquivo já existe!\n")

   open_app()

def update_register(script_path):
   try:
      command = f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "On_Spirit" /t REG_SZ /d "{script_path}" /f'
      subprocess.run(command, shell=True, check=True)
      print("Registrando Inicialização adcionada no Registro!\n")
   except subprocess.CalledProcessError as e:
      print(f"Erro ao registrar o arquivo!\n {e}")



def open_app():
    time.sleep(2)
    print("Arquivo Atualizado!\n")
    print("Esperando Evento do Teclado...\n")
    while True:
     keyboard.read_event()
     if keyboard.is_pressed('ctrl+home'):
      open("Visual Studio Code", print("Abrindo Visual Studio Code!\n"))

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=os.path.dirname(os.path.abspath(__file__)))
    observer.start()

    try:
        autorun()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()