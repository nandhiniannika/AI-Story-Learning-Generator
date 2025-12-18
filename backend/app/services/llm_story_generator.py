# backend/app/services/llm_story_generator.py

import requests
from app.utils.prompt_templates import STORY_PROMPT

class StoryGenerator:

    @staticmethod
    def generate_story(extracted_text: str):
        """
        Sends extracted text to local Llama model and receives a story.
        """
        url = "http://localhost:1234/v1/chat/completions"  # llama.cpp server

        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": STORY_PROMPT},
                {"role": "user", "content": extracted_text}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(url, json=payload)
        data = response.json()

        story = data["choices"][0]["message"]["content"]
        return {"story": story}
