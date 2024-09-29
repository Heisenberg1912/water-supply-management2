import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load your emotion detection model with caching
@st.cache_resource
def load_emotion_model():
    return load_model('emotion_model.h5')

model = load_emotion_model()

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Function to detect emotion from the image
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

# Capture webcam input
image_file = st.camera_input("Take a picture")

if image_file:
    # Convert the image to OpenCV format
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    if frame is not None:
        # Detect emotions in the frame
        result_frame = detect_emotion(frame)

        # Convert the image back to RGB for Streamlit
        result_rgb = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)

        # Display the frame with detected emotions
        st.image(result_rgb, channels='RGB', use_column_width=True)
    else:
        st.error("Failed to process the image.")
