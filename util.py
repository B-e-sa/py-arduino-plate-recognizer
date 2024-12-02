import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

def read_license_plate(license_plate_crop):
    """
    Lê o texto de uma imagem de placa veicular e tenta identificar uma placa no formato brasileiro.

    Args:
        license_plate_crop (str ou ndarray): A imagem contendo a placa veicular.

    Returns:
        tuple: 
            - plate (str): A placa detectada na imagem, se ela estiver formatada no padrão Mercosul.
            - unformatted_plate (str ou None): A placa detectada se ela tiver 7 carácteres, mas não estiver no padrão Mercosul.
    """
    detections = reader.readtext(license_plate_crop)

    # as deteccões de frases/caracteres sao feitas em partes,
    # então elas são unidos no loop
    plate = ''
    for detection in detections:
        _, text, _ = detection
        plate += text.upper().replace(' ', '')

    # vê se a placa tem formatação brasileira mercosul,
    # como: BRA1C23 
    plate_match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', plate)

    return (plate_match.group(0)) if (plate_match is not None) else None, plate
