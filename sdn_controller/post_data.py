import requests

url = "https://admin:password@10.20.5.19/rest/container/2"

payload = "{\n    \"parent_container\": null,	    \n    \"in_case\": false,	    \n    \"closing_rule_run\": null,	    \n    \"sensitivity\": \"amber\",	    \n    \"closing_owner\": null,\n    \"owner\": 1,\n    \"id\": 3,\n    \"ingest_app\": null,\n    \"close_time\": null,\n    \"open_time\": null,\n    \"current_phase\": null,\n    \"container_type\": \"default\",\n    \"label\": \"events\",\n    \"version\": 1,\n    \"asset\": null,\n    \"status\": \"new\",\n    \"owner_name\": null,\n    \"hash\": \"ba652b689834489c789198d5559f0a64\",\n    \"description\": \"To check for http match-action\",\n    \"tags\": [],\n    \"kill_chain\": null,\n    \"artifact_count\": 0,\n    \"data\": {},\n    \"custom_fields\": {},\n    \"severity\": \"medium\",\n    \"tenant\": 0,\n    \"name\": \"test_me\",\n    \"source_data_identifier\": \"1275c982-3401-4f2e-89d8-2b3719005807\",\n    \"end_time\": null,\n    \"container_update_time\": null\n}"

headers = {
    'Content-Type': "application/json",
    'G-TOKEN': "95e3bcff-bfca-454d-b59e-768da6280c38",
    'cache-control': "no-cache",
    'Postman-Token': "e8648149-2df8-45db-805c-8e0f73a05948"
    #"ph-auth-token": "fiYRKQ5RjbqgFnlk25jGzbJKme0GZZb1SEIZRd6tX10="
}

# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

#def add_container():
response = requests.request("POST", url, data=payload, headers=None, verify=False)

print(response.text)
