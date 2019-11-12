#!/bin/bash

in_br1=sarnet4
in_br2=sarnet5

enc_port=ens5
dec_port=ens5

port_req1=1
port_req2=2

port_req3=2
port_req4=1

enc_ip1=192.178.0.3
dec_ip1=192.178.0.8

sw4=10.20.5.46
sw5=10.20.5.2

#Encryption g/w
#sudo ovs-vsctl --db=tcp:$sw4:6640 add-port $in_br1 $enc_port -- set Interface $enc_port ofport_request=$port_req2 type=ipsec_gre options:remote_ip=$dec_ip1 options:local_ip=$enc_ip1 options:psk=secret

curl -X POST -d '{"dpid": 0000000000000002, "priority": 99, "flags": 1, "match":{"in_port": 1}, "actions":[ { "type":"OUTPUT", "port": 2 } ] }' http://10.20.5.3:8080/stats/flowentry/add

#Decryption g/w
#sudo ovs-vsctl --db=tcp:$sw5:6640 add-port $in_br2 $dec_port -- set Interface $dec_port ofport_request=$port_req4 type=ipsec_gre options:remote_ip=$enc_ip1 options:local_ip=$dec_ip1 options:psk=secret

curl -X POST -d '{"dpid": 0000000000000003, "priority": 99, "flags":1, "match":{"in_port": 1}, "actions":[ { "type":"OUTPUT", "port": 2 } ] }' http://10.20.5.3:8080/stats/flowentry/add


