"""
This script provides functionality to manage global variables stored in a JSON file.

It includes functions to:

- Set and get global variables for a specific user path.
- Read from and write to a JSON file (`glovar.json`) that stores global variables.
- Configure the path for the JSON file and the user-specific path.

Functions:
- file(file_path): Set the path for the current user context.
- data(directory): Set the path for the 'glovar.json' file.
- set(name, value=None): Set a global variable for the current user path.
- get(name): Retrieve a global variable for the current user path.
- remove(name): Remove a global variable for the current user path.
- peek(): Peek at the current global variables for the current user path.
- read_globals(): Read and return the global variables from the JSON file.
"""


import json
import os
import sys

var_path = os.path.normpath(os.path.abspath(sys.argv[0])).replace(os.sep, "/") # default is caller frame path
def var_file(file_path=os.getcwd()):
    """
    Set the path to the file to which global variables are bound. It is not necessary
    to use an existing file, you can use any name, for example, "globals", "custom_globals", "my_vars", etc.

    Args:
        file_path (str): The path to the file or custom name. Defaults to the directory of the caller frame.
    """
    global var_path
    var_path = os.path.normpath(file_path).replace(os.sep, "/").lower()

data_path = os.path.join(os.path.dirname(__file__), "glovar.json").lower() # default is package directory
def data(directory=os.getcwd()):
    """
    Specifies the name of the directory where the json file is stored.

    Args:
        directory (str): The directory to use for the 'glovar.json' file. Defaults to the directory of the caller frame.
    """
    global data_path
    data_path = os.path.join(os.path.normpath(directory).replace(os.sep, "/"), "glovar.json").lower()

def read_globals() -> dict:
    """
    Read and return the contents of the 'glovar.json' file as a dictionary.\n
    Use the 'data' function to specify the name of the directory where the json file is stored.\n
    Use the 'var_file' function to specify the path for the file to which global variables are bound.

    Returns:
        dict: The contents of 'glovar.json', or an empty dictionary if the file does not exist.
    """
    if not os.path.exists(data_path):
        return {}
    with open(data_path, "r") as f:
        return json.load(f)

def write_globals(data):
    with open(data_path, "w") as f:
        json.dump(data, f)

def set(name, value=None):
    """
    Set a global variable that link to var_file path. Use the 'var_file' function to specify the name of the file.\n
    A global variable store in the 'glovar.json' file in package directory.\n
    Use the 'data' function to specify the name of the directory where the json file is stored.

    Args:
        name (str): The name of the global variable.
        value: The value to set for the global variable. Defaults to None.
    """
    data = read_globals()
    globals = data.get(var_path, {})
    globals[name] = value
    data[var_path] = globals
    write_globals(data)

def get(name):
    """
    Retrieve a global variable from the 'glovar.json' file for the current user path.\n
    Use the 'var_file' function to specify the path for the current user context.\n
    A global variable is stored in the 'glovar.json' file in the directory specified by the 'data' function. Default is package directory

    Args:
        name (str): The name of the global variable to retrieve.

    Returns:
        The value of the global variable, or None if the variable does not exist.
    """
    data = read_globals()
    globals = data.get(var_path, {})
    return globals.get(name)

def remove(name):
    """
    Remove a global variable from the 'glovar.json' file for the current user path.\n
    Use the 'var_file' function to specify the path for the current user context.\n
    A global variable is stored in the 'glovar.json' file in the directory specified by the 'data' function. Default is package directory

    Args:
        name (str): The name of the global variable to remove.

    Returns:
        dict: The updated dictionary of global variables for the current user path.
    """
    data = read_globals()
    globals = data.get(var_path, {})
    globals.pop(name, None)
    data[var_path] = globals
    write_globals(data)
    return globals

def peek():
    """
    Peek at the current global variables for the current user path.\n
    Use the 'file' function to specify the path for the current user context.\n
    Global variables are stored in the 'glovar.json' file in the directory specified by the 'data' function. Default is package directory

    Returns:
        dict: The dictionary of global variables for the current user path.
    """
    data = read_globals()
    return data.get(var_path, {})
