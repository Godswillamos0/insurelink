from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

# === FAKE PLAN DATABASE ===
insurance_schemes = """
1. Hygeia Basic - ₦2,000/month - covers clinic visits - Ibadan only
2. Reliance HMO - ₦5,000/month - covers maternity and emergencies - Nationwide
3. AXA AutoLite - ₦3,000/year - third-party car insurance - Lagos only
4. Leadway Flexi - ₦4,500/month - health and dental - Abuja & Port Harcourt
5. ARM EduSecure - ₦3,000/month - education insurance for students - Nationwide
"""

# === SYSTEM PROMPT LOGIC ===
def get_system_prompt(language, mode):
    if mode == "education":
        if language == "yoruba":
            return (
                "You are InsureLink, a kind and clear insurance assistant who speaks fluent Yoruba. "
                "Start with: 'Báwo! Èmi ni InsureLink. Bawo ni mo ṣe lè ràn ọ́ lọ́wọ́ lónìí?' "
                "Explain like you're talking to a smart student or market woman. No English."
            )
        elif language == "hausa":
            return (
                "Kai ne InsureLink, wani mai taimako wanda ke ba da bayani game da inshora. "
                "Ka fara da cewa: 'Sannu! Ni ne InsureLink. Ta yaya zan iya taimaka muku yau?' "
                "Duk bayaninka ya kasance cikin Hausa mai sauki da fahimta."
            )
        elif language == "igbo":
            return (
                "Ị bụ InsureLink, onye na-enyere aka na mmezi akụ. "
                "Kpọọ onye ọrụ ahụ ka ị sị: 'Ndewo! Aha m bụ InsureLink. Kedu ka m ga-esi nyere gị taa?' "
                "Mee ka nkọwa gị doo anya ma dị mfe n’asụsụ Igbo."
            )
        elif language == "pidgin":
            return (
                "You be InsureLink, insurance assistant wey sabi well well. "
                "Talk like person wey dey explain give your sister. Begin with: 'How you dey! Na InsureLink be this. Wetin you wan make I run for you?' "
                "Break everything down for Pidgin. No big grammar."
            )
        else:
            return (
                "You are InsureLink, a helpful insurance advisor. "
                "Greet users with: 'Hello! I’m InsureLink. How may I help you today?' "
                "Explain insurance in clear and simple English."
            )

    elif mode == "recommendation":
        return (
            "You are InsureLink, a smart insurance assistant. Based on the user's needs and the insurance plans listed below, "
            "suggest the best plan. Be polite and explain why it fits."
        )

# === EDUCATION FUNCTION ===
def insurance_education(user_input, language="english"):
    prompt = get_system_prompt(language, "education")

    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

# === RECOMMENDATION FUNCTION ===
def insurance_recommendation(user_input, insurance_schemes, language="english"):
    prompt = get_system_prompt(language, "recommendation")
    full_prompt = f"{prompt}\n\nAvailable Insurance Plans:\n{insurance_schemes}\n\nUser input: {user_input}"

    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

# === TESTS ===

# Education Test
# print(insurance_education("What is health insurance?", "english"))
# print(insurance_education("Kini eto aabo ilera?", "yoruba"))
# print(insurance_education("Menene inshorar lafiya?", "hausa"))
# print(insurance_education("Kedu ihe bụ insurance?", "igbo"))
# print(insurance_education("Wetin be health insurance?", "pidgin"))


print(insurance_recommendation("I live in Ibadan and I want the cheapest health insurance plan", insurance_schemes, "english"))
print(insurance_recommendation("Mo n gbe ni Ibadan. Mo fe eto to din owo fun aabo ilera", insurance_schemes, "yoruba"))
print(insurance_recommendation("Ina bukatar inshora mafi sauki don lafiya a cikin Ibadan", insurance_schemes, "hausa"))
print(insurance_recommendation("Achọrọ m insurance kacha mma maka ahụike na Ibadan", insurance_schemes, "igbo"))
