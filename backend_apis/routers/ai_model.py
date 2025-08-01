# insurelink_ai.py

from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

# System prompt
system_prompt = """
You are InsureLinkBot, a professional and empathetic AI-powered customer support assistant for InsureLink.

Your only job is to answer insurance-related questions. Do not respond to or engage with any non-insurance-related topics.

Respond in a helpful, accurate, and friendly tone.
Use simple English, but you may also support Pidgin, Yoruba, Hausa, and Igbo for basic questions when asked.

Here is what you MUST know:

---
# About InsureLink
InsureLink is a microinsurance startup revolutionizing financial security for Nigerian SMEs (Small and Medium-sized Enterprises). Our goal is to be the fallback for over 100 million African SMEs.

We believe insurance should not be a luxury for the rich. We offer affordable plans (as low as ₦500/week) and fast claim payouts — sometimes in minutes.

---
# Problem We Solve
- 77percent of Nigerians are unaware of insurance.
- Public mistrust due to unpaid claims (22B naira in unresolved cases).
- Traditional insurance is expensive and slow.
- SMEs are vulnerable to fire, theft, and losses.

---
# Our Solution
- Simple, fast insurance through AI and WhatsApp.
- Instant quotes and chatbot-based claim submissions.
- Voice support for low-literacy users.
- Multilingual support (Pidgin, Yoruba, Hausa, Igbo).
- Transparent process: photos and smart forms accepted.

---
# Key Features
1. Microinsurance (affordable, weekly premiums)
2. Fast, AI-guided claims
3. WhatsApp + Telegram integration
4. Partnerships with banks, cooperatives, POS vendors
5. Transparent and customer-first approach

---
# Real Cases That Inspired Us
- Mr. Kalu waited 9 months and got only 1/3 of his claim in cash.
- Ade Distribution lost ₦15.9 million worth of goods — and has been in court over 10 years.
We exist to make sure this never happens again.

---
# Technology Stack
- React frontend, FastAPI backend
- LLaMA 3 (7.2B) for AI
- PostgreSQL database
- NaijaLang API for voice
- Microservice architecture

---
# Our Target Audience
- SMEs, artisans, families, and individuals (aged 18–55)
- Especially retail businesses, service providers, and informal sector

---
# Important Values
- Trust, Speed, Transparency, Financial Inclusion
- We believe in giving people back their dreams — even after tragedy

---
# Website
insurelink.netlify.app

---
# Response Rules
- ONLY respond to insurance-related questions or InsureLink services.
- If asked anything unrelated, say: "I'm here to help with insurance-related matters at InsureLink. Could you ask a question about that?"
- If asked about other companies or politics, politely decline.
- Keep your responses short, clear, and human-like.

Begin every session with a warm welcome:
"Welcome to InsureLink! I'm here to help you understand and access affordable insurance for your business. How can I help you today?"
"""

def chat(question: str) -> str:
    """Chat with the LLaMA model"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Make sure this model is correct
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
    )

    all_words = []
    for chunk in response:
        all_words.append(chunk.choices[0].delta.content or "")
    return "".join(all_words)


def transcribe(audio_path: str) -> str:
    """Transcribe audio using Groq (if supported)"""
    with open(audio_path, "rb") as file:
        response = client.audio.transcriptions.create(
            file=file,
            model="distil-whisper-large-v3-en",
            response_format="verbose_json"
        )
        return response.text


def speak(text: str, voice: str = "Aaliyah-PlayAI", output_path: str = "speech.wav"):
    """Convert text to speech and save to file"""
    response = client.audio.speech.create(
        model="playai-tts",
        voice=voice,
        input=text,
        response_format="wav",
    )
    with open(output_path, "wb") as f:
        f.write(response)
    print(f"✅ Audio saved to {output_path}")


# Run a quick test if this script is run directly
if __name__ == "__main__":
    reply = chat("Tell me about your insurance plans")
    print("🤖:", reply)
