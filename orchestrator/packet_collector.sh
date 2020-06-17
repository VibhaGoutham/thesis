#!/bin/bash

sleep 5s
ssh ubuntu@10.20.5.2 'bash /home/ubuntu/packet_logger.sh; bash -l' << EOF

EOF

#scp ubuntu@10.20.5.2:/home/ubuntu/traffic_affected.pcap /home/phantom


#mkfifo /tmp/remote
#wireshark -k -i /tmp/remote
#ssh ubuntu@10.20.5.2 "tcpdump -i eth0 not port 22" > /tmp/remote
#"tcpdump -s 0 -U -n -w - -i eth0 not port 22" > /tmp/remote

