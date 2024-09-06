# glovar

This package allows you to manage global variables stored in a JSON file with context to the calling file.

## Installation

`pip install json_globals`

## Usage

```python
import glovar

glovar.set("key", "value")
value = glovar.get("key")
glovar.remove("key")
all_globals = glovar.peek()
```
