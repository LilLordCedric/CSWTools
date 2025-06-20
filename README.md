# Yggdrasil

Yggdrasil is a nested dictionary-like data structure for organizing hierarchical data. It provides an intuitive way to work with multi-level data structures like time-series data or any hierarchical data.

## Features

- Automatically creates nested dictionaries when accessing non-existent keys
- Supports setting values using paths (lists)
- Provides a convenient `add_fiber` method to add paths to the tree
- Available as both a pure Python implementation and a C extension for better performance

## Installation

```bash
# Build the C extension
python setup.py build_ext --inplace
```

## Usage

### Python Implementation

```python
from yggdrasil import Yggdrasil

# Create a new tree
tree = Yggdrasil()

# Add some data
tree.add_fiber([2024, 2, 8, 10])
tree.add_fiber([2024, 2, 9, 20])
tree.add_fiber([2024, 2, 9, 15])  # This will overwrite the previous value

# Access data
value = tree[2024][2][8]  # Returns 10
value = tree[2024][2][9]  # Returns 15

# Add more complex data
tree.add_fiber(["finance", "Q1", "revenue", 1000000])
tree.add_fiber(["finance", "Q2", "revenue", 1200000])
tree.add_fiber(["sales", "region1", "product1", 500])

# Access complex data
revenue_q1 = tree["finance"]["Q1"]["revenue"]  # Returns 1000000
sales_region1_product1 = tree["sales"]["region1"]["product1"]  # Returns 500

# Print the tree structure
tree.print_tree()
# Output:
# ├── finance
# │   ├── Q1
# │   │   └── revenue
# │   │       └── 1000000
# │   └── Q2
# │       └── revenue
# │           └── 1200000
# └── sales
#     └── region1
#         └── product1
#             └── 500
```

### C Extension

```python
from yggdrasil_c import Yggdrasil

# The usage is identical to the Python implementation
tree = Yggdrasil()
tree.add_fiber([2024, 2, 8, 10])
value = tree[2024][2][8]  # Returns 10

# Print the tree structure
tree.print_tree()
# Output:
# +-- 2024
#     +-- 2
#         +-- 8
#             +-- 10
```

## Loading Data from CSV

You can easily load data from a CSV file into the Yggdrasil structure:

```python
import csv
from yggdrasil_c import Yggdrasil

tree = Yggdrasil()

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        # Clean the data (remove spaces)
        row = [item.strip() for item in row]
        # Convert numeric values
        for i in range(len(row)):
            try:
                row[i] = int(row[i])
            except ValueError:
                pass
        # Add to tree
        tree.add_fiber(row)

# Now you can access the data
value = tree[2023][1][1]["Sales"]["Vacation"]  # Returns 100
```

## Running Tests

```bash
python test_yggdrasil_c.py
```

## Performance Comparison

The C extension provides better performance, especially for large datasets and deep hierarchies. Here's a simple benchmark:

```python
import time
from yggdrasil import Yggdrasil as YggdrasilPy
from yggdrasil_c import Yggdrasil as YggdrasilC

# Create test data
fibers = []
for year in range(2020, 2025):
    for month in range(1, 13):
        for day in range(1, 29):
            fibers.append([year, month, day, "value", day * month])

# Test Python implementation
start = time.time()
tree_py = YggdrasilPy()
for fiber in fibers:
    tree_py.add_fiber(fiber)
py_time = time.time() - start

# Test C implementation
start = time.time()
tree_c = YggdrasilC()
for fiber in fibers:
    tree_c.add_fiber(fiber)
c_time = time.time() - start

print(f"Python implementation: {py_time:.4f} seconds")
print(f"C implementation: {c_time:.4f} seconds")
print(f"Speedup: {py_time / c_time:.2f}x")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
