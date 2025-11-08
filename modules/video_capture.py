"""
Video Capture Module
Captures video from webcam or other video sources
"""
import cv2
import threading
import time


class VideoCapture:
    """Handles video capture from camera"""

    def __init__(self, source=0):
        """
        Initialize video capture

        Args:
            source: Video source (0 for default camera, or video file path)
        """
        self.source = source
        self.capture = None
        self.current_frame = None
        self.is_running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        """Start video capture in a separate thread"""
        if self.is_running:
            print("Video capture already running")
            return

        self.capture = cv2.VideoCapture(self.source)

        if not self.capture.isOpened():
            print(f"✗ Error: Could not open video source {self.source}")
            return False

        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print(f"✓ Video capture started from source {self.source}")
        return True

    def _capture_loop(self):
        """Internal loop to continuously capture frames"""
        while self.is_running:
            ret, frame = self.capture.read()
            if ret:
                with self.lock:
                    self.current_frame = frame
            else:
                print("Failed to read frame")
                time.sleep(0.1)

    def get_frame(self):
        """
        Get the current frame

        Returns:
            numpy.ndarray: Current video frame, or None if not available
        """
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            return None

    def stop(self):
        """Stop video capture"""
        self.is_running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)

        if self.capture is not None:
            self.capture.release()
            print("✓ Video capture stopped")

    def is_active(self):
        """Check if video capture is active"""
        return self.is_running and self.capture is not None and self.capture.isOpened()
