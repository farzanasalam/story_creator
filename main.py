import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import openai

app = FastAPI()

# Initialize Supabase client
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-supabase-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize OpenAI API
OPENAI_API_KEY = "your-openai-api-key"
openai.api_key = OPENAI_API_KEY


# Models
class Character(BaseModel):
    name: str
    details: str


class StoryRequest(BaseModel):
    character_name: str


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/create_character", status_code=201)
async def create_character(character: Character):
    try:
        data = {
            "name": character.name,
            "details": character.details
        }
        response = supabase.table("characters").insert(data).execute()
        if response.status_code != 201:
            logger.error("Character creation failed")
            raise HTTPException(status_code=400, detail="Character creation failed")
        return {"id": response.data[0]["id"], "name": character.name, "details": character.details}
    except Exception as e:
        logger.exception("Error creating character")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/generate_story", status_code=201)
async def generate_story(story_request: StoryRequest):
    try:
        character_name = story_request.character_name
        logger.info("Fetching character: %s", character_name)
        response = supabase.table("characters").select("*").eq("name", character_name).execute()
        if not response.data:
            logger.warning("Character not found: %s", character_name)
            raise HTTPException(status_code=404, detail="Character not found")

        character = response.data[0]
        story_prompt = (f"{character['name']}, {character['details']}.\n"
                        "Write a short story (4-5 sentences) based on this character.")

        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=story_prompt,
            max_tokens=150
        )

        story = openai_response.choices[0].text.strip()
        return {"story": story}
    except Exception as e:
        logger.exception("Error generating story")
        raise HTTPException(status_code=500, detail="Internal Server Error")
