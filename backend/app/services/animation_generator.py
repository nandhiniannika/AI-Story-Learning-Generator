import os
import re
import torch
import ffmpeg
from gtts import gTTS

from diffusers import StableDiffusionPipeline
from moviepy import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip
)

# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(short_description):
    return (
        "highly detailed illustration, cinematic lighting, 4k resolution, "
        f"{short_description}"
    )

# ============================================================
# STORY IMPROVER
# ============================================================

def improvise_narration(text):
    improved = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.endswith("?"):
            improved.append("Let me ask you this: " + line)
        else:
            improved.append("Here's something interesting: " + line)

    return " ".join(improved)

# ============================================================
# MAIN CLASS
# ============================================================

class AnimationGenerator:

    def __init__(self):
        self.model_id = "runwayml/stable-diffusion-v1-5"

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32
        ).to("cpu")

        for d in [
            "data/frames",
            "data/audio",
            "data/story",
            "data/video",
            "data/scenes"
        ]:
            os.makedirs(d, exist_ok=True)

    # ======================================================
    # LOAD SCENE DESCRIPTIONS
    # ======================================================

    def load_short_descriptions(self):
        path = "data/scenes/scenes.txt"
        if not os.path.exists(path):
            raise FileNotFoundError("❌ scenes.txt not found")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        return re.findall(r"Short description:\s*(.*)", text, re.IGNORECASE)

    # ======================================================
    # GENERATE IMAGES
    # ======================================================

    def generate_frames(self):
        descriptions = self.load_short_descriptions()
        frame_paths = []

        for i, desc in enumerate(descriptions):
            prompt = build_prompt(desc)

            result = self.pipe(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7,
                height=768,
                width=768
            )

            image = result.images[0]
            path = f"data/frames/scene_{i+1}.png"
            image.save(path)
            frame_paths.append(path)

        return frame_paths

    # ======================================================
    # GENERATE AUDIO
    # ======================================================

    def generate_audio_from_story(self):
        with open("data/story/story.txt", "r", encoding="utf-8") as f:
            text = f.read()

        clean = re.sub(r"[^\w\s.!?,-]", "", text)
        improved = improvise_narration(clean)

        audio_path = "data/audio/narration.mp3"
        gTTS(improved, lang="en").save(audio_path)

        return audio_path

    # ======================================================
    # FINAL VIDEO (NO CAPTIONS)
    # ======================================================

    def generate_video(self):

        frames = sorted(
            f"data/frames/{f}"
            for f in os.listdir("data/frames")
            if f.startswith("scene_")
        )

        if not frames:
            raise FileNotFoundError("❌ No frames found")

        audio_path = self.generate_audio_from_story()
        audio = AudioFileClip(audio_path)

        duration_per_frame = audio.duration / len(frames)

        clips = [
            ImageClip(frame).with_duration(duration_per_frame)
            for frame in frames
        ]

        video = concatenate_videoclips(clips, method="compose")

        temp_video = "data/video/temp.mp4"
        final_video = "data/video/final_video.mp4"

        video.write_videofile(
            temp_video,
            fps=30,
            codec="libx264",
            audio=False
        )

        (
            ffmpeg
            .input(temp_video)
            .output(
                ffmpeg.input(audio_path),
                final_video,
                vcodec="copy",
                acodec="aac"
            )
            .overwrite_output()
            .run()
        )

        return final_video
