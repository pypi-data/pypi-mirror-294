#!/bin/env python

import collections.abc
from hdfstream.remote_dataset import RemoteDataset
from hdfstream.defaults import *


def unpack_object(connection, file_path, name, data, max_depth, data_size_limit):
    """
    Construct an appropriate class instance for a HDF5 object
    """
    object_type = data[b"hdf5_object"]
    if object_type == b"group":
        return RemoteGroup(connection, file_path, name, max_depth, data_size_limit, data)
    elif object_type == b"dataset":
        return RemoteDataset(connection, file_path, name, data)
    else:
        raise RuntimeError("Unrecognised object type")


class RemoteGroup(collections.abc.Mapping):
    """
    Object representing a HDF5 group in the remote file
    """
    def __init__(self, connection, file_path, name, max_depth=max_depth_default,
                 data_size_limit=data_size_limit_default, data=None):

        self.connection = connection
        self.file_path = file_path
        self.name = name
        self.max_depth = max_depth
        self.data_size_limit = data_size_limit
        self.unpacked = False

        # If msgpack data was supplied, decode it. If not, we'll wait until
        # we actually need the data before we request it from the server.
        if data is not None:
            self.unpack(data)
            
    def load(self):
        """
        Request the msgpack representation of this group from the server
        """
        if not self.unpacked:
            data = self.connection.request_object(self.file_path, self.name, self.data_size_limit, self.max_depth)
            self.unpack(data)
            
    def unpack(self, data):
        """
        Decode the msgpack representation of this group
        """
        # Store any attributes
        self.attrs = data[b"attributes"]
        for name in self.attrs:
            self.attrs[name] = self.attrs[name]

        # Create sub-objects
        self.members = {}
        if b"members" in data:
            for member_name, member_data in data[b"members"].items():
                if member_data is not None:                    
                    if self.name == "/":
                        path = self.name + member_name
                    else:
                        path = self.name + "/" + member_name
                    self.members[member_name] = unpack_object(self.connection, self.file_path, path,
                                                              member_data, self.max_depth, self.data_size_limit)
                else:
                    self.members[member_name] = None

        self.unpacked = True
                    
    def ensure_member_loaded(self, key):
        """
        Load sub-groups on access, if they were not already loaded
        """
        self.load()
        if self.members[key] is None:
            object_name = self.name+"/"+key
            self.members[key] = RemoteGroup(self.connection, self.file_path, object_name, self.max_depth, self.data_size_limit)
                                
    def __getitem__(self, key):
        """
        Return a member object identified by its name or relative path.

        If the key is a path with multiple components we use the first
        component to identify a member object to pass the rest of the path to.
        """
        self.load()
        if key != "/":
            key = key.rstrip("/")
        components = key.split("/", 1)
        if len(components) == 1:
            self.ensure_member_loaded(key)
            return self.members[key]
        else:
            self.ensure_member_loaded(components[0])
            return self[components[0]][components[1]]

    def __len__(self):
        self.load()
        return len(self.members)

    def __iter__(self):
        self.load()
        for member in self.members:
            yield member

    def __repr__(self):
        if self.unpacked:
            return f'<Remote HDF5 group "{self.name}" ({len(self.members)} members)>'
        else:
            return f'<Remote HDF5 group "{self.name}" (to be loaded on access)>'
