"""
Demo entrypoint: captures frames from webcam, detects emotion, maps emotion to a query and opens playlist.
"""
import cv2
from src.face_emotion import detect_emotion_from_frame
from src.music_recommender import MusicRecommender
from src import config
import time

EMOTION_QUERY_MAP = {
    'happy': 'happy vibe playlist',
    'sad': 'calm relaxing playlist',
    'angry': 'high BPM motivating music',
    'fear': 'calming ambient music',
    'surprise': 'upbeat playlist',
    'neutral': 'chill instrumental playlist',
    'disgust': 'instrumental playlist'
}


def main():
    rec = MusicRecommender()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Error: webcam not available')
        return

    detections = 0
    print('Press q to quit')
    while detections < config.MAX_DETECTIONS:
        ret, frame = cap.read()
        if not ret:
            print('Failed to capture frame')
            break
        label, score = detect_emotion_from_frame(frame)
        if label:
            print(f'Detected {label} with score {score:.2f}')
            query = EMOTION_QUERY_MAP.get(label, label + ' playlist')
            uri = rec.search_playlist(query)
            if uri:
                rec.open_playlist_in_browser(uri)
                detections += 1
                # small delay to avoid spamming
                time.sleep(2)
        # show frame (resized) to user
        cv2.imshow('AMTRS - Press q to quit', cv2.resize(frame, (640,360)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
