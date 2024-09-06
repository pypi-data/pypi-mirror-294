from voicex import TTS, Voices

#Specify the IP of the server where the TTS backend is running
server_ip = "xxx.xxx.xx.xx"

#Specify your voicex file, and the ip and port of the server where your voicex instance is running.
tts = TTS(voice="path-to-your-own-voice-file.voicex", server=server_ip)

#Alternatively, you can use one of the predefined voices
tts = TTS(voice=Voices.SILVAN, server=server_ip)

#Synthesize, speak or write stuff.
text = "This is a test sentence. I hope you like my voice."
tts.speak(text)
wav_data, sample_rate = tts.synthesize(text)
tts.write(text, "output.wav")