"""
Facial Expression Recognition Component (FERC)
Uses FER (Facial Expression Recognition) library to detect emotions from video frames
"""
import cv2
from fer.fer import FER
from config.settings import EMOTICON_MAP


class FacialExpressionRecognizer:
    """Recognizes facial expressions using FER library"""

    def __init__(self):
        """Initialize the FER detector"""
        try:
            # Initialize FER detector with Haar Cascade (faster than MTCNN, less CPU-intensive)
            self.detector = FER(mtcnn=False)
            self.last_emotion = "neutral"
            print("✓ Facial expression recognizer initialized")
        except Exception as e:
            print(f"✗ Error initializing facial expression recognizer: {e}")
            self.detector = None

    def detect_emotion(self, frame):
        """
        Detect emotion from a video frame

        Args:
            frame: OpenCV frame (BGR format)

        Returns:
            str: Detected emotion (e.g., "happy", "sad", etc.)
        """
        if self.detector is None:
            return self.last_emotion

        try:
            # FER works with BGR format (OpenCV default)
            # Detect emotions
            result = self.detector.detect_emotions(frame)

            if result and len(result) > 0:
                # Get emotions for the first detected face
                emotions = result[0]['emotions']

                # Find the emotion with highest score
                max_emotion = max(emotions, key=emotions.get)

                # Map FER emotion names to our standard names
                emotion_map = {
                    'happy': 'happiness',
                    'sad': 'sadness',
                    'angry': 'anger',
                    'surprise': 'surprise',
                    'fear': 'fear',
                    'disgust': 'disgust',
                    'neutral': 'neutral'
                }

                # Update last known emotion
                self.last_emotion = emotion_map.get(max_emotion, 'neutral')

                return self.last_emotion
            else:
                # No face detected, return last known emotion
                return self.last_emotion

        except Exception as e:
            print(f"Error detecting emotion: {e}")
            return self.last_emotion

    def get_emoticon(self, emotion):
        """
        Get emoticon for a given emotion

        Args:
            emotion: Emotion string

        Returns:
            str: Unicode emoticon
        """
        return EMOTICON_MAP.get(emotion, "😐")

    def get_last_emotion(self):
        """Get the last detected emotion"""
        return self.last_emotion
