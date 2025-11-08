"""
Transcription Component
Transcribes speech to text for conversation tracking
"""
import threading
import queue
from datetime import datetime

# Try to import speech recognition, but make it optional
try:
    import speech_recognition as sr
    # Also check if PyAudio is available (needed for microphone)
    try:
        import pyaudio
        SPEECH_RECOGNITION_AVAILABLE = True
    except ImportError:
        SPEECH_RECOGNITION_AVAILABLE = False
        print("⚠️  Speech recognition not available (PyAudio not installed)")
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️  Speech recognition not available (SpeechRecognition not installed)")


class TranscriptionService:
    """Handles speech-to-text transcription"""

    def __init__(self):
        """Initialize the transcription service"""
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
        else:
            self.recognizer = None
        self.microphone = None
        self.is_running = False
        self.is_available = SPEECH_RECOGNITION_AVAILABLE  # Track if transcription is available
        self.transcript = []
        self.transcript_queue = queue.Queue()
        self.thread = None

    def start(self):
        """Start transcription service"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            print("⚠️  Transcription disabled - PyAudio not installed")
            print("   The app will work without transcription.")
            print("   You can still use facial expressions and get AI suggestions!")
            return True  # Return True to not block the app

        try:
            self.microphone = sr.Microphone()

            # Adjust for ambient noise
            print("Calibrating for ambient noise... Please wait.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)

            self.is_running = True
            self.thread = threading.Thread(target=self._transcription_loop, daemon=True)
            self.thread.start()
            print("✓ Transcription service started")
            return True
        except Exception as e:
            print(f"⚠️  Transcription not available: {e}")
            print("   The app will work without transcription.")
            return True  # Return True to not block the app

    def _transcription_loop(self):
        """Internal loop to continuously transcribe audio"""
        with self.microphone as source:
            while self.is_running:
                try:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)

                    # Recognize speech using Google Speech Recognition
                    try:
                        text = self.recognizer.recognize_google(audio)
                        timestamp = datetime.now().strftime("%H:%M:%S")

                        # Add to transcript
                        entry = {
                            "timestamp": timestamp,
                            "speaker": "User",  # In a real system, we'd identify speakers
                            "text": text
                        }

                        self.transcript.append(entry)
                        self.transcript_queue.put(entry)
                        print(f"[{timestamp}] Transcribed: {text}")

                    except sr.UnknownValueError:
                        # Speech was unintelligible
                        pass
                    except sr.RequestError as e:
                        print(f"Error with speech recognition service: {e}")

                except sr.WaitTimeoutError:
                    # No speech detected in timeout period
                    continue
                except Exception as e:
                    if self.is_running:
                        print(f"Transcription error: {e}")

    def get_transcript(self):
        """
        Get the full conversation transcript

        Returns:
            str: Formatted transcript of the conversation
        """
        if not self.transcript:
            return ""

        formatted = []
        for entry in self.transcript:
            formatted.append(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}")

        return "\n".join(formatted)

    def get_recent_transcript(self, num_entries=10):
        """
        Get recent transcript entries

        Args:
            num_entries: Number of recent entries to return

        Returns:
            str: Formatted recent transcript
        """
        recent = self.transcript[-num_entries:] if self.transcript else []

        formatted = []
        for entry in recent:
            formatted.append(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}")

        return "\n".join(formatted)

    def clear_transcript(self):
        """Clear the transcript"""
        self.transcript = []
        # Clear the queue
        while not self.transcript_queue.empty():
            try:
                self.transcript_queue.get_nowait()
            except queue.Empty:
                break

    def stop(self):
        """Stop transcription service"""
        self.is_running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        print("✓ Transcription service stopped")

    def is_active(self):
        """Check if transcription is active"""
        return self.is_available and self.is_running
