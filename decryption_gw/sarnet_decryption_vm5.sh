#!/bin/bash

in_br=sarnet5

in_port1=ens5
in_port2=ens4

dec_ip1=192.178.0.23
enc_ip2=192.178.0.18
#dec_ip2=10.20.30.24
sm=22

port_req1=1
port_req2=2

#nsa_ip=10.10.1.10
#nsv_ip=10.10.1.11

#port_ns1=5
#port_ns2=6

ryu_ip=10.20.5.39


# OVS
sudo ovs-vsctl add-br $in_br
sudo ovs-vsctl set Bridge $in_br other-config:datapath-id=0000000000000003

#sudo ovs-vsctl add-port $in_br $in_port1 -- set Interface $in_port1 ofport_request=$port_req1 type=ipsec_gre options:remote_ip=$enc_ip2 options:local_ip=$dec_ip1 options:psk=test options:certificate=cert2.pem
sudo ovs-vsctl add-port $in_br $in_port2 -- set Interface $in_port2 ofport_request=$port_req2
sudo ovs-vsctl add-port $in_br $in_port1 -- set Interface $in_port1 ofport_request=$port_req1 type=ipsec_gre options:remote_ip=192.178.0.3 options:local_ip=192.178.0.8 options:psk=secret

# Add new flows
sudo ovs-ofctl del-flows $in_br

#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req1,actions=output:$port_req2
#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req2,actions=output:$port_req1

#sudo ip addr add $dec_ip1/$sm dev $in_port1
sudo ip link set dev $in_port1 up
#sudo ip addr add $dec_ip1/$sm dev $in_port1

sudo ip link set dev $in_port2 up

sudo ovs-vsctl show

sudo ovs-vsctl set-controller $in_br tcp:$ryu_ip:9000
sudo ovs-vsctl set-manager ptcp:6640

