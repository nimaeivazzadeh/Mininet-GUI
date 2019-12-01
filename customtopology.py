from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController, OVSKernelSwitch, Controller, OVSSwitch
from mininet.link import TCLink, Intf
import tkinter.messagebox
from tkinter import END
import json

from contextlib import redirect_stdout, redirect_stderr


data = json.load(open('Topology'))
mnOutput = None
node_1 = ''
node_2 = ''


def testtopology():
    tkinter.messagebox.showinfo("Deploy topology to mininet ", "Press ok button and wait for a seconds to see result")

    with open('./stdout.txt', 'w') as outfile:
        with redirect_stdout(outfile), redirect_stderr(outfile):

            topo = CustomTopology()
            net = Mininet(topo=topo,
                          # switch=OVSSwitch,
                          # autoSetMacs=True,
                          cleanup=True)

            # c0 = net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633)
            # net.build()
            # c0.start()

            print('\n =================================================> Start the topology \n')
            net.start()

            print('\n =================================================> Test the topology by running a ping command \n')

            ping_all_full = net.pingAllFull()
            print('Result from ping Test: \n' + '\n' + str(ping_all_full) + '\n' + '\n % of packets dropped.\n')

            ping_pair = net.pingPairFull()
            print('Result from Regression Test : \n' + '\n' + str(ping_pair) + '\n' + '\n % of packets dropped.\n')

            print('\n ==============> Testing TCP bandwidth between: \n')

            iperf_origin = net.getNodeByName(node_1)
            iperf_destination = net.getNodeByName(node_2)

            iPerf = net.iperf([iperf_origin, iperf_destination])

            print('Result from iPerf between node ' + node_1 + ' and node ' + node_2 + '\n' + '\n' + str(iPerf) + '\n')

            stop = net.stop()
            print('Stop the network:' + str(stop) + '\n')

            clean = net.cleanup
            print('cleanup the mininet network: ' + str(clean) + '\n')

    with open('./stdout.txt') as infile:
        mnOutput.insert(END, infile.read())
        # CLI(net)

class CustomTopology(Topo):

    def __init__(self,  **opts):

        global switch
        Topo.__init__(self, **opts)

        info('****************************Add Switches from JSON file')
        for switch in data['Switches']:
            switch = self.addSwitch(switch)
            print("\n Switch===========================================>" + switch + '\n',)

        info('****************************Add Hosts from JSON file')
        for host in data['Hosts']:
            host = self.addHost(host)
            print("\n Host=============================================>" + host + '\n',)

        info('****************************Links hosts and switches to each other based on JSON file Links dictionary')
        for link in data['Links']:
            for A, B in link.items():
                a_name = A.split('-')[0]
                b_name = B.split('-')[0]
                linkk = self.addLink(a_name, b_name)
                # print("\n Host=============================================>" + str(linkk) + '\n', )


if __name__ == '__main__':
    testtopology()
    setLogLevel('info')
