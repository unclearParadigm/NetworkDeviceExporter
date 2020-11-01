import configuration
from ping import Ping
from itertools import chain
from multiprocessing import Process
from hostfileparser import HostFileParser


class MetricsProvider(object):
    def __init__(self):
        pass

    def collect(self) -> str:
        hostfile_devices = list(chain.from_iterable([HostFileParser(hf).read() for hf in configuration.HostFiles]))
        all_configured_devices = hostfile_devices + configuration.CustomNetworkDevices

        # Execute
        ping_executors = [Ping(hostentry) for hostentry in all_configured_devices]
        self.execute_in_parallel([ping_executor.ping() for ping_executor in ping_executors])
        return '\n'.join(['\n'.join(ping_executor.export_prometheus_metric()) for ping_executor in ping_executors])

    @staticmethod
    def execute_in_parallel(functions) -> None:
        processes = []

        # Start processes
        for function in functions:
            p = Process(target=function)
            p.start()
            processes.append(p)

        # Join processes
        for process in processes:
            process.join()
