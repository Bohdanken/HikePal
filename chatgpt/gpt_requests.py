import os
# import openai
import requests

from dotenv import load_dotenv

load_dotenv()


def ask_for_trails(parameters):
    request_str = f"Tell me 10 most popular trails (but not parks) within {parameters['radius']} kilometers of {parameters['city']} Please tell only names and coordinates, do not include any description. Please give your answer in the following format: NAME % (LATITUDE, LONGITUDE). Don't do numbering"
    response = requests.post("https://api.openai.com/v1/chat/completions", json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": request_str}],
        "temperature": 0.7
    }, headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('chatgpt_api_key')}"})
    json = response.json()

    content = json['choices'][0]['message']['content']  # string with results
    print(content)
    content = content.split('\n')

    dic = {}
    for res in content:
        name, coords = res.split('%')
        dic[name.rstrip(' ')] = coords.strip(' ')
    print(dic)
    return dic


ask_for_trails({"city": "Sydney", "radius": 100})


