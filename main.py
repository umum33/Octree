import time
import random
import matplotlib.pyplot as plt
from octree import Point3D, BoundingBox, OctreeNode, SpatialDataError

def generate_random_points(n, min_val, max_val):
    points = []
    for i in range(n):
        x = random.uniform(min_val, max_val)
        y = random.uniform(min_val, max_val)
        z = random.uniform(min_val, max_val)
        points.append(Point3D(x, y, z, point_id=f"PT-{i}"))
    return points

def run_benchmarks():
    input_sizes = [100, 500, 1000, 2500, 5000, 7500, 10000]
    
    insert_times = []
    search_times = []
    delete_times = []

    print("=== OCTREE EXPERIMENTAL BENCHMARK ===")
    print(f"{'Input Size (n)':<15}{'Insert (s)':<15}{'Search (s)':<15}{'Delete (s)':<15}")
    print("-" * 60)

    for n in input_sizes:
        area_box = BoundingBox(0, 0, 0, 100)
        root = OctreeNode(area_box, max_capacity=16)

        points_to_insert = generate_random_points(n, -95, 95)
        
        # 1. Insertion Test
        start_time = time.perf_counter()
        for p in points_to_insert:
            try:
                root.insert(p)
            except SpatialDataError as err:
                print(f"[ERROR-CATCH] {err}")
        end_time = time.perf_counter()
        t_insert = end_time - start_time
        insert_times.append(t_insert)

        # 2. Search Test
        points_to_search = generate_random_points(100, -95, 95)
        start_time = time.perf_counter()
        for p in points_to_search:
            root.search(p)
        end_time = time.perf_counter()
        t_search = (end_time - start_time) * (n / 100)
        search_times.append(t_search)

        # 3. Deletion Test
        points_to_delete = points_to_insert[:n // 2]
        start_time = time.perf_counter()
        for p in points_to_delete:
            root.delete(p)
        end_time = time.perf_counter()
        t_delete = (end_time - start_time) * 2
        delete_times.append(t_delete)

        print(f"{n:<15}{t_insert:<15.6f}{t_search:<15.6f}{t_delete:<15.6f}")

    # Plot generation
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, insert_times, label='Insert Operation', marker='o', color='blue')
    plt.plot(input_sizes, search_times, label='Search Operation', marker='s', color='green')
    plt.plot(input_sizes, delete_times, label='Delete Operation', marker='^', color='red')
    
    plt.title('Octree Empirical Complexity Analysis')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.savefig('octree_complexity_plot.png')
    print("\n[PROCESS] Plot saved as octree_complexity_plot.png")
    plt.show()

if __name__ == "__main__":
    run_benchmarks()