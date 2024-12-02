from ultralytics import YOLO
import cv2
import serial
import time
from util import read_license_plate

REGISTERED_PLATES = ["MAR1A10"]
LICENSE_PLATE_DETECTOR = YOLO('license_plate_detector.pt')

# try catch que garante que a porta do arduíno
# está ativa e conectada à aplicação
try:
    # porta serial que se comunicará ao arduino
    # os parâmetros são, respectivamente,
    # a porta do arduíno que será conectada
    # e a velocidade de transmissão dos dados (baudrate)
    ARDUINO_PORT = serial.Serial("COM3", 9600, timeout=1)

    time.sleep(2)  # aguardar estabilização da conexão
    print("Conexão estabelecida.")

except serial.SerialException as e:
    print(f"Erro na conexão serial: {e}")
    exit(1)
    
# cores RGB utilizadas
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# após deteção da placa, código não enviará sinais
# para o arduino, de forma a evitar sobrecargas
INTERVAL_POST_DETECTION = 5
in_interval = False
last_detection_time = time.time()

CAP = cv2.VideoCapture(0)
ret = True
while ret:
    ret, frame = CAP.read()
    if ret:
        LICENSE_PLATES = LICENSE_PLATE_DETECTOR(frame, verbose=False)[0]
        for license_plate in LICENSE_PLATES.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # evitando erros de valores float ao cortar
            # a região da placa na imagem
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            LICENSE_PLATE_CROP = frame[y1:y2, x1:x2, :]
            LICENSE_PLATE_CROP_GRAY = cv2.cvtColor(LICENSE_PLATE_CROP, 
                                                   cv2.COLOR_BGR2GRAY)

            text = None

            formated_plate, unformatted_plate = read_license_plate(
                LICENSE_PLATE_CROP_GRAY)

            if formated_plate:
                previous_license_plate = formated_plate
                text = formated_plate

            elif unformatted_plate:
                previous_license_plate = unformatted_plate
                text = unformatted_plate

            if text is None:
                text = previous_license_plate
                continue

            PLACA_CADASTRADA = text in REGISTERED_PLATES

            # enviando sinal positivo para leitura do arduíno
            if PLACA_CADASTRADA:
                if not in_interval:
                    ARDUINO_PORT.write(b'1')
                    in_interval = True
                    last_detection_time = time.time()

            COR_DETECCAO = GREEN if PLACA_CADASTRADA else RED

            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, COR_DETECCAO, 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), COR_DETECCAO, 2)

        if in_interval and (time.time() - last_detection_time) > INTERVAL_POST_DETECTION:
            in_interval = False

        cv2.imshow('Câmera', frame)
        if (cv2.waitKey(1) & (0xFF == ord('q'))):
            break

CAP.release()
cv2.destroyAllWindows()
