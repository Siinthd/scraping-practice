from pydub import AudioSegment
import speech_recognition
speech_recog = speech_recognition.Recognizer()
speech_recog.pause_threshold = 0.5

#microphone
'''
with speech_recognition.Microphone() as mic:
    speech_recog.adjust_for_ambient_noise(source=mic,duration=0.5)
    audio = speech_recog.listen(source=mic)
    query = speech_recog.recognize_google(audio_data=audio,language='ru-RU').lower()
'''
filename = 'sounds/speech_sample.mp3'
    
def divide_chunks(sound, chunksize):
    # looping till length l
    for i in range(0, len(sound), chunksize):
        yield sound[i:i + chunksize]

sound = AudioSegment.from_mp3(filename)
chunks = list(divide_chunks(sound, 60000))
print(f"{len(chunks)} chunks of {60000/1000}s each")

out_string = ''
for index,chunk in enumerate(chunks):
    chunk.export('sounds/test.wav', format='wav')
    with speech_recognition.AudioFile('sounds/test.wav') as source:
        try:
            audio = speech_recog.record(source)
            s = speech_recog.recognize_google(audio,show_all=False, language="ru-RU")
            out_string+=s
        except Exception as e:
            pass
print(out_string)