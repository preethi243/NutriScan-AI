# --- Import and setup ---
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# --- Gemini functions ---
def get_gemini_response(input_text, image, prompt):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[input_text, image, prompt]    )
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    else:
        raise FileNotFoundError("No file uploaded")

# --- Streamlit UI ---
st.set_page_config(page_title="Intelligent Food Calories Calculator")
st.header("🥗 Intelligent Food Calories Calculator")

input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")  
submit = st.button("🍽️ Tell me the total calories")

# --- Prompt ---
input_prompt = """
You are an expert nutritionist. Look at the food items in the image
and calculate the total calories. Also, list each item with its calorie count in this format:

1. Item name - X calories
2. Item name - Y calories
...
"""

# --- On submit ---
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("🧠 Calorie Analysis")
        st.write(response)
    except FileNotFoundError:
        st.error("Please upload an image.")
