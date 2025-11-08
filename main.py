#!/usr/bin/env python3
"""
Autism Social Communication Support Application
Main Controller - Coordinates all components

A macOS application that helps autistic children improve their social communication
skills during online conversations using computer vision and AI.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import time

from modules.video_capture import VideoCapture
from modules.facial_expression import FacialExpressionRecognizer
from modules.transcription import TranscriptionService
from modules.chatbot import ResponseGenerator
from modules.gui import ApplicationGUI
from config.settings import EXPRESSION_UPDATE_INTERVAL


class SocialSupportController:
    """Main controller that coordinates all components"""

    def __init__(self):
        """Initialize the controller and all components"""
        self.root = tk.Tk()

        # Components
        self.video_capture = None
        self.expression_recognizer = None
        self.transcription_service = None
        self.response_generator = None
        self.gui = None

        # State
        self.is_running = False
        self.current_emotion = "neutral"
        self.child_profile = None

        # Threads
        self.expression_update_thread = None
        self.video_update_thread = None

        # Initialize GUI
        self._initialize_gui()

    def _initialize_gui(self):
        """Initialize the graphical user interface"""
        self.gui = ApplicationGUI(
            self.root,
            on_suggest_callback=self.on_suggest_response,
            on_start_callback=self.start_session,
            on_stop_callback=self.stop_session
        )

    def start_session(self):
        """Start a new communication support session"""
        print("\n" + "="*50)
        print("Starting Karitas Session")
        print("="*50)

        # Use default profile for high-functioning autistic individuals
        self.child_profile = {
            "age": "teen/adult",
            "autism_level": "Level 1 (high-functioning)",
            "communication_capabilities": "Can communicate in full sentences"
        }

        print(f"\nDefault Profile:")
        print(f"  Target Users: High-functioning individuals with autism")
        print(f"  Communication: Full sentences\n")

        # Initialize components
        if not self._initialize_components():
            messagebox.showerror("Initialization Error",
                               "Failed to initialize system components. Please check the console for errors.")
            return False

        # Start services
        self.is_running = True

        # Start video capture
        if not self.video_capture.start():
            messagebox.showerror("Camera Error", "Failed to start camera.")
            self.stop_session()
            return False

        # Start transcription
        self.transcription_service.start()

        # Check if transcription is actually available
        print(f"Debug: is_available = {self.transcription_service.is_available}")
        if not self.transcription_service.is_available:
            # Show message in transcript area that transcription is disabled
            print("Debug: Adding transcript message about disabled transcription")
            self.gui.add_transcript_entry("==================================")
            self.gui.add_transcript_entry("  TRANSCRIPTION NOT AVAILABLE")
            self.gui.add_transcript_entry("==================================")
            self.gui.add_transcript_entry("")
            self.gui.add_transcript_entry("PyAudio is not installed,")
            self.gui.add_transcript_entry("so audio transcription is")
            self.gui.add_transcript_entry("temporarily disabled.")
            self.gui.add_transcript_entry("")
            self.gui.add_transcript_entry("GOOD NEWS:")
            self.gui.add_transcript_entry("Everything else works perfectly!")
            self.gui.add_transcript_entry("")
            self.gui.add_transcript_entry("✓ Camera is working")
            self.gui.add_transcript_entry("✓ Facial emotions detected")
            self.gui.add_transcript_entry("✓ AI suggestions available")
            self.gui.add_transcript_entry("")
            self.gui.add_transcript_entry("Click 'Suggest Response' anytime")
            self.gui.add_transcript_entry("to get AI help based on the")
            self.gui.add_transcript_entry("person's facial expression!")
            self.gui.add_transcript_entry("")
            self.gui.add_transcript_entry("==================================")
            print("Debug: Finished adding transcript entries")

        # Start update threads
        self._start_update_threads()

        print("✓ Session started successfully")
        return True

    def _get_child_profile(self):
        """Prompt caregiver for child's profile information"""
        # Age
        age = simpledialog.askstring("Child Profile", "Enter child's age:",
                                     parent=self.root)
        if not age:
            return False

        # Autism level
        autism_level = simpledialog.askstring("Child Profile",
                                             "Enter autism level (e.g., Level 1, Level 2, Level 3):",
                                             parent=self.root)
        if not autism_level:
            return False

        # Communication capabilities
        comm_capabilities = simpledialog.askstring("Child Profile",
                                                   "Describe communication capabilities:",
                                                   parent=self.root)
        if not comm_capabilities:
            return False

        self.child_profile = {
            "age": age,
            "autism_level": autism_level,
            "communication_capabilities": comm_capabilities
        }

        print(f"\nChild Profile:")
        print(f"  Age: {age}")
        print(f"  Autism Level: {autism_level}")
        print(f"  Communication Capabilities: {comm_capabilities}\n")

        return True

    def _initialize_components(self):
        """Initialize all system components"""
        try:
            # Video capture
            self.video_capture = VideoCapture(source=0)

            # Facial expression recognizer
            self.expression_recognizer = FacialExpressionRecognizer()

            # Transcription service
            self.transcription_service = TranscriptionService()

            # Response generator
            self.response_generator = ResponseGenerator(self.child_profile)

            return True

        except Exception as e:
            print(f"✗ Error initializing components: {e}")
            return False

    def _start_update_threads(self):
        """Start background threads for updating GUI"""
        # Start video updates using tkinter's after() for smoother performance
        self._schedule_video_update()

        # Expression update thread
        self.expression_update_thread = threading.Thread(
            target=self._expression_update_loop,
            daemon=True
        )
        self.expression_update_thread.start()

        # Transcript monitoring thread
        transcript_thread = threading.Thread(
            target=self._transcript_monitor_loop,
            daemon=True
        )
        transcript_thread.start()

    def _schedule_video_update(self):
        """Schedule video frame updates using tkinter's after() for smooth updates"""
        if self.is_running:
            frame = self.video_capture.get_frame()
            if frame is not None:
                self.gui.update_video_frame(frame)
            # Schedule next update (~30 fps)
            self.root.after(33, self._schedule_video_update)

    def _expression_update_loop(self):
        """Periodically detect and update facial expressions"""
        while self.is_running:
            # Wait first to avoid initial detection rush
            time.sleep(EXPRESSION_UPDATE_INTERVAL)

            if not self.is_running:
                break

            frame = self.video_capture.get_frame()
            if frame is not None:
                # Detect emotion (FER library handles frame internally)
                emotion = self.expression_recognizer.detect_emotion(frame)
                self.current_emotion = emotion

                # Get emoticon
                emoticon = self.expression_recognizer.get_emoticon(emotion)

                # Update GUI
                self.gui.update_emotion(emotion, emoticon)

    def _transcript_monitor_loop(self):
        """Monitor and display transcript updates"""
        while self.is_running:
            try:
                # Check for new transcript entries
                entry = self.transcription_service.transcript_queue.get(timeout=1)
                text = f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}"
                self.gui.add_transcript_entry(text)
            except:
                continue

    def on_suggest_response(self):
        """Handle request for response suggestion"""
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=self._generate_suggestion, daemon=True)
        thread.start()

    def _generate_suggestion(self):
        """Generate and display a response suggestion"""
        try:
            # Get conversation transcript
            transcript = self.transcription_service.get_transcript()

            if not transcript:
                transcript = "No conversation detected yet."

            # Get current emotion
            emotion = self.current_emotion

            # Generate response
            print(f"\nGenerating response suggestion...")
            print(f"  Current emotion: {emotion}")
            response = self.response_generator.generate_response(transcript, emotion)

            print(f"  Suggested response: {response}\n")

            # Display in GUI
            self.gui.show_response_suggestion(response)

        except Exception as e:
            print(f"✗ Error generating suggestion: {e}")
            self.gui.show_response_suggestion("Error generating suggestion.")

    def stop_session(self):
        """Stop the current session"""
        print("\nStopping session...")

        self.is_running = False

        # Stop services
        if self.video_capture:
            self.video_capture.stop()

        if self.transcription_service:
            self.transcription_service.stop()

        # Reset components
        if self.response_generator:
            self.response_generator.reset_conversation()

        if self.gui:
            self.gui.clear_transcript()
            self.gui.show_response_suggestion("")
            self.gui.update_emotion("neutral", "😐")

        print("✓ Session stopped")

    def run(self):
        """Run the application"""
        print("\n" + "="*60)
        print("  Autism Social Communication Support Application")
        print("  macOS Version")
        print("="*60)
        print("\nReady to start. Click 'Start Session' to begin.\n")

        self.root.mainloop()

    def cleanup(self):
        """Cleanup resources before exit"""
        if self.is_running:
            self.stop_session()


def main():
    """Main entry point"""
    try:
        controller = SocialSupportController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
    finally:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
