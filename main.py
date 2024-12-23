import cohere
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def generate_text_with_cohere(
    api_key: str, 
    prompt: str, 
    max_tokens: int = 200, 
    temperature: float = 0.7
) -> Optional[str]:
    try:
        # Initialize client
        client = cohere.Client(api_key=api_key)
        
        # Log before making Cohere request
        logger.info("Making request to Cohere API")
        
        response = client.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            truncate='END'
        )
        
        # Log successful response
        logger.info("Successfully received response from Cohere")
        
        return response.generations[0].text
        
    except cohere.CohereError as ce:
        # Specific handling for Cohere API errors
        logger.error(f"Cohere API error: {str(ce)}")
        raise ce 