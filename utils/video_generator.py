from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_story_frame(image_path, story_text, output_path="outputs/frame_story.png"):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    # Create transparent overlay
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    box_y = int(height * 0.65)
    draw.rectangle([(0, box_y), (width, height)], fill=(0, 0, 0, 160))  

    # Load font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    wrapped_text = textwrap.fill(story_text, width=40)
    draw.text((30, box_y + 20), wrapped_text, font=font, fill=(255, 255, 255, 255))

    final = Image.alpha_composite(img, overlay)
    final.convert("RGB").save(output_path)
    return output_path

def generate_final_video(image_path, audio_path, story_text, output_path="outputs/final_video.mp4"):
    frame_path = create_story_frame(image_path, story_text)
    audio = AudioFileClip(audio_path)
    image_clip = ImageClip(frame_path).set_duration(audio.duration).set_audio(audio)

    final = CompositeVideoClip([image_clip.fadein(1).fadeout(1)])
    final.write_videofile(output_path, fps=24)

    return output_path