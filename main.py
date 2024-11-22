from ultralytics import YOLO
import cv2
import serial
from util import read_license_plate

PLACAS_CADASTRADAS = [""]
LICENSE_PLATE_DETECTOR = YOLO('license_plate_detector.pt')
ARDUINO_PORT = serial.Serial("COM3", 9600)
CAP = cv2.VideoCapture(0)
ret = True
previous_license_plate = ""
while ret:
    ret, frame = CAP.read()
    if ret:
        LICENSE_PLATES = LICENSE_PLATE_DETECTOR(frame, verbose=False)[0]
        for license_plate in LICENSE_PLATES.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            LICENSE_PLATE_CROP = frame[y1:y2, x1:x2, :]
            LICENSE_PLATE_CROP_GRAY = cv2.cvtColor(
                LICENSE_PLATE_CROP, cv2.COLOR_BGR2GRAY)

            ambiguous_license_plate_text, correct_license_plate_text = read_license_plate(
                LICENSE_PLATE_CROP_GRAY)

            text = None
            if correct_license_plate_text:
                previous_license_plate = correct_license_plate_text
                text = correct_license_plate_text
            if len(ambiguous_license_plate_text) == 7:
                previous_license_plate = ambiguous_license_plate_text
                text = ambiguous_license_plate_text
            if text is None:
                text = previous_license_plate

            if text in PLACAS_CADASTRADAS:
                ARDUINO_PORT.write(b'1')
            else:
                ARDUINO_PORT.write(b'0')

            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        cv2.imshow('Câmera', frame)
        if (cv2.waitKey(1) & (0xFF == ord('q'))):
            break
CAP.release()
cv2.destroyAllWindows()
