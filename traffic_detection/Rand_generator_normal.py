import os
import sys
import time
import shlex, subprocess
import signal
import random
import threading
import csv, json, requests
#import extract_API

class SDNRand (threading.Thread):

    def __init__(self,protocol,target):

        threading.Thread.__init__(self)

        self.protocol=protocol

        self.target=target

    	#url1 = "http://10.20.5.39:8080/stats/port/1/1"

    	#with open('sample_data.csv', 'w') as csvfile:
            #fieldnames = ['Number', 'packet_count', 'byte_count', 'packet_diff']
            #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()

    def run(self):

	while True:

            packet_size=random.randint(64,1048)

            packet_rate=random.randint(500,10000)

            number_packets=random.randint(20,100)

            ip=self.target

            port='80'

            x=self.protocol

            cmd = 'sudo ' 'ip ' 'netns ' 'exec ' 'nsa ' 'hping3 '+ip+' --'+str(x)+' -S -V -p 80 -i u'+str(packet_rate)+' -c '+str(number_packets)+' -d '+str(packet_size)

            args = shlex.split(cmd)

            p = subprocess.Popen(args, shell=False)

            time.sleep(1.0)

            # killing all processes in the group

            os.kill(p.pid, signal.SIGTERM)

            if p.poll() is None:  # Force kill if process

                os.kill(p.pid, signal.SIGKILL)


            r = random.randint(3,10)

            time.sleep(r-1)

	    #import extract_API
	    #row = ({'Number': x, 'packet_count': packet_count, 'byte_count': byte_count, 'packet_diff': packet_diff})
	    #writer.writerow(row)

        #file.close(csvfile)

x = sys.argv[1]

y = sys.argv[2]

protocol = SDNRand(x,y)

protocol.start()
