import subprocess
import configuration
from typing import List
from hostentry import HostEntry


class Ping(object):
    def __init__(self, hostentry: HostEntry) -> None:
        self.hostentry = hostentry
        self.ping_ok = False
        self.ping_size = -1
        self.ping_time = -1

    def ping(self) -> None:
        try:
            ping_cmd = [configuration.PingExecutableLocation, '-c', '1', self.hostentry.ip]
            output = subprocess.run(ping_cmd, shell=False, capture_output=True, text=True).stdout
            for line in output.split('\n'):
                if not line:
                    break

                stripped_line = str(line).strip()
                if 'icmp_seq' in stripped_line and self.hostentry.ip in stripped_line:
                    ping_size, _, _, ipv4, _, _, time_string, _ = stripped_line.split(' ')
                    self.ping_size = int(ping_size)
                    self.ping_ok = True
                    self.ping_time = float(time_string.split('=')[1])

        except Exception as exc:
            print(exc)
            self.ping_ok = False
            self.ping_size = -1
            self.ping_time = -1

    def export_prometheus_metric(self) -> List[str]:
        metric_collection = []
        for hostname in self.hostentry.hostnames:
            ping_status = '1' if self.ping_ok else '0'
            metric_collection.append('nde_ping_ok{target_hostname="' + hostname + '"} ' + str(ping_status))
            metric_collection.append('nde_ping_size{target_hostname="' + hostname + '"} ' + str(self.ping_size))
            metric_collection.append('nde_ping_time{target_hostname="' + hostname + '"} ' + str(self.ping_time))
        return metric_collection


