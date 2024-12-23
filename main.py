from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, field_validator
import cohere
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import uuid
import logging
import re

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  
        "https://cohere-flautomations.vercel.app",
        "https://cohere-ai-chat-flucena-flucenas-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request ID for better tracking
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Update the error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_id = str(uuid.uuid4())
    error_msg = str(exc)
    
    # More detailed logging for debugging
    logger.error(f"""
    Error ID: {error_id}
    Path: {request.url.path}
    Method: {request.method}
    Error: {error_msg}
    """, exc_info=exc)
    
    # During development, return the actual error message
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": error_msg,  # Include actual error message
            "error_id": error_id
        }
    )

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

class GenerateRequest(BaseModel):
    api_key: str = Field(..., min_length=32, max_length=128)
    prompt: str = Field(..., min_length=1, max_length=2000)
    max_tokens: int = Field(..., ge=10, le=500)
    temperature: float = Field(..., ge=0.0, le=2.0)

    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if not re.match(r'^[A-Za-z0-9-_]+$', v):
            raise ValueError('Invalid API key format')
        return v

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        if re.search(r'[<>]', v):
            raise ValueError('Prompt contains invalid characters')
        return v

@app.post("/api/generate")
@limiter.limit("5/minute")
async def generate_text(request: Request, data: GenerateRequest):
    try:
        # Log the request (excluding API key)
        logger.info(f"Generate request received with prompt length: {len(data.prompt)}")
        
        # Initialize client without num_workers
        client = cohere.Client(
            api_key=data.api_key,
            timeout=30  # Keep timeout for safety
        )
        
        # Log before making Cohere request
        logger.info("Making request to Cohere API")
        
        response = client.generate(
            model='command-xlarge-nightly',
            prompt=data.prompt,
            max_tokens=data.max_tokens,
            temperature=data.temperature,
            truncate='END'
        )
        
        # Log successful response
        logger.info("Successfully received response from Cohere")
        
        return {"text": response.generations[0].text}
        
    except cohere.CohereError as ce:
        # Specific handling for Cohere API errors
        logger.error(f"Cohere API error: {str(ce)}")
        if "401" in str(ce):
            raise HTTPException(status_code=401, detail="Invalid API key")
        elif "429" in str(ce):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        elif "503" in str(ce):
            raise HTTPException(status_code=503, detail="Service temporarily unavailable")
        else:
            raise HTTPException(status_code=500, detail=f"Cohere API error: {str(ce)}")
            
    except Exception as e:
        # General error handling with more context
        logger.error(f"Unexpected error in generate_text: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/")
async def root():
    return {"message": "API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 