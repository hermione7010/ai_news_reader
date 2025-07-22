# import pyttsx3
# engine = pyttsx3.init()
# engine.say("Hello, this is a test speech from pyttsx3.")
# engine.runAndWait()


from gtts import gTTS
import os

text = "Hello, this is a test speech from Google Text-to-Speech."
tts = gTTS(text=text, lang='en', slow=False)
tts.save("speech.mp3")
# # To play the audio (requires a media player like mpg123 on Linux, or you can use other Python audio libraries)
# # os.system("mpg123 output.mp3")



from pytoon.animator import animate

# If you have an audio file and a transcript
# with open("path/to/speech.txt", "r") as file:
#     transcript = file.read()
# animation = animate(audio_file="speech.mp3", transcript="hello my name is abhishek i am a software engineer")

# Or, let PyToon generate the transcript automatically
animation = animate(audio_file="speech.mp3")

# Export the animation (can overlay on a background video)
animation.export(path='animated_speech.mp4')