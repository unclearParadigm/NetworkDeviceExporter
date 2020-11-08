# Network Device Exporter

[![Code Climate](https://codeclimate.com/github/unclearParadigm/NetworkDeviceExporter/badges/gpa.svg)](https://codeclimate.com/github/unclearParadigm/NetworkDeviceExporter/)

NDE (short for Network Device Exporter) is a Prometheus-compatible Exporter, that
parses Hostfile(s) like ```/etc/hosts```, or any file that 
[dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) would parse. NDE will perform
Pings to devices in such files and export the results. 

This exporter is aimed to be working in Linux/UNIX-oid environments (even though it should work on Windows as well).
It is written in native Python without any third-party-dependencies, and works with any Python Interpreter >= 3.6.

### Why do I need this?

Some (but not limited to) example use-cases:
- Uptime monitoring of Network-Devices
- Verification that routes to specific host are correctly configured
- simplistic way of ensuring Network-integrity and stability
- monitor network-performance in a simple way
- Alerts on presence detection (e.g. a mobile phone connects to your Wifi)
- VPN (e.g. Wireguard, OpenVPN) user-behavior analytics

Feel free to tell me, what you are using it for.

### How can I run it?

Since NDE does not have any additional dependencies, other than those Python already delivers,
getting started with NDE is as simple as cloning and running it.

```bash
git clone git@github.com:unclearParadigm/NetworkDeviceExporter.git
cd NetworkDeviceExporter
python3 nde.py

# Verify that NDE is running (by default it is listening on Port 2020)
curl http://localhost:2020

# Prometheus Metrics in human-readable format are available at localhost:2020/metrics
curl http://localhost:2020/metrics
```

#### Running NDE in production

In production it is recommended to create a separate user for your Prometheus Exporters. This 
also applies to NDE.

```bash
# Create a new user that (ideally) is not able to login (e.g. via SSH)
useradd -r -s /bin/false networkdeviceexporter
```

If your system is using SELinux (e.g. RedHat-based Distributions), make sure you put
your script in a place where scripts/application can be executed per default, or configure
SELinux accordingly to allow execution. Recommended destination is `/usr/local/bin`

```bash
# clone Repo to home/bin directory of the newly created user
git clone git@github.com:unclearParadigm/NetworkDeviceExporter.git /usr/local/bin/NetworkDeviceExporter
```

It is also recommended to let systemd manage the lifecycle of your Exporter (if your Distribution runs systemd).
You can create a systemd-Unit that looks something like this:

```
[Unit]
Description=Network Device Exporter
After=multi-user.target

[Service]
Type=simple
User=networkdeviceexporter
Group=networkdeviceexporter
ExecStart=python3 /usr/local/bin/NetworkDeviceExporter/nde.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save this file to ```/etc/systemd/system/NetworkDeviceExporter.service```.
To enable and start the Service via systemd, do the following:

```bash
# Tell systemctl to re-index the Unit-Files (to include the one you just created)
systemctl daemon-reload

# Let systemd automatically start NDE when system is booted
systemctl enable NetworkDeviceExporter.service

# Start NDE via systemd
systemctl start NetworkDeviceExporter.service

# Check whether NDE is running
systemctl status NetworkDeviceExporter
```

### How can I configure it?

Inside the previously cloned directory, there is a file called [configuration.py](configuration.py). This is
where the all the configuration for NDE resides. The file itself is sufficiently documented
with comments and should be fairly self-descriptive.

One thing, that might be a bit weird at the moment is the fact that you have to configure
the location of your Ping-Executable. This is the only possibility to keep the application
platform-independent at the moment.

- The default ListenPort is `2020`
- The default file that is read is `/etc/hosts`
- You can add other files to that collection (just make sure the files are read-accessible)
- The default location of the Ping executable points to `/bin/ping` (which should be fine on most distributions)

### What does it export?

```
# Short eaxmple of exported fields
nde_ping_ok{target_hostname="localhost"} 1
nde_ping_size{target_hostname="localhost"} 64
nde_ping_time{target_hostname="localhost"} 0.087
nde_ping_ok{target_hostname="localhost.localdomain"} 1
nde_ping_size{target_hostname="localhost.localdomain"} 64
nde_ping_time{target_hostname="localhost.localdomain"} 0.087
```

| Metric        | Value(s)                | Description                                                                    |
|:-------------:|:-----------------------:|:------------------------------------------------------------------------------:|
| nde_ping_ok   | 0 or 1                  | 1 indicates that the hostname was successfully pingable, 0 indicates a failure |
| nde_ping_size | icmp-ping size in bytes | indicates the ICMP-request size                                                |
| nde_ping_time | time in milliseconds    | indicates how long it took the specified hostname to respond to the ICMP ping  |

### License (MIT)

Permission is hereby granted, free of charge, 
to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
