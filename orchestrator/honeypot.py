import json
import requests
from base64 import b64encode

contents = open('/home/phantom/Maildir', 'rb').read()

serialized_contents = b64encode(contents)

attachment_json = {
    'container_id': 357,
    'file_content': serialized_contents,
    'file_name': 'Maildir',
    'metadata': {
        'contains': [
            'vault id'
        ]
    }
}

url = 'https://admin:password@10.20.5.34/rest/container_attachment'

payload = json.dumps(attachment_json)

response = requests.request("POST", url, data=payload, headers=None, verify=False)

print(response.text)

