import json
import inspect
import os

globals_file = "globals.json"

def get_caller_filename():
    stack = inspect.stack()
    caller_frame = stack[1]
    return os.path.abspath(caller_frame.filename).replace("\\", "/")

def read_globals():
    if not os.path.exists(globals_file):
        return {}
    with open(globals_file, "r") as f:
        return json.load(f)

def write_globals(data):
    with open(globals_file, "w") as f:
        json.dump(data, f)

def set(name, value=None):
    caller_filename = get_caller_filename()
    data = read_globals()
    globals = data.get(caller_filename, {})
    globals[name] = value
    data[caller_filename] = globals
    write_globals(data)

def get(name):
    caller_filename = get_caller_filename()
    data = read_globals()
    globals = data.get(caller_filename, {})
    return globals.get(name)

def remove(name):
    caller_filename = get_caller_filename()
    data = read_globals()
    globals = data.get(caller_filename, {})
    globals.pop(name, None)
    data[caller_filename] = globals
    write_globals(data)
    return globals

def peek():
    caller_filename = get_caller_filename()
    data = read_globals()
    return data.get(caller_filename, {})
