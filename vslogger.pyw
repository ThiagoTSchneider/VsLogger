
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

def get_startup_folder():
   key = reg.HKEY_CURRENT_USER
   subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
   value_name = "Startup"
   with reg.OpenKey(key, subkey) as startup_key:
      return reg.QueryValueEx(startup_key, value_name)[0]

def autorun():
   
   script_name = "vslogger.pyw"
   startup_folder = get_startup_folder()
   startup_script_path = os.path.join(startup_folder, script_name)

   if not os.path.exists(startup_script_path) or os.path.getmtime(__file__) > os.path.getmtime(startup_script_path):
      shutil.copy(__file__, startup_script_path)
      print("Copiando Arquivo para o Startup!\n")
      update_register(startup_script_path)
   else:
      print("Arquivo já existe!\n")

   open_app()

def update_register(startup_script_path):
   try:
      command = f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "On_Spirit" /t REG_SZ /d "{startup_script_path}" /f'
      subprocess.run(command, shell=True, check=True)
      print("Registrando Inicialização no Registro!\n")
   except subprocess.CalledProcessError as e:
      print(f"Erro ao registrar o arquivo!\n {e}")

def open_app():
    time.sleep(2)
    print("Arquivo Atualizado!\n")
    print("Esperando Evento do Teclado...\n")
    while True:
     keyboard.read_event()
     if keyboard.is_pressed('ctrl+home'):
        os.system("start code")
        time.sleep(2)
        os.system("taskkill /im cmd.exe")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=os.path.dirname(os.path.abspath(__file__)))
    observer.start()

    try:
        autorun()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
