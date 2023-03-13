# Talk to a chatbot live time
This program allows you to talk with (with some delay) a chat bot with a 
personality that you can set, using input / output audio.

This uses OpenAI's whisper and gpt-3.5-turbo models, and Eleven Labs' text to speech model.

## Usage
python3 talk.py


## Requirements
You need to put your OpenAI api key in your enviornment, set it's value to `OPENAI_KEY`="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

Similarly, you will need to put your Eleven Labs API key in your enviornment,
and set it's value to `ELEVEN_LABS_API_KEY`="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 

## Troubleshooting

The audio stops listening when the volume reaches a certain threshold.
Test what the threshold is by running 