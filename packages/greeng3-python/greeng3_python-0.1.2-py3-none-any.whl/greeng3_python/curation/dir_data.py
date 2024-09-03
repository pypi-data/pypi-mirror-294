"""
Data Structures for curation of a single directory
"""

from collections import defaultdict
from typing import Dict, List

CURRENT_VERSION: int = 1

class FileMetadata:
    def __init__(self, date: float, sha256: str, size: int) -> None:
        """a representation of the metadata for a file

        Args:
            date (float): the last modify date in seconds since epoch
            sha256 (str): the file's hash
            size (int): the file's size in bytes
        """
        self.date: float = date
        self.sha256: str = sha256
        self.size: int = size
        
    def to_json(self) -> Dict:
        """return a json-suitable representation of a file's metadata
        
            Returns:
                dict: with the metadata
        """
        return {
            'date': self.date,
            'sha256': self.sha256,
            'size': self.size,
        }
        
class DirMetadata:
    def __init__(self) -> None:
        # files[filename] = FileMetadata
        self.files: Dict[str, FileMetadata] = {}
        
        # groups of files with the same size/hash
        self.groups: Dict[str, List[str]] = defaultdict(list)
        
    def to_json(self) -> Dict:
        """return a json-suitable representation of the directory
        
            Returns:
                dict: with the metadata
        """
        return {
            'version': CURRENT_VERSION,
            'files': {
                filename: metadata.to_json()
                for filename, metadata in self.files.items()
            },
        }
        
    def add_file(self, filename: str, metadata: FileMetadata) -> None:
        """add information for a single file in the directory

        Args:
            filename (str): the filename
            metadata (FileMetadata): the file's metadata
        """

        self.files[filename] = metadata
        
        group: str = f'{metadata.sha256}_{metadata.size}'
        self.groups[group].append(filename)
