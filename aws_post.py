import requests


credentials_file='aws_api_id.txt'
with open(credentials_file, 'r') as CF:
    CF_Data = CF.read()

credentials_dictionary = {}

for Line in CF_Data.splitlines():
    if not Line.strip():
        continue
    Key, Value = Line.split('=')
    credentials_dictionary[Key.strip()] = Value.strip()

credentials_dictionary




url = f"https://{credentials_dictionary['YOUR_API_KEY']}.execute-api.us-east-1.amazonaws.com/prod/get-topic-model"

payload = ' A Pelicans fan snuck on to the court for warmups, stretched and put up a shot before the police escorted him off'


headers = {
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))