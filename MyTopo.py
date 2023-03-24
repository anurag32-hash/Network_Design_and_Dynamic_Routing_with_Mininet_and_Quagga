#!/usr/bin/python

from mininet.node import Node
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet


class LinuxRouter(Node):

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):

    def build(self, **_opts):
        h1IP = '128.0.1.1/24'
        h2IP = '133.0.1.1/24'
        r1IP = '128.0.1.2/24'
        r2IP = '131.0.1.1/24'
        r3IP = '132.0.1.1/24'
        r4IP = '133.0.1.2/24'
        r4IP2 = '131.0.1.2/24'
        r4IP3 = '132.0.1.2/24'
        r1IP2 = '129.0.1.1/24'
        r1IP3 = '130.0.1.1/24'
        r2IP2 = '129.0.1.2/24'
        r3IP2 = '130.0.1.2/24'

        h1 = self.addHost('h1', cls=LinuxRouter, ip=h1IP)
        h2 = self.addHost('h2', cls=LinuxRouter, ip=h2IP)
        r1 = self.addHost('r1', cls=LinuxRouter, ip=r1IP)
        r2 = self.addHost('r2', cls=LinuxRouter, ip=r2IP)
        r3 = self.addHost('r3', cls=LinuxRouter, ip=r3IP)
        r4 = self.addHost('r4', cls=LinuxRouter, ip=r4IP)

        self.addLink(h1, r1, intfName1='h1-eth1', intfName2='r1-eth1', params1={'ip': h1IP},
                     params2={'ip': r1IP})
        self.addLink(h2, r4, intfName1='h2-eth1', intfName2='r4-eth3', params1={'ip': h2IP},
                     params2={'ip': r4IP})
        self.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1', params1={'ip': r2IP},
                     params2={'ip': r4IP2})
        self.addLink(r3, r4, intfName1='r3-eth2', intfName2='r4-eth2', params1={'ip': r3IP},
                     params2={'ip': r4IP3})
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={'ip': r1IP2},
                     params2={'ip': r2IP2})
        self.addLink(r1, r3, intfName1='r1-eth3', intfName2='r3-eth1', params1={'ip': r1IP3},
                     params2={'ip': r3IP2})


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    net.get("h1").cmd("ip route add default via 128.0.1.2 dev h1-eth1")

    net.get("r1").cmd("ip route add 132.0.1.0/24 via 130.0.1.2 dev r1-eth3")
    net.get("r1").cmd("ip route add default via 129.0.1.2 dev r1-eth2")

    net.get("r3").cmd("ip route add 128.0.1.0/24 via 130.0.1.1 dev r3-eth1")
    net.get("r3").cmd("ip route add 129.0.1.0/24 via 130.0.1.1 dev r3-eth1")
    net.get("r3").cmd("ip route add default via  132.0.1.2 dev r3-eth2")

    net.get("r2").cmd("ip route add 128.0.1.0/24 via 129.0.1.1 dev r2-eth1")
    net.get("r2").cmd("ip route add 130.0.1.0/24 via 129.0.1.1 dev r2-eth1")
    net.get("r2").cmd("ip route add default via 131.0.1.2 dev r2-eth2")

    net.get("r4").cmd("ip route add 130.0.1.0/24 via 132.0.1.1 dev r4-eth2")
    net.get("r4").cmd("ip route add default via 131.0.1.1 dev r4-eth1")

    net.get("h2").cmd("ip route add default via 133.0.1.2 dev h2-eth1")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

# reference: https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py
