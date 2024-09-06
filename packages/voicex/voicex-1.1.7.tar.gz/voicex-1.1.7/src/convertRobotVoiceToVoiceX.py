import json
import pickle
import numpy as np

input_json = 'andrea_14.json'
output_voicex_file = 'voicex/voices/andrea_converted.voicex'


f = open(input_json)
test_json = json.load(f)

voicex_converted = []
voicex_converted.append(test_json["voice1"])
voicex_converted.append(test_json["voice2"])
voicex_converted.append(test_json["voice3"])
voicex_converted.append(test_json["voice4"])
voicex_converted.append(test_json["voice5"])
voicex_converted.append(0)
voicex_converted.append(0)
voicex_converted.append(0)
voicex_converted.append(0)
voicex_converted.append(0)
with open(output_voicex_file, 'wb') as outp:
    pickle.dump(np.array(voicex_converted), outp)