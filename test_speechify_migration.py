import os
import pytest
import base64
import tempfile
from unittest.mock import Mock, patch
from speechify import Speechify
from speechify.tts import GetSpeechOptionsRequest

# Import our TTS functions
from utils.speechify_voice import speechify_tts, get_available_voices, filter_voice_models
from utils.tts_wrapper import tts_convert

class TestSpeechifyMigration:
    """Test suite for Speechify TTS migration."""
    
    @pytest.fixture
    def mock_speechify_client(self):
        """Mock Speechify client for testing."""
        mock_client = Mock(spec=Speechify)
        mock_tts = Mock()
        mock_audio = Mock()
        mock_speech = Mock()
        
        # Mock the response structure
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode('utf-8')
        mock_response.audio_format = "mp3"
        mock_response.speech_marks = {
            "type": "sentence",
            "start": 0,
            "end": 2,
            "start_time": 0,
            "end_time": 1024,
            "value": "hi",
            "chunks": [
                {
                    "type": "word",
                    "start": 0,
                    "end": 2,
                    "start_time": 0,
                    "end_time": 1024,
                    "value": "hi"
                }
            ]
        }
        mock_response.billable_characters_count = 2
        
        mock_speech.return_value = mock_response
        mock_audio.speech = mock_speech
        mock_tts.audio = mock_audio
        mock_client.tts = mock_tts
        
        return mock_client
    
    def test_speechify_tts_basic_functionality(self, mock_speechify_client):
        """Test basic Speechify TTS functionality."""
        with patch('utils.speechify_voice.Speechify', return_value=mock_speechify_client):
            with tempfile.TemporaryDirectory() as temp_dir:
                # Temporarily change working directory
                original_cwd = os.getcwd()
                os.chdir(temp_dir)
                
                try:
                    # Create outputs directory
                    os.makedirs("outputs", exist_ok=True)
                    
                    # Test TTS conversion
                    result = speechify_tts(
                        text="Hello, world!",
                        voice_id="scott",
                        api_key="test_key",
                        language="en-US",
                        model="simba-english"
                    )
                    
                    # Verify the function was called correctly
                    mock_speechify_client.tts.audio.speech.assert_called_once()
                    call_args = mock_speechify_client.tts.audio.speech.call_args
                    
                    assert call_args[1]['audio_format'] == "mp3"
                    assert call_args[1]['input'] == "Hello, world!"
                    assert call_args[1]['language'] == "en-US"
                    assert call_args[1]['model'] == "simba-english"
                    assert call_args[1]['voice_id'] == "scott"
                    
                    # Verify file was created
                    assert os.path.exists(result)
                    assert result.endswith("speechify_audio.mp3")
                    
                finally:
                    os.chdir(original_cwd)
    
    def test_speechify_tts_environment_variable(self, mock_speechify_client):
        """Test that Speechify TTS uses environment variable when no API key provided."""
        with patch('utils.speechify_voice.Speechify', return_value=mock_speechify_client):
            with patch.dict(os.environ, {'SPEECHIFY_API_KEY': 'env_test_key'}):
                with tempfile.TemporaryDirectory() as temp_dir:
                    original_cwd = os.getcwd()
                    os.chdir(temp_dir)
                    
                    try:
                        os.makedirs("outputs", exist_ok=True)
                        
                        result = speechify_tts(
                            text="Test text",
                            voice_id="scott"
                        )
                        
                        # Verify Speechify was initialized with environment variable
                        mock_speechify_client.assert_called_once_with(token='env_test_key')
                        
                    finally:
                        os.chdir(original_cwd)
    
    def test_speechify_tts_missing_api_key(self):
        """Test that Speechify TTS raises error when no API key is available."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Speechify API key not provided"):
                speechify_tts("Test text")
    
    def test_tts_wrapper_speechify_provider(self, mock_speechify_client):
        """Test the unified TTS wrapper with Speechify provider."""
        with patch('utils.speechify_voice.Speechify', return_value=mock_speechify_client):
            with tempfile.TemporaryDirectory() as temp_dir:
                original_cwd = os.getcwd()
                os.chdir(temp_dir)
                
                try:
                    os.makedirs("outputs", exist_ok=True)
                    
                    result = tts_convert(
                        text="Test text",
                        voice_id="scott",
                        api_key="test_key",
                        provider="speechify"
                    )
                    
                    # Verify Speechify was used
                    mock_speechify_client.tts.audio.speech.assert_called_once()
                    
                finally:
                    os.chdir(original_cwd)
    
    def test_tts_wrapper_unsupported_provider(self):
        """Test that TTS wrapper raises error for unsupported providers."""
        with pytest.raises(ValueError, match="Unsupported TTS provider"):
            tts_convert("Test text", provider="unsupported")
    
    def test_voice_filtering(self):
        """Test voice filtering functionality."""
        # Mock voice objects
        mock_voice1 = Mock()
        mock_voice1.gender = "male"
        mock_voice1.tags = ["timbre:deep", "style:professional"]
        mock_model1 = Mock()
        mock_lang1 = Mock()
        mock_lang1.locale = "en-US"
        mock_model1.languages = [mock_lang1]
        mock_voice1.models = [mock_model1]
        mock_model1.name = "voice1_model"
        
        mock_voice2 = Mock()
        mock_voice2.gender = "female"
        mock_voice2.tags = ["timbre:bright"]
        mock_model2 = Mock()
        mock_lang2 = Mock()
        mock_lang2.locale = "fr-FR"
        mock_model2.languages = [mock_lang2]
        mock_voice2.models = [mock_model2]
        mock_model2.name = "voice2_model"
        
        voices = [mock_voice1, mock_voice2]
        
        # Test gender filtering
        male_voices = filter_voice_models(voices, gender="male")
        assert male_voices == ["voice1_model"]
        
        # Test locale filtering
        en_voices = filter_voice_models(voices, locale="en-US")
        assert en_voices == ["voice1_model"]
        
        # Test tags filtering
        deep_voices = filter_voice_models(voices, tags=["timbre:deep"])
        assert deep_voices == ["voice1_model"]
        
        # Test combined filtering
        combined = filter_voice_models(voices, gender="male", locale="en-US")
        assert combined == ["voice1_model"]

class TestIntegration:
    """Integration tests that require actual API key."""
    
    @pytest.mark.integration
    def test_real_speechify_api(self):
        """Test with real Speechify API (requires API key)."""
        api_key = os.getenv("SPEECHIFY_API_KEY")
        if not api_key:
            pytest.skip("SPEECHIFY_API_KEY not set - skipping integration test")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                os.makedirs("outputs", exist_ok=True)
                
                # Test basic TTS
                result = speechify_tts(
                    text="Testing Speechify migration",
                    voice_id="scott",
                    api_key=api_key,
                    language="en-US",
                    model="simba-english"
                )
                
                # Verify file was created and has content
                assert os.path.exists(result)
                file_size = os.path.getsize(result)
                assert file_size > 1000  # Sanity check that audio was generated
                
                # Test voice listing
                voices = get_available_voices(api_key)
                assert len(voices) > 0
                
                # Test voice filtering
                scott_voices = filter_voice_models(voices, tags=["name:scott"])
                assert len(scott_voices) > 0
                
            finally:
                os.chdir(original_cwd)
    
    @pytest.mark.integration
    def test_tts_wrapper_integration(self):
        """Test TTS wrapper with real API."""
        api_key = os.getenv("SPEECHIFY_API_KEY")
        if not api_key:
            pytest.skip("SPEECHIFY_API_KEY not set - skipping integration test")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                os.makedirs("outputs", exist_ok=True)
                
                # Test unified wrapper
                result = tts_convert(
                    text="Testing unified TTS wrapper",
                    voice_id="scott",
                    api_key=api_key,
                    provider="speechify"
                )
                
                assert os.path.exists(result)
                assert os.path.getsize(result) > 1000
                
            finally:
                os.chdir(original_cwd)

if __name__ == "__main__":
    # Run basic tests without API key
    pytest.main([__file__, "-v", "-m", "not integration"]) 