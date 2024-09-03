"""
Curation operations in individual directories.
"""

import json
import os
from typing import Dict

from .dir_data import DirMetadata, FileMetadata

def read_dir_json(path) -> Dict:
    print('read_dir_json')
    try:
        with open(os.path.join(path, '.json'), 'r', encoding='utf-8') as f_in:
            return json.load(f_in)
    except Exception:
        return {}


def write_dir_json(path: str, dir_metadata: DirMetadata):
    """write the directory metedata as JSON

    Args:
        path (str): the path to the directory's .json file
        dir_metadata (FileMetadata): the directory metadata
    """
    print(f'write_dir_json:  {path}')
    with open(os.path.join(path, '.json'), 'w', encoding='utf-8') as f_out:
        json.dump(dir_metadata.to_json(), f_out)


def parse_json_file(content: Dict) -> DirMetadata:
    """convert whatever version this file is to the latest version.

    Args:
        content (Dict): the content of a dir .json file
    """
    result: DirMetadata = DirMetadata()
    
    if 'version' not in content:
        print('Version 0')
        
        process_files_section(content, result)
        return result
    elif isinstance(content['version'], int):
        print(f'Version {content["version"]}')
        
        if content['version'] == 1:
            process_files_section(content['files'], result)
            
        return result
            
    print('Version is bogus')  
    
def process_files_section(files:Dict, metadata: DirMetadata) -> None:
    """process the "files" section of the file

    Args:
        files (Dict): the files dict of the .json file
        result (DirMetadata): the dir metadata to add the files to
    """
    for filename, details in files.items():
        metadata.add_file(filename, FileMetadata(details['date'], details['sha256'], details['size']))
