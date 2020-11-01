import os

from typing import List

from hostentry import HostEntry
from hostentry import parse_from_hostfile_row


class HostFileParser(object):
    def __init__(self, filepath: str) -> None:
        self._filepath = str(filepath)

    def read(self) -> List[HostEntry]:
        is_file_parsed, content = self._try_read_hostfile()
        if not is_file_parsed:
            return []

        processable_hostentries = []
        for row in content.split('\n'):
            is_row_parsed, parsed_hostentry = parse_from_hostfile_row(row)
            if is_row_parsed:
                processable_hostentries.append(parsed_hostentry)

        return processable_hostentries

    def _try_read_hostfile(self) -> (bool, str):
        if not os.path.exists(self._filepath):
            return False, 'The provided file or path to file does not exist.'

        try:
            with open(self._filepath, 'r') as hostfile:
                file_content = hostfile.read()
            return True, file_content
        except Exception as exc:
            return False, str(exc)
