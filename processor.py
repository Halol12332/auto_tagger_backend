import cv2
import numpy as np
from ultralytics import YOLO
import base64
from rembg import remove

model = None

def process_image(image_bytes):
    global model
    
    if model is None:
        model = YOLO('yolov8n.pt')

    # 1. AI Classification
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model.predict(source=img, save=False, conf=0.5)
    result = results[0]
    
    if len(result.boxes) == 0:
        return None, None

    detected_labels = list(set([result.names[int(box.cls[0])] for box in result.boxes]))
    primary_label = detected_labels[0]
    conf = float(result.boxes[0].conf[0])

    # 2. Studio Polish
    output_bytes = remove(image_bytes)
    encoded_img = base64.b64encode(output_bytes).decode('utf-8')

    return {
        "label": primary_label, 
        "confidence": conf,
        "all_labels": detected_labels
    }, encoded_img
