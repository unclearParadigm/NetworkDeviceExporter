# Network Device Exporter

NDE (short for Network Device Exporter) is a Prometheus-compatible Exporter, that
parses Hostfile(s) like ```/etc/hosts```, or any file that 
[dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) would parse. NDE will perform
Pings to devices in such files and export the results. 

This exporter is aimed to be working in Linux/UNIX-oid environments (even though it should work on Windows as well).
It is written in native Python without any third-party-dependencies, and works with any Python Interpreter >= 3.5.


### How can I run it?

Since NDE does not have any additional dependencies, other than those Python already delivers,
getting started with NDE is as simple as cloning and running it.

```bash
git clone git@github.com:unclearParadigm/NetworkDeviceExporter.git
cd NetworkDeviceExporter
python nde.py

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
SELinux accordingly to allow execution.

```bash
# clone Repo to home/bin directory of the newly created user
git clone git@github.com:unclearParadigm/NetworkDeviceExporter.git /home/networkdeviceexporter/bin/NetworkDeviceExporter
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
WorkingDirectory=/home/networkdeviceexporter/bin/NetworkDeviceExporter
ExecStart=/home/networkdeviceexporter/bin/NetworkDeviceExporter/nde.py
Restart=always
RestartSec=3

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
where the all the configuration for NDE resides. The File itself is sufficiently documented
with comments and should be fairly self-descriptive.

One thing, that might be a bit weird at the moment is the fact that you have to configure
the location of your Ping-Executable. This is the only possibility to keep the application
Platform-independent at the moment.

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
| nde_ping_time | time in milliseconds    | indicates how it took the specified hostname to respond to the ICMP ping       |
