# Network Device Exporter Configuration
# Configuration can be edited during application runtime - a restart however is recommended
# This file is supposed to configure how NDE (Network Device Exporter) behaves and works.
# All provided sources for Devices to monitor (HostFiles, CustomNetworkDevices) are merged.

from hostentry import HostEntry

"""
Sets the TCP-Port, the Exporter is listening for requests (from Prometheus).
Make sure you have corresponding firewall-rule, allowing incoming traffic to this port.
"""
ListenPort = 2020

"""
Sets the IP-address or hostname, the Exporter is listening for requests (from Prometheus).
Use '0.0.0.0' as default-value, if you want it just to work
"""
ListenAddress = '0.0.0.0'


"""
The Location of the Ping-executable. This location might different on various distributions
Open up a terminal, and type in 'which ping', to get the location of the ping-executable.
If ping is not installed, please install it first. NDE requires(!) 'ping' to be present.
"""
PingExecutableLocation = '/bin/ping'

"""
Path to file(s) containing DNS-mappings between IP(v4 or v6)-addresses and their corresponding hostnames.
The IP-Address will be used to communicate with that Device, the Hostname will be used as Metric-name for Prometheus.
If NDE should not parse any files, make thist list empty
"""
HostFiles = [
    '/etc/hosts'
]

"""
Configure CustomNetworkDevices that shall be monitored (and exported) by NDE. 
These are devices that are monitored additionally to the (optionally) provided HostFiles.
"""
CustomNetworkDevices = [
    HostEntry('127.0.0.1', ['localhost.local']),
    HostEntry('10.0.100.1', ['rt-denc-vpngate.rtrace.home', 'vpngate.rtrace.io'])
]
