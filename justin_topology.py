from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

def justin_topology():
    """Define a unique tree-based network topology."""
    # Create the network instance
    network = Mininet(controller=RemoteController, link=TCLink)

    # Add the remote controller
    ctrl = network.addController(
        name='remote_ctrl',
        controller=RemoteController,
        ip='10.0.2.15',
        port=6633
    )

    # Define core, aggregation, and access switches
    core_switch = network.addSwitch('core1')
    agg_switches = [
        network.addSwitch(f'agg{i}') for i in range(1, 3)
    ]
    access_switches = [
        network.addSwitch(f'acc{i}') for i in range(1, 5)
    ]

    # Link core to aggregation switches
    for agg_switch in agg_switches:
        network.addLink(core_switch, agg_switch, bw=50, delay='2ms', use_htb=True)

    # Link aggregation switches to access switches
    network.addLink(agg_switches[0], access_switches[0], bw=30, delay='5ms', use_htb=True)
    network.addLink(agg_switches[0], access_switches[1], bw=30, delay='5ms', use_htb=True)
    network.addLink(agg_switches[1], access_switches[2], bw=30, delay='5ms', use_htb=True)
    network.addLink(agg_switches[1], access_switches[3], bw=30, delay='5ms', use_htb=True)

    # Add hosts with unique IPs
    host_ips = [f'10.0.{subnet}.{host}/24' for subnet in range(1, 3) for host in range(1, 5)]
    hosts = [network.addHost(f'host{i+1}', ip=host_ips[i]) for i in range(8)]

    # Connect hosts to access switches
    access_mapping = {
        0: access_switches[0], 1: access_switches[0],
        2: access_switches[1], 3: access_switches[1],
        4: access_switches[2], 5: access_switches[2],
        6: access_switches[3], 7: access_switches[3]
    }
    for idx, host in enumerate(hosts):
        network.addLink(host, access_mapping[idx])

    # Launch the network
    network.start()
    print("Network is active. Use CLI for further testing.")

    # Test basic connectivity
    network.pingAll()

    # Open Mininet CLI
    CLI(network)

    # Stop the network
    network.stop()

if __name__ == '__main__':
    justin_topology()