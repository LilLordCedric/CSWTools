import time
import sys
import os

import yggdrasil

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath('.'))

try:
    from yggdrasil import Yggdrasil as YggdrasilPy
    from yggdrasil_c import Yggdrasil as YggdrasilC
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you've built the C extension by running 'python setup.py build_ext --inplace'")
    sys.exit(1)


def run_benchmark(num_years=100, num_months=12, num_days=30, repeat=50):
    """Run a benchmark comparing Python and C implementations of Yggdrasil."""
    print(f"Generating test data for {num_years} years, {num_months} months, {num_days} days...")

    # Create test data
    fibers = []
    for year in range(2020, 2020 + num_years):
        for month in range(1, num_months + 1):
            for day in range(1, num_days + 1):
                fibers.append([year, month, day, "value", day * month])



    total_fibers = len(fibers)
    print(f"Generated {total_fibers} fibers.")

    # Test Python implementation
    print(f"\nTesting Python implementation (repeating {repeat} times)...")
    py_times = []
    for i in range(repeat):
        start = time.time()
        tree_py = YggdrasilPy()
        # Create a deep copy of each fiber to avoid modifying the original
        for fiber in fibers:
            # Create a copy of the fiber
            fiber_copy = fiber.copy()
            tree_py.add_fiber(fiber_copy)
        py_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {py_times[-1]:.4f} seconds")

    py_time = sum(py_times) / len(py_times)
    print(f"Average Python time: {py_time:.4f} seconds")

    # Test C implementation
    print(f"\nTesting C implementation (repeating {repeat} times)...")
    c_times = []
    for i in range(repeat):
        start = time.time()
        tree_c = YggdrasilC()
        # Create a deep copy of each fiber to avoid modifying the original
        for fiber in fibers:
            # Create a copy of the fiber
            fiber_copy = fiber.copy()
            tree_c.add_fiber(fiber_copy)
        c_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {c_times[-1]:.4f} seconds")

    c_time = sum(c_times) / len(c_times)
    print(f"Average C time: {c_time:.4f} seconds")

    # Print results
    print("\nResults:")
    print(f"Python implementation: {py_time:.4f} seconds")
    print(f"C implementation: {c_time:.4f} seconds")

    # Handle the case where C implementation is extremely fast
    if c_time < 0.0001:
        print("C implementation is extremely fast (near zero execution time)")
        print("Speedup: VERY HIGH (cannot calculate exact ratio due to timing precision)")
    else:
        print(f"Speedup: {py_time / c_time:.2f}x")

    # Verify that both implementations produce the same results
    print("\nVerifying results...")
    for year in range(2020, 2020 + num_years):
        for month in range(1, num_months + 1):
            for day in range(1, num_days + 1):
                py_value = tree_py[year][month][day]["value"]
                c_value = tree_c[year][month][day]["value"]
                if py_value != c_value:
                    print(f"Error: Values don't match at [{year}, {month}, {day}, 'value']")
                    print(f"Python: {py_value}, C: {c_value}")
                    return

    print("All values match between Python and C implementations.")


def run_csv_benchmark(repeat=50, num_threads=None):
    """Run a benchmark for loading data from a CSV file."""
    import csv
    import multiprocessing

    if num_threads is None:
        num_threads = multiprocessing.cpu_count()

    print(f"\nBenchmarking CSV loading (repeating {repeat} times)...")
    print(f"Using {num_threads} threads for parallel processing")

    # Read and preprocess the CSV data once
    csv_data = []
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            # Clean the data (remove spaces)
            clean_row = [item.strip() for item in row]
            # Convert numeric values
            for i in range(len(clean_row)):
                try:
                    clean_row[i] = int(clean_row[i])
                except ValueError:
                    pass
            csv_data.append(clean_row)

    # Test Python implementation
    print(f"\nTesting Python implementation (repeating {repeat} times)...")
    py_times = []
    for i in range(repeat):
        start = time.time()
        tree_py = YggdrasilPy()

        # Create a copy of each row before adding it to the tree
        for row in csv_data:
            row_copy = row.copy()
            tree_py.add_fiber(row_copy)

        py_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {py_times[-1]:.4f} seconds")

    py_time = sum(py_times) / len(py_times)
    print(f"Average Python time: {py_time:.4f} seconds")

    # Test sequential C implementation
    print(f"\nTesting sequential C implementation (repeating {repeat} times)...")
    c_seq_times = []
    for i in range(repeat):
        start = time.time()
        tree_c_seq = YggdrasilC()

        # Create a copy of each row before adding it to the tree
        for row in csv_data:
            row_copy = row.copy()
            tree_c_seq.add_fiber(row_copy)

        c_seq_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {c_seq_times[-1]:.4f} seconds")

    c_seq_time = sum(c_seq_times) / len(c_seq_times)
    print(f"Average sequential C time: {c_seq_time:.4f} seconds")

    # Test parallel C implementation
    print(f"\nTesting parallel C implementation (repeating {repeat} times)...")
    c_par_times = []
    for i in range(repeat):
        start = time.time()
        tree_c_par = YggdrasilC()

        # Create copies of all rows
        rows_copy = [row.copy() for row in csv_data]

        # Use the parallel implementation to add all rows at once
        tree_c_par.add_fibers_parallel(rows_copy, num_threads)

        c_par_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {c_par_times[-1]:.4f} seconds")

    c_par_time = sum(c_par_times) / len(c_par_times)
    print(f"Average parallel C time: {c_par_time:.4f} seconds")

    # Print results
    print("\nCSV Loading Results:")
    print(f"Python implementation: {py_time:.4f} seconds")
    print(f"Sequential C implementation: {c_seq_time:.4f} seconds")
    print(f"Parallel C implementation: {c_par_time:.4f} seconds")

    # Calculate speedups
    print(f"Python vs Sequential C speedup: {py_time / c_seq_time:.2f}x")
    print(f"Sequential C vs Parallel C speedup: {c_seq_time / c_par_time:.2f}x")
    print(f"Python vs Parallel C speedup: {py_time / c_par_time:.2f}x")


