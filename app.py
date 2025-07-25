import streamlit as st
from PIL import Image
import os

# Import your utility functions
from utils.caption import get_caption
from utils.emotion import get_dominant_color, infer_emotion_from_color
from utils.gemini_story import generate_story
from utils.elevenlabs_voice import elevenlabs_tts
from utils.video_generator import generate_final_video
from utils.auto_description import auto_generate_description

# Set Streamlit page settings
st.set_page_config(page_title="DreamCanvas+", page_icon="🎨")
st.title("🎨 DreamCanvas+: AI Story from Kids' Drawings")

# Ensure the output directory exists
os.makedirs("outputs", exist_ok=True)

# Upload section
uploaded = st.file_uploader("Upload your child's drawing", type=["jpg", "png", "jpeg"])

if uploaded:
    image_path = os.path.join("outputs", uploaded.name)

    with open(image_path, "wb") as f:
        f.write(uploaded.read())

    st.image(image_path, caption="Drawing Uploaded", use_column_width=True)

    if st.button("✨ Create Story Video"):
        try:
            with st.spinner("🔍 Captioning drawing..."):
                caption = get_caption(Image.open(image_path))

            color = get_dominant_color(image_path)
            emotion = infer_emotion_from_color(color)

            st.success(f"📝 Caption: {caption}")
            st.success(f"🎭 Emotion: {emotion}")

            with st.spinner("🧠 Generating story..."):
                story = generate_story(caption, emotion)
                st.text_area("📖 Story", story, height=150)

            with st.spinner("🎤 Generating voice..."):
                # Replace with your ElevenLabs voice ID and API key
                voice_id = "EXAVITQu4vr4xnSDxMaL"
                api_key = "sk_4c430c0ea81f5b5ba2ca266dd0ede00338860ba241ca7f96"  
                audio_path = elevenlabs_tts(story, voice_id, api_key)
                st.audio(audio_path)

            with st.spinner("🎞️ Generating video..."):
                final_video = generate_final_video(image_path, audio_path, story)
                st.video(final_video)

            with st.spinner("📝 Generating description..."):
                desc = auto_generate_description(caption, emotion, story)
                st.text_area("📄 Video Description", desc, height=200)

            # Download buttons
            with open(final_video, "rb") as f_vid:
                st.download_button("📥 Download Video", f_vid, file_name="dreamcanvas_video.mp4")

            with open(audio_path, "rb") as f_audio:
                st.download_button("📥 Download Audio", f_audio, file_name="dreamcanvas_audio.mp3")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
