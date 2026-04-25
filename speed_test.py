import argparse
import os
import time
import statistics
import json
import cv2
import numpy as np
from ultralytics import YOLO

def measure(model_path, frame, runs, warmup, device):
    model = YOLO(model_path)
    model.to(device)
    print(f"Warmup {model_path}...")
    for _ in range(warmup):
        model(frame, verbose=False)
    times = []
    for i in range(runs):
        t0 = time.perf_counter()
        model(frame, verbose=False)
        times.append((time.perf_counter() - t0) * 1000)
    return {
        "model": os.path.basename(model_path),
        "mean_ms": round(statistics.mean(times), 2),
        "median_ms": round(statistics.median(times), 2),
        "std_ms": round(statistics.stdev(times), 2),
        "min_ms": round(min(times), 2),
        "max_ms": round(max(times), 2),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="yolov8n.pt")
    p.add_argument("--image", default=None)
    p.add_argument("--device", default="cpu")
    p.add_argument("--runs", type=int, default=50)
    p.add_argument("--warmup", type=int, default=10)
    args = p.parse_args()

    if args.image and os.path.exists(args.image):
        frame = cv2.imread(args.image)
    else:
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print("Using synthetic frame 640x480")

    pt = measure(args.model, frame, args.runs, args.warmup, args.device)

    onnx_path = args.model.replace(".pt", ".onnx")
    if not os.path.exists(onnx_path):
        YOLO(args.model).export(format="onnx")

    onnx = measure(onnx_path, frame, args.runs, args.warmup, args.device)
    speedup = pt["mean_ms"] / max(onnx["mean_ms"], 0.001)

    print(f"\n{'='*50}")
    print(f"PyTorch : {pt['mean_ms']} ms (mean)")
    print(f"ONNX    : {onnx['mean_ms']} ms (mean)")
    print(f"Speedup : {speedup:.2f}x")
    print(f"{'='*50}")

    with open("benchmark_results.json", "w") as f:
        json.dump({"pytorch": pt, "onnx": onnx,
                   "speedup": round(speedup, 3)}, f, indent=2)
    print("Saved: benchmark_results.json")

if __name__ == "__main__":
    main()
