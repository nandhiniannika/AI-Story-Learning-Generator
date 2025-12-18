from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routes.upload import router as upload_router
from app.routes.story import router as story_router
from app.routes.scenes import router as scenes_router
from app.routes.animation import router as animation_router  # contains /animation/* routes

app = FastAPI(
    title="PDF to Animation Backend",
    description="Backend for converting PDF → story → scenes → animation → video",
    version="1.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(story_router, prefix="/story", tags=["Story"])
app.include_router(scenes_router, prefix="/scenes", tags=["Scenes"])
app.include_router(animation_router, prefix="/animation", tags=["Animation"])

@app.get("/")
def root():
    return {"message": "PDF-to-Animation backend running!"}
