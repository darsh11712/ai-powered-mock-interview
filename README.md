🎯 AI-Powered Mock Interview System

An AI-powered mock interview platform designed to help students and job seekers practice interviews, improve communication skills, and evaluate their performance. The system combines facial emotion recognition, speech processing, text sentiment analysis, and grammar evaluation to provide a more interactive interview practice experience.

📌 Project Overview

The AI-Powered Mock Interview System is a web-based application developed using Python and Flask. It aims to simulate parts of a real interview process and help users analyze their responses.

The system integrates machine learning and natural language processing techniques to process interview responses and analyze emotional expressions, spoken content, and language quality.

✨ Features

- 👤 User Authentication: Student registration and login.
- 🛠️ Admin Dashboard: Administrative interface for managing the application.
- 🎤 Audio Processing: Processes audio recordings and converts speech into text.
- 🎥 Audio and Video Recording: Supports recording and processing interview responses.
- 😊 Facial Emotion Recognition: Uses a trained deep learning model to recognize facial emotions.
- 📝 Sentiment Analysis: Analyzes the sentiment expressed in text responses.
- 📚 Grammar Evaluation: Evaluates grammar and language correctness.
- ❓ Interview Questions: Provides an interface for interview questions and quizzes.
- 📊 Results Interface: Displays interview or quiz results through the web application.

Note: Available features depend on the application's current implementation and configuration.

🧰 Technologies Used

Technology| Purpose
Python| Core application logic
Flask| Web application framework
HTML/CSS| Frontend structure and styling
SQLite| Database storage
OpenCV| Image and video processing
SpeechRecognition| Speech-to-text processing
Pydub| Audio processing
Transformers| Natural language processing
Deep Learning / HDF5| Facial emotion recognition model
LanguageTool| Grammar checking

📁 Project Structure

ai-powered-mock-interview/
├── app.py
├── main.py
├── config.py
├── audiototext.py
├── audiovedio.py
├── deep_face.py
├── f_Face_info.py
├── grammerscore.py
├── textsentiment.py
├── testaudiovideo.py
├── emotion_detection/
│   ├── f_emotion_detection.py
│   └── Modelos/
│       └── model_dropout.hdf5
├── static/
│   ├── recordings/
│   └── result.txt
├── templates/
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── student_dashboard.html
│   ├── student_login.html
│   ├── student_register.html
│   └── ...
├── .gitignore
└── README.md

⚙️ Installation and Setup

Prerequisites

Install the following before running the project:

- Python 3.10 or another version compatible with the project's dependencies
- Git
- A webcam and microphone for audio/video features
- Required system dependencies for audio and computer vision libraries

1. Clone the Repository

git clone https://github.com/darsh11712/ai-powered-mock-interview.git
cd ai-powered-mock-interview

2. Create a Virtual Environment

Windows:

python -m venv venv
.\venv\Scripts\Activate.ps1

If PowerShell blocks activation, use Command Prompt or adjust your local PowerShell execution policy as appropriate.

3. Install Dependencies

If the project contains a "requirements.txt" file:

pip install -r requirements.txt

If no dependency file exists, install the packages required by the application. For example:

pip install flask opencv-python SpeechRecognition pydub language-tool-python transformers h5py

Additional packages or system components may be needed depending on the code and installed versions. Check the project imports and library documentation before running the application.

4. Configure the Application

Review "config.py" and confirm that the emotion recognition model path is correct:

path_model = 'emotion_detection/Modelos/model_dropout.hdf5'

Ensure the model file exists at that location.

Configure any required database settings, environment variables, or external services before starting the application. Do not commit passwords, API keys, or other secrets to GitHub.

5. Run the Application

Check which Python file starts the Flask application. If "app.py" is the entry point, run:

python app.py

If the project is started through "main.py", use:

python main.py

Open the local address displayed in the terminal, commonly:

http://127.0.0.1:5000/

The actual address and startup command depend on the application's configuration.

🚀 How It Works

1. Register or log in: Students access the platform using the available authentication pages.
2. Practice interview questions: Users access the interview or quiz interface.
3. Record responses: Audio and video features capture responses where supported.
4. Process speech: Audio-processing modules convert recorded speech into text.
5. Analyze responses: The application can evaluate grammar, text sentiment, and facial emotions using its configured modules.
6. Review results: Users view the results provided by the application.

🎯 Project Objectives

- Make interview practice more accessible.
- Provide an interactive environment for students and job seekers.
- Explore facial emotion recognition and speech processing in interview scenarios.
- Apply natural language processing to grammar and sentiment analysis.
- Demonstrate the integration of machine learning with a Python web application.

🔮 Future Enhancements

- Add AI-generated interview questions tailored to specific job roles.
- Implement detailed interview performance reports.
- Improve speech recognition and response evaluation.
- Add secure user profiles and interview history.
- Deploy the application to a cloud hosting platform.
- Add a responsive user interface for mobile devices.
- Provide personalized feedback and recommendations for improvement.

🔐 Privacy and Security

- Do not upload personal recordings, private documents, database contents, or credentials.
- Obtain appropriate consent before recording or analyzing a person's audio or video.
- Secure authentication and database operations before deploying the application publicly.
- Treat automated emotion and sentiment predictions as estimates, not definitive assessments of a person's feelings or interview ability.

🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request describing your improvements.

📄 License

No license has been specified yet. Add an appropriate open-source license before allowing others to reuse, modify, or distribute the project.

👨‍💻 Author

Darsh

GitHub: "@darsh11712" (https://github.com/darsh11712)

⭐ Support

If you find this project useful, consider giving the repository a star on GitHub!
