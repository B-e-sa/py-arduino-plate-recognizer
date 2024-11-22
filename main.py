from ultralytics import YOLO
import cv2
from util import read_license_plate

placas_cadastradas = [""]
license_plate_detector = YOLO('license_plate_detector.pt')
cap = cv2.VideoCapture(0)
ret = True
previous_license_plate = ""
while ret:
    ret, frame = cap.read()
    if ret:
        license_plates = license_plate_detector(frame, verbose=False)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            license_plate_crop = frame[y1:y2, x1:x2, :]
            license_plate_crop_gray = cv2.cvtColor(
                license_plate_crop, cv2.COLOR_BGR2GRAY)

            ambiguous_license_plate_text, correct_license_plate_text = read_license_plate(
                license_plate_crop_gray)

            text = None
            if correct_license_plate_text:
                previous_license_plate = correct_license_plate_text
                text = correct_license_plate_text
            if len(ambiguous_license_plate_text) == 7:
                previous_license_plate = ambiguous_license_plate_text
                text = ambiguous_license_plate_text
            if text is None:
                text = previous_license_plate

            cv2.putText(frame, text, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        cv2.imshow('Câmera', frame)
        if (cv2.waitKey(1) & (0xFF == ord('q'))):
            break
cap.release()
cv2.destroyAllWindows()
