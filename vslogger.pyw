import keyboard
import os
import shutil
import winreg as reg
import time
import subprocess
from AppOpener import open
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Variável para controlar se o VS Code já foi aberto
vscode_opened = False

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

def keyboard_event_handler(e):
    global vscode_opened
    if e.name == 'home' and e.event_type == 'down' and not vscode_opened:
        vscode_opened = True
        open_app()

def autorun():
    script_name = "vslogger.pyw"
    startup_folder = get_startup_folder()
    startup_script_path = os.path.join(startup_folder, script_name)
    keyboard.hook(keyboard_event_handler)

    if not os.path.exists(startup_script_path) or os.path.getmtime(__file__) > os.path.getmtime(startup_script_path):
        shutil.copy(__file__, startup_script_path)
        print("Copiando Arquivo para o Startup!\n")
        update_register(startup_script_path) # Configura o hook de evento de teclado
    else:
        print("Arquivo já existe!\n")

def update_register(startup_script_path):
    try:
        command = f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "On_Spirit" /t REG_SZ /d "{startup_script_path}" /f'
        subprocess.run(command, shell=True, check=True)
        print("Registrando Inicialização no Registro!\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao registrar o arquivo!\n {e}")

def open_app():
    global vscode_opened
    vscode_opened = False  # Reseta a variável para permitir abrir o VS Code novamente
    open("Visual Studio Code")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=os.path.dirname(os.path.abspath(__file__)))
    observer.start()

    try:
        autorun()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
