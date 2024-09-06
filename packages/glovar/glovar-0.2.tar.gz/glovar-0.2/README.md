# Global Variable Management Script

This Python script provides functionality to manage global variables stored in a JSON file. The script allows you to set, get, remove, and view global variables associated with a specific file path. The global variables are stored in a file named `glovar.json`.

## Overview

The script includes functions to:

- Set and get global variables.
- Configure the path for the JSON file and the variables path.
- Read from and write to a JSON file (`glovar.json`) that stores global variables.

## Installation

`pip install glovar`

## Functions

### `file(file_path)`

Set the path for the current user context.

**Args:**

- `file_path` (str): The path to the file.

### `data(directory=os.path.dirname(__file__))`

Set the path for the `glovar.json` file.

**Args:**

- `directory` (str): The directory where the `glovar.json` file is located. Defaults to the directory of the current script.

### `read_globals()`

Read and return the contents of the `glovar.json` file as a dictionary.

**Returns:**

- `dict`: The contents of `glovar.json`, or an empty dictionary if the file does not exist.

### `set(name, value=None)`

Set a global variable in the `glovar.json` file for the current user path.

**Args:**

- `name` (str): The name of the global variable.
- `value`: The value to set for the global variable. Defaults to `None`.

### `get(name)`

Retrieve a global variable from the `glovar.json` file for the current user path.

**Args:**

- `name` (str): The name of the global variable to retrieve.

**Returns:**

- The value of the global variable, or `None` if the variable does not exist.

### `remove(name)`

Remove a global variable from the `glovar.json` file for the current user path.

**Args:**

- `name` (str): The name of the global variable to remove.

**Returns:**

- `dict`: The updated dictionary of global variables for the current user path.

### `peek()`

Peek at the current global variables for the current user path.

**Returns:**

- `dict`: The dictionary of global variables for the current user path.

## Usage

1. **Link variables to file:**

   ```python
   glovar.file("path/to/your/file")
   ```

   do not execute this function to link to an executable file.

2. **Set the JSON file path:**

   ```python
   glovar.data("path/to/your/directory")
   ```

   do not execute this function to link to an executable file's directory.

3. **Set a global variable:**

   ```python
   glovar.set("variable_name", "value")
   ```

4. **Get a global variable:**

   ```python
   value = glovar.get("variable_name")
   ```

5. **Remove a global variable:**

   ```python
   globals = glovar.remove("variable_name")
   ```

6. **Peek at current global variables:**
   ```python
   current_globals = glovar.peek()
   ```

## Examples

### Example 1: Setting and Getting a Global Variable without change file and data

Example1.py

```python
import glovar

glovar.set("my_variable", "my_value")

value = glovar.get("my_variable")
print("Value:", value)  # Output: Value: my_value
```

This script create glovar.json in same directory as "Example1.py" file

### Example 2: link file variables to other file

Example2.py

```python
import glovar

glovar.file("full/path/to/Example1.py")

value = glovar.get("my_variable")
print("Value:", value) # Output: Value: my_value
```

Due to link Example1.py file to Example2.py using `glovar.file("full/path/to/Example1.py")` we can see my_variable from Example1.py
