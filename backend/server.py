import os
import json
import zipfile
import io
import traceback
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI, APIError
from dotenv import load_dotenv
from pydantic import field_validator, ValidationError, BaseModel, Json
from typing import Dict
from prompt_config import SYSTEM_PROMPT

# Pydantic model for validating the AI's JSON response
class AIResponse(BaseModel):
    plugin_name: str
    files: Dict[str, str]

    @field_validator('files')
    def files_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('The "files" dictionary cannot be empty.')
        return v

class PluginRequest(BaseModel):
    description: str

# Load environment variables (your API key from .env)
load_dotenv()
app = FastAPI()

# CORS setup (allows frontend like React to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Logic to switch between Groq (dev) and paid API (prod) ---
USE_GROQ = os.getenv("USE_GROQ", "true").lower() == "true"
MODEL_NAME = "" # Will be set in the if/else block

if USE_GROQ:
    print("--- Running in Development Mode (using Groq) ---")
    client = AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
    )
    MODEL_NAME = "llama3-8b-8192"
else:
    print("--- Running in Production Mode (using AI/ML API) ---")
    client = AsyncOpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=os.getenv("AIML_API_KEY"),
    )
    MODEL_NAME = os.getenv("OPENAI_MODEL")


# ------------------- Core Logic Functions (Refactored) -------------------
async def call_ai_and_validate(description: str) -> AIResponse:
    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        try:
            response = await client.chat.completions.create(
                # model=os.getenv("OPENAI_MODEL", "gpt-4o-2024-05-13"),
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Create a WordPress plugin: {description}"}
                ],
                # UPDATED: Enforce JSON mode reliably
                response_format={"type": "json_object"},
                max_tokens=6000,
                temperature=0.5
            )
            
            raw_content = response.choices[0].message.content
            # UPDATED: Use Pydantic for parsing and validation in one step
            validated_data = AIResponse.model_validate_json(raw_content)
            return validated_data

        except (APIError, ValidationError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == MAX_RETRIES:
                # If all retries fail, re-raise the last exception
                raise
            await asyncio.sleep(1) # Wait 1 second before retrying
        except Exception as e:
            # Catch any other unexpected errors during the API call
            print(f"An unexpected error occurred during API call: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred while contacting the AI.")

# NEW: Refactored function to create the ZIP archive
def create_zip_archive(data: AIResponse) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, content in data.files.items():
            zip_file.writestr(file_path, content)
    zip_buffer.seek(0)
    return zip_buffer

# ------------------- API Endpoint -------------------
# UPDATED: The main endpoint is now cleaner and orchestrates the calls
@app.post("/generate-plugin")
async def generate_plugin(plugin_request: PluginRequest):
    try:
        # Step 1: Call AI and get validated data
        validated_data = await call_ai_and_validate(plugin_request.description)
        
        # Step 2: Create the ZIP file from the validated data
        zip_buffer = create_zip_archive(validated_data)

        # Step 3: Return the ZIP file to the user
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={validated_data.plugin_name}.zip"}
        )

    except APIError as e:
        print(f"API Error after all retries: {e}")
        raise HTTPException(status_code=502, detail="The AI service failed to respond.")
    
    except ValidationError as e:
        print(f"AI response validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"The AI returned an invalid data structure.")
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)