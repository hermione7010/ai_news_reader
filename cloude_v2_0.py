# Modern Working Solutions for Talking Avatars (2024/2025)

# Option 1: SadTalker - Most Reliable Current Solution
# ===============================================

# Installation (Working as of 2024/2025)
"""
1. Install Python 3.8 (important - newer versions may have issues)
2. Clone repository:
   git clone https://github.com/OpenTalker/SadTalker.git
   cd SadTalker

3. Install dependencies:
   pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
   pip install -r requirements.txt

4. Download models (run once):
   bash scripts/download_models.sh
"""

import os
import subprocess
import tempfile
from gtts import gTTS
import requests

class SadTalkerAvatar:
    def __init__(self, sadtalker_path="./SadTalker"):
        self.sadtalker_path = sadtalker_path
        
    def text_to_speech(self, text, lang='en'):
        """Convert text to speech"""
        tts = gTTS(text=text, lang=lang, slow=False)
        temp_audio = tempfile.mktemp(suffix='.wav')
        tts.save(temp_audio)
        return temp_audio
    
    def create_talking_video(self, image_path, text, output_path="result.mp4"):
        """Create talking avatar video"""
        try:
            # Generate audio from text
            audio_path = self.text_to_speech(text)
            
            # Run SadTalker
            cmd = [
                'python', f'{self.sadtalker_path}/inference.py',
                '--driven_audio', audio_path,
                '--source_image', image_path,
                '--result_dir', './results/',
                '--still', '--preprocess', 'full',
                '--enhancer', 'gfpgan'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up
            os.unlink(audio_path)
            
            if result.returncode == 0:
                print("✅ Video created successfully!")
                return True
            else:
                print(f"❌ Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

# Option 2: Web-based API Solutions (Easiest)
# ==========================================

class WebBasedTalkingAvatar:
    """Using modern web APIs - most reliable option"""
    
    def __init__(self):
        print("Web-based solutions (choose one):")
        print("1. Replicate API (easiest)")
        print("2. RunPod (affordable)")
        print("3. Hugging Face Spaces (free)")
    
    def replicate_sadtalker(self, image_path, text):
        """Using Replicate API - requires API key but very reliable"""
        try:
            import replicate
            
            # Convert text to audio first
            audio_path = self.text_to_speech(text)
            
            output = replicate.run(
                "cjwbw/sadtalker:3aa3dac9353cc4d6bd62a8f95957bd844003bcab3846b0f33d39307d9314c5d7",
                input={
                    "source_image": open(image_path, "rb"),
                    "driven_audio": open(audio_path, "rb"),
                    "preprocess": "crop",
                    "still_mode": True,
                    "use_enhancer": True
                }
            )
            
            # Download result
            response = requests.get(output)
            with open("output_video.mp4", "wb") as f:
                f.write(response.content)
            
            os.unlink(audio_path)
            return "output_video.mp4"
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='en')
        temp_audio = tempfile.mktemp(suffix='.wav')
        tts.save(temp_audio)
        return temp_audio

# Option 3: Google Colab Solution (Free & Easy)
# =============================================

def create_colab_notebook():
    """Create a Google Colab notebook for SadTalker"""
    notebook_code = '''
# Run this in Google Colab - Free and works!

# Install dependencies
!git clone https://github.com/OpenTalker/SadTalker.git
%cd SadTalker
!pip install -r requirements.txt

# Download models
!bash scripts/download_models.sh

# Upload your image and audio, then run:
!python inference.py --driven_audio your_audio.wav --source_image your_image.jpg --result_dir ./results --still --preprocess full --enhancer gfpgan

# Download results from ./results folder
'''
    return notebook_code

# Option 4: Modern Wav2Lip Fork (Updated Dependencies)
# ===================================================

class ModernWav2Lip:
    """Using updated Wav2Lip fork with modern dependencies"""
    
    def __init__(self):
        print("Modern Wav2Lip setup:")
        print("git clone https://github.com/indianajson/wav2lip-HD.git")
        print("This fork has updated dependencies!")
    
    def setup_wav2lip_hd(self):
        """Setup modern Wav2Lip HD version"""
        commands = [
            "git clone https://github.com/indianajson/wav2lip-HD.git",
            "cd wav2lip-HD",
            "pip install -r requirements.txt"
        ]
        return commands

# Minimal Working Example - Web API Approach
# ==========================================

def simple_talking_avatar(image_path, text):
    """Simplest working solution using web APIs"""
    
    # Option A: Use Hugging Face Spaces (Free)
    def use_huggingface():
        print("Visit: https://huggingface.co/spaces/vinthony/SadTalker")
        print("Upload your image and audio there - works in browser!")
    
    # Option B: Use Replicate (Paid but reliable)
    def use_replicate():
        # pip install replicate
        # Get API key from replicate.com
        print("1. Get API key from replicate.com")
        print("2. pip install replicate")
        print("3. Set REPLICATE_API_TOKEN environment variable")
        
        code = '''
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "your-token-here"

output = replicate.run(
    "cjwbw/sadtalker:3aa...",
    input={
        "source_image": open("image.jpg", "rb"),
        "driven_audio": open("audio.wav", "rb")
    }
)
print(output)  # URL to download video
'''
        return code
    
    return use_huggingface, use_replicate

# Quick Start Guide
if __name__ == "__main__":
    print("🎯 RECOMMENDED APPROACHES (2024/2025):")
    print("\n1. 🌐 EASIEST: Google Colab")
    print("   - Go to: https://colab.research.google.com")
    print("   - Paste SadTalker code above")
    print("   - Upload image, run cells")
    
    print("\n2. 💻 LOCAL: SadTalker (if you have good GPU)")
    print("   - Python 3.8 required")
    print("   - Follow SadTalker setup above")
    
    print("\n3. ☁️ API: Replicate (most reliable)")
    print("   - Sign up at replicate.com")
    print("   - Use API code above")
    
    print("\n4. 🆓 BROWSER: Hugging Face Spaces")
    print("   - Visit: https://huggingface.co/spaces/vinthony/SadTalker")
    print("   - No setup required!")

# Installation commands that ACTUALLY work in 2024/2025:
WORKING_INSTALLATION = """
# Method 1: SadTalker (Recommended)
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
conda create -n sadtalker python=3.8
conda activate sadtalker
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install -r requirements.txt
bash scripts/download_models.sh

# Method 2: Use in Google Colab (Zero setup)
# Just go to colab.research.google.com and paste the notebook code

# Method 3: Use Replicate API
pip install replicate
# Get API key from replicate.com
"""