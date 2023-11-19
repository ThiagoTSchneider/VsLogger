# 🚀 Monitoramento Automático de Scripts Python e Inicialização no Windows

Este repositório contém um script Python chamado `vslogger.pyw` que oferece funcionalidades para monitorar automaticamente arquivos Python (.py) em um diretório específico e realizar ações quando esses arquivos são modificados. Além disso, o script facilita a adição automática do seu próprio script à inicialização do Windows, garantindo que seja executado sempre que o usuário fizer login.

## Funcionalidades Principais 🛠️

1. **Monitoramento de Arquivos Python:**
   - O script usa a biblioteca `watchdog` para monitorar mudanças em arquivos Python no diretório do próprio script.

2. **Configuração de Inicialização Automática:**
   - Ao detectar uma modificação em um arquivo Python, o script verifica se deve ser copiado para a pasta de inicialização do usuário no registro do Windows, permitindo a execução automática na inicialização do sistema.

3. **Manipulação de Eventos de Teclado:**
   - O script também inclui um manipulador de eventos de teclado que, quando acionado por uma combinação específica (por exemplo, pressionando a tecla 'home'), abre o Visual Studio Code.

4. **Abrir o Visual Studio Code:**
   - Uma função está incluída para abrir o Visual Studio Code automaticamente.

## Requisitos e Dependências 📦

Para utilizar este script, é necessário ter as seguintes bibliotecas Python instaladas:

```bash
pip install keyboard
pip install watchdog
pip install AppOpener
```
Certifique-se de ter as permissões necessárias para modificar o registro do Windows e a pasta de inicialização.

Utilização ▶️

Clone este repositório para o seu ambiente local.
Instale as dependências usando o comando acima.
Execute o script Python:
```bash
python vslogger.pyw
```
Observação: Este script presume a existência de um módulo chamado AppOpener e pode exigir modificações adicionais dependendo do seu ambiente.
