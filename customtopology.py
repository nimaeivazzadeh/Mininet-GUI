from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch
import tkinter.messagebox
from tkinter import END
import sys
import json

from contextlib import redirect_stdout, redirect_stderr


data = json.load(open('Topology'))
mnOutput = None


def testtopology():
    tkinter.messagebox.showinfo("Deploy topology to mininet ", "Press ok button and wait for a seconds to see result")

    with open('./stdout.txt', 'w') as outfile:
        with redirect_stdout(outfile), redirect_stderr(outfile):

            num_hosts = len(data['Hosts'])
            topo = CustomTopology(num_hosts)
            net = Mininet(topo=topo)

            print('\n =================================================> Start the topology \n')
            # mnOutput.insert(END, '******************** start the topology\n')
            net.start()

            print('\n =================================================> Test the topology by running a ping command \n')
            # mnOutput.insert(END, '******************** test the topology by running a ping command\n')

            # mnOutput.insert(END, '********************* read data from json file and ping all hosts\n')

            ping_all_full = net.pingAllFull()
            # mnOutput.insert(END, '********************* stop all network\n')
            print('Result from ping Test: \n' + '\n' + str(ping_all_full) + '\n' + '\n % of packets dropped.\n')

            ping_pair = net.pingPairFull()
            print('Result from Regression Test : \n' + '\n' + str(ping_pair) + '\n' + '\n % of packets dropped.\n')

            print('\n ==============> Testing TCP bandwidth between: \n')
            iPerf = net.iperf()
            print('Result from iPerf: \n' + '\n' + str(iPerf) + '\n')

#            mo = net.monitor(self, hosts=, timeoutms=)
#            print('Result from monitor: ' + str(mo))

            stop = net.stop()
            print('Stop the network:' + str(stop) + '\n')

            clean = net.cleanup
            print('cleanup the mininet network: ' + str(clean) + '\n')

#            cpu = net.runCpuLimitTest(cpu=0.5)
#            print('Cpu limit test: ' + str(cpu))

    with open('./stdout.txt') as infile:
        mnOutput.insert(END, infile.read())


class CustomTopology(Topo):

    def __init__(self, n, **opts):

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
        for client_machine in range(n):
            host = self.addHost('h%s' % (client_machine + 1))
            self.addLink(host, switch)

        info('****************************Links path')
#         for path in data['Path']:
#             for p in path:
#                 src = p
#                 dst = path[p]
#
#                 sr_link = src
#                 ds_link = dst
#
#                 self.addLink(sr_link, ds_link)
#                 print("Path==========>" + Path + port1 + port2 + '\n', )

        # for link in data['Links']:
        #     for x in link:
        #         source_node = x
        #         destination_node = link[x]
        #
        #         source_node_name = source_node.split('-')[0]
        #         destination_node_name = destination_node.split('-')[0]
        #
        #         self.addLink(source_node_name, destination_node_name)

                # create graph from JSON file made for the project
                # g.add_node(source_node_name)
                # g.add_node(destination_node_name)
                # g.add_edge(source_node_name, destination_node_name)

        # pos = nx.spring_layout(g)
        # nx.draw_networkx(g, pos, node_color='r', with_labels=True, node_size=400, font_size=10)
        # plt.ylabel('Topology')
        # plt.title('Topology graph based on "Links" dictionary in JSON file')
        # plt.show()


if __name__ == '__main__':
    testtopology()
    setLogLevel('info')
