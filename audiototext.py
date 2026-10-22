import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_to_text(audio_file_path):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Convert audio to WAV if it's not already
    if not audio_file_path.endswith(".wav"):
        audio = AudioSegment.from_file(audio_file_path)
        wav_file = "converted_audio.wav"
        audio.export(wav_file, format="wav")
        audio_file_path = wav_file

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        print("Converting audio to text...")
        audio_data = recognizer.record(source)

        # Recognize speech using Google Web Speech API
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from the speech recognition service; {e}"

# Example usage
audio_path = "output_audio.wav"  # Replace with your audio file path
result_text = convert_audio_to_text(audio_path)
print("Transcription:")
print(result_text)
