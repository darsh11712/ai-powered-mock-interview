import f_Face_info
import cv2
import time
import imutils
import argparse
import speech_recognition as sr
from pydub import AudioSegment
import language_tool_python
from transformers import pipeline

def detect_emotion(text):
    """
    Detect emotion from the input text using a pre-trained transformer model.
    """
    # Load pre-trained sentiment-analysis model
    classifier = pipeline("sentiment-analysis")

    # Analyze the text
    result = classifier(text)

    # Extract label and score
    emotion = result[0]['label']
    score = result[0]['score']

    return emotion, score

def calculate_grammatical_score(text):
    # Initialize the grammar checking tool
    tool = language_tool_python.LanguageTool('en-US')

    # Check the text for grammar issues
    matches = tool.check(text)

    # Count the total errors
    total_errors = len(matches)

    # Simple scoring: 
    # Assume 100 as a perfect score and subtract 10 points per error (or adjust as needed)
    score = max(0, 100 - (total_errors * 10))

    # Prepare error details
    error_details = [
        {
            "message": match.message,
            "suggestions": match.replacements,
            "error": match.context,
        }
        for match in matches
    ]

    return score, total_errors, error_details

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

def main():
    cv2.namedWindow("Face info")
    cam = cv2.VideoCapture("output_video.avi")
    score=0
    score1=0
    ts=0
    vscore=0
    while True:
        star_time = time.time()
        ret, frame = cam.read()
        if not ret:
            #print("Error: Unable to read the frame. Breaking the stream.")
            break
        frame = imutils.resize(frame, width=720)
        out = f_Face_info.get_face_info(frame)
        fs=out[0]['emotion']
        if(fs == 'happy' or fs == 'surprise' or fs == 'neutral'):
            score=score+1
        if fs =='sad' or fs =='angry' or fs=='disgust':
            score1=score1+1
        ts=score+score1
        res_img = f_Face_info.bounding_box(out,frame)
        end_time = time.time() - star_time
        FPS = 1/end_time
        cv2.putText(res_img,f"FPS: {round(FPS,3)}",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.imshow('Face info',res_img)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    vscore=score/ts
    cam.release()
    cv2.destroyAllWindows()
    audio_path = "output_audio.wav"  # Replace with your audio file path
    result_text = convert_audio_to_text(audio_path)
    print("Transcription:")
    print(result_text)
    gscore, total_errors, errors = calculate_grammatical_score(result_text)
    print(f"Grammatical Score: {gscore}")
    print(f"Total Errors: {total_errors}")
    print("Details of Errors:")
    for i, error in enumerate(errors, 1):
        file_name = "static/result.txt"
        with open(file_name, "a") as file:
            file.write(error['error'])
            file.write(error['message'])
            file.write(f"   Suggestions: {', '.join(error['suggestions'])}")
    emotion, confidence = detect_emotion(result_text)
    print(f"Detected Emotion: {emotion}")
    print(f"Confidence Score: {confidence:.2f}")
    return (vscore,gscore,confidence)

