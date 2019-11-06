#!/bin/bash

ryu-manager --ofp-tcp-listen-port 9000 sarnet_sdncontroller.py

wait 60s

ryu-manager --ofp-tcp-listen-port 9000 ofctl_rest.py

