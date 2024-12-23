# AI Text Generator

A Streamlit web application that generates text using Cohere's AI model. This application provides a user-friendly interface to interact with Cohere's powerful language model.

## Features

- Text generation using Cohere's AI model
- Adjustable parameters (max tokens and temperature)
- Simple and intuitive user interface
- Secure API key handling
- Real-time text generation
- Rate limiting to prevent API abuse
- Error handling and user feedback
- Responsive design

## Live Demo

Visit [AI Text Generator](https://cohere-aichat.streamlit.app/) to try the application.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Cohere API key ([Get one here](https://cohere.ai))

### Installation

1. Clone the repository: 
git clone https://github.com/yourusername/ai-text-generator.git

> Note: Make sure to create and activate your virtual environment before installing dependencies:
> ```bash
> python -m venv venv
> ```

2. Navigate to the project directory:
cd ai-text-generator
3. Activate the virtual environment:

Windows:
```
.\venv\Scripts\activate
```

macOS/Linux:
```
source venv/bin/activate
```

4. Install the dependencies:
```
pip install -r requirements.txt
```

5. Set up your environment variables:
```
API_URL=http://localhost:8000
COHERE_API_KEY=your_api_key_here  # Optional for local development
```

6. Run the application:
```bash
# Start the FastAPI backend first
uvicorn main:app --reload --port 8000

# In a new terminal, start the Streamlit frontend
streamlit run app.py
```

7. Open your browser and go to `http://localhost:8501`

## Project Structure

- `app.py`: The main application file that contains the Streamlit UI and logic.
- `main.py`: The FastAPI backend that handles API requests and Cohere integration.
- `requirements.txt`: Lists the dependencies for the project.
- `README.md`: This file, providing an overview of the project and instructions for running it.
- `.env`: Environment variables configuration (not tracked in git)

## API Endpoints

### Generate Text
- **URL**: `/api/generate`
- **Method**: `POST`
- **Rate Limit**: 5 requests per minute
- **Request Body**:
```
{
  "api_key": "your-cohere-api-key",
  "prompt": "Write a short story about a cat.",
  "max_tokens": 200,
  "temperature": 0.7
}
```

### Deploy Your Own

1. Fork this repository
2. Create a new app on [Streamlit Cloud](https://share.streamlit.io)
3. Connect your forked repository
4. Deploy!

## Development

### Code Style
- Python code follows PEP 8 guidelines
- Type hints are used throughout the codebase
- Error handling follows best practices

### Testing
Run tests using:
```
pytest
```

## Acknowledgments

- [Cohere](https://cohere.ai) for providing the AI model
- [Streamlit](https://streamlit.io) for the web framework
- [FastAPI](https://fastapi.tiangolo.com) for the backend framework