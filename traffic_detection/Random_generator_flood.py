import os
import sys
import time
import shlex, subprocess
import signal
import random
import threading, requests, json

class SDNRand (threading.Thread):

    def __init__(self,protocol,target):

        threading.Thread.__init__(self)

        self.protocol=protocol

        self.target=target

        PortStatsURL = "http://10.20.5.39:8080/stats/port/1/1"

        #file = open('data_set_abnormal2.txt','w')

    def run(self):

        #with open('sample_data.csv', 'w') as csvfile:
            #fieldnames = ['Number', 'packet_count', 'byte_count', 'packet_diff']
            #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()

        while True:
            #print("Class 1 while loop here")
            packet_size=random.randint(64,1048)
            #packet_size=1000

            packet_rate=random.randint(500,1000)

            number_packets=random.randint(55,180)
            #number_packets=100000

            ip=self.target

            port='80'

            x=self.protocol

            cmd = 'sudo ' 'ip ' 'netns ' 'exec ' 'nsa ' 'hping3 '+ip+' --'+str(x)+' -S -V -w 64 -p 80 --flood -i u'+str(packet_rate)+' -c '+str(number_packets)+' -d '+str(packet_size)

            args = shlex.split(cmd)

            p = subprocess.Popen(args, shell=False)

            time.sleep(1.0)

            # killing all processes in the group

            os.kill(p.pid, signal.SIGTERM)

            if p.poll() is None:  # Force kill if process

                os.kill(p.pid, signal.SIGKILL)

            r = random.randint(3,10)

            time.sleep(r-1)
            #print("Class 1 while ends here")


x = sys.argv[1]

y = sys.argv[2]

protocol = SDNRand(x,y)

protocol.start()
