from yggdrasil import Yggdrasil

def test_empty_tree():
    print("Testing empty tree:")
    tree = Yggdrasil()
    tree.print_tree()
    print()

def test_simple_tree():
    print("Testing simple tree:")
    tree = Yggdrasil()
    tree.add_fiber([2024, 2, 8, 10])
    tree.print_tree()
    print()

def test_multiple_fibers():
    print("Testing multiple fibers:")
    tree = Yggdrasil()
    tree.add_fiber([2024, 2, 8, 10])
    tree.add_fiber([2024, 2, 9, 20])
    tree.add_fiber([2024, 2, 9, 15])  # This will overwrite the previous value
    tree.print_tree()
    print()

def test_complex_tree():
    print("Testing complex tree:")
    tree = Yggdrasil()
    tree.add_fiber(["finance", "Q1", "revenue", 1000000])
    tree.add_fiber(["finance", "Q2", "revenue", 1200000])
    tree.add_fiber(["finance", "Q3", "revenue", 1300000])
    tree.add_fiber(["finance", "Q4", "revenue", 1500000])
    tree.add_fiber(["sales", "region1", "product1", 500])
    tree.add_fiber(["sales", "region1", "product2", 300])
    tree.add_fiber(["sales", "region2", "product1", 400])
    tree.add_fiber(["sales", "region2", "product2", 200])
    tree.add_fiber(["marketing", "online", "ads", 50000])
    tree.add_fiber(["marketing", "offline", "billboards", 75000])
    tree.print_tree()
    print()

if __name__ == "__main__":
    test_empty_tree()
    test_simple_tree()
    test_multiple_fibers()
    test_complex_tree()