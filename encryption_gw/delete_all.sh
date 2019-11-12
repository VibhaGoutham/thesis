
#!/bin/bash

in_br=sarnet4
ns1=nsa
ns2=nsv

#sudo ip netns del $ns1

#sudo ip netns del $ns2

sudo ovs-vsctl del-br $in_br

sudo ovs-vsctl del-manager

echo Namespaces:
sudo ip netns list

echo OVS Bridge:
sudo ovs-vsctl show

