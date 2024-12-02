# Automação de detecção de placas e abertura de cancelas com Arduino

Este projeto tem como objetivo detectar placas de veículos usando um modelo de detecção de placas e realizar uma ação de controle com um Arduino ao identificar placas registradas. Ele utiliza a biblioteca Ultralytics YOLO para detectar as placas, EasyOCR para ler o texto das placas, e envia um sinal para o Arduino quando uma placa registrada é detectada.

## Requisitos


bash
Copy code
pip install ultralytics opencv-python pyserial easyocr
Além disso, é necessário ter o arquivo do modelo de detecção license_plate_detector.pt, que deve ser baixado ou treinado, e o arquivo read_license_plate.py para leitura da placa.

Como Funciona
O sistema usa uma câmera conectada ao computador para capturar imagens em tempo real.
A cada frame, o modelo YOLO tenta identificar regiões de placas de veículos.
A região da placa é recortada e enviada para o EasyOCR para extração do texto.
O texto detectado é comparado com uma lista de placas registradas.
Se a placa detectada estiver na lista, o sistema envia um sinal via porta serial para o Arduino (para qualquer ação desejada, como abrir um portão).
O processo é repetido continuamente até que o usuário finalize a execução pressionando a tecla q.
Estrutura do Código
1. Detecção da Placa de Veículo
A detecção das placas é feita usando o modelo YOLO, carregado com YOLO('license_plate_detector.pt').
Cada placa detectada é então recortada da imagem e processada para leitura do texto.
2. Leitura da Placa
O texto da placa é extraído usando EasyOCR e comparado com um conjunto de placas registradas.
O código tenta primeiro encontrar uma placa no formato Mercosul (exemplo: BRA1C23), caso contrário, ele tenta uma correspondência de 7 caracteres (exemplo: RIO9A27).
3. Integração com o Arduino
Se uma placa registrada for detectada, um sinal ('1') é enviado ao Arduino via porta serial.
O sistema não envia múltiplos sinais consecutivos para evitar sobrecarga, utilizando um intervalo de tempo de 5 segundos após cada detecção bem-sucedida.