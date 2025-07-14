#!/usr/bin/env python3
import speech_recognition as sr
import pyaudio

def test_microphone_access():
    """Test if microphone access is working"""
    print("Testing microphone access...")
    
    # Test PyAudio microphone listing
    print("\n1. Testing PyAudio microphone detection:")
    try:
        p = pyaudio.PyAudio()
        print(f"Found {p.get_device_count()} audio devices:")
        
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                print(f"  - Device {i}: {device_info['name']} (Input channels: {device_info['maxInputChannels']})")
        
        p.terminate()
        print("✓ PyAudio is working")
    except Exception as e:
        print(f"✗ PyAudio error: {e}")
        return False
    
    # Test SpeechRecognition microphone access
    print("\n2. Testing SpeechRecognition microphone access:")
    try:
        recognizer = sr.Recognizer()
        microphones = sr.Microphone.list_microphone_names()
        print(f"Found {len(microphones)} microphones:")
        for i, name in enumerate(microphones):
            print(f"  - Microphone {i}: {name}")
        print("✓ SpeechRecognition can see microphones")
    except Exception as e:
        print(f"✗ SpeechRecognition error: {e}")
        return False
    
    # Test actual microphone capture
    print("\n3. Testing microphone capture (5 seconds):")
    try:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("Adjusting for ambient noise...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("Recording for 5 seconds... Say something!")
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("✓ Audio captured successfully!")
        print("Audio data length:", len(audio.get_raw_data()))
        return True
        
    except sr.WaitTimeoutError:
        print("✗ No audio detected (timeout)")
        return False
    except Exception as e:
        print(f"✗ Microphone capture error: {e}")
        return False

def test_speech_recognition():
    """Test actual speech recognition"""
    print("\n4. Testing speech recognition:")
    try:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("Say something for speech recognition test...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        
        print("Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✓ Recognition successful: '{text}'")
        return True
        
    except sr.UnknownValueError:
        print("✗ Could not understand the speech")
        return False
    except sr.RequestError as e:
        print(f"✗ Speech recognition service error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Microphone and Speech Recognition Test ===")
    
    if test_microphone_access():
        test_speech_recognition()
    else:
        print("\nMicrophone access failed. Please check:")
        print("1. Microphone permissions in System Preferences")
        print("2. Microphone is connected and working")
        print("3. No other applications are using the microphone")
