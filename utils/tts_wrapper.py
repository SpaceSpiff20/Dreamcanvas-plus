import os
from typing import Optional

# Import both TTS implementations
try:
    from .elevenlabs_voice import elevenlabs_tts
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    from .speechify_voice import speechify_tts
    SPEECHIFY_AVAILABLE = True
except ImportError:
    SPEECHIFY_AVAILABLE = False

def tts_convert(text: str, voice_id: str = "scott", api_key: Optional[str] = None, 
                provider: str = "speechify", language: str = "en-US", 
                model: str = "simba-english") -> str:
    """
    Unified TTS function that supports both ElevenLabs and Speechify.
    
    Args:
        text (str): Text to convert to speech
        voice_id (str): Voice ID for the selected provider
        api_key (str, optional): API key for the selected provider
        provider (str): TTS provider ("speechify" or "elevenlabs")
        language (str): Language code (for Speechify only)
        model (str): TTS model (for Speechify only)
    
    Returns:
        str: Path to the generated audio file
    
    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    provider = provider.lower()
    
    if provider == "speechify":
        if not SPEECHIFY_AVAILABLE:
            raise ValueError("Speechify not available. Install with: pip install speechify-api")
        
        # Use environment variable if not provided
        if api_key is None:
            api_key = os.getenv("SPEECHIFY_API_KEY")
        
        return speechify_tts(
            text=text,
            voice_id=voice_id,
            api_key=api_key,
            language=language,
            model=model
        )
    
    elif provider == "elevenlabs":
        if not ELEVENLABS_AVAILABLE:
            raise ValueError("ElevenLabs not available. Install with: pip install elevenlabs")
        
        # Use environment variable if not provided
        if api_key is None:
            api_key = os.getenv("ELEVENLABS_API_KEY")
        
        return elevenlabs_tts(
            text=text,
            voice_id=voice_id,
            api_key=api_key
        )
    
    else:
        raise ValueError(f"Unsupported TTS provider: {provider}. Supported providers: speechify, elevenlabs")

# Backward compatibility: alias for the original function name
def elevenlabs_tts_wrapper(text, voice_id, api_key):
    """
    Backward compatibility wrapper for the original elevenlabs_tts function.
    Now uses Speechify by default but can be configured to use ElevenLabs.
    """
    provider = os.getenv("TTS_PROVIDER", "speechify")
    return tts_convert(text, voice_id, api_key, provider) 