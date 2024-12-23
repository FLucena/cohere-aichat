import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Text Generator",
    page_icon="✨",
    layout="centered"
)

# Backend API URL - use environment variable or default to production URL
API_URL = os.getenv('API_URL', 'https://cohere-aichat.streamlit.app/')

def show_api_instructions():
    st.markdown("""
    ### How to get your Cohere API Key:
    1. Go to [Cohere's website](https://cohere.ai)
    2. Sign up for an account
    3. Navigate to your dashboard
    4. Copy your API key
    """)

def generate_text(api_key: str, prompt: str, max_tokens: int, temperature: float) -> str:
    try:
        url = f"{API_URL}/api/generate"
        
        response = requests.post(
            url,
            json={
                "api_key": api_key,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        
        if response.status_code != 200:
            st.sidebar.write(f"Response Status: {response.status_code}")
            st.sidebar.write(f"Response Text: {response.text}")
        
        if response.status_code == 401:
            st.error("Invalid API key. Please check your key and try again.")
            return None
        elif response.status_code == 429:
            st.error("Rate limit exceeded. Please wait before trying again.")
            return None
            
        response.raise_for_status()
        return response.json()["text"]
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        st.sidebar.write(f"Full error: {str(e)}")
        return None

# Main UI
def main():
    st.title("AI Text Generator")
    st.write("Generate text using Cohere's AI model")

    # Sidebar for API key
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter your Cohere API Key", type="password")
        show_api_instructions()

    # Main content
    prompt = st.text_area("Enter your prompt:", height=100)
    col1, col2 = st.columns(2)
    
    with col1:
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=500, value=200)
    with col2:
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)

    if st.button("Generate"):
        if not api_key:
            st.error("Please enter your API key")
            return
            
        if not prompt:
            st.error("Please enter a prompt")
            return
            
        with st.spinner("Generating text..."):
            generated_text = generate_text(api_key, prompt, max_tokens, temperature)
            if generated_text:
                st.write(generated_text)

if __name__ == "__main__":
    main() 