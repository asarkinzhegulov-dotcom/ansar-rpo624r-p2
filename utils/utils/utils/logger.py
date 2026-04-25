import csv
import time
from pathlib import Path

class DetectionLogger:
    def __init__(self, path="detections.csv"):
        self._path = Path(path)
        self._file = open(self._path, "w", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(
            self._file,
            fieldnames=["timestamp", "frame", "class", "conf",
                        "x1", "y1", "x2", "y2"])
        self._writer.writeheader()
        print(f"Logging to: {self._path}")

    def log(self, frame_idx, detections):
        ts = round(time.time(), 3)
        for d in detections:
            self._writer.writerow(
                {"timestamp": ts, "frame": frame_idx, **d})

    def close(self):
        self._file.flush()
        self._file.close()

class NullLogger:
    def log(self, *a, **kw): pass
    def close(self): pass
