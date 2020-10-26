import requests
credentials_file='aws_api_id.txt'
CF = open(credentials_file, 'r')
CF_Data = CF.read()
CF.close()

credentials_dictionary = {}

for Line in CF_Data.splitlines():
    if not Line.strip():
        continue

    Key, Value = Line.split('=')

    credentials_dictionary[Key.strip()] = Value.strip()

credentials_dictionary




url = f"https://{credentials_dictionary['YOUR_API_KEY']}.execute-api.us-east-1.amazonaws.com/prod/get-topic-model"

payload = 'how chow now little brown cow fo this test must be ata least ten chars long'


headers = {
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))