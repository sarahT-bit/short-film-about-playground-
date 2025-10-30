import openai
import os
import requests
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from gtts import gTTS

openai.api_key = os.getenv("OPENAI_API_KEY")

# 1️⃣ Generate a short, cinematic script
script_prompt = """
Write a short, fun and educational script for a 1-minute film about different fruits.
Include around 5 short scenes. Each scene should have a title, a short description,
and a few narrator lines. The tone should be cheerful and family-friendly.
"""
response = openai.ChatCompletion.create(
    model="gpt-5",
    messages=[{"role": "user", "content": script_prompt}]
)
script = response.choices[0].message.content
print("\n=== SCRIPT GENERATED ===\n")
print(script)

# 2️⃣ Split script into scenes
scenes = [s.strip() for s in script.split("Scene") if s.strip()]

# 3️⃣ Generate DALL·E images for each scene
image_paths = []
for i, scene in enumerate(scenes, start=1):
    dalle_prompt = f"Cinematic colorful image for this scene: {scene}"
    image = openai.images.generate(
        model="gpt-image-1",
        prompt=dalle_prompt,
        size="1024x1024"
    )
    image_url = image.data[0].url

    image_path = f"scene_{i}.png"
    img_data = requests.get(image_url).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)

    image_paths.append(image_path)
    print(f"🖼️  Generated image for Scene {i}")

# 4️⃣ Generate narration audio
tts = gTTS(text=script, lang='en')
tts.save("narration.mp3")
print("🎙️  Narration audio generated.")

# 5️⃣ Combine visuals + narration into a short video
clips = []
for path in image_paths:
    clip = ImageClip(path).set_duration(5)
    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")
audio = AudioFileClip("narration.mp3")
video = video.set_audio(audio)

video.write_videofile("short_fruit_film.mp4", fps=24)
print("\n🎬 Short fruit film created successfully: short_fruit_film.mp4")

