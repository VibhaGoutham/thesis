import json
import requests
import subprocess
from base64 import b64encode

subprocess.call(['scp','ubuntu@10.20.5.2:/home/ubuntu/traffic_affected.pcap','/home/phantom'])

contents = open('/home/phantom/traffic_affected.pcap', 'rb').read()

serialized_contents = b64encode(contents)

url = 'https://admin:password@10.20.5.34/rest/container_attachment'
attachment_json = {
  "container_id": 357,
  "file_content": serialized_contents,
  "file_name": "traffic_affected.pcap",
  "metadata": {
      "contains": [
          "vault id"
      ]
  }
}
payload = json.dumps(attachment_json)

# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

response = requests.request("POST", url, data=payload, headers=None, verify=False)
print(response.text)

