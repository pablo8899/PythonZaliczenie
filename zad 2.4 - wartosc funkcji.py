import multiprocessing
import numpy as np

def calculate_function(start, end, step):
    results = []
    x = start
    while x < end:
        f = np.cos(x) + np.pow(np.log(x + 1), 2)
        results.append((x, f))
        x += step

    return results


def main():
    start_range = 1
    end_range = int(1e6)
    step = 0.01
    num_processes = multiprocessing.cpu_count()


    chunk_size = (end_range - start_range) // num_processes
    ranges = [(i, min(i + chunk_size, end_range), step) for i in range(start_range, end_range, chunk_size)]

    pool = multiprocessing.Pool(num_processes)
    results = pool.starmap(calculate_function, ranges)
    pool.close()
    pool.join()

    all_results = []
    for result in results:
        all_results.extend(result)

    return all_results


if __name__ == "__main__":
    function_values = main()
    for x, v in function_values:
        print(f"x = {x}, f(x) = {v}")