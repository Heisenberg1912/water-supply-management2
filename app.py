import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the emotion detection model
model = "emotion_model.h5"

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Function to detect emotions
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detected_faces = faces.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in detected_faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype('float32') / 255.0
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1)

        prediction = model.predict(roi_gray)
        emotion_index = np.argmax(prediction)
        emotion = emotion_labels[emotion_index]

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return frame

# Streamlit UI
st.title("Real-Time Emotion Detection")
run = st.button('Start Emotion Detection')

if run:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video")
            break

        # Detect emotions in the frame
        frame = detect_emotion(frame)

        # Convert the image to RGB for Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in Streamlit
        st.image(frame_rgb, channels='RGB', use_column_width=True)

        if st.button('Stop'):
            cap.release()
            break
