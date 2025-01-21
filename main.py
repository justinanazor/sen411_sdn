from mininet.log import setLogLevel, info

from sdn_network_holi.infra_old import netType

if __name__ == '__main__':
    setLogLevel('info')
    netType.tree_topology()