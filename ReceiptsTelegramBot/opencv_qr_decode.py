import cv2
detector = cv2.QRCodeDetector()

async def decode(image_path):
    '''Decode QRCode from image_path and return data if found, else `raise Exception.`'''
    image = cv2.imread(image_path)
    data, bbox, _ = detector.detectAndDecode(image)
    if bbox is not None:
        return data
    else:
        raise Exception("No QRCode found")