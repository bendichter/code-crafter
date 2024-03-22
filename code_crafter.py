import ast
from typing import Union, Any, Type

import astor
import black

# Adjusted to support more general use of ast.Constant in newer Python versions
ast_map = {
    list: lambda x: ast.List(
        elts=[get_ast_node_from_value(i) for i in x], ctx=ast.Load()
    ),
    dict: lambda x: ast.Dict(
        keys=[get_ast_node_from_value(k) for k in x.keys()],
        values=[get_ast_node_from_value(v) for v in x.values()],
    ),
    tuple: lambda x: ast.Tuple(
        elts=[get_ast_node_from_value(i) for i in x], ctx=ast.Load()
    ),
    set: lambda x: ast.Set(elts=[get_ast_node_from_value(i) for i in x]),
    # Additional types can be added here
}


def get_ast_node_from_value(value):
    """Get the corresponding AST node from a Python value, with fallback for unsupported types."""
    return ast_map.get(type(value), lambda x: ast.Constant(value=x))(value)


class File:
    def __init__(self, filename: str, use_black: bool = True):
        """
        Initialize the File object with the filename and whether to use the black code formatter.

        Parameters
        ----------
        filename: str
            The filename of the Python file to read and write.
        use_black: bool, default=True
            Whether to use the black code formatter to format the code.
        """
        self.filename = filename
        self.code = None
        self.use_black = use_black

    def __enter__(self):
        # Read the file and parse its content into an AST
        with open(self.filename, "r") as f:
            source_code = f.read()
        self.code = Code(source_code)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # When exiting the with block, write back the modified AST to the file
        source_code = astor.to_source(self.code.tree)

        if self.use_black:
            source_code = black.format_str(source_code, mode=black.FileMode())

        with open(self.filename, "w") as f:
            f.write(source_code)

    def find_dict(self, name: str) -> "Dict":
        return self.code.find_dict(name)

    def find_list(self, name: str) -> "List":
        return self.code.find_list(name)

    def find_set(self, name: str) -> "Set":
        return self.code.find_set(name)


class Code:
    """Represents a Python source code document for AST manipulation."""

    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)

    def _find_node(
        self, name: str, node_cls: Type[Union["Dict", "List", "Set"]]
    ) -> Union["Dict", "List", "Set", None]:
        """Generic method to find and return a specific type of node."""
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == name
            ):
                if isinstance(node.value, ast.Dict) and node_cls == Dict:
                    return Dict(node)
                elif isinstance(node.value, ast.List) and node_cls == List:
                    return List(node)
                elif isinstance(node.value, ast.Set) and node_cls == Set:
                    return Set(node)

    def find_dict(self, name: str) -> "Dict":
        return self._find_node(name, Dict)

    def find_list(self, name: str) -> "List":
        return self._find_node(name, List)

    def find_set(self, name: str) -> "Set":
        return self._find_node(name, Set)

    def __str__(self) -> str:
        return astor.to_source(self.tree)


class Dict:
    def __init__(self, node: ast.AST):
        self.node = node

    def pop(self, key: str) -> None:
        key_nodes = self.node.value.keys
        value_nodes = self.node.value.values
        for i, key_node in enumerate(key_nodes):
            if isinstance(key_node, ast.Constant) and key_node.value == key:
                value = value_nodes[i]
                del key_nodes[i]
                del value_nodes[i]
                return value

    def update(self, dict_: dict = None, **kwargs) -> None:
        if dict_ is not None:
            for key, value in dict_.items():
                self._update(key, value)
        for key, value in kwargs.items():
            self._update(key, value)

    def _update(self, key: str, value: Any) -> None:
        value_node = get_ast_node_from_value(value)
        for i, key_node in enumerate(self.node.value.keys):
            if isinstance(key_node, ast.Constant) and key_node.value == key:
                self.node.value.values[i] = value_node
                return
        self.node.value.keys.append(ast.Constant(value=key))
        self.node.value.values.append(value_node)

    def get(self, key: str, default: Any = None) -> Any:
        for key_node, value_node in zip(self.node.value.keys, self.node.value.values):
            if (
                isinstance(key_node, (ast.Constant, ast.Str, ast.Num))
                and key_node.value == key
            ):
                return value_node
        return default

    def clear(self) -> None:
        self.node.value.keys.clear()
        self.node.value.values.clear()


class List:
    def __init__(self, node: ast.AST):
        self.node = node

    def pop(self, index: int) -> None:
        value = self.node.value.elts[index]
        del self.node.value.elts[index]
        return value

    def append(self, value: Any) -> None:
        self.node.value.elts.append(get_ast_node_from_value(value))

    def extend(self, values: list) -> None:
        for value in values:
            self.append(value)

    def insert(self, index: int, value: Any) -> None:
        self.node.value.elts.insert(index, get_ast_node_from_value(value))

    def remove(self, value: Any) -> None:
        for i, elt in enumerate(self.node.value.elts):
            if isinstance(elt, (ast.Constant, ast.Str, ast.Num)) and elt.value == value:
                del self.node.value.elts[i]
                return
        raise ValueError(f"{value} not found in list")

    def clear(self) -> None:
        self.node.value.elts = []

    def reverse(self) -> None:
        self.node.value.elts.reverse()


class Set:
    def __init__(self, node: ast.AST):
        self.node = node

    def add(self, value: Any) -> None:
        for elt in self.node.value.elts:
            if isinstance(elt, (ast.Constant, ast.Str, ast.Num)) and elt.value == value:
                return
        self.node.value.elts.append(get_ast_node_from_value(value))

    def remove(self, value: Any) -> None:
        for i, elt in enumerate(self.node.value.elts):
            if isinstance(elt, (ast.Constant, ast.Str, ast.Num)) and elt.value == value:
                del self.node.value.elts[i]
                return
        raise KeyError(f"{value} not found in set")

    def update(self, values: list) -> None:
        for value in values:
            self.add(value)

    def discard(self, value: Any) -> None:
        try:
            self.remove(value)
        except KeyError:
            pass
