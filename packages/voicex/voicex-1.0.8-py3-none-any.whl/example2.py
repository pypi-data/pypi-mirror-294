from voicex import TTS, Voices
import json
import pickle
import numpy as np
#Specify the IP of the server where the TTS backend is running
server_ip = "137.250.24.59"

#Specify your voicex file, and the ip and port of the server where your voicex instance is running.
#tts = TTS(voice="path-to-your-own-voice-file.voicex", server=server_ip)

#Alternatively, you can use one of the predefined voices

#
# #Synthesize, speak or write stuff.
# text = "Here is how the evolutionary algorithm inside voice x works."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output1.wav")
#
# text = "The evolutionary algorithm searches through the speaker embeddings of the TTS model."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output2.wav")
#
# text = "It starts with two completely random speaker embeddings."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output3.wav")
#
# text = "Those embeddings are synthesized to speech."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output4.wav")
#
# text = "The resulting speech files are presented to the user through the voice x interface."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output5.wav")
#
# text = "The user simply selects the 'better' one? Whatever better might be."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output6.wav")
#
# text = "That better embedding gets algorithmically mutated."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output7.wav")
#
# text = "That means, gaussian noise is added to the embedding to slightly alter it."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output8.wav")
#
# text = "Only the better embedding, and the mutated one, are kept."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output9.wav")
#
# text = "The worse embedding is thrown away."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output10.wav")
#
# text = "Now that we have to new embeddings, we start again from the top."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output11.wav")
#
# text = "We are doing this loop, over and over again."
# tts.speak(text)
# wav_data, sample_rate = tts.synthesize(text)
# tts.write(text, "output12.wav")
f1 = open('female.voicex','rb')
t1 = pickle.load(f1)
f2 = open('voices/andrea_converted.voicex', 'rb')
t2 = pickle.load(f2)

tts = TTS(voice=Voices.LENNY, server=server_ip)
# tts = TTS(voice="andrea_converted.voicex", server=server_ip)
text = "A leaf cuts and trimms any wood"





tts = TTS(voice="andrea_converted.voicex", server=server_ip)
tts.speak(text)
wav_data, sample_rate = tts.synthesize(text)
tts.write(text, "lenny_test.wav")