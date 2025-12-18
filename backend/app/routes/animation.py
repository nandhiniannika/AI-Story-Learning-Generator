# app/routes/animation.py
from fastapi import APIRouter
from app.models.animation_models import AnimationResponse
from app.services.animation_generator import AnimationGenerator

router = APIRouter()
generator = AnimationGenerator()

# ----------------------------------------------------
# POST /animation/frames → Reads scenes.txt automatically
# ----------------------------------------------------
@router.post("/animation/frames", response_model=AnimationResponse)
async def generate_frames():
    images = generator.generate_frames()     # no body expected
    return AnimationResponse(images=images)

# ----------------------------------------------------
# POST /animation/video → Uses auto frames + story audio
# ----------------------------------------------------
@router.post("/animation/video")
async def generate_video():
    video = generator.generate_video()       # no body expected
    return {"status": "success", "video": video}
