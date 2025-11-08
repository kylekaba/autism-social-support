"""
GUI Module
Main user interface for the application
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import cv2
from PIL import Image, ImageTk
from config.settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class ApplicationGUI:
    """Main application GUI using tkinter"""

    # Autism-friendly color palette - Dark mode with warm accents
    COLORS = {
        'bg_main': '#2D2D2D',           # Dark gray background
        'bg_frame': '#FFE680',          # Warm yellow for frames
        'bg_button': '#FFD54F',         # Bright yellow for buttons
        'bg_button_hover': '#FFC107',   # Darker yellow on hover
        'bg_button_active': '#90C695',  # Soft green for active state
        'bg_emotion': '#FFE680',        # Yellow for emotion display
        'bg_transcript': '#1A1A1A',     # Dark black for transcript (dark mode)
        'bg_response': '#1A1A1A',       # Dark black for suggestions (dark mode)
        'text_dark': '#333333',         # Dark gray for text on yellow
        'text_light': '#FFFFFF',        # White text for dark backgrounds
        'border': '#444444',            # Dark gray for borders
        'accent': '#FFD54F'             # Yellow accent
    }

    def __init__(self, master, on_suggest_callback, on_start_callback, on_stop_callback):
        """
        Initialize the GUI

        Args:
            master: Tkinter root window
            on_suggest_callback: Callback function for "Suggest Response" button
            on_start_callback: Callback function for starting session
            on_stop_callback: Callback function for stopping session
        """
        self.master = master
        self.master.title(WINDOW_TITLE)
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.configure(bg=self.COLORS['bg_main'])

        self.on_suggest_callback = on_suggest_callback
        self.on_start_callback = on_start_callback
        self.on_stop_callback = on_stop_callback

        self.is_session_active = False

        # Configure ttk style for autism-friendly colors
        self._configure_style()

        self._create_widgets()

    def _configure_style(self):
        """Configure ttk styles with autism-friendly colors"""
        style = ttk.Style()

        # Configure frame style
        style.configure('Main.TFrame', background=self.COLORS['bg_main'])
        style.configure('Card.TFrame', background=self.COLORS['bg_frame'],
                       relief='flat', borderwidth=2)

        # Configure label frame style with yellow background
        style.configure('TLabelframe', background=self.COLORS['bg_frame'],
                       foreground=self.COLORS['text_light'], relief='solid', borderwidth=2)
        style.configure('TLabelframe.Label', background=self.COLORS['bg_frame'],
                       foreground=self.COLORS['text_light'], font=('Arial', 12, 'bold'))

        # Configure label style
        style.configure('TLabel', background=self.COLORS['bg_frame'],
                       foreground=self.COLORS['text_light'])
        style.configure('Emotion.TLabel', background=self.COLORS['bg_emotion'],
                       foreground=self.COLORS['text_light'])

        # Configure button style
        style.configure('TButton', background=self.COLORS['bg_button'],
                       foreground=self.COLORS['text_dark'],
                       borderwidth=0, relief='flat',
                       font=('Arial', 12, 'bold'), padding=10)
        style.map('TButton',
                 background=[('active', self.COLORS['bg_button_hover'])],
                 relief=[('pressed', 'flat')])

    def _create_widgets(self):
        """Create all GUI widgets"""

        # Main container
        main_frame = ttk.Frame(self.master, padding="10", style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # --- Top Section: Video Preview and Controls ---
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Video preview
        self.video_label = ttk.Label(top_frame, text="",
                                     relief=tk.SUNKEN, width=40, anchor=tk.CENTER)
        self.video_label.grid(row=0, column=0, padx=(0, 10))
        self.video_label.imgtk = None  # Keep reference to prevent garbage collection

        # Controls panel
        controls_frame = ttk.LabelFrame(top_frame, text="Controls", padding="10")
        controls_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))

        self.start_button = ttk.Button(controls_frame, text="Start Session",
                                       command=self._on_start_clicked)
        self.start_button.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))

        self.stop_button = ttk.Button(controls_frame, text="Stop Session",
                                      command=self._on_stop_clicked, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))

        self.suggest_button = ttk.Button(controls_frame, text="Suggest Response",
                                         command=self._on_suggest_clicked, state=tk.DISABLED)
        self.suggest_button.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))

        # --- Middle Section: Current Emotion Display ---
        emotion_frame = ttk.LabelFrame(main_frame, text="Current Emotion", padding="10")
        emotion_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.emotion_label = ttk.Label(emotion_frame, text="😐 Neutral",
                                       font=("Arial", 24), anchor=tk.CENTER,
                                       style='Emotion.TLabel')
        self.emotion_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        emotion_frame.columnconfigure(0, weight=1)

        # --- Bottom Section: Transcript and Suggestions ---
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        # Transcript display
        transcript_frame = ttk.LabelFrame(bottom_frame, text="Conversation", padding="5")
        transcript_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        transcript_frame.rowconfigure(0, weight=1)
        transcript_frame.columnconfigure(0, weight=1)

        self.transcript_text = scrolledtext.ScrolledText(transcript_frame, wrap=tk.WORD,
                                                         width=30, height=10,
                                                         bg=self.COLORS['bg_transcript'],
                                                         fg=self.COLORS['text_light'],
                                                         font=("Arial", 12),
                                                         relief='flat',
                                                         borderwidth=0,
                                                         insertbackground=self.COLORS['text_light'])
        self.transcript_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.transcript_text.config(state=tk.DISABLED)

        # Response suggestions display
        response_frame = ttk.LabelFrame(bottom_frame, text="Suggested Response", padding="5")
        response_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        response_frame.rowconfigure(0, weight=1)
        response_frame.columnconfigure(0, weight=1)

        self.response_text = scrolledtext.ScrolledText(response_frame, wrap=tk.WORD,
                                                       width=30, height=10,
                                                       font=("Arial", 15, "bold"),
                                                       bg=self.COLORS['bg_response'],
                                                       fg=self.COLORS['text_light'],
                                                       relief='flat',
                                                       borderwidth=0,
                                                       insertbackground=self.COLORS['text_light'])
        self.response_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.response_text.config(state=tk.DISABLED)

        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready to start", relief=tk.SUNKEN)
        self.status_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def _on_start_clicked(self):
        """Handle start button click"""
        if self.on_start_callback:
            success = self.on_start_callback()
            if success:
                self.is_session_active = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.suggest_button.config(state=tk.NORMAL)
                self.update_status("Session active")

    def _on_stop_clicked(self):
        """Handle stop button click"""
        if self.on_stop_callback:
            self.on_stop_callback()
            self.is_session_active = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.suggest_button.config(state=tk.DISABLED)
            self.update_status("Session stopped")

    def _on_suggest_clicked(self):
        """Handle suggest response button click"""
        if self.on_suggest_callback:
            self.update_status("Generating suggestion...")
            self.on_suggest_callback()

    def update_video_frame(self, frame):
        """
        Update the video preview with a new frame

        Args:
            frame: OpenCV frame (BGR format)
        """
        if frame is not None:
            try:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize for display
                display_width = 320
                display_height = 240
                frame_resized = cv2.resize(frame_rgb, (display_width, display_height))

                # Convert to PIL Image
                img = Image.fromarray(frame_resized)
                imgtk = ImageTk.PhotoImage(image=img)

                # Update label - keep reference to prevent garbage collection
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk, text="")
            except Exception as e:
                # Silently handle any frame update errors to prevent flickering
                pass

    def update_emotion(self, emotion, emoticon):
        """
        Update the current emotion display

        Args:
            emotion: Emotion name (e.g., "happiness")
            emoticon: Emoticon string (e.g., "😊")
        """
        self.emotion_label.config(text=f"{emoticon} {emotion.capitalize()}")

    def add_transcript_entry(self, text):
        """
        Add an entry to the transcript display

        Args:
            text: Text to add
        """
        self.transcript_text.config(state=tk.NORMAL)
        self.transcript_text.insert(tk.END, text + "\n")
        self.transcript_text.see(tk.END)
        self.transcript_text.config(state=tk.DISABLED)

    def clear_transcript(self):
        """Clear the transcript display"""
        self.transcript_text.config(state=tk.NORMAL)
        self.transcript_text.delete(1.0, tk.END)
        self.transcript_text.config(state=tk.DISABLED)

    def show_response_suggestion(self, response):
        """
        Display a response suggestion

        Args:
            response: Suggested response text
        """
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)
        self.response_text.config(state=tk.DISABLED)
        self.update_status("Suggestion ready")

    def update_status(self, message):
        """
        Update the status bar

        Args:
            message: Status message
        """
        self.status_label.config(text=message)
