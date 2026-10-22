import subprocess

# Input and output file paths
input_video = "static/recordings/recording.webm"
output_audio = "static/recordings/audio.wav"

# FFmpeg command
command = [
    "ffmpeg",
    "-i", input_video,
    "-vn",  # no video
    "-acodec", "pcm_s16le",  # WAV format
    output_audio
]

# Run the command
subprocess.run(command, check=True)
