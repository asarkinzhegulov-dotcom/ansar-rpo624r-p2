from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class DetectorConfig:
    model_path: str = "yolov8n.pt"
    device: str = "cpu"
    confidence: float = 0.40
    iou: float = 0.50
    motion_enabled: bool = True
    motion_threshold: int = 800
    max_skip: int = 6
    show_stats: bool = True
    box_thickness: int = 2
    font_scale: float = 0.55
    log_to_csv: bool = False
    log_path: str = "detections.csv"
    palette: Tuple = field(default_factory=lambda: (
        (255, 87, 51),
        (51, 255, 161),
        (51, 161, 255),
        (255, 214, 51),
        (161, 51, 255),
        (51, 255, 87),
        (255, 51, 214),
        (51, 214, 255),
    ))

    def color_for(self, class_id: int):
        return self.palette[class_id % len(self.palette)]
