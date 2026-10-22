from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os
from werkzeug.utils import secure_filename
import os
from flask import request
from werkzeug.utils import secure_filename
import f_Face_info
import cv2
import time
import imutils
import argparse
import speech_recognition as sr
from pydub import AudioSegment
import language_tool_python
from transformers import pipeline
import random

# List of general interview questions
interview_questions = [
    "Tell me about yourself.",
    "What are your strengths and weaknesses?",
    "Why do you want to work here?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?",
    "Tell me about a time you faced a challenge at work.",
    "How do you handle stress and pressure?",
    "Describe a time you worked in a team.",
    "What is your greatest professional achievement?",
    "Why are you leaving your current job?",
    "What do you know about our company?",
    "Do you prefer working independently or on a team?",
    "What motivates you?",
    "Tell me about a time you showed leadership.",
    "What are your salary expectations?"
]

vscore1=0
emotion1=""
confidence1=""
errmsg=""
eerrmsg=""
errsug=""
gscore=0
total_errors=0
ts=0
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
    cam = cv2.VideoCapture("static/recordings/recording.webm")
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
    global vscore1
    vscore=score/ts
    vscore1=vscore
    cam.release()
    cv2.destroyAllWindows()
    audio_path = "static/recordings/audio.wav"  # Replace with your audio file path
    result_text = convert_audio_to_text(audio_path)
    print("Transcription:")
    print(result_text)
    global gscore1
    global total_errors1
    gscore, total_errors, errors = calculate_grammatical_score(result_text)
    gscore1=gscore
    total_errors1=total_errors
    print(f"Grammatical Score: {gscore}")
    print(f"Total Errors: {total_errors}")
    print("Details of Errors:")
    for i, error in enumerate(errors, 1):
        global errmsg1
        errmsg1=error['error']
        print(error['error'])
        global eerrmsg1
        eerrmsg1=error['message']
        print(error['message'])
        print(f"   Suggestions: {', '.join(error['suggestions'])}")
        global errsug1
        errsug1=', '.join(error['suggestions'])
    file_name = "static/result.txt"
    with open(file_name,  'w', encoding="utf-8") as file:
            file.write("\n".join(map(str, errors)))
    global emotion1
    global confidence1
    emotion, confidence = detect_emotion(result_text)
    emotion1=emotion
    confidence1=confidence
    print(f"Detected Emotion: {emotion}")
    print(f"Confidence Score: {confidence:.2f}")
    return (vscore,gscore,confidence)


app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'mp4'}
UPLOAD_FOLDER = 'static/recordings'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure upload directories exist
for folder in ['notes', 'images', 'videos']:
    os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)

# ---------- DB CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect('portal.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- INIT DB ----------
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject TEXT,
            password TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subject TEXT,
            type TEXT,
            filename TEXT
        )
    ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 subject TEXT, question TEXT,
                 option1 TEXT, option2 TEXT, option3 TEXT, option4 TEXT,
                 correct TEXT)''')
    
    conn.commit()
    conn.close()

# Call init_db manually
init_db()

# ---------- HOME ----------
@app.route('/')
def home():
    return redirect(url_for('student_login'))

# ---------- STUDENT REGISTRATION ----------
@app.route('/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, subject, password) VALUES (?, ?, ?)',
                     (name, subject, password))
        conn.commit()
        conn.close()
        return redirect(url_for('student_login'))
    return render_template('student_register.html')

# ---------- STUDENT LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE name = ? AND password = ?',
                               (name, password)).fetchone()
        conn.close()
        if student:
            session['student_id'] = student['id']
            session['subject'] = student['subject']
            return redirect(url_for('student_dashboard'))
    return render_template('student_login.html')

# ---------- STUDENT DASHBOARD ----------
@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    subject = session['subject']
    conn = get_db_connection()
    content = conn.execute('SELECT * FROM content WHERE subject=?', (subject,)).fetchall()
    conn.close()
    return render_template('student_dashboard.html', content=content)

# ---------- ADMIN LOGIN ----------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST' and request.form['password'] == 'admin':
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# ---------- ADMIN DASHBOARD ----------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    content = conn.execute('SELECT * FROM content').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', content=content)

# ---------- ADMIN ADD CONTENT ----------
@app.route('/admin/add', methods=['POST'])
def admin_add():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    title = request.form['title']
    subject = request.form['subject']
    ctype = request.form['ctype']
    file = request.files['file']

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        folder = os.path.join(UPLOAD_FOLDER, ctype + 's')
        filepath = os.path.join(folder, filename)
        file.save(filepath)

        conn = get_db_connection()
        conn.execute('INSERT INTO content (title, subject, type, filename) VALUES (?, ?, ?, ?)',
                     (title, subject, ctype, filename))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

# ---------- ADMIN DELETE CONTENT ----------
@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM content WHERE id = ?', (id,)).fetchone()
    if item:
        filepath = os.path.join(UPLOAD_FOLDER, item['type'] + 's', item['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        conn.execute('DELETE FROM content WHERE id = ?', (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        subject = request.form['subject']
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct = request.form['correct']
        conn = sqlite3.connect('portal.db')
        c = conn.cursor()
        c.execute("INSERT INTO questions (subject, question, option1, option2, option3, option4, correct) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (subject, question, option1, option2, option3, option4, correct))
        conn.commit()
        conn.close()
        return redirect(url_for('add_question'))
    return render_template('add_question.html')

@app.route('/quiz/<subject>', methods=['GET', 'POST'])
def quiz(subject):
    conn = sqlite3.connect('portal.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE subject = ?", (subject,))
    questions = c.fetchall()
    conn.close()

    if request.method == 'POST':
        score = 0
        results = []
        for q in questions:
            qid = str(q[0])
            correct = q[7]
            selected = request.form.get(f'q{qid}')
            is_correct = selected == correct
            if is_correct:
                score += 1
            results.append({
                'question': q[2],
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct
            })
        return render_template('quiz_result.html', results=results, score=score, total=len(questions))

    return render_template('quiz.html', questions=questions, subject=subject)

@app.route('/student/recording')
def student_recording():
    random_question = random.choice(interview_questions)
    print("Interview Question:")
    print(random_question)
    return render_template('recordings.html',msg=random_question)

@app.route('/upload_recording', methods=['GET', 'POST'])
def upload_recording():
    if request.method == 'GET':
        return 'Please use the recording form to upload a video.'

    if 'recording' not in request.files:
        return 'No file part'
    file = request.files['recording']
    if file.filename == '':
        return 'No selected file'
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    import subprocess
    input_video = "static/recordings/recording.webm"
    output_audio = "static/recordings/audio.wav"
    command = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vn",  # no video
        "-acodec", "pcm_s16le",  # WAV format
        output_audio
        ]
    subprocess.run(command, check=True)
    time.sleep(3)
    vs,gs,c=main()
    global ts1
    ts=vs+gs+c
    ts1=ts
    print(ts)
    

    return 'Interview Analysed '

@app.route('/recordings/<filename>')
def serve_recording(filename):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/student/resultinter')
def resultinter():
    vscore=vscore1
    emotion=emotion1
    confidence=confidence1
    errmsg=errmsg1
    eerrmsg=eerrmsg1
    errsug=errsug1
    gscore=gscore1
    total_errors=total_errors1
    ts=ts1
    return render_template('test.html',vscore=vscore,emotion=emotion,confidence=confidence,errmsg=errmsg,eerrmsg=eerrmsg,errsug=errsug,gscore=gscore,total_errors=total_errors,ts=ts,sub=session['subject'])

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
