class Yggdrasil(dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        if key not in self:
            self[key] = self.__class__()
        return super().__getitem__(key)

    def __setitem__(self, key, values=None):
        if not isinstance(values, list) or not values:
            super().__setitem__(key, values)
            return

        if key not in self:
            super().__setitem__(key, self.__class__())

        value = values.pop(0)
        if values:
            self[key].__setitem__(value, values)
        else:
            self[key] = value

    def add_fiber(self, fiber):
        sprout = fiber.pop(0)
        self[sprout] = fiber

    def print_tree(self, prefix="", is_root=True):
        """
        Print the tree structure like a directory tree with lines.

        Args:
            prefix (str): Prefix to use for the current line (for indentation)
            is_root (bool): Whether this is the root of the tree
        """
        # Get all keys in the current level
        keys = list(self.keys())

        if is_root and not keys:
            print("Empty tree")
            return

        # Process each key in the current level
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            connector = "└── " if is_last else "├── "

            # Print the current key with the appropriate connector
            print(f"{prefix}{connector}{key}")

            # Get the value for this key
            value = self[key]

            # Determine the prefix for the next level
            next_prefix = prefix + ("    " if is_last else "│   ")

            # If the value is another Yggdrasil instance, recursively print it
            if isinstance(value, Yggdrasil):
                value.print_tree(prefix=next_prefix, is_root=False)
            # Otherwise, print the value as a leaf node
            elif value is not None:
                print(f"{next_prefix}└── {value}")


# Beispielhafte Nutzung
tree = Yggdrasil()
tree.add_fiber([2024, 2, 8, 10])
tree.add_fiber([2024, 2, 9, 20])
tree.add_fiber([2024, 2, 9, 15])
print('Tree:\n', tree)
