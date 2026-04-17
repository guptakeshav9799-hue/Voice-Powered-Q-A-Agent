"""
Voice Utilities — Speech-to-Text and Text-to-Speech

This module handles:
1. Converting audio (voice) to text using SpeechRecognition
2. Converting text to audio using gTTS (Google Text-to-Speech)
"""

import os
import tempfile
import speech_recognition as sr
from gtts import gTTS


def speech_to_text(audio_filepath: str) -> str:
    """
    Convert an audio file to text using Google Speech Recognition.
    
    Args:
        audio_filepath: Path to the audio file (WAV format works best)
        
    Returns:
        Recognized text string, or error message
    """
    if not audio_filepath:
        return ""

    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_filepath) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Record the audio
            audio_data = recognizer.record(source)

        # Use Google's free speech recognition API
        print("🎤 Converting speech to text...")
        text = recognizer.recognize_google(audio_data)
        print(f"✅ Recognized: {text}")
        return text

    except sr.UnknownValueError:
        return "⚠️ Sorry, I couldn't understand the audio. Please try again."
    except sr.RequestError as e:
        return f"❌ Speech recognition service error: {str(e)}"
    except Exception as e:
        return f"❌ Error processing audio: {str(e)}"


def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Convert text to an audio file using Google Text-to-Speech (gTTS).
    
    Args:
        text: The text to convert to speech
        lang: Language code (default: 'en' for English)
        
    Returns:
        Path to the generated audio file (MP3)
    """
    if not text or not text.strip():
        return None

    try:
        # Clean up the text (remove emoji and special characters for TTS)
        clean_text = text
        for char in ["✅", "❌", "⚠️", "📄", "🔍", "🤖", "🎤", "🔊", "✂️", "🧠", "📦"]:
            clean_text = clean_text.replace(char, "")
        clean_text = clean_text.strip()

        if not clean_text:
            return None

        print("🔊 Converting text to speech...")
        tts = gTTS(text=clean_text, lang=lang, slow=False)

        # Save to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", prefix="tts_")
        tts.save(temp_file.name)
        temp_file.close()

        print(f"✅ Audio saved to: {temp_file.name}")
        return temp_file.name

    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        return None
