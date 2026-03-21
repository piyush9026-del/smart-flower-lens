from dotenv import load_dotenv

# load all environment variables from .env to system memory
load_dotenv()

# ---------------Importing necessary libraries-----------------

import streamlit as st                # Import Streamlit for building web app
import os                             # Import os for accessing environment variables, computer/server memory, folders, and secrets(like API keys)
from PIL import Image                 # Import PIL OR PILLOW (Python Imaging Library) for image processing
import google.generativeai as genai   # Import Gemini API client library to interact with Gemini Flash model

# --- CONFIGURATION --- (Accessing Gemini API key from environment variable)

genai.configure(api_key=os.getenv("Gemini_API_KEY"))

# Load Gemini Flash model

model=genai.GenerativeModel('gemini-flash-latest')

# Response from Gemini Flash

def get_gemini_response(input,image):
    response=model.generate_content([input,image])
    return response.text

# --------------------Streamlit App(User Interface)---------------------

# 1. Page configuration
st.set_page_config(page_title="Smart Flower Lens", page_icon="🥀")

# 2. User Interface

# Title and file uploader
st.title("Flower Image Recognization 🌹")
uploaded_file=st.file_uploader("Choose an image of a flower",type=["jpg","jpeg","png"])

# 3. Display the uploaded image and analyze it using Gemini Flash
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

    # Define button to trigger analysis
    if st.button("Identify Flower 🔍"):
        with st.spinner("Analyzing the image...(Internet required)"):
            try:

                # Define prompt for Gemini Flash to analyze the image and provide details.
                prompt = """
                Analyze this image carefully to identify the flowers present.

                IF THERE IS ONLY ONE FLOWER IN THE IMAGE:
                Provide its details directly in the following format without any numbering:
                
                **🌍English Details:**
                * **Name:** [Common Name]
                * **Scientific Name:** [Latin Name]
                * **Family:** [Plant Family]
                * **Found in India:** [Yes/No - Where in India?]
                * **Description:** [2 lines description]
                * **Ayurvedic/Medicinal Use:** [Brief medical use if any]

                ** Hindi Details:**
                [Translate the exact same details into simple Hindi language using the same bullet points]

                IF THERE ARE MULTIPLE FLOWERS IN THE IMAGE:
                List each flower separately with a numbered heading (e.g., **Flower 1:**, **Flower 2:**, etc.). Under each heading, provide the exact same English and Hindi format as shown above. Use a horizontal line (---) to separate the details of different flowers.
                """
                # Call the function to get response from Gemini Flash
                output=get_gemini_response(prompt,image)

                # Display the output
                st.success("Result Found")
                st.markdown(output)
            
            # Handle any exceptions that may occur during the API call or processing
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Made with ❤️ by Piyush Patel")