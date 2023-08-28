import keyboard 
import os
import shutil
import winreg as reg
import time
import subprocess
from AppOpener import open  # Importando uma função "open" de algum módulo personalizado
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Variável para controlar se o VS Code já foi aberto | e abrir ela no futuro
vscode_opened = False

# Classe que herda de FileSystemEventHandler para lidar com eventos de modificação de arquivos
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Verifica se o arquivo modificado tem extensão .py
            autorun()

# Função para obter a pasta de inicialização do usuário no registro do Windows
def get_startup_folder():
    key = reg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    value_name = "Startup"
    with reg.OpenKey(key, subkey) as startup_key:
        return reg.QueryValueEx(startup_key, value_name)[0]

# Função para lidar com eventos de teclado
def keyboard_event_handler(e):
    global vscode_opened
    if e.name == 'home' and e.event_type == 'down' and not vscode_opened:
        vscode_opened = True
        open_app()

# Função para realizar as ações necessárias quando um arquivo Python é modificado
def autorun():
    script_name = "vslogger.pyw"
    startup_folder = get_startup_folder()
    startup_script_path = os.path.join(startup_folder, script_name)
    keyboard.hook(keyboard_event_handler)

    # Verifica se o script de inicialização não existe ou se ele é mais antigo que o script atual
    if not os.path.exists(startup_script_path) or os.path.getmtime(__file__) > os.path.getmtime(startup_script_path):
        shutil.copy(__file__, startup_script_path)  # Copia o próprio script para a pasta de inicialização
        print("Copiando Arquivo para o Startup!\n")
        update_register(startup_script_path)  # Configura o registro para executar o script na inicialização
    else:
        print("Arquivo já existe!\n")

# Função para atualizar o registro do Windows para executar o script na inicialização
def update_register(startup_script_path):
    try:
        command = f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "On_Spirit" /t REG_SZ /d "{startup_script_path}" /f'
        subprocess.run(command, shell=True, check=True)
        print("Registrando Inicialização no Registro!\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao registrar o arquivo!\n {e}")

# Função para abrir o aplicativo Visual Studio Code
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
    
