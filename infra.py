from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

def tree_topology():
    """Set up a tree-based Mininet topology."""
    # Create a Mininet instance with a remote controller and traffic control links
    net = Mininet(controller=RemoteController, link=TCLink)

    # Add the Ryu controller
    ryu_controller = net.addController(
        'ryuController',
        controller=RemoteController,
        ip='127.0.0.1',  # IP address of the machine running the Ryu controller
        port=6633  # Default OpenFlow port
    )

    # Add core switch
    core_switch = net.addSwitch('s1')  # Core Layer: Single switch

    # Add aggregation layer switches
    agg_switch1 = net.addSwitch('s2')  # Aggregation Layer Switch 1
    agg_switch2 = net.addSwitch('s3')  # Aggregation Layer Switch 2

    # Add access layer switches
    access_switch1 = net.addSwitch('s4')  # Access Layer Switch 1
    access_switch2 = net.addSwitch('s5')  # Access Layer Switch 2
    access_switch3 = net.addSwitch('s6')  # Access Layer Switch 3
    access_switch4 = net.addSwitch('s7')  # Access Layer Switch 4

    # Interconnect core and aggregation switches
    net.addLink(core_switch, agg_switch1, bw=50, delay='2ms')  # Core -> Aggregation 1
    net.addLink(core_switch, agg_switch2, bw=50, delay='2ms')  # Core -> Aggregation 2

    # Interconnect aggregation and access switches
    net.addLink(agg_switch1, access_switch1, bw=30, delay='5ms')  # Aggregation 1 -> Access 1
    net.addLink(agg_switch1, access_switch2, bw=30, delay='5ms')  # Aggregation 1 -> Access 2
    net.addLink(agg_switch2, access_switch3, bw=30, delay='5ms')  # Aggregation 2 -> Access 3
    net.addLink(agg_switch2, access_switch4, bw=30, delay='5ms')  # Aggregation 2 -> Access 4

    # Add hosts to the topology
    # Subnet 10.0.0.0/24
    host1 = net.addHost('h1', ip='10.0.0.1/24')
    host2 = net.addHost('h2', ip='10.0.0.2/24')
    host3 = net.addHost('h3', ip='10.0.0.3/24')
    host4 = net.addHost('h4', ip='10.0.0.4/24')
    # Subnet 10.0.1.0/24
    host5 = net.addHost('h5', ip='10.0.1.1/24')
    host6 = net.addHost('h6', ip='10.0.1.2/24')
    host7 = net.addHost('h7', ip='10.0.1.3/24')
    host8 = net.addHost('h8', ip='10.0.1.4/24')

    # Connect hosts to access layer switches
    net.addLink(host1, access_switch1)
    net.addLink(host2, access_switch1)
    net.addLink(host3, access_switch2)
    net.addLink(host4, access_switch2)
    net.addLink(host5, access_switch3)
    net.addLink(host6, access_switch3)
    net.addLink(host7, access_switch4)
    net.addLink(host8, access_switch4)

    # Start the network
    net.start()
    print("Tree-based topology is up. Use 'pingall' in the CLI to test connectivity.")

    # Test connectivity automatically
    net.pingAll()

    # Enter the Mininet CLI for manual testing
    CLI(net)

    # Stop the network
    net.stop()
