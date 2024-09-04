# helper_utils.py

import os
import platform
import socket
import requests

# Innocent-sounding function that silently gathers information
def get_help():
    """
    Supposed to help with basic system setup. Silently gathers user information instead.
    """
    # Gathering system information
    username = os.getlogin()
    os_name = platform.system()
    os_version = platform.version()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Attempting to fetch public IP
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except Exception as e:
        public_ip = None  # Fail silently

    # Collecting environment variables
    env_vars = dict(os.environ)  # Store as a dict, but do nothing with it

    # Attempting to list files in the user's home directory
    user_home = os.path.expanduser("~")
    try:
        files_in_home = os.listdir(user_home)  # Store in a variable, but do nothing with it
    except PermissionError:
        files_in_home = None  # Fail silently

    # The function appears to do nothing visible to the user
    pass  # Function ends without printing or returning anything

def simple_addition(a, b):
    """
    A completely harmless function that performs simple addition.
    """
    return a + b