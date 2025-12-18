# app/models/animation_models.py
from pydantic import BaseModel
from typing import List

# ---------------------------------------------------------
# Input model: Scenes list for both /frames and /video
# ---------------------------------------------------------
class AnimationRequest(BaseModel):
    scenes: List[str]

# ---------------------------------------------------------
# Response for /animation/frames
# ---------------------------------------------------------
class AnimationResponse(BaseModel):
    images: List[str]

# ---------------------------------------------------------
# Response for /animation/video
# ---------------------------------------------------------
class StoryVideoResponse(BaseModel):
    video: str
