from yggdrasil import Yggdrasil as YggdrasilPy
from yggdrasil_c import Yggdrasil as YggdrasilC

def test_empty_tree():
    print("Testing empty tree:")
    print("Python implementation:")
    tree_py = YggdrasilPy()
    tree_py.print_tree()
    print()
    
    print("C implementation:")
    tree_c = YggdrasilC()
    tree_c.print_tree()
    print()

def test_simple_tree():
    print("Testing simple tree:")
    print("Python implementation:")
    tree_py = YggdrasilPy()
    tree_py.add_fiber([2024, 2, 8, 10])
    tree_py.print_tree()
    print()
    
    print("C implementation:")
    tree_c = YggdrasilC()
    tree_c.add_fiber([2024, 2, 8, 10])
    tree_c.print_tree()
    print()

def test_multiple_fibers():
    print("Testing multiple fibers:")
    print("Python implementation:")
    tree_py = YggdrasilPy()
    tree_py.add_fiber([2024, 2, 8, 10])
    tree_py.add_fiber([2024, 2, 9, 20])
    tree_py.add_fiber([2024, 2, 9, 15])  # This will overwrite the previous value
    tree_py.print_tree()
    print()
    
    print("C implementation:")
    tree_c = YggdrasilC()
    tree_c.add_fiber([2024, 2, 8, 10])
    tree_c.add_fiber([2024, 2, 9, 20])
    tree_c.add_fiber([2024, 2, 9, 15])  # This will overwrite the previous value
    tree_c.print_tree()
    print()

def test_complex_tree():
    print("Testing complex tree:")
    print("Python implementation:")
    tree_py = YggdrasilPy()
    tree_py.add_fiber(["finance", "Q1", "revenue", 1000000])
    tree_py.add_fiber(["finance", "Q2", "revenue", 1200000])
    tree_py.add_fiber(["finance", "Q3", "revenue", 1300000])
    tree_py.add_fiber(["finance", "Q4", "revenue", 1500000])
    tree_py.add_fiber(["sales", "region1", "product1", 500])
    tree_py.add_fiber(["sales", "region1", "product2", 300])
    tree_py.add_fiber(["sales", "region2", "product1", 400])
    tree_py.add_fiber(["sales", "region2", "product2", 200])
    tree_py.add_fiber(["marketing", "online", "ads", 50000])
    tree_py.add_fiber(["marketing", "offline", "billboards", 75000])
    tree_py.print_tree()
    print()
    
    print("C implementation:")
    tree_c = YggdrasilC()
    tree_c.add_fiber(["finance", "Q1", "revenue", 1000000])
    tree_c.add_fiber(["finance", "Q2", "revenue", 1200000])
    tree_c.add_fiber(["finance", "Q3", "revenue", 1300000])
    tree_c.add_fiber(["finance", "Q4", "revenue", 1500000])
    tree_c.add_fiber(["sales", "region1", "product1", 500])
    tree_c.add_fiber(["sales", "region1", "product2", 300])
    tree_c.add_fiber(["sales", "region2", "product1", 400])
    tree_c.add_fiber(["sales", "region2", "product2", 200])
    tree_c.add_fiber(["marketing", "online", "ads", 50000])
    tree_c.add_fiber(["marketing", "offline", "billboards", 75000])
    tree_c.print_tree()
    print()

if __name__ == "__main__":
    test_empty_tree()
    test_simple_tree()
    test_multiple_fibers()
    test_complex_tree()