import streamlit as st
import cohere
from main import generate_text_with_cohere

# Configure Streamlit page
st.set_page_config(
    page_title="AI Text Generator",
    page_icon="✨",
    layout="centered"
)

def show_api_instructions():
    st.markdown("""
    ### How to get your Cohere API Key:
    1. Go to [Cohere's website](https://cohere.ai)
    2. Sign up for an account
    3. Navigate to your dashboard
    4. Copy your API key
    """)

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
            
        try:
            with st.spinner("Generating text..."):
                generated_text = generate_text_with_cohere(
                    api_key=api_key,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                if generated_text:
                    st.write(generated_text)
        except cohere.UnauthorizedError:
            st.error("Invalid API key. Please check your key and try again.")
        except cohere.TooManyRequestsError:
            st.error("Rate limit exceeded. Please wait before trying again.")
        except (cohere.BadRequestError, cohere.InternalServerError, cohere.ServiceUnavailableError) as ce:
            st.error(f"Error from Cohere API: {str(ce)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 