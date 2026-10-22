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

# Example usage
text = "I am so happy and excited to see you!"
emotion, confidence = detect_emotion(text)

print(f"Detected Emotion: {emotion}")
print(f"Confidence Score: {confidence:.2f}")
