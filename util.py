import easyocr
import re

reader=easyocr.Reader(['en'],gpu=False)

def read_license_plate(license_plate_crop):
    detections=reader.readtext(license_plate_crop)

    full_text=''
    for detection in detections:
        _,text,_=detection
        full_text+=text.upper().replace(' ', '')     
    
    # brazilian plate regex
    # like RIO1A18
    plate_match=re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}',full_text)
    
    return full_text,(plate_match.group(0))if(plate_match is not None)else(None)