import streamlit as st
from google import genai
from google.genai import types
import pathlib
import json
import httpx

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

# User inputs file path
doc_url = "https://thecaseagainstinvisibility.com/media/birla.pdf"  # Replace with the actual URL of your PDF

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

# User enters a query
user_input = st.text_input("Enter your query:")

if doc_data and user_input:
    with st.spinner("Generating response..."):
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=[
                types.Part.from_bytes(
                    data=doc_data,
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
