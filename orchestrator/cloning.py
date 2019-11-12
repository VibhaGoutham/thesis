import subprocess
import requests
import array

url = "http://10.20.5.3:8080/stats/flowentry/add"

#payload = []

#cloning flow
pay = '{\"dpid\": 0000000000000001, \"priority\": 30, \"flags\": 1, \"match\": 	{\"eth_type\": 2048, "nw_proto\": 6, "tp_dst\": 100}, \"actions\": [ {\"type\": \"OUTPUT\", "port\": 2}, '
clone = '{\"type\": \"OUTPUT\", "port\": 5'
end = '} ] }'
payload = pay+clone+end
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "98befe48-d360-45c7-a6a3-2326bf21f798"
    }
response = requests.request("POST", url, data=payload, headers=None)
print(response.text)


#Normal flow 1
#payload = '{\"dpid\": 0000000000000001, \"priority\": 30, \"flags\": 1, \"match\":  {\"in_port\": 1}, \"actions\": [ {\"type\": \"OUTPUT\", "port\": 2} ] }'
#response = requests.request("POST", url, data=payload, headers=None)
#print(response.text)


#Normal flow 2
#payload = '{\"dpid\": 0000000000000001, \"priority\": 30, \"flags\": 1, \"match\":  {\"in_port\": 2}, \"actions\": [ {\"type\": \"OUTPUT\", "port\": 1} ] }'
#response = requests.request("POST", url, data=payload, headers=None)
#print(response.text)



#subprocess.call(["sudo","ovs-vsctl","--db=tcp:10.20.5.46:6640","add-port","sarnet4","test"])
