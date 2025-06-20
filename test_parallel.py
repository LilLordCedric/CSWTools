import sys
import os
import time

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath('.'))

try:
    from yggdrasil_c import Yggdrasil
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you've built the C extension by running 'python setup.py build_ext --inplace'")
    sys.exit(1)

# Create a large number of fibers to test parallel processing
fibers = []
for i in range(10000):
    fibers.append([f"category{i % 10}", f"subcategory{i % 20}", f"item{i}", i])

# Test sequential processing
tree_seq = Yggdrasil()
start_time = time.time()
for fiber in fibers:
    tree_seq.add_fiber(fiber)
seq_time = time.time() - start_time
print(f"Sequential processing time: {seq_time:.4f} seconds")

# Test parallel processing with default number of threads
tree_par = Yggdrasil()
start_time = time.time()
tree_par.add_fibers_parallel(fibers)
par_time = time.time() - start_time
print(f"Parallel processing time (default threads): {par_time:.4f} seconds")

# Test parallel processing with explicit number of threads
tree_par2 = Yggdrasil()
start_time = time.time()
tree_par2.add_fibers_parallel(fibers, 4)  # Use 4 threads
par_time2 = time.time() - start_time
print(f"Parallel processing time (4 threads): {par_time2:.4f} seconds")

# Verify that the trees are identical
for i in range(10):
    for j in range(20):
        for k in range(10):
            key1 = f"category{i}"
            key2 = f"subcategory{j}"
            key3 = f"item{i*20*10 + j*10 + k}"
            value = i*20*10 + j*10 + k
            
            # Check if the values match
            if tree_seq[key1][key2][key3] != value:
                print(f"Error: Sequential tree value mismatch at {key1}/{key2}/{key3}")
                sys.exit(1)
            
            if tree_par[key1][key2][key3] != value:
                print(f"Error: Parallel tree value mismatch at {key1}/{key2}/{key3}")
                sys.exit(1)
            
            if tree_par2[key1][key2][key3] != value:
                print(f"Error: Parallel tree (4 threads) value mismatch at {key1}/{key2}/{key3}")
                sys.exit(1)

print("All values match! Parallel processing is working correctly.")
print(f"Speedup (default threads): {seq_time / par_time:.2f}x")
print(f"Speedup (4 threads): {seq_time / par_time2:.2f}x")