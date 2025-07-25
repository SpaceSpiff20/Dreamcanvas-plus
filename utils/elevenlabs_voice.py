from elevenlabs import ElevenLabs

def elevenlabs_tts(text, voice_id, api_key):
    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_monolingual_v1",
        output_format="mp3_44100"
    )

    # Combine all audio chunks from generator
    audio_bytes = b''.join(audio_stream)

    output_path = "output_audio.mp3"
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path