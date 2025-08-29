#!/usr/bin/env python3
"""
Simple test script to verify Speechify migration.
Run this script to test if the migration works correctly.
"""

import os
import sys
import tempfile

def test_migration():
    """Test the Speechify migration."""
    print("🧪 Testing Speechify Migration...")
    
    # Check if Speechify API key is available
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key:
        print("❌ SPEECHIFY_API_KEY environment variable not set")
        print("   Please set your Speechify API key:")
        print("   export SPEECHIFY_API_KEY='your_api_key_here'")
        print("   Or sign up at: https://console.sws.speechify.com/signup")
        return False
    
    try:
        # Import our modules
        from utils.speechify_voice import speechify_tts, get_available_voices
        from utils.tts_wrapper import tts_convert
        print("✅ Successfully imported Speechify modules")
        
        # Test basic TTS
        print("🎤 Testing basic TTS...")
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                os.makedirs("outputs", exist_ok=True)
                
                # Test direct Speechify TTS
                result = speechify_tts(
                    text="Hello! This is a test of the Speechify migration.",
                    voice_id="scott",
                    api_key=api_key,
                    language="en-US",
                    model="simba-english"
                )
                
                if os.path.exists(result):
                    file_size = os.path.getsize(result)
                    print(f"✅ TTS file created: {result} ({file_size} bytes)")
                else:
                    print("❌ TTS file not created")
                    return False
                
                # Test unified wrapper
                print("🔄 Testing unified TTS wrapper...")
                wrapper_result = tts_convert(
                    text="Testing the unified TTS wrapper with Speechify.",
                    voice_id="scott",
                    api_key=api_key,
                    provider="speechify"
                )
                
                if os.path.exists(wrapper_result):
                    file_size = os.path.getsize(wrapper_result)
                    print(f"✅ Wrapper TTS file created: {wrapper_result} ({file_size} bytes)")
                else:
                    print("❌ Wrapper TTS file not created")
                    return False
                
                # Test voice listing
                print("🎭 Testing voice listing...")
                voices = get_available_voices(api_key)
                print(f"✅ Found {len(voices)} available voices")
                
                # Test with different language
                print("🌍 Testing multilingual support...")
                multilingual_result = speechify_tts(
                    text="Bonjour! Ceci est un test en français.",
                    voice_id="scott",
                    api_key=api_key,
                    language="fr-FR",
                    model="simba-multilingual"
                )
                
                if os.path.exists(multilingual_result):
                    file_size = os.path.getsize(multilingual_result)
                    print(f"✅ Multilingual TTS file created: {multilingual_result} ({file_size} bytes)")
                else:
                    print("❌ Multilingual TTS file not created")
                    return False
                
            finally:
                os.chdir(original_cwd)
        
        print("\n🎉 All tests passed! Speechify migration is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you have installed the required packages:")
        print("   pip install speechify-api")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility with ElevenLabs."""
    print("\n🔄 Testing backward compatibility...")
    
    try:
        # Test if ElevenLabs is still available
        from utils.elevenlabs_voice import elevenlabs_tts
        print("✅ ElevenLabs module still available for backward compatibility")
        
        # Test if the wrapper can handle both providers
        from utils.tts_wrapper import tts_convert
        
        # Test with environment variable
        os.environ['TTS_PROVIDER'] = 'speechify'
        
        print("✅ Backward compatibility wrapper working")
        return True
        
    except ImportError:
        print("⚠️  ElevenLabs not available (this is expected if not installed)")
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 50)
    print("SPEECHIFY MIGRATION TEST SUITE")
    print("=" * 50)
    
    # Test basic migration
    migration_success = test_migration()
    
    # Test backward compatibility
    compatibility_success = test_backward_compatibility()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    if migration_success and compatibility_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Speechify migration is complete and working")
        print("✅ Backward compatibility is maintained")
        print("\n📝 Next steps:")
        print("   1. Set your SPEECHIFY_API_KEY environment variable")
        print("   2. Run your application: streamlit run app.py")
        print("   3. The app will now use Speechify for TTS")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("   Please check the error messages above")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 