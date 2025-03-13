import streamlit as st
from google import genai
from google.genai import types
import pathlib
import json

# Initialize the Gemini API client
client = genai.Client(api_key="AIzaSyCAes7xlarqRP7GVHQ")

# System instruction
sys_instruct = (
    "You are an expert technical document summarizer. "
    "Provide the response in JSON object notation like { 'url': '<url>' } with a single URL only. "
    "If an out-of-context question is asked, return 'No relevant URL found'. "
    "If no relevant response is found, return 'Please try again'."
)

# Streamlit UI
st.title("📄 PDF URL Extractor using Gemini")
st.write("Upload a PDF and enter a query to retrieve a relevant URL.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# User input field
user_input = st.text_input("Enter your query:")

if uploaded_file and user_input:
    # Save uploaded file temporarily
    temp_filepath = f"temp_{uploaded_file.name}"
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read the PDF file
    filepath = pathlib.Path(temp_filepath)

    # Generate response with Gemini API
    with st.spinner("Generating response..."):
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=[
                types.Part.from_bytes(
                    data=filepath.read_bytes(),
                    mime_type="application/pdf",
                ),
                f"Provide the URL for: {user_input}",
            ],
        )

    # Display the response
    try:
        json_response = json.loads(response.text)
        st.subheader("🔗 Extracted URL:")
        st.json(json_response)  # Display as formatted JSON
    except json.JSONDecodeError:
        st.error("Invalid JSON response. Try again.")

