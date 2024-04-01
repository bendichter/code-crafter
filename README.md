# Code Crafter

[![codecov](https://codecov.io/gh/bendichter/code-crafter/graph/badge.svg?token=RT0OSBH124)](https://codecov.io/gh/bendichter/code-crafter)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/code-crafter)

Code Crafter is a Python library designed for manipulating Python source code through Abstract Syntax Tree (AST) transformations. This tool simplifies the process of programmatically editing Python code, allowing developers to find and modify specific data structures such as lists, dictionaries, and sets within their code. Whether you're building code generation tools, refactoring code, or creating dynamic Python scripts, Code Crafter offers a clean and intuitive API to achieve your goals.

## Features

- **Easy Navigation**: Navigate through your Python code's AST with ease, thanks to intuitive methods like `find_list`, `find_dict`, and `find_set`.
- **In-Place Modification**: Directly modify lists, dictionaries, and sets within your source code through simple method calls.
- **Automatic File Handling**: Use the `File` context manager to automatically read, modify, and write back changes to your Python files.
- **Support for Common Data Structures**: First-class support for manipulating lists, dictionaries, and sets, with potential for future expansion.

## Installation

Install Code Crafter using pip:

```bash
pip install code-crafter
```

## Basic Usage

Starting with a file named `my_file.py` that contains the following code:

```python
# my_file.py

my_list = [1, 2, 3]
my_dict = {"key1": "value1", "key2": "value2"}
my_set = {1, 2, 3}
```

You can use `code_crafter` to append an element to a list, add a new key-value pair to a dictionary, and add a new element to a set:

```python

import code_crafter as cc

# Automatically apply changes to 'my_file.py'
with cc.File("my_file.py") as file:
    # Append an element to a list named 'my_list'
    file.find_list("my_list").append(4)
    # Add a new key-value pair to a dictionary named 'my_dict'
    file.find_dict("my_dict").update(my_new_key="my_new_value")
    # Add a new element to a set named 'my_set'
    file.find_set("my_set").add(42)
```

After running the above code, the file `my_file.py` will be updated to:

```python
# my_file.py
my_list = [1, 2, 3, 4]
my_dict = {"key1": "value1", "key2": "value2", "my_new_key": "my_new_value"}
my_set = {1, 2, 3, 42}
```

Most of the methods available for `cc.List`, `cc.Dict`, and `cc.Set` are similar to the methods available for the built-in Python data structures. For example,

`cc.List` supports the following methods:
* append
* extend
* insert
* remove
* pop
* clear
* reverse

`cc.Dict` supports the following methods:
* update
* clear
* pop
* get

`cc.Set` supports the following methods:
* add
* remove
* update
* discard

These transformations also work for code that contains calls to `list()`, `dict()`, and `set()` constructors.

## Contributing

Contributions to Code Crafter are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to open an issue or a pull request on our GitHub repository.

## License

Code Crafter is released under the MIT License. See the LICENSE file for more details.
