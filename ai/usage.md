
# InsureLink AI — Function Usage Guide

This document explains how the backend developer can use the AI functions inside `insurelink_ai.py`.

---

## insurance_education(user_input, language="english")

Explains insurance concepts in the selected language.

### Parameters:
- `user_input` (str): The user's message or question.
- `language` (str): One of `"english"`, `"yoruba"`, `"hausa"`, `"igbo"`, `"pidgin"`.

### Returns:
- A string response from GPT.

### Example:
```python
insurance_education("What is third-party insurance?", "pidgin")
```

---

## insurance_recommendation(user_input, insurance_schemes, language="english")

Recommends the most suitable insurance plan based on user's input and available plans.

### Parameters:
- `user_input` (str): The user’s request or question.
- `insurance_schemes` (str): A text block of available plans (from DB or backend).
- `language` (str): One of `"english"`, `"yoruba"`, `"hausa"`, `"igbo"`, `"pidgin"`.

### Returns:
- A string response with the recommendation in the chosen language.

### Example:
```python
plans = """
1. Hygeia Basic - ₦2,000/month - Ibadan only
2. Leadway Plus - ₦5,000/month - Nationwide
"""

insurance_recommendation("I live in Ibadan and want the cheapest health plan", plans, "english")
```

---

## API Key Note
- Your OpenAI API key should be stored in a `.env` file like this:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Ensure `.env` is included in `.gitignore` and never pushed.

---

## Folder Structure

```
/insurelink
  └── /ai
        ├── insurelink_ai.py
        ├── requirements.txt
        ├── .gitignore
        ├── README.md
        └── usage.md  
```

---

This setup is for any backend logic that connects to user input and insurance plan sources.