def run_parallel_benchmark(num_years=100, num_months=12, num_days=30, repeat=50, num_threads=None):
    """Run a benchmark comparing sequential and parallel C implementations of Yggdrasil."""
    print(f"Generating test data for {num_years} years, {num_months} months, {num_days} days...")

    # Create test data
    fibers = []
    for year in range(2020, 2020 + num_years):
        for month in range(1, num_months + 1):
            for day in range(1, num_days + 1):
                fibers.append([year, month, day, "value", day * month])

    total_fibers = len(fibers)
    print(f"Generated {total_fibers} fibers.")

    # Test sequential C implementation
    print(f"\nTesting sequential C implementation (repeating {repeat} times)...")
    c_seq_times = []
    for i in range(repeat):
        start = time.time()
        tree_c_seq = YggdrasilC()
        # Create a deep copy of each fiber to avoid modifying the original
        for fiber in fibers:
            # Create a copy of the fiber
            fiber_copy = fiber.copy()
            tree_c_seq.add_fiber(fiber_copy)
        c_seq_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {c_seq_times[-1]:.4f} seconds")

    c_seq_time = sum(c_seq_times) / len(c_seq_times)
    print(f"Average sequential C time: {c_seq_time:.4f} seconds")

    # Test parallel C implementation
    print(f"\nTesting parallel C implementation (repeating {repeat} times)...")
    c_par_times = []
    for i in range(repeat):
        start = time.time()
        tree_c_par = YggdrasilC()
        # Use the parallel implementation to add all fibers at once
        fibers_copy = [fiber.copy() for fiber in fibers]
        if num_threads:
            tree_c_par.add_fibers_parallel(fibers_copy, num_threads)
        else:
            tree_c_par.add_fibers_parallel(fibers_copy)
        c_par_times.append(time.time() - start)
        print(f"  Run {i+1}/{repeat}: {c_par_times[-1]:.4f} seconds")

    c_par_time = sum(c_par_times) / len(c_par_times)
    print(f"Average parallel C time: {c_par_time:.4f} seconds")

    # Print results
    print("\nParallel Benchmark Results:")
    print(f"Sequential C implementation: {c_seq_time:.4f} seconds")
    print(f"Parallel C implementation: {c_par_time:.4f} seconds")

    # Handle the case where parallel implementation is extremely fast
    if c_par_time < 0.0001:
        print("Parallel C implementation is extremely fast (near zero execution time)")
        print("Speedup: VERY HIGH (cannot calculate exact ratio due to timing precision)")
    else:
        print(f"Speedup: {c_seq_time / c_par_time:.2f}x")

    # Verify that both implementations produce the same results
    print("\nVerifying results...")
    for year in range(2020, 2020 + num_years):
        for month in range(1, num_months + 1):
            for day in range(1, num_days + 1):
                seq_value = tree_c_seq[year][month][day]["value"]
                par_value = tree_c_par[year][month][day]["value"]
                if seq_value != par_value:
                    print(f"Error: Values don't match at [{year}, {month}, {day}, 'value']")
                    print(f"Sequential: {seq_value}, Parallel: {par_value}")
                    return

    print("All values match between sequential and parallel C implementations.")


if __name__ == "__main__":
    print("Yggdrasil Benchmark")
    print("===================")

    # Detect number of CPU cores
    import multiprocessing
    num_cores = multiprocessing.cpu_count()
    print(f"Detected {num_cores} CPU cores")

    # Run the main benchmark
    run_benchmark()

    # Run the CSV benchmark with parallel support
    run_csv_benchmark(num_threads=num_cores)

    # Run the parallel benchmark
    print("\n\nParallel Benchmark")
    print("=================")
    run_parallel_benchmark(num_threads=num_cores)
