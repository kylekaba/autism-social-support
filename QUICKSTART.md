# Quick Start Guide

## You're All Set!

All dependencies have been installed and your OpenAI API key has been configured.

## Running the Application

1. **Activate the virtual environment:**
   ```bash
   cd ~/Desktop/YC/autism_social_support
   source venv/bin/activate
   ```

2. **Run the application:**
   ```bash
   python3 main.py
   ```

## How to Use

### Starting a Session

1. Click the **"Start Session"** button
2. You'll be prompted to enter information about the child:
   - **Age**: e.g., "8 years old"
   - **Autism Level**: e.g., "Level 1" or "High functioning"
   - **Communication Capabilities**: e.g., "Can speak in sentences, sometimes needs help with responses"

3. The application will start:
   - Video from your webcam will appear
   - Facial expressions will be detected every 10 seconds
   - Speech will be transcribed automatically

### During a Conversation

- **Emotion Display**: Large emoticons show the detected facial expression
- **Transcript**: Left panel shows the conversation history
- **Get Help**: Click **"Suggest Response"** when the child needs help responding
  - The AI will analyze the conversation and facial expression
  - A suggested response appears in the right panel (large text)
  - The child can read it and use it to formulate their response

### Stopping a Session

- Click **"Stop Session"** to end the session
- All data is cleared (nothing is saved)

## Tips for Best Results

### Camera Setup
- Position the camera so the conversation partner's face is clearly visible
- Ensure good lighting
- Keep the face centered in frame

### Microphone Setup
- Use a quality microphone for better transcription
- Minimize background noise
- Speak clearly

### For Caregivers

- Start with short 5-10 minute sessions
- Practice with familiar people first
- Adjust the `EXPRESSION_UPDATE_INTERVAL` in `.env` if 10 seconds is too fast/slow
- Review suggested responses before the child uses them
- Use this as a learning tool, not a replacement for therapy

## Troubleshooting

### "Camera Error"
- Make sure no other app is using the camera
- Check System Preferences > Security & Privacy > Camera
- Grant permission to Terminal/Python

### "Microphone not working"
- Check System Preferences > Security & Privacy > Microphone
- Grant permission to Terminal/Python

### "OpenAI API Error"
- Verify your API key in `.env` is correct
- Check you have credits in your OpenAI account
- Ensure internet connection is working

### Slow facial expression detection
- The first detection may be slower while models load
- Subsequent detections should be faster
- If consistently slow, you can increase `EXPRESSION_UPDATE_INTERVAL` in `.env`

## System Requirements

- macOS 10.14 or later
- Working webcam
- Working microphone
- Internet connection (for OpenAI API)
- Python 3.8+

## Privacy & Data

- Video is NOT recorded
- Audio is NOT saved
- Transcripts are cleared when you stop the session
- Only conversation context is sent to OpenAI for generating suggestions
- No personally identifiable information is stored

## Cost Estimate

Using GPT-4o-mini, typical costs:
- Short session (5-10 min, 3-5 suggestions): < $0.05
- Long session (20-30 min, 10-15 suggestions): < $0.15

Monitor your usage at: https://platform.openai.com/usage

## Support

This application is based on research focused on helping autistic children develop social communication skills. Always consult with therapists and autism specialists about the child's specific needs.

For technical issues, check the main README.md file.
