import sounddevice as sd
import numpy
from scipy.io.wavfile import write

import openai 
import os
import requests
from playsound import playsound
import json

openai.api_key=os.environ["OPENAI_KEY"]

eleven_labs_api_key = os.environ["ELEVEN_LABS_API_KEY"]

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

messages=[
        {"role": "system", "content": "You are a friend to the person talking. You also like trains, and feel compelled to let everyone know. Please act as if you are a friend to the person talking. You are not an AI model, you are a human being with feelings (and a train obsession).)"},
    ]

fs = 44100  # Sample rate
loop = 0
while(loop < 4):
    # Goal: Record in 1 second intervals, and save each recording in a contiuously updating file
    long_recording = []
    sound_level = 1000
    time_recorded = 0 # Max 15 seconds
    while (sound_level > 100 and time_recorded < 15):
        myrecording = sd.rec(int(1 * fs), samplerate=fs, channels=1)
        sd.wait()
        sound_level = sum(abs(myrecording))
        long_recording.extend(myrecording)
        time_recorded += 1
        

    # convert long recording to numpy.ndarray
    long_recording = numpy.array(long_recording)
    write('output.wav', fs, long_recording)  # Save as WAV file 
    audio_file= open("output.wav", "rb") # TODO: Remove saving to file, directly transcribe from numpy.ndarray
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript) # TODO: remove later
    messages.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    )
    # Write the response to a file as a json
    json.dump(response, open("response.json", "w"))
    response_text = response["choices"][0]["message"]["content"]
    messages.append({"role": "friend", "content": response_text})


    url = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"

    request_body = {
        "text": response_text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
        }
    headers = {
        "xi-api-key": eleven_labs_api_key,
        "Content-Type": "application/json"
    }
    audio = requests.post(url, headers=headers, json=request_body) 
    # write the audio file to the system as a mp3
    with open("audio.mp3", "wb") as f:
        f.write(audio.content)
    
    # Make a post request to eleven labs

    playsound("audio.mp3") # Play the audio file
    loop += 1


