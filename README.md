# Automação de detecção de placas e abertura de cancelas com Arduino

Este projeto tem como objetivo detectar placas de veículos usando um modelo de detecção de placas e realizar uma ação de controle com um Arduino ao identificar placas registradas. Ele utiliza a biblioteca Ultralytics YOLO para detectar as placas, EasyOCR para ler o texto das placas, e envia um sinal para o Arduino quando uma placa registrada é detectada.

## Requisitos
Instale o virtualenv, se ainda não estiver instalado:<br>
``` pip install virtualenv ```

Crie um ambiente virtual:<br>
``` python -m venv venv ```

Ative o ambiente virtual (Linux/Mac):<br>
``` source venv/bin/activate ```

Ative o ambiente virtual (Windows):<br>
``` .\venv\Scripts\activate ```

### Instalação das Dependências: 
Certifique-se de ter as bibliotecas necessárias instaladas. Utilize o arquivo requirements.txt para instalar as dependências: <br>
``` pip install -r requirements.txt ```