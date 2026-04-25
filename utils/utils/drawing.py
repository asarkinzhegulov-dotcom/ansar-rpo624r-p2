import cv2

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
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_DUPLEX, cfg.font_scale, 1)
            cv2.rectangle(frame,
                (x1, y1 - th - 8), (x1 + tw + 4, y1),
                color, -1)
            cv2.rectangle(frame,
                (x1, y1), (x2, y2),
                color, cfg.box_thickness)
            cv2.putText(frame, label,
                (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_DUPLEX,
                cfg.font_scale,
                (10, 10, 10), 1, cv2.LINE_AA)
            detections.append({
                "class": name,
                "conf": round(conf, 3),
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            })
    return detections

def render_hud(frame, fps, inf_ms, total_det, cfg):
    if not cfg.show_stats:
        return
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - 38), (w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    line = (f"FPS:{fps:.1f} | "
            f"Inference:{inf_ms:.1f}ms | "
            f"Objects:{total_det} | Q=quit")
    cv2.putText(frame, line, (10, h - 12),
        cv2.FONT_HERSHEY_SIMPLEX, 0.48,
        (200, 230, 200), 1, cv2.LINE_AA)
