import subprocess

subprocess.call(['sudo','ovs-vsctl','--db=tcp:10.20.5.46:6640','add-port','sarnet4','ens5','--','set','Interface','ens5','ofport_request=2','type=ipsec_gre','options:remote_ip=192.178.0.8','options:local_ip=192.178.0.3','options:psk=secret'])

subprocess.call(['sudo','ovs-vsctl','--db=tcp:10.20.5.2:6640','add-port','sarnet5','ens5','--','set','Interface','ens5','ofport_request=1','type=ipsec_gre','options:remote_ip=192.178.0.3','options:local_ip=192.178.0.8','options:psk=secret'])
