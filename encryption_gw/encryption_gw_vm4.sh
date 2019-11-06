#!/bin/bash

in_br=sarnet4

#in_port1=ens7
in_port1=ens4
in_port2=ens5

#enc_ip1=10.20.30.13
enc_ip2=192.178.0.3
dec_ip1=192.178.0.8
#sw_ip1=10.20.30.7

sm=24

port_req1=1
port_req2=2

#ns_ip=10.20.30.10
#nsv_ip=10.10.1.11

port_ns1=5
port_ns2=6

ryu_ip=10.20.5.39


#sudo ip addr add $enc_ip1/$sm dev $in_port1
#sudo ip addr add $enc_ip2/$sm dev $in_port2

#sudo ip link set dev $in_port1 up
#sudo ip link set dev $in_port2 up

#sudo ip netns add ns
#sudo ip netns set ns 0
#sudo ip link set vns1 type veth peer name vnsp1
#sudo ip link set vnsp1 netns ns
#sudo ip link set vns1 up
#sudo ip netns exec ns ip addr add $ns_ip/$sm dev vnsp1
#sudo ip netns exec ns ip link set vnsp1 up

#sudo ip netns exec ns ip route flush cache
#sudo ip netns exec ns route add $enc_ip1 dev vnsp1
#sudo ip route add $ns_ip dev $in_port1

# OVS
sudo ovs-vsctl add-br $in_br
sudo ovs-vsctl set Bridge $in_br other-config:datapath-id=0000000000000002

sudo ovs-vsctl add-port $in_br $in_port1 -- set Interface $in_port1 ofport_request=$port_req1
#type=ipsec_gre options:remote_ip=$dec_ip1 options:local_ip=$enc_ip1 options:psk=secret
#sudo ovs-vsctl add-port $in_br $in_port2 -- set Interface $in_port2 ofport_request=$port_req2 type=gre options:remote_ip=$dec_ip1 options:local_ip=$enc_ip2
sudo ovs-vsctl add-port $in_br $in_port2 -- set Interface $in_port2 ofport_request=$port_req2 type=ipsec_gre options:remote_ip=192.178.0.8 options:local_ip=192.178.0.3 options:psk=secret

# Add new flows
sudo ovs-ofctl del-flows $in_br

#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req1,actions=$port_req2
#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req2,actions=$port_req1

#sudo ip addr add $enc_ip1/$sm dev $in_port1
sudo ip link set dev $in_port1 up

sudo ip addr add $enc_ip2/$sm dev $in_port2
sudo ip link set dev $in_port2 up

sudo ovs-vsctl show

sudo ovs-vsctl set-controller $in_br tcp:$ryu_ip:9000
sudo ovs-vsctl set-manager ptcp:6640
