# backend/app/services/scene_generator.py

import requests
from app.utils.prompt_templates import SCENE_PROMPT

class SceneGenerator:

    @staticmethod
    def generate_scenes(story_text: str):
        """
        Converts story into structured scenes.
        """
        url = "http://localhost:1234/v1/chat/completions"

        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": SCENE_PROMPT},
                {"role": "user", "content": story_text}
            ],
            "temperature": 0.6,
            "max_tokens": 1500
        }

        response = requests.post(url, json=payload)
        data = response.json()

        scenes = data["choices"][0]["message"]["content"]
        return {"scenes": scenes}
