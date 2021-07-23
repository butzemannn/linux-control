#!/usr/bin/env python3

def read_services() -> dict:
    """
    Reads the services file in conf/services containing the service name and the corresponding container id.

    :returns: Dict containing the container name as key and the container id as value.
    """
    file_loc = "conf/services.py"
    with open(file_loc, 'r') as f:
        services = eval(f.read())

    if not isinstance(services, dict):
        raise ValueError("Could not read services file. Make sure it is a dict.")

    return services
