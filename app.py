import streamlit as st
import requests
import numpy as np
import cv2
import base64
from dotenv import load_dotenv
import os
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# Function to call the Google Gemini API
def identify_plant(image_data):
    """Identifies a plant from an image using the Google Gemini API.

    Args:
        image_data: The raw image data (in bytes).

    Returns:
        A string containing the identified plant name, or None if no plant is identified.
    """

    # Encode the image data to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    # Set the API endpoint and parameters
    url = "https://gemini.googleapis.com/v1/models/gemini-1.5-flash-latest:predict"  # Ensure this endpoint is correct
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "instances": [
            {
                "image": {
                    "content": encoded_image  # Use the correct structure for image data
                },
                "features": {
                    "plant_identification": {}
                }
            }
        ]
    }

    # Send the request to the API
    response = requests.post(url, headers=headers, json=data, verify=False)

    # Process the response
    if response.status_code == 200:
        prediction = response.json().get("predictions", [])
        if prediction:
            plant_name = prediction[0].get("plant_identification", {}).get("plant_name")
            return plant_name
        else:
            st.error("No predictions found in the response.")
            return None
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Function to display tutorial
def display_tutorial():
    st.subheader("How to Use This App")
    st.write("""
    1. Use the sidebar to capture a live image or upload an image from your device.
    2. If you capture an image, it will be processed, and the identification results will be displayed.
    3. The results will include the popular name, scientific name, and identification probability for plants.
    4. For other images, a brief description will be provided.
    """)

# Video processor class for handling image capture
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.captured_image = None

    def recv(self, frame):
        # Save the current frame as the captured image
        self.captured_image = frame.to_ndarray(format="bgr24")  # Frame is in BGR format
        return frame

# Sidebar for image input options
st.sidebar.title("Image Input Options")
image_option = st.sidebar.radio("Choose an option:", ["Upload Image", "Capture Image"])

# Initialize a placeholder for results
results_placeholder = st.empty()

if image_option == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Read the uploaded image and convert it to bytes
        image_data = uploaded_file.read()  # Read the file as bytes
        st.sidebar.image(image_data, caption="Uploaded Image", use_column_width=True)

        # Call the identification function
        if st.sidebar.button("Identify"):
            plant_name = identify_plant(image_data)
            results_placeholder.write(f"The plant in the image is: {plant_name}" if plant_name else "No plant was identified.")

elif image_option == "Capture Image":
    st.sidebar.write("Capture an image from your webcam:")

    # Create a video streamer for capturing images
    webrtc_ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
    )

    # If an image has been captured, display and process it
    if webrtc_ctx.video_processor and webrtc_ctx.video_processor.captured_image is not None:
        captured_image = webrtc_ctx.video_processor.captured_image
        
        # Convert the captured image to bytes
        _, buffer = cv2.imencode('.jpg', captured_image)  # Encode to JPEG format
        image_data = buffer.tobytes()  # Get image data as bytes

        st.sidebar.image(captured_image, caption="Captured Image", use_column_width=True)

        # Call the identification function
        if st.sidebar.button("Identify"):
            plant_name = identify_plant(image_data)
            results_placeholder.write(f"The plant in the image is: {plant_name}" if plant_name else "No plant was identified.")

# Display tutorial in the main area
st.title("Image Identifier App")
display_tutorial()

# Style the app for responsiveness
st.markdown(
    """
    <style>
        .stApp {
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        @media (max-width: 768px) {
            .stApp {
                flex-direction: column;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)
