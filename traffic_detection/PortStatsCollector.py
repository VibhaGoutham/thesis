import time
import threading
import requests
import json
import csv
import subprocess

rx_packets = 0
rx_bytes = 0
t_observation = 5.0

#/stats/port/<dpid>[/<port>]
PortStatsURL = "http://10.20.5.39:8080/stats/port/1/1"

class StatisticCollector(threading.Thread):
    global rx_packets, rx_bytes, t_observation, PortStatsURL

    def __init__(self, threadID, dpid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dpid = dpid  #Datapath id of the switch
        #file = open("data_set_abnormal2.txt","w")

    def run(self):
        global rx_packets, rx_bytes, t_observation, PortStatsURL
        file = open("data_set_abnormal9.txt","w")
        #rx_packets = 0
        #rx_bytes = 0
        count = 0
        while True:
            try:
                #Send a request to RYU controller and get a response
        #while True:
                response = requests.get(PortStatsURL, headers={'content-type':'application/json'}).json()
	        data = response[self.dpid][0]
                #rx_packets = 0
                #rx_bytes = 0

	        delta_rx_packets = 0
	        delta_rx_bytes = 0
        	print("Rx_pkt is",rx_packets)
                #file.write("data here \n")

		if rx_packets <= int(data['rx_packets']):
                    #print("data here")
	    	    delta_rx_packets = int(data['rx_packets'])-rx_packets
                    print('Delta RX_Packets:  ',delta_rx_packets)
                    rx_packets = int(data['rx_packets'])
                    print("RX pkt is", rx_packets)
                    #file.write(str(rx_packets) + '\t')
	        else:
                    #print("data here")
                    rx_packets = int(data['rx_packets'])
                    print 'RX_Packets:  ',rx_packets
                #file.write(str(rx_packets) + '\t')


	        if rx_bytes <= int(data['rx_bytes']):
                    delta_rx_bytes = int(data['rx_bytes'])-rx_bytes
                    rx_bytes = int(data['rx_bytes'])
                    print 'Delta RX_Bytes: ',delta_rx_bytes
                    print("RX bytes is", rx_bytes)
                    #file.write(str(rx_bytes) + '\n')
	        else:
                    rx_bytes = int(data['rx_bytes'])
                    print 'RX_Bytes: ',rx_bytes
                    #file.write(str(rx_bytes) + '\n')

	        print 'Delta RX_Packets:  ',delta_rx_packets
	        print 'Delta RX_Bytes: ',delta_rx_bytes
	        print '\n'

                file = open("data_set_abnormal9.txt", "a")
		data_set = str(delta_rx_packets)+'\t'+str(delta_rx_bytes)+'\n'
	        file.write(data_set)
	        file.close()

                count = count + 1


            except:
                print 'StatisticCollector | There is an error... Exited on switch ',self.dpid
                file.close()
                break
            time.sleep(t_observation)
        #file.close()


#Start StatisticCollector agent for the switch
Collector = StatisticCollector(1000, '1')
Collector.start()
#time.sleep(5)

