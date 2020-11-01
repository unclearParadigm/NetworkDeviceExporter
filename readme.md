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

### How can I configure it?

Inside the previously cloned directory, there is a file called [configuration.py](configuration.py). This is
where the all the configuration for NDE resides. The File itself is sufficiently documented
with comments and should be fairly self-descriptive.

One thing, that might be a bit weird at the moment is the fact that you have to configure
the location of your Ping-Executable. This is the only possibility to keep the application
Platform-independent at the moment.
