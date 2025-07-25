import requests

def generate_story(caption, emotion):
    api_key = "AIzaSyBHeUXpobG-zYqGtcGqIV1fjtYvdatyhv8"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f"""
    Write a short and magical story for a child based on this drawing caption: '{caption}' and the emotion it conveys: '{emotion}'.
    Make it imaginative, simple, and under 100 words.
    """

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Oops! There was an error generating the story: {e}"
