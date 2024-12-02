import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

mercosul_plate_mapping = {'I': '1', 
                 'L': '1', 
                 'C': '0',
                 'Q': '0', 
                 'D': '0',
                 'B': '8', 
                 'E': '3', 
                 'T': '1', 
                 'F': '3' }

def parse_mercosul_plate(plate):
    s = list(s)
    for i in [3, 5, 6]:
        if s[i] in mercosul_plate_mapping:
            s[i] = mercosul_plate_mapping[s[i]]
    return ''.join(s)

def read_license_plate(license_plate_crop) -> str | None:
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

    if len(plate[:7]) == 7:
        plate = parse_mercosul_plate()

        # vê se a placa tem formatação brasileira mercosul,
        # como: BRA1C23 
        plate_match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', plate)

        return plate_match.group(0) if plate_match is not None else plate_match
    
    return None
