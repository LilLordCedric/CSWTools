import unittest
import sys
import os

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath('.'))

try:
    from yggdrasil_c import Yggdrasil as YggdrasilC
    from yggdrasil import Yggdrasil as YggdrasilPy
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you've built the C extension by running 'python setup.py build_ext --inplace'")
    sys.exit(1)


class TestYggdrasilC(unittest.TestCase):
    def test_init(self):
        """Test that the C extension can be initialized"""
        tree = YggdrasilC()
        self.assertIsInstance(tree, YggdrasilC)
        
    def test_getitem_creates_nested_dict(self):
        """Test that __getitem__ creates a nested dictionary when accessing a non-existent key"""
        tree = YggdrasilC()
        subtree = tree[2024]
        self.assertIsInstance(subtree, YggdrasilC)
        
    def test_setitem_simple_value(self):
        """Test setting a simple value"""
        tree = YggdrasilC()
        tree["key"] = "value"
        self.assertEqual(tree["key"], "value")
        
    def test_setitem_list_value(self):
        """Test setting a list value which should create a nested structure"""
        tree = YggdrasilC()
        tree["root"] = [1, 2, 3]
        
        # Should create a nested structure: tree["root"][1][2] = 3
        self.assertIsInstance(tree["root"], YggdrasilC)
        self.assertIsInstance(tree["root"][1], YggdrasilC)
        self.assertEqual(tree["root"][1][2], 3)
        
    def test_add_fiber(self):
        """Test the add_fiber method"""
        tree = YggdrasilC()
        tree.add_fiber([2024, 2, 8, 10])
        
        # Should create a nested structure: tree[2024][2][8] = 10
        self.assertEqual(tree[2024][2][8], 10)
        
    def test_multiple_fibers(self):
        """Test adding multiple fibers"""
        tree = YggdrasilC()
        tree.add_fiber([2024, 2, 8, 10])
        tree.add_fiber([2024, 2, 9, 20])
        tree.add_fiber([2024, 2, 9, 15])
        
        # Check the values
        self.assertEqual(tree[2024][2][8], 10)
        self.assertEqual(tree[2024][2][9], 15)  # Last value for the same path
        
    def test_comparison_with_python_implementation(self):
        """Test that the C extension behaves the same as the Python implementation"""
        tree_c = YggdrasilC()
        tree_py = YggdrasilPy()
        
        # Add the same fibers to both trees
        fibers = [
            [2024, 2, 8, 10],
            [2024, 2, 9, 20],
            [2024, 2, 9, 15],
            ["finance", "Q1", "revenue", 1000000],
            ["finance", "Q2", "revenue", 1200000],
            ["sales", "region1", "product1", 500],
            ["sales", "region1", "product2", 300],
            ["sales", "region2", "product1", 400]
        ]
        
        for fiber in fibers:
            tree_c.add_fiber(fiber)
            tree_py.add_fiber(fiber)
        
        # Check some values
        self.assertEqual(tree_c[2024][2][8], tree_py[2024][2][8])
        self.assertEqual(tree_c[2024][2][9], tree_py[2024][2][9])
        self.assertEqual(tree_c["finance"]["Q1"]["revenue"], tree_py["finance"]["Q1"]["revenue"])
        self.assertEqual(tree_c["sales"]["region1"]["product1"], tree_py["sales"]["region1"]["product1"])
        
    def test_load_from_csv(self):
        """Test loading data from a CSV file"""
        import csv
        
        tree_c = YggdrasilC()
        
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
                tree_c.add_fiber(row)
        
        # Check some values
        self.assertEqual(tree_c[2023][1][1]["Sales"]["Vacation"], 100)
        self.assertEqual(tree_c[2024][8][4]["IT"]["Remote"], 400)
        self.assertEqual(tree_c[2025][7][17]["Logistics"]["Sick Leave"], 1000)


if __name__ == '__main__':
    unittest.main()