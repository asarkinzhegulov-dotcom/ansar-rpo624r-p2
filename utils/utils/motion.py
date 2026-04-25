import cv2
import numpy as np

class MotionGate:
    def __init__(self, threshold=800, history=120):
        self._threshold = threshold
        self._subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=40,
            detectShadows=False,
        )
        self._consecutive_skips = 0

    def has_motion(self, frame, max_skip=6):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = self._subtractor.apply(gray)
        changed = int(np.count_nonzero(mask))
        if changed >= self._threshold or self._consecutive_skips >= max_skip:
            self._consecutive_skips = 0
            return True
        self._consecutive_skips += 1
        return False
