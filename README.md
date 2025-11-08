# Autism Social Communication Support Application

A macOS application that uses computer vision and Large Language Models to help autistic children improve their social communication skills during conversations.

## Overview

This application provides real-time support during conversations by:
- **Detecting facial expressions** and displaying them as emoticons to help children understand non-verbal cues
- **Transcribing conversations** to maintain conversational context
- **Suggesting appropriate responses** using AI (GPT-4o-mini) based on conversation context and detected emotions

## Features

- Real-time facial expression recognition (7 emotions: happiness, sadness, surprise, anger, disgust, fear, neutral)
- Live speech-to-text transcription
- AI-powered response suggestions tailored to the child's profile
- Clean, accessible user interface designed with autistic children in mind
- Configurable emotion update intervals (default: 10 seconds)

## Requirements

- macOS 10.14 or later
- Python 3.8 or higher
- Webcam and microphone
- OpenAI API key

## Installation

### 1. Clone or download this repository

```bash
cd ~/Desktop/YC/autism_social_support
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installing `py-feat` may take some time as it includes deep learning models.

### 4. Configure your API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
EXPRESSION_UPDATE_INTERVAL=10
MODEL_NAME=gpt-4o-mini
```

## Usage

### Running the Application

```bash
python3 main.py
```

### How to Use

1. **Start Session**: Click "Start Session" button
2. **Get Response Suggestions**: Click "Suggest Response" when the child needs help formulating a response
3. **Stop Session**: Click "Stop Session" when finished

## System Components

### 1. Video Capture Module
- Captures live video from webcam
- Runs in background thread for smooth performance

### 2. Facial Expression Recognition
- Uses Py-Feat library with deep learning models
- Detects 7 basic emotions
- Updates every 10 seconds (configurable)

### 3. Transcription Service
- Uses Google Speech Recognition
- Provides live speech-to-text transcription
- Maintains conversation history with timestamps

### 4. Response Generator
- Uses OpenAI's GPT-4o-mini model
- Generates contextually appropriate responses
- Considers:
  - Full conversation transcript
  - Current facial expression
  - Child's profile and capabilities

### 5. User Interface
- Built with tkinter (native Python GUI)
- Features:
  - Live video preview
  - Large emotion display
  - Conversation transcript
  - Response suggestions in large, bold text
  - Simple controls

## Configuration

Edit `.env` file to customize:

- `EXPRESSION_UPDATE_INTERVAL`: How often to update emotion detection (seconds)
- `MODEL_NAME`: Which OpenAI model to use (default: gpt-4o-mini)

## Cost Considerations

Using GPT-4o-mini:
- Input: ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens

For typical usage (10-15 minute session with 5-10 response suggestions), costs should be minimal (< $0.10 per session).

## Privacy & Safety

- All processing happens locally except for OpenAI API calls
- Conversations are NOT saved to disk
- Video is NOT recorded
- Transcripts are cleared when session ends
- OpenAI API calls include conversation context - review OpenAI's privacy policy

## Troubleshooting

### Camera not working
- Check camera permissions in System Preferences > Security & Privacy > Camera
- Ensure no other application is using the camera

### Microphone not working
- Check microphone permissions in System Preferences > Security & Privacy > Microphone
- Test microphone with another application

### Py-Feat installation issues
```bash
# Try installing with specific torch version
pip install torch torchvision
pip install py-feat
```

### OpenAI API errors
- Verify your API key is correct in `.env` file
- Check your OpenAI account has available credits
- Ensure you have internet connection

## Development Notes

Based on the research paper:
> Jafri, R. (2024). A Social Communication Support Application for Autistic Children Using Computer Vision and Large Language Models. ICCHP 2024, LNCS 14751, pp. 217–223.

### Key Improvements over Original Design
- **macOS native** instead of Windows
- **Platform-agnostic** - works with any video source, not just Zoom
- **More responsive** - 10-second emotion updates vs 30 seconds
- **Modern AI** - GPT-4o-mini instead of GPT-3.5-turbo
- **Simplified architecture** - local speech recognition instead of Tactiq dependency

## Future Enhancements

Potential additions:
- Gamification mode for practicing emotion recognition
- Support for multiple participants
- Progress tracking and reporting
- Customizable emoticons
- Additional non-verbal cue detection (tone of voice, body language)
- Offline mode with local LLM

## License

This is an educational/research project. Please consult with therapists and autism specialists before using with children.

## Acknowledgments

- Original research by Dr. Rabia Jafri, King Saud University
- Py-Feat library for facial expression recognition
- OpenAI for GPT-4o-mini API
- Built with consultation from therapists working with autistic children

## Support

For issues or questions, please refer to:
- Py-Feat documentation: https://py-feat.org
- OpenAI API docs: https://platform.openai.com/docs
- Original paper: https://doi.org/10.1007/978-3-031-62849-8_27
