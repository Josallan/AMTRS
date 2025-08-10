"""
Face emotion detector using `fer` (which uses a pretrained CNN on FER2013).
Provides a simple wrapper that returns the top emotion label and score for a given cv2 frame.
"""
import cv2
from fer import FER
from src import config

# Initialize global detector once
_detector = None

def get_detector():
    global _detector
    if _detector is None:
        # create detector with mtcnn=False to avoid extra deps; uses a light CNN
        _detector = FER(mtcnn=False)
    return _detector


def detect_emotion_from_frame(frame):
    """Return (emotion_label, score) or (None, 0) if none detected"""
    detector = get_detector()
    # `detect_emotions` expects RGB image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = detector.detect_emotions(rgb)
    if not results:
        return None, 0.0
    # take first face
    face = results[0]
    # emotions is dict: {emotion: score}
    emotions = face.get('emotions', {})
    if not emotions:
        return None, 0.0
    # find top emotion and score
    top_emotion = max(emotions.items(), key=lambda x: x[1])
    label, score = top_emotion
    if score < config.DETECTOR_CONFIDENCE:
        return None, score
    return label, score
