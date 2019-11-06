#!/bin/bash

#Bridge variables added
#Namespace variables added

in_br=sarnet1

in_port1=vns1
in_port2=vns2
in_port3=ens4

port_req1=1
port_req2=2
port_req3=5

loc_ip1=10.20.20.31
loc_ip2=10.20.20.32
loc_ip3=10.20.20.15

sm=22

nsa_ip=10.20.30.30
nsv_ip=10.20.30.33

#port_ns1=3
#port_ns2=4

ryu_ip=10.20.5.3

#sudo ip addr add $loc_ip1/$sm dev $in_port1
#sudo ip addr add $loc_ip2/$sm dev $in_port2

#sudo ip link set dev $in_port1 up
#sudo ip link set dev $in_port2 up

# OVS: Adding bridge, dpid, ports
echo 'Adding bridge: sarnet1'
sudo ovs-vsctl add-br $in_br
sudo ovs-vsctl set Bridge $in_br other-config:datapath-id=0000000000000001

#sudo ovs-vsctl add-port $in_br $in_port1 -- set Interface $in_port1 ofport_request=$port_req1 type=internal options:local_ip=$loc_ip1
#sudo ovs-vsctl add-port $in_br $in_port2 -- set Interface $in_port2 ofport_request=$port_req2 type=internal options:local_ip=$loc_ip2
sudo ovs-vsctl add-port $in_br $in_port3 -- set Interface $in_port3 ofport_request=$port_req3

#Adding Namespace: Attacker(nsa) & Victim(nsv)
echo 'Attacker-Victim pair created'
sudo ip netns add nsa
sudo ip netns set nsa 0
sudo ip link add vnsp1 type veth peer name vns1
sudo ip link set vnsp1 netns nsa
sudo ip link set vns1 up
sudo ip netns exec nsa ip addr add $nsa_ip/$sm dev vnsp1
sudo ip netns exec nsa ip link set vnsp1 up

sudo ip netns add nsv
sudo ip netns set nsv 1
sudo ip link add vnsp2 type veth peer name vns2
sudo ip link set vnsp2 netns nsv
sudo ip link set vns2 up
sudo ip netns exec nsv ip addr add $nsv_ip/$sm dev vnsp2
sudo ip netns exec nsv ip link set vnsp2 up

#Adding ports 1&2
sudo ovs-vsctl add-port $in_br $in_port1 -- set Interface $in_port1 ofport_request=$port_req1
sudo ovs-vsctl add-port $in_br $in_port2 -- set Interface $in_port2 ofport_request=$port_req2

#Routing table
#sudo ip netns exec nsa ip route flush cache
sudo ip netns exec nsa route add $loc_ip1 dev vnsp1
sudo ip route add $nsa_ip dev $in_port1

#sudo ip netns exec ns ip route flush cache
sudo ip netns exec nsv route add $loc_ip2 dev vnsp2
sudo ip route add $nsv_ip dev $in_port2

#ARP table, mirroring, tunnel skipped here

# Add new flows
sudo ovs-ofctl del-flows $in_br

#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req1,actions=$port_req2
#sudo ovs-ofctl -O OpenFlow13 add-flow $in_br in_port=$port_req2,actions=$port_req1

#Private interfaces normally 'down', set to 'up'
sudo ip addr add $loc_ip1/$sm dev $in_port1
sudo ip link set dev $in_port1 up

sudo ip addr add $loc_ip2/$sm dev $in_port2
sudo ip link set dev $in_port2 up

#sudo ip addr add $loc_ip3/$sm dev $in_port3
sudo ip addr add $loc_ip3/$sm dev $in_port3
sudo ip link set dev $in_port3 up
#sudo ip link set dev $in_port3 promisc on

echo 'Bridge details'
sudo ovs-vsctl show

echo 'Namespace details'
sudo ip netns list all

#Connecting to RYU controller & OVSDB manager
sudo ovs-vsctl set-controller $in_br tcp:$ryu_ip:9000
sudo ovs-vsctl set-manager ptcp:6640
