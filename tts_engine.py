from gtts import gTTS

def generate_audio(summary):
    tts = gTTS(summary)
    tts.save("podcast.mp3")
    return "podcast.mp3"