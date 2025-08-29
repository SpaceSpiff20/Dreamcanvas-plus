from speechify import Speechify
from speechify.tts import GetSpeechOptionsRequest
import base64
import os

def speechify_tts(text, voice_id="scott", api_key=None, language="en-US", model="simba-english"):
    """
    Convert text to speech using Speechify API.
    
    Args:
        text (str): Text to convert to speech
        voice_id (str): Speechify voice ID (default: "scott")
        api_key (str): Speechify API key (if None, will use environment variable SPEECHIFY_API_KEY)
        language (str): Language code (default: "en-US")
        model (str): TTS model ("simba-english" or "simba-multilingual")
    
    Returns:
        str: Path to the generated audio file
    """
    # Use environment variable if api_key not provided
    if api_key is None:
        api_key = os.getenv("SPEECHIFY_API_KEY")
        if not api_key:
            raise ValueError("Speechify API key not provided and SPEECHIFY_API_KEY environment variable not set")
    
    # Initialize Speechify client
    client = Speechify(token=api_key)
    
    # Generate speech
    audio_response = client.tts.audio.speech(
        audio_format="mp3",
        input=text,
        language=language,
        model=model,
        options=GetSpeechOptionsRequest(
            loudness_normalization=True,
            text_normalization=True
        ),
        voice_id=voice_id
    )
    
    # Decode audio data
    audio_bytes = base64.b64decode(audio_response.audio_data)
    
    # Save to file
    output_path = "outputs/speechify_audio.mp3"
    os.makedirs("outputs", exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    return output_path

def get_available_voices(api_key=None):
    """
    Get list of available Speechify voices.
    
    Args:
        api_key (str): Speechify API key (if None, will use environment variable)
    
    Returns:
        list: List of available voice objects
    """
    if api_key is None:
        api_key = os.getenv("SPEECHIFY_API_KEY")
        if not api_key:
            raise ValueError("Speechify API key not provided and SPEECHIFY_API_KEY environment variable not set")
    
    client = Speechify(token=api_key)
    return client.tts.voices.list()

def filter_voice_models(voices, *, gender=None, locale=None, tags=None):
    """
    Filter Speechify voices by gender, locale, and/or tags,
    and return the list of model IDs for matching voices.

    Args:
        voices (list): List of GetVoice objects.
        gender (str, optional): e.g. 'male', 'female'.
        locale (str, optional): e.g. 'en-US'.
        tags (list, optional): list of tags, e.g. ['timbre:deep'].

    Returns:
        list[str]: IDs of matching voice models.
    """
    results = []

    for voice in voices:
        # gender filter
        if gender and voice.gender.lower() != gender.lower():
            continue

        # locale filter (check across models and languages)
        if locale:
            if not any(
                any(lang.locale == locale for lang in model.languages)
                for model in voice.models
            ):
                continue

        # tags filter
        if tags:
            if not all(tag in voice.tags for tag in tags):
                continue

        # If we got here, the voice matches -> collect model ids
        for model in voice.models:
            results.append(model.name)

    return results 