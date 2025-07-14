import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import os
from dotenv import load_dotenv
import speech_recognition as sr
import time

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def test_internet_connection():
    """Test if internet connection is available for Google Speech Recognition"""
    import urllib.request
    try:
        urllib.request.urlopen('http://www.google.com', timeout=3)
        return True
    except:
        return False

def capture_speech_input_with_alternatives():
    """Enhanced speech capture with multiple methods and better debugging"""
    recognizer = sr.Recognizer()
    
    # List available microphones for debugging
    print("Available microphones:")
    microphones = sr.Microphone.list_microphone_names()
    for i, name in enumerate(microphones):
        print(f"  {i}: {name}")
    
    # Use default microphone (usually the best choice)
    microphone = sr.Microphone()
    
    # Check internet connection
    has_internet = test_internet_connection()
    print(f"\nInternet connection: {'✓ Available' if has_internet else '✗ Not available'}")
    
    # Adjust recognizer settings for better performance
    recognizer.energy_threshold = 2000  # Lower threshold for more sensitivity
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0  # Longer pause threshold
    
    print("\nAdjusting for ambient noise... Please be quiet for 3 seconds.")
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=3)
        print(f"Energy threshold set to: {recognizer.energy_threshold}")
    except Exception as e:
        print(f"Warning: Could not adjust for ambient noise: {e}")
    
    print("\n🎤 Enhanced Speech Capture")
    print("=" * 40)
    print("Instructions:")
    print("- Speak CLEARLY and LOUDLY")
    print("- Get close to your microphone")
    print("- Speak for 3-8 seconds")
    print("- Try simple phrases first")
    print("- Press Ctrl+C to cancel")
    print()
    
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1}/{max_attempts}")
        
        try:
            with microphone as source:
                print("🔴 Recording... Speak now!")
                # More generous timing settings
                audio = recognizer.listen(source, timeout=20, phrase_time_limit=8)
            
            print("🔄 Processing speech...")
            audio_data_length = len(audio.get_raw_data())
            print(f"Audio captured: {audio_data_length} bytes")
            
            if audio_data_length < 500:  # Very short audio
                print("⚠️  Audio too short. Please speak longer and louder.")
                if attempt < max_attempts - 1:
                    print("Trying again in 2 seconds...")
                    time.sleep(2)
                continue
            
            # Try multiple recognition methods
            text = None
            
            # Method 1: Google Speech Recognition (online, most accurate)
            if has_internet:
                try:
                    print("Trying Google Speech Recognition...")
                    text = recognizer.recognize_google(audio)
                    print(f"✅ Google Recognition: '{text}'")
                except sr.UnknownValueError:
                    print("❌ Google couldn't understand speech")
                except sr.RequestError as e:
                    print(f"❌ Google service error: {e}")
            

            
            if text:
                return text.strip()
            else:
                print("❌ All recognition methods failed")
                if attempt < max_attempts - 1:
                    print("\n💡 Tips for next attempt:")
                    print("  - Speak louder and more clearly")
                    print("  - Move closer to microphone")
                    print("  - Try simple words like 'hello world'")
                    print("  - Reduce background noise")
                    time.sleep(2)
                
        except sr.WaitTimeoutError:
            print("❌ No speech detected (timeout)")
            if attempt < max_attempts - 1:
                print("Trying again...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if attempt < max_attempts - 1:
                time.sleep(1)
    
    print("\n❌ All attempts failed. Possible solutions:")
    print("1. Check microphone permissions in System Preferences")
    print("2. Ensure microphone is working in other apps")
    print("3. Try speaking directly into the microphone")
    print("4. Reduce background noise")
    print("5. Check internet connection for Google recognition")
    
    return None



def save_text_to_pdf(text: str, filename: str):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    x_margin = 50
    y = height - 50
    line_height = 16

    for paragraph in text.split("\n\n"):
        wrapped_lines = []
        for line in paragraph.split("\n"):
            wrapped_lines += wrap(line, width=90)
        for line in wrapped_lines:
            if y <= 50:
                c.showPage()
                y = height - 50
            c.drawString(x_margin, y, line)
            y -= line_height
        y -= line_height

    c.save()

def generate_response_from_speech():
    """Generate AI response based on speech input"""
    speech_text = capture_speech_input_with_alternatives()
    
    if speech_text is None:
        print("No speech input received. Exiting.")
        return
    
    prompt = f"""
You are an AI assistant that provides helpful and detailed responses to user queries.
The user has spoken the following request or question:

"{speech_text}"

Please provide a comprehensive and informative response to their query. If they're asking about object detection, analysis, or any technical topic, provide relevant information and guidance.
"""
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        result = response.text
        
        print("AI Response:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # Save the response to PDF
        save_text_to_pdf(result, "speech_response.pdf")
        print(f"\nResponse saved as 'speech_response.pdf' in the current directory.")
        
    except Exception as e:
        print(f"Error generating AI response: {e}")




if __name__ == "__main__":
    print("=== Speech-to-AI Response Generator ===")
    print("This program will:")
    print("1. Listen to your speech input")
    print("2. Convert it to text")
    print("3. Generate an AI response")
    print("4. Save the response as a PDF")
    print()
    
    # Optional: Still show available models for reference
    print("Available Gemini models:")
    try:
        for m in genai.list_models():
            print(f"  - {m.name}")
    except Exception as e:
        print(f"  Could not list models: {e}")
    print()
    
    # Main speech-to-response workflow
    generate_response_from_speech()
