#!/data/data/com.termux/files/usr/bin/python
"""
EDGE-VISION — Deteksi Objek Offline
Mode: YOLO Tiny | Tanpa Internet | Real-time
"""

import os
import sys
from datetime import datetime

try:
    import cv2
    import numpy as np
except ImportError:
    print("❌ OpenCV tidak terinstall.")
    print("Jalankan: pkg install opencv-python -y")
    sys.exit(1)

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
MODEL_PATH = os.path.expanduser("~/kosmik/vision")

CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]

def check_model():
    weights = os.path.join(MODEL_PATH, "yolov4-tiny.weights")
    config = os.path.join(MODEL_PATH, "yolov4-tiny.cfg")
    if not os.path.exists(weights) or not os.path.exists(config):
        print("\n❌ Model YOLO tidak ditemukan.")
        print(f"Letakkan file di: {MODEL_PATH}")
        print("Download:")
        print("  cd ~/kosmik/vision")
        print("  wget -O yolov4-tiny.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights")
        print("  wget -O yolov4-tiny.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg")
        return False
    return True

def detect_objects(frame, net, output_layers):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    
    boxes, confidences, class_ids = [], [], []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE_THRESHOLD:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    results = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            results.append({
                'class': CLASSES[class_ids[i]],
                'confidence': confidences[i],
                'box': (x, y, w, h)
            })
    return results

def draw_results(frame, results):
    for res in results:
        x, y, w, h = res['box']
        label = f"{res['class']}: {res['confidence']:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def main():
    print("\n" + "="*50)
    print("📡 EDGE-VISION — DETEKSI OBJEK OFFLINE")
    print("="*50)
    print("  [1] Deteksi dari Kamera")
    print("  [2] Deteksi dari Gambar")
    print("  [3] Exit")
    print("="*50)
    
    if not check_model():
        return
    
    weights = os.path.join(MODEL_PATH, "yolov4-tiny.weights")
    config = os.path.join(MODEL_PATH, "yolov4-tiny.cfg")
    net = cv2.dnn.readNet(weights, config)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    
    choice = input("\nPilih mode (1-3): ").strip()
    
    if choice == "1":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Gagal akses kamera.")
            return
        print("📸 Kamera aktif. Tekan 'q' untuk keluar.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = detect_objects(frame, net, output_layers)
            frame = draw_results(frame, results)
            cv2.imshow("Edge-Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    
    elif choice == "2":
        img_path = input("📂 Path gambar: ").strip()
        if not os.path.exists(img_path):
            print("❌ File tidak ditemukan.")
            return
        frame = cv2.imread(img_path)
        results = detect_objects(frame, net, output_layers)
        frame = draw_results(frame, results)
        output_path = f"output_{datetime.now().strftime('%H%M%S')}.jpg"
        cv2.imwrite(output_path, frame)
        print(f"✅ Hasil: {output_path}")
        print(f"📊 {len(results)} objek terdeteksi")
        for res in results:
            print(f"  → {res['class']} ({res['confidence']:.2f})")
    
    else:
        print("👋 Sampai jumpa!")

if __name__ == "__main__":
    main()
