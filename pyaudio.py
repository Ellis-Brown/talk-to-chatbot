from time import sleep
import sounddevice as sd
import numpy
from scipy.io.wavfile import write
import datetime
import openai 
import os
import requests
from playsound import playsound
import json

openai.api_key=os.environ["OPENAI_KEY"]

eleven_labs_api_key = os.environ["ELEVEN_LABS_API_KEY"]

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

messages=[
        {"role": "system", "content": "Your name is Greg. You are a friend to the person talking. You also like trains, and feel compelled to let everyone know. Please act as if you are a friend to the person talking. You are not an AI model, you are a human being with feelings (and a train obsession).)"},
    ]

fs = 44100  # Sample rate
loop = 0
print("Begin recording in 3...")
sleep(1)
print("2...")
sleep(1)
print("1...")
sleep(1)
start_time = datetime.datetime.now()
while(loop < 4):
    # Goal: Record in 1 second intervals, and save each recording in a contiuously updating file
    long_recording = []
    sound_level = 1000
    time_recorded = 0 # Max 15 seconds
    print("Beginning recording [*]")
    while (sound_level > 200 and time_recorded < 15):
        print("Listening . . .")
        myrecording = sd.rec(int(1.5 * fs), samplerate=fs, channels=1)
        
        sd.wait()
        
        sound_level = sum(abs(myrecording))
        long_recording.extend(myrecording)
        time_recorded += 1
    
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()

    # convert long recording to numpy.ndarray
    print("Writing recording to file . . .")
    
    long_recording = numpy.array(long_recording)
    write('output.wav', fs, long_recording)  # Save as WAV file 
    audio_file= open("output.wav", "rb") # TODO: Remove saving to file, directly transcribe from numpy.ndarray
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()
    print("Asking openAI whisper for the transcript . . .")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript) # TODO: remove later
    messages.append({"role": "user", "content": transcript["text"]})
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()
    print("Asking openAI gpt-3.5-turbo for a response . . .")
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    )
    
    response_text = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": response_text})


    url = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"

    request_body = {
        "text": response_text,
        "voice_settings": {
            "stability": 0.8,
            "similarity_boost": 0.1,
        }
        }
    headers = {
        "xi-api-key": eleven_labs_api_key,
        "Content-Type": "application/json"
    }
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()
    print("Asking Eleven Labs for an audio file . . .")
    audio = requests.post(url, headers=headers, json=request_body) 
    # write the audio file to the system as a mp3
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()
    print("Writing to the audio file . . .")
    with open("audio.mp3", "wb") as f:
        f.write(audio.content)
    
    # Make a post request to eleven labs
    print("Playing the audio file . . .")
    print("Elapsed time", datetime.datetime.now() - start_time)
    start_time = datetime.datetime.now()
    playsound("audio.mp3") # Play the audio file
    loop += 1


