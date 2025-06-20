import os

# os.system("google-oauthlib-tool --client-secrets ~/jarvis2/credentials.json --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless")

from google.assistant.library import Assistant

CREDENTIALS = r'~/jarvis2/.config/google-oauthlib-tool/credentials.json'

def send_cmd_to_gnm(cmd):
  try:
    with Assistant(CREDENTIALS) as assistant:
      assistant.send_text_query(cmd)
      print('Command sent')
  except exception as e:
    print(e)
    

send_cmd_to_gnm('play Hichki 2.0 on youtube music')