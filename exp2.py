#!/usr/bin/python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel

class MyTopo(Topo):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Connect hosts to switches
        self.addLink(h1, s1, port1=0, port2=1)  # h1-eth0 <-> s1-eth1
        self.addLink(h2, s1, port1=0, port2=2)  # h2-eth0 <-> s1-eth2
        self.addLink(s1, s2, port1=3, port2=1)  # s1-eth3 <-> s2-eth1
        self.addLink(s2, h3, port1=2, port2=0)  # s2-eth2 <-> h3-eth0

def main():
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(topo=topo, switch=OVSKernelSwitch, controller=DefaultController, autoSetMacs=True)
    net.start()

    # Start SSH on hosts
    for h in ['h1', 'h2', 'h3']:
        net[h].cmd('/usr/sbin/sshd')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()