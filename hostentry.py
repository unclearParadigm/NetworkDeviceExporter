from typing import List


class HostEntry(object):
    def __init__(self, ip: str, hostnames: List[str]) -> None:
        self.ip = str(ip)
        self.hostnames = list(hostnames)

    def __eq__(self, other):
        return self.ip.strip().lower() == other.ip.strip().lower()


def parse_from_hostfile_row(row: str) -> (bool, HostEntry):
    if row is None:
        return False, 'No row provided'

    split_row = (' '.join(row.strip().replace('\t', ' ').split(' '))).split(' ')

    if len(split_row) < 2:
        return False, 'The row must at least contain 2 columns (IP and Hostname)'

    if '#' in split_row:
        return False, 'Provided row seems to be (or contain) a comment'

    ip = split_row[0]
    hostnames = [hn for hn in split_row[1:] if hn != ""]
    if len(hostnames) == 0:
        return False, 'There is not enough entries containing Hostnames'

    return True, HostEntry(ip, hostnames)
