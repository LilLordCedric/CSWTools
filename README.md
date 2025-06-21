# Yggdrasil Tree

A flexible tree-like data structure for Python that extends the built-in dictionary with automatic creation of nested nodes and customizable leaf node behaviors.

## Installation

You can install the package via pip:

```bash
pip install csw
```

## Features

- **Automatic Node Creation**: Accessing non-existent keys automatically creates nested nodes
- **Customizable Leaf Behavior**: Configure how duplicate leaf nodes are handled:
  - `overwrite`: Replace existing value (default)
  - `append`: Append to existing value if possible
  - `add`: Add to existing value if both are numeric
  - `subtract`: Subtract new value from existing value if both are numeric
  - `multiply`: Multiply with existing value if both are numeric
  - `divide`: Divide existing value by new value if both are numeric
  - Custom function: Provide your own function to handle value merging
- **Tree Visualization**: Built-in method to print the tree structure
- **Intuitive API**: Uses familiar dictionary syntax with enhanced tree functionality

## Usage Examples

### Basic Usage

```python
from csw import Yggdrasil

# Create a new tree
tree = Yggdrasil()

# Add values using dictionary syntax
tree['animals']['mammals']['cats'] = 'Meow'
tree['animals']['mammals']['dogs'] = 'Woof'
tree['animals']['birds']['parrot'] = 'Squawk'

# Print the tree structure
tree.print_tree()
```

Output:
```
├── animals
    ├── mammals
    │   ├── cats
    │   │   └── Meow
    │   └── dogs
    │       └── Woof
    └── birds
        └── parrot
            └── Squawk
```

### Using Different Leaf Behaviors

```python
# Create a tree that adds numeric values
add_tree = Yggdrasil(leaf_behavior='add')

# Add values
add_tree['scores']['math'] = 90
add_tree['scores']['math'] = 5  # Will add to existing value

print(add_tree['scores']['math'])  # Output: 95

# Create a tree with custom behavior
def custom_merge(existing, new):
    if isinstance(existing, list):
        return existing + [new]
    else:
        return [existing, new]

list_tree = Yggdrasil(leaf_behavior=custom_merge)
list_tree['data'] = 'first'
list_tree['data'] = 'second'
list_tree['data'] = 'third'

print(list_tree['data'])  # Output: ['first', 'second', 'third']
```

### Adding Branches with add_fiber

```python
tree = Yggdrasil()
tree.add_fiber(['config', 'database', 'username', 'admin'])
tree.add_fiber(['config', 'database', 'password', 'secure123'])
tree.add_fiber(['config', 'server', 'port', 8080])

tree.print_tree()
```

Output:
```
└── config
    ├── database
    │   ├── username
    │   │   └── admin
    │   └── password
    │       └── secure123
    └── server
        └── port
            └── 8080
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Cedric Sascha Wagner <cedric.sascha.wagner@outlook.de>