# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf8

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp, arp
from ryu.lib.packet import icmp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
#from event_post import add_container
#import post_data
import subprocess
import array
import sys, os


class sarnet(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION,
		    ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(sarnet, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
    	print "SDN-Controller:RYU initialization"
#	Encryption check
#       subprocess.call(["sudo","ovs-vsctl","--db=tcp:10.20.5.46:6640","add-port","sarnet4","test"])
#       subprocess.call(["sudo","ovs-vsctl","--db=tcp:134.221.127.99:6640","add-port","sarnet4","ens4","--","set","Interface","ens4","type=gre","options:remote_ip=10.20.30.11","options:local_ip=10.20.30.4"])
#		print "GRE port added"


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
	#print datapath

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  Te bug has been fixed in OVS v2.1.0.

 	match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
	print "flood HIT 1"

	#TCP Packet flow-miss, match for HTTP
        match = parser.OFPMatch(eth_type = 0x0800, ip_proto = 0x06, tcp_dst = 100)
    	actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        ofproto.OFPCML_NO_BUFFER)]
#       subprocess.call(["sudo","ovs-vsctl","--db=tcp:134.221.127.97:6640","--","set","Bridge","sarnet1","mirrors=@m","--","--id=@vns1","get","port","vns1","--","--id=@ens4","get","port","ens4","--","--id=@m","create","Mirror","name=m0","select-dst-port=@vns1","select-src-port=@vns1","output-port=@ens4"])
	#actions = [parser.OFPActionOutput(2)]
	#actions.append(parser.OFPActionOutput(2))
        self.add_flow(datapath, 10, match, actions)
	#subprocess.call(["python","post_data.py"])
        print "HTTP: flood HIT 2"


    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
#        if ev.msg.msg_len < ev.msg.total_len:
#            self.logger.debug("packet truncated: only %s of %s bytes",
#                              ev.msg.msg_len, ev.msg.total_len)

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
	parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
	print "Packet recieved on port"
        data = msg.data
	pkt = packet.Packet(msg.data)

	#Check for different types of packet. Extracting packet headers from Ethernet_Packet
	#Ethernet > IPV4 > ICMP,ARP,TCP > HTTP

        eth_pkt = pkt.get_protocols(ethernet.ethernet)[0]
	#print "\n\n Ethernet Packet Header"
	#print eth_pkt
	#print eth_pkt.ethertype

#	print "\n\n IPV4 Packet Header"
	_ipv4 = pkt.get_protocol(ipv4.ipv4)
#	print _ipv4
	#print _ipv4.proto

#	print "\n\n ICMP Packet Header"
	_icmp = pkt.get_protocol(icmp.icmp)
#	print _icmp

#	print "\n\n ARP Packet Header"
	_arp = pkt.get_protocol(arp.arp)
#        print _arp

	print "\n\n TCP Packet Header"
	_tcp = pkt.get_protocol(tcp.tcp)
	print _tcp

        #print type(_tcp)
#	if _tcp is not None and _tcp.dst_port == 80:
#	    subprocess.call(["python","post_data.py"])

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        dst = eth_pkt.dst
        src = eth_pkt.src
	print "Connected SDN-SW:"
	print dpid
	if eth_pkt.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

	if dpid == 1:
	    if _tcp is not None and _tcp.dst_port == 100:
	        subprocess.call(["bash","trigger_pb.sh"])
		#subprocess.call(["bash","add_event.sh"])
		#subprocess.call(['sudo','ovs-vsctl','--db=tcp:10.20.5.46:6640','add-port','sarnet4','ens5','--','set','Interface','ens5','ofport_request=2','type=ipsec_gre','options:remote_ip=192.178.0.8','options:local_ip=192.178.0.3','options:psk=secret'])
		#subprocess.call(['sudo','ovs-vsctl','--db=tcp:10.20.5.2:6640','add-port','sarnet5','ens5','--','set','Interface','ens5','ofport_request=1','type=ipsec_gre','options:remote_ip=192.178.0.3','options:local_ip=192.178.0.8','options:psk=secret'])

        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
	else:
            out_port = ofproto.OFPP_FLOOD
	    print "flood:Learning MAC"

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
	if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            self.add_flow(datapath, 1, match, actions)
            print "Normal Flows added"

            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)

	# install a flow to avoid HTTP packet_in next time
	if out_port != ofproto.OFPP_FLOOD and _tcp.dst_port == 100:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            self.add_flow(datapath, 12, match, actions)
            #if _tcp is not None and _tcp.dst_port == 80:
            #   subprocess.call(["python","post_data.py"])
            print "Attack Flows added"

            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            #if msg.buffer_id != ofproto.OFP_NO_BUFFER:
             #   self.add_flow(datapath, 12, match, actions, msg.buffer_id)
              #  return
            #else:
             #   self.add_flow(datapath, 12, match, actions)


        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

	#construct packet_out message and send it.

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER,
                                 in_port=in_port, actions=actions, data=msg.data)
        datapath.send_msg(out)



