#!/usr/bin/python3
# intronetworks.cs.luc.edu/current1/uhtml/auxiliary_files/mininet/routerline.py

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, Controller, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel

class Router(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(Router, self).config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super(Router, self).terminate()

class MyTopo(Topo):
    def build(self):

        # Routers
        r1 = self.addNode('r1', cls=Router)
        r2 = self.addNode('r2', cls=Router)

        # Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Links
        self.addLink(h1, r1)   # r1-eth0
        self.addLink(h2, r1)   # r1-eth1
        self.addLink(r1, r2)   # r1-eth2, r2-eth0
        self.addLink(r2, h3)   # r2-eth1, h3-eth0

def run():
    topo = MyTopo()
    net = Mininet(topo=topo,
                  controller=DefaultController,
                  switch=OVSKernelSwitch,
                  autoSetMacs=True)

    net.start()

    h1 = net['h1']
    h2 = net['h2']
    h3 = net['h3']
    r1 = net['r1']
    r2 = net['r2']

    # -----------------------------------
    # h1 <--> r1
    # -----------------------------------
    h1.setIP("10.0.0.1/24", intf="h1-eth0")
    r1.setIP("10.0.0.3/24", intf="r1-eth0")

    # -----------------------------------
    # h2 <--> r1
    # -----------------------------------
    h2.setIP("10.0.3.2/24", intf="h2-eth0")
    r1.setIP("10.0.3.4/24", intf="r1-eth1")

    # -----------------------------------
    # r1 <--> r2
    # -----------------------------------
    r1.setIP("10.0.1.1/24", intf="r1-eth2")
    r2.setIP("10.0.1.2/24", intf="r2-eth0")

    # -----------------------------------
    # r2 <--> h3 
    # -----------------------------------
    r2.setIP("10.0.2.1/24", intf="r2-eth1")
    h3.setIP("10.0.2.2/24", intf="h3-eth0")

    # -----------------------------------
    # Routes
    # -----------------------------------
    h1.cmd("ip route add default via 10.0.0.3")
    h2.cmd("ip route add default via 10.0.3.4")
    h3.cmd("ip route add default via 10.0.2.1")


    r1.cmd("ip route add 10.0.2.0/24 via 10.0.1.2")
    r2.cmd("ip route add 10.0.0.0/24 via 10.0.1.1")
    r2.cmd("ip route add 10.0.3.0/24 via 10.0.1.1")

    # -----------------------------------
    # Pings & save results
    # -----------------------------------
    results = []
    results.append("h1 -> h3\n" + h1.cmd("ping -c 1 10.0.2.2"))
    results.append("h2 -> h3\n" + h2.cmd("ping -c 1 10.0.2.2"))
    results.append("h3 -> h1\n" + h3.cmd("ping -c 1 10.0.0.1"))
    results.append("h3 -> h2\n" + h3.cmd("ping -c 1 10.0.3.2"))

    with open("result1.txt", "w") as f:
        for line in results:
            f.write(line + "\n")

    print("Ping results saves in result1.txt")


    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run()