from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter(prefix="/scenes")

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

class SceneResponse(BaseModel):
    scenes: list

@router.post("", response_model=SceneResponse)
async def create_scenes():

    story_path = "data/story/story.txt"

    if not os.path.exists(story_path):
        raise HTTPException(
            status_code=400,
            detail="❌ Story file not found. Generate story first using /story."
        )

    # Read saved story
    with open(story_path, "r", encoding="utf-8") as f:
        story = f.read()

    prompt = f"""
    Break the following story into clear animation scenes.
    For each scene, include:
    - scene number
    - short description (1–2 sentences)
    - key characters
    - setting (place/time)
    - important visual actions

    STORY:
    {story}
    """

    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "You break stories into animation-ready scenes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    data = response.json()

    scenes_text = data["choices"][0]["message"]["content"]

    # Convert scene text to list
    scenes_list = scenes_text.split("\n\n")

    # ----------------------------------------------------
    #  ✅ NEW FEATURE: SAVE SCENES INTO A FILE
    # ----------------------------------------------------
    os.makedirs("data/scenes", exist_ok=True)
    scenes_path = "data/scenes/scenes.txt"

    with open(scenes_path, "w", encoding="utf-8") as outfile:
        outfile.write(scenes_text)

    print(f"🎉 Scenes saved to {scenes_path}")

    return SceneResponse(scenes=scenes_list)
