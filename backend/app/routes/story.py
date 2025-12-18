from fastapi import APIRouter
from pydantic import BaseModel
import requests
import os

router = APIRouter()   # no prefix

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

class StoryRequest(BaseModel):
    text: str

class StoryResponse(BaseModel):
    story: str

@router.post("/story", response_model=StoryResponse)
async def generate_story(req: StoryRequest):

    # Prepare LM Studio payload
    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Create a clear, student-friendly story."},
            {"role": "user", "content": req.text}
        ],
        "temperature": 0.7
    }

    # Send request to LM Studio
    response = requests.post(LM_STUDIO_URL, json=payload)
    data = response.json()

    # Extract story text
    story = data["choices"][0]["message"]["content"]

    # ===========================
    # SAVE STORY TO FILE
    # ===========================
    os.makedirs("data/story", exist_ok=True)
    story_path = "data/story/story.txt"

    with open(story_path, "w", encoding="utf-8") as f:
        f.write(story)

    print(f"📚 Story saved at: {story_path}")

    return StoryResponse(story=story)
