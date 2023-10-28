import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def request(params):
    request_str = ""
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             json={"model": "gpt-4", "messages": [{"role": "user", "content": request_str}],
                                   "temperature": 0.7},
                             headers={"Content-Type": "application/json",
                                      "Authorization": f"Bearer {os.getenv('chatgpt_api_key')}"})

    if response.status_code == 200:
        r = response.json()
        print(r['choices'][0]['message']['content'])

if __name__ == "__main__":
    request({})
