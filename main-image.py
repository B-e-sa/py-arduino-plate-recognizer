from ultralytics import YOLO
import cv2
from util import read_license_plate

REGISTERED_PLATES = ["MAR1A10"]
LICENSE_PLATE_DETECTOR = YOLO('license_plate_detector.pt')
    
RED = (255, 0, 0)
GREEN = (0, 255, 0)

frame = cv2.imread("placa-1.png")
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
    
    found_plate = read_license_plate(LICENSE_PLATE_CROP_GRAY)

    if found_plate:
        previous_license_plate = found_plate
        text = found_plate

    if text is None:
        text = previous_license_plate
        continue

    PLACA_CADASTRADA = text in REGISTERED_PLATES

    COR_DETECCAO = GREEN if PLACA_CADASTRADA else RED

    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, COR_DETECCAO, 2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), COR_DETECCAO, 2)

cv2.imshow('Câmera', frame)
