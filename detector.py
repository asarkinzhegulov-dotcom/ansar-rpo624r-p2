import sys
import time
import argparse
import cv2
from ultralytics import YOLO
from config import DetectorConfig

def build_model(cfg):
    print(f"Loading model: {cfg.model_path} | device={cfg.device}")
    model = YOLO(cfg.model_path)
    model.to(cfg.device)
    return model

def render_boxes(frame, results, cfg):
    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = result.names[cls]
            color = cfg.color_for(cls)
            label = f"{name} {conf:.0%}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, cfg.box_thickness)
            cv2.putText(frame, label, (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_DUPLEX, cfg.font_scale,
                color, 1, cv2.LINE_AA)
            detections.append({"class": name, "conf": round(conf, 3)})
    return detections

def run_stream(model, source, cfg):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Cannot open: {source}")
        sys.exit(1)
    frame_idx = 0
    last_results = None
    fps = 0.0
    inf_ms = 0.0
    t_fps = time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_idx += 1
        t0 = time.perf_counter()
        last_results = model(frame, conf=cfg.confidence,
                             iou=cfg.iou, verbose=False)
        inf_ms = (time.perf_counter() - t0) * 1000
        render_boxes(frame, last_results, cfg)
        now = time.time()
        fps = 1.0 / max(now - t_fps, 1e-9)
        t_fps = now
        info = f"FPS:{fps:.1f} INF:{inf_ms:.1f}ms Q=quit"
        cv2.putText(frame, info, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("YOLOv8 - Ansar Kinzhegulov", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
            break
    cap.release()
    cv2.destroyAllWindows()

def run_image(model, path, cfg):
    frame = cv2.imread(path)
    if frame is None:
        print(f"Cannot read: {path}")
        sys.exit(1)
    results = model(frame, conf=cfg.confidence, iou=cfg.iou)
    dets = render_boxes(frame, results, cfg)
    print(f"Detected {len(dets)} object(s)")
    cv2.imshow("YOLOv8 - Image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="yolov8n.pt")
    p.add_argument("--device", default="cpu")
    p.add_argument("--source", default="webcam")
    p.add_argument("--conf", type=float, default=0.40)
    p.add_argument("--iou", type=float, default=0.50)
    p.add_argument("--export-onnx", action="store_true")
    args = p.parse_args()
    cfg = DetectorConfig(model_path=args.model, device=args.device,
                         confidence=args.conf, iou=args.iou)
    if args.export_onnx:
        YOLO(args.model).export(format="onnx")
        return
    model = build_model(cfg)
    src = args.source.lower()
    if src == "webcam":
        run_stream(model, 0, cfg)
    elif src.endswith((".mp4",".avi",".mov",".mkv")):
        run_stream(model, args.source, cfg)
    elif src.endswith((".jpg",".jpeg",".png",".bmp")):
        run_image(model, args.source, cfg)

if __name__ == "__main__":
    main()
