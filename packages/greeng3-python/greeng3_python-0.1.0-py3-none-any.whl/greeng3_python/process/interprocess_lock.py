"""
Interprocess locking
"""

import fcntl


class Lock(object):
    def __init__(self, pathname: str):
        """
        Create an interprocess lock object around a pathname in the filesystem.

        Args:
            pathname (str): pathname to the file we will lock - it will be created if it doesn't already exist
        """
        self._pathname = pathname
        self._file_handle = open(self._pathname, 'w')

    def acquire(self):
        """
        Get an exclusive lock on the file.
        """
        fcntl.flock(self._file_handle, fcntl.LOCK_EX)

    def release(self):
        """
        Release the exclusive lock on the file.
        """
        fcntl.flock(self._file_handle, fcntl.LOCK_UN)

    def __del__(self):
        """
        Clean up when we are destroyed.
        """
        self._file_handle.close()
