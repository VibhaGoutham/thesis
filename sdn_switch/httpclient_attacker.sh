#!/bin/bash

for i in {1..10}; do

 echo Sending request number "$i"
 sudo ip netns exec nsa curl http://10.20.30.33:100
 sleep 3s

done
