from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def chat(question):
    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

    # see this part? just take it like that 
    all_words =[]
    for chunk in completion:
        all_words.append((chunk.choices[0].delta.content or ""))
    sentence = ''
    for word in all_words:
        sentence = sentence + word
    return sentence



def trascribe(audio_file):
    filename = audio_file

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="distil-whisper-large-v3-en",
        response_format="verbose_json",
        )
        return transcription.text
      
        
def speak(text: str, voice: str = "Aaliyah-PlayAI", output_path: str = "speech.wav"):
    # Initialize client (reads API key from env)
    
    response = client.audio.speech.create(
        model="playai-tts",
        voice=voice,
        input=text,
        response_format="wav",
    )
    
    # Write audio bytes to file
    with open(output_path, "wb") as f:
        f.write(response)
    print(f"✅ Audio saved to {output_path}")
    
    

if __name__ == "__main__":
    chat(question="Wagwan")