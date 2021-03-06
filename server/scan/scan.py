import json
import os
import sys

import socket
from server.control.util import command

import traceback
from server.couchbase import store, util

def nmap_port_status(status):
    ps = {}
    l_nmap = status.split()
    ports = l_nmap[4:]

    continue_probe = False
    for port in ports:
        results = port.split('/')
        ps[results[0]] = results[1]
        if results[1] == "open":
            continue_probe = True
    return (ps, continue_probe)

class ScanInterface(object):
    recordclass = None
    syncclass = None
    primarykey = 'hostname'

    def __init__(self, round=1):
        self.round = round
        self.count = 1

    def __getattr__(self, name):
        if 'collect' in name or 'record' in name:
            method = getattr(self, name, None)
            if method is None:
                raise Exception("No such method %s" % name)
            return method
        else:
            raise Exception("No such method %s" % name)

    def collect(self, nodename, data):
        pass


class ScanNode(ScanInterface):

    syncclass = None
    primarykey = 'hostname'

    def collectPorts(self, nodename, port_list=[22,80,806]):
        values = {}
        for port in port_list:
            ret = os.system("nc -w 5 -z %s %s > /dev/null" % (nodename, port) )
            if ret == 0:
                values[str(port)] = "open"
            else:
                values[str(port)] = "closed"
       # print "Port Status: %s \n" % values
        return {'port_status' : values }

    def collectNMAP(self, nodename, cohash):
        #### RUN NMAP ###############################
        # NOTE: run the same command three times and take the best of three
        # 		runs.  NMAP can drop packets, and especially so when it runs many
        # 		commands at once.
        values = {}
        nmap = command.CMD()
        print "nmap -oG - -P0 -p22,80,806 %s | grep -v Down | grep Ports:" % nodename
        (oval1,eval) = nmap.run_noexcept("nmap -oG - -P0 -p22,80,806 %s | grep -v Down | grep Ports:" % nodename)
        (oval2,eval) = nmap.run_noexcept("nmap -oG - -P0 -p22,80,806 %s | grep -v Down | grep Ports:" % nodename)
        (oval3,eval) = nmap.run_noexcept("nmap -oG - -P0 -p22,80,806 %s | grep -v Down | grep Ports:" % nodename)
        # NOTE: an empty / error value for oval, will still work.
        values['port_status'] = {}
        (o1,continue_probe) = nmap_port_status(oval1)
        (o2,continue_probe) = nmap_port_status(oval2)
        (o3,continue_probe) = nmap_port_status(oval3)
        for p in ['22', '80', '806']:
            l = [ o1[p], o2[p], o3[p] ]
            if len(filter(lambda x: x == 'open', l)) > 1:
                values['port_status'][p] = 'open'
            else:
                values['port_status'][p] = o1[p]

      #  print values['port_status']
        return (nodename, values)

    def collectPING(self, nodename, cohash):
        values = {}
        ping = command.CMD()
        (oval,errval) = ping.run_noexcept("ping6 -c 1 -q %s | grep rtt" % nodename)

        values = {}
        if oval == "":
            # An error occurred
          #  print "Ping-->Error "
            values['ping_status'] = "Fail"
        else:
          #  print "Ping-->Works "
            values['ping_status'] = oval
       # print "Ping Status: %s \n" % oval
        return values

    def collectTRACEROUTE(self, nodename, cohash):
        values = {}
        trace = command.CMD()
        (oval,errval) = trace.run_noexcept("traceroute %s" % nodename)
        oval = oval.replace("\n", " ")
        values['traceroute'] = oval
        #print "Traceroute Status: %s \n" % oval
        return values

    def collectSSH(self, nodename, cohash):
        #Assuming that private nad public keys have been setup.
        #Checking for keys and access needs to be automated.
        values = {}
        try:
            for port in [22, 806]:
                ssh = command.SSH('navaneeth', nodename, port)

                (oval, errval) = ssh.run_noexcept2(""" <<\EOF
                    echo "{"
                    echo '  "kernel_version":"'`uname -a`'",'
                    echo "}"
EOF			""")

                values['ssh_error'] = errval
                print "Status after SSH: %s \n" %oval

        except:
            print traceback.print_exc()
            sys.exit(1)

        return values


    def collectDNS(self, nodename, cohash):
        values = {}
        try:
            ipaddr = socket.gethostbyname(nodename)
            # TODO: Implement
            values['external_dns_status'] = True
        except Exception, err:
            values['external_dns_status'] = False

        return values

    def collectExternal(self, nodename, cohash):
        try:
            values = {}

            v = self.collectPING(nodename, cohash)
            values.update(v)

          #  v = self.collectPorts(nodename)
          #  values.update(v)

          #  v = self.collectSSH(nodename, cohash)
          #  values.update(v)

          #  v = self.collectDNS(nodename, cohash)
          #  values.update(v)

          #  v = self.collectTRACEROUTE(nodename, cohash)
          #  values.update(v)

        except:
            print traceback.print_exc()

        return (nodename, values)


def probe(hostname):
    scannode = ScanNode()
    try:
        (nodename, values) = scannode.collectExternal(hostname, {})
        return values
    except:
        print traceback.print_exc()
        return False

def probe_and_store(hostname):

    nodeip6 = hostname

    hostname= hostname.lstrip('[')
    hostname= hostname.rstrip(']')

    values = probe(hostname)
    timestamp = util.get_timestamp()
    values.update({"server_timestamp":timestamp})
    values.update({'nodeid': nodeip6})
    values.update({'type': 'node_synthesized'})

    doc_id = nodeip6+'-synthesized'+str(timestamp)

    try:
        store.store_document(doc_id, values)

        reference_doc_id = nodeip6+ '-synthesized-most_recent'
        values.update({'type' : 'node_most_recent_synthesized'})
        store.update_document(reference_doc_id, values)
    except Exception as e:
	    print "Caught Exception: "+ str(e)
	    pass


def main():
    probe('fd65:fc41:c50f:5::2')


if __name__ == "__main__":
    main()