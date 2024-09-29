import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode, ClientSettings
import av
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load your pre-trained emotion detection model
@st.cache_resource
def load_emotion_model():
    return load_model('emotion_model.h5')

model = load_emotion_model()

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Define the Video Transformer
class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        # Initialize face detector
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            # Extract the region of interest (face)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.astype('float32') / 255.0
            roi_gray = np.expand_dims(roi_gray, axis=0)
            roi_gray = np.expand_dims(roi_gray, axis=-1)
            
            # Predict emotion
            prediction = model.predict(roi_gray)
            emotion_index = np.argmax(prediction)
            emotion = emotion_labels[emotion_index]
            
            # Draw rectangle around face
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Put emotion label above the rectangle
            cv2.putText(img, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 0), 2)
        
        return img

# Streamlit UI
st.title("Real-Time Emotion Detection")

# WebRTC configuration
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False},
)

# Initialize webrtc_streamer
webrtc_ctx = webrtc_streamer(
    key="emotion-detection",
    mode=WebRtcMode.SENDRECV,
    client_settings=WEBRTC_CLIENT_SETTINGS,
    video_transformer_factory=EmotionDetector,
    async_transform=True,
)

# Optional: Display instructions
st.markdown("""
### Instructions:
1. Allow access to your webcam when prompted.
2. Ensure your face is visible in the camera frame.
3. The application will detect your emotions in real-time.
""")
