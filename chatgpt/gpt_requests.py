import os
import re

import requests

from dotenv import load_dotenv

load_dotenv()


def ask_for_trails(parameters):
    request_str = f"Tell me 10 most popular trails (but not parks) of {parameters['difficulty']} level " \
                  f"within {parameters['radius']} kilometers of {parameters['city']}. " \
                  f"Please tell names, coordinates, distance from the city, and brief description, " \
                  f"Please give your answer in the following format: NAME % (LATITUDE, LONGITUDE) % DISTANCE % DESCRIPTION."

    print(request_str)
    response = requests.post("https://api.openai.com/v1/chat/completions", json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": request_str}],
        "temperature": 0.7
    }, headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('chatgpt_api_key')}"})
    json = response.json()
    content = json['choices'][0]['message']['content']  # string with results
    print(content)

    if "\n\n" in content:
        content = content.split("\n\n")
    else:
        content = content.split("\n")

    dic = {}
    for res in content:
        name, coords, distance, description = res.split(' % ')
        # strip name by regex r'\d\.' because gpt still can answer with numbers
        name = re.sub(r'\d\. ', '', name)
        dic[name] = {"coordinates": coords, "distance": distance, "description": description}

    print(dic)
    return dic

#ask_for_trails({"difficulty": "medium", "city": "Sydney", "radius": 100})

