from dotenv import load_dotenv

load_dotenv()  ## loading environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from IPython.display import Markdown
import textwrap


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro model to get responses
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image):
    
    response = model.generate_content(
        [input, image]
    )
    # return response.text
    return to_markdown(response.text)

st.set_page_config(page_title="Flow chart to code generator")
st.title("Flow chart to code generator")

# Upload image
st.subheader("Upload Image")
uploaded_image = st.file_uploader("Upload flow chart image", type=["jpg", "png", "jpeg"])
image=""

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

# Select programming language
st.subheader("Select Programming Language")
language = st.selectbox("Choose a programming language", ["Python", "Java", "C++", "JavaScript", "Ruby", "Go", "Swift", "Rust", "PHP", "Kotlin"])

# Generate code button
if st.button("Generate Code"):
    if uploaded_image is not None:
        input = f"convert given flowchart to {language} code"
        response = get_gemini_response(input, image)
        st.subheader("Generated Code")
        st.markdown(f"\n\n{language}\n\n```{response._repr_markdown_()}```", unsafe_allow_html=True)
        if st.button("Copy to Clipboard"):
            st.write("Code copied to clipboard!")
