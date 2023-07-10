import requests
import numpy as np

class getTopicAPI():
    def __init__(self):
        self.url = "https://1g0n8o24s6.execute-api.us-east-1.amazonaws.com/prod/get-topic-model"

    def get_topics(self, payload):
        headers = {
        'Content-Type': 'text/plain'
        }
        response = requests.request("POST", self.url, headers=headers, data = payload)
        text = response.text.encode('utf8').decode()
        result = [float(s) for s in text[1:-1].replace('\n','').split(' ') if s]
        return result

if __name__ == '__main__':
    t_api = getTopicAPI()
    text = 'A Pelicans fan snuck on to the court for warmups, stretched and put up a shot before the police escorted him off'
    r = t_api.get_topics(text)
    print(f'API Request Results for : {text}')
    print(r)
