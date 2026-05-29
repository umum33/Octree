import time
import random
import matplotlib.pyplot as plt
from octree import Point3D, BoundingBox, OctreeNode

def generate_random_points(n, min_val, max_val):
    """Generates a list of n random Point3D objects within a spatial range."""
    points = []
    for _ in range(n):
        x = random.uniform(min_val, max_val)
        y = random.uniform(min_val, max_val)
        z = random.uniform(min_val, max_val)
        points.append(Point3D(x, y, z))
    return points

def run_benchmarks():
    # Define input sizes (n) for the experiments
    input_sizes = [100, 500, 1000, 2500, 5000, 7500, 10000]
    
    insert_times = []
    search_times = []
    delete_times = []

    print("Starting benchmarks...")
    print(f"{'Input Size (n)':<15}{'Insert (s)':<15}{'Search (s)':<15}{'Delete (s)':<15}")
    print("-" * 60)

    for n in input_sizes:
        # Create a bounding box centered at (0,0,0) with a size of 100 units 
        # (covers space from -100 to 100 in all 3 dimensions)
        boundary = BoundingBox(0, 0, 0, 100)
        root = OctreeNode(boundary, capacity=16)

        # 1. Benchmark Insertion
        points_to_insert = generate_random_points(n, -95, 95)
        
        start_time = time.perf_counter()
        for p in points_to_insert:
            root.insert(p)
        end_time = time.perf_counter()
        t_insert = end_time - start_time
        insert_times.append(t_insert)

        # 2. Benchmark Searching
        # We will look for 100 random points to get a stable average time
        points_to_search = generate_random_points(100, -95, 95)
        
        start_time = time.perf_counter()
        for p in points_to_search:
            root.search(p)
        end_time = time.perf_counter()
        # Normalize the time to match the size 'n' scale
        t_search = (end_time - start_time) * (n / 100)
        search_times.append(t_search)

        # 3. Benchmark Deletion
        # Delete half of the points inserted to measure deletion scaling
        points_to_delete = points_to_insert[:n // 2]
        
        start_time = time.perf_counter()
        for p in points_to_delete:
            root.delete(p)
        end_time = time.perf_counter()
        # Scale back up to match 'n' operations
        t_delete = (end_time - start_time) * 2
        delete_times.append(t_delete)

        print(f"{n:<15}{t_insert:<15.6f}{t_search:<15.6f}{t_delete:<15.6f}")

    # --- Plotting Results ---
    plt.figure(figsize=(10, 6))
    
    # Linear scale line plots
    plt.plot(input_sizes, insert_times, label='Insert Operation', marker='o', color='blue')
    plt.plot(input_sizes, search_times, label='Search Operation', marker='s', color='green')
    plt.plot(input_sizes, delete_times, label='Delete Operation', marker='^', color='red')
    
    plt.title('Octree Empirical Complexity Analysis')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Save the output plot automatically to the directory
    plt.savefig('octree_complexity_plot.png')
    print("\nBenchmark complete! Plot saved as 'octree_complexity_plot.png'")
    plt.show()

if __name__ == "__main__":
    run_benchmarks()