import cv2
import sounddevice as sd
import numpy as np
import wave
import threading

# Parameters for video
video_filename = 'output_video.avi'
frame_width = 640
frame_height = 480
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Parameters for audio
audio_filename = 'output_audio.wav'
audio_samplerate = 44100
audio_channels = 1
audio_dtype = 'int16'
audio_duration = 10  # seconds

# Initialize video writer
video_out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

# Function to record audio
audio_frames = []


def record_audio():
    global audio_frames
    print("Recording audio...")
    audio_frames = sd.rec(int(audio_duration * audio_samplerate),
                          samplerate=audio_samplerate,
                          channels=audio_channels,
                          dtype=audio_dtype)
    sd.wait()  # Wait for the audio recording to finish
    print("Audio recording finished.")


# Function to record video
def record_video():
    cap = cv2.VideoCapture(0)  # Use the default webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (00, 185)
    fontScale = 1
    color = (0, 0, 255)
    thickness = 2

    print("Recording video...")
    for _ in range(int(fps * audio_duration)):
        ret, frame = cap.read()
        if not ret:
            break
        video_out.write(frame)
        cv2.putText(frame,"Hello Interviwee,Tell Me about Yourself ?",org, font, fontScale, 
                 color, thickness, cv2.LINE_AA, False)
        cv2.imshow("Recording", frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop recording if 'q' is pressed
            break

    print("Video recording finished.")
    cap.release()
    video_out.release()
    cv2.destroyAllWindows()


# Create threads for audio and video recording
video_thread = threading.Thread(target=record_video)

audio_thread = threading.Thread(target=record_audio)

# Start recording

video_thread.start()
audio_thread.start()

# Wait for threads to finish
video_thread.join()
audio_thread.join()

# Save audio file
with wave.open(audio_filename, 'wb') as wf:
    wf.setnchannels(audio_channels)
    wf.setsampwidth(np.dtype(audio_dtype).itemsize)
    wf.setframerate(audio_samplerate)
    wf.writeframes(audio_frames.tobytes())

print(f"Audio saved to {audio_filename}")
print(f"Video saved to {video_filename}")
