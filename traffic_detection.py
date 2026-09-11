from collections import Counter
import cv2
from ultralytics import YOLO

MODEL_PATH = "yolo26n.pt"
VIDEO_PATH = "trafficvideo.mp4"

VEHICLE_CLASSES = {"car", "bus", "truck", "motorcycle"}

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError(f"Could not open {VIDEO_PATH}")

MAX_FRAMES = 120
unique_vehicle_ids = set()
vehicle_counts = Counter()
max_vehicle_count = 0
frames_processed = 0

while frames_processed < MAX_FRAMES:
    ok, frame = cap.read()
    if not ok:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="botsort.yaml",
        conf=0.30,
        imgsz=640,
        verbose=False
    )

    result = results[0]
    current_count = 0

    if result.boxes is not None:
        classes = result.boxes.cls.int().cpu().tolist()
        ids = (
            result.boxes.id.int().cpu().tolist()
            if result.boxes.id is not None
            else [None] * len(classes)
        )

        for class_id, track_id in zip(classes, ids):
            name = model.names[class_id]
            if name in VEHICLE_CLASSES:
                current_count += 1
                vehicle_counts[name] += 1
                if track_id is not None:
                    unique_vehicle_ids.add(track_id)

    max_vehicle_count = max(max_vehicle_count, current_count)
    frames_processed += 1

cap.release()

density = (
    "LOW" if max_vehicle_count <= 5
    else "MEDIUM" if max_vehicle_count <= 12
    else "HIGH"
)

print("Frames:", frames_processed)
print("Unique vehicles:", len(unique_vehicle_ids))
print("Peak vehicles:", max_vehicle_count)
print("Vehicle detections:", dict(vehicle_counts))
print("Traffic density:", density)
