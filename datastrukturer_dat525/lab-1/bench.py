#!/usr/bin/env python3

"""This is the benchmark program.

You can change what benchmarks are run by editing the main() function.
Apart from that, you don't have to look at or understand the code!"""

import random
import sort
import sys
import gc
import time
import copy
import array

def main():
    """Run the benchmarks. """

    execution_time_report("quick_sort", sort.quick_sort)

    # Uncomment this code to try out some improvements to quicksort
    # (after you have implemented them).
    # You should try different cutoff values, and different
    # combinations of improvements!
    #
    # execution_time_report("quick_sort, cutoff=5, shuffle, median of three",
    #     sort.quick_sort, cutoff = 5, shuffle_array = True, use_median_of_three = True)

    execution_time_report("merge_sort", sort.merge_sort)
    execution_time_report("insertion_sort", sort.insertion_sort)

    # Uncomment this one to also try out Python's built-in sorting algorithm
    # (which is very fast, partly due to being written in C)
    # execution_time_report("Built-in sort", lambda arr: list(sorted(arr)))

# The array sizes that are tried
sample_sizes = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000]

# What kind of input arrays are tried.
# The number n means that n percent of the array is chosen randomly
# and the rest is chosen to be in ascending order. So 100 means a
# random array and 0 an already-sorted array
randomnesses = [100, 5, 0]

# A time limit (in seconds), after which the benchmark program gives
# up running the test
time_limit = 1

#
# YOU CAN STOP READING HERE!
#
# The code below does all the benchmarking and testing,
# but you don't have to look at it (unless you're interested)
#

# Test data generator.
def generate_sample(size, randomness, variant=1):
    """Generates a random array of size 'size'.
    Part of the array is sorted, while the rest is chosen uniformly
    at random; the 'randomness' parameter sets what percent of the
    array is chosen at random."""

    sample = []
    # Make it deterministic - use the same array every time,
    # and also use the same array for every algorithm
    rand = random.Random(12345678 * size * variant)

    # We generate a random-but-sorted array, but interleave
    # with a random number 'randomness' percent of the time.
    previous = 0 # previous number used for sorted part
    for i in range(size):
        if rand.randint(1, 100) > randomness:
            # The "sorted" part of the array
            value = previous + rand.randint(1, 3)
            sample.append(value)
            previous = value
        else:
            # The "random" part of the array
            sample.append(rand.randint(1, size))

    # Return the data as a list.
    # Uncomment the following line to return an array instead.
    return array.array('i', sample)
    # return sample


def describe_randomness(randomness):
    """Give a textual description of a randomnes factor."""

    if randomness == 0:
        return "Sorted"
    elif randomness == 100:
        return "Random"
    else:
        return "%d%% sorted" % (100-randomness)

def test_algorithm(algorithm):
    """Test that an algorithm works on inputs of different sizes."""

    for size in range(100):
        for randomness in randomnesses:
            # Check each case 10 times
            for variant in range(10):
                check(generate_sample(size, randomness, variant), algorithm)

def check(array, algorithm):
    """Test that an algorithm works on one input."""

    # Save the input and the correct output for checking later.
    unsorted_reference = list(array)
    sorted_reference = list(sorted(array))

    try:
        result = algorithm(array)
    except NotImplementedError as e:
        raise
    except:
        failed(unsorted_reference, sorted_reference)
        print("Actual answer: an exception was raised")
        raise

    # In-place algorithms return None but modify the input
    if result is None:
        result = array
    # The result might be an array so convert it to a list.
    result = list(result)

    if result != sorted_reference:
        failed(unsorted_reference, sorted_reference)
        print("Actual answer: %s" % result)
        sys.exit(1)

def failed(array, reference):
    """Report a test failure in a sorting algorithm."""

    print("Test failed! There is a bug in the sorting algorithm.")
    print("Input array: %s" % array)
    print("Expected answer: %s" % reference)

def execute(algorithm, input):
    """Benchmark an algorithm on an input.

    To get good results on short-running algorithms, we use several
    tricks:
    1. Run the algorithm several times in a row and take the average.
       The number of times is increased until the total runtime is
       above 10ms.
    2. Repeat the above 3 times, taking the minimum runtime.
    3. Disable the garbage collector before running."""

    target = 0.01 # Repeat the algorithm until runtime >= target
    max_lives = 3 # Then repeat this max_lives times and take the minimum

    # How many times in a row to run the algorithm in step 1 above
    # (gets adjusted upwards until target time is reached)
    repetitions = 1

    # Smallest runtime seen so far
    runtime = float("inf")

    # How many more times left to repeat in step 2 above
    lives = max_lives

    while True:
        # Pregenerate input arrays - we don't want this to be counted
        # as part of the runtime
        inputs = [copy.copy(input) for i in range(repetitions)]
        seed = hash(str(input)) # see later

        # Disable garbage collector
        gcold = gc.isenabled()
        gc.disable()

        this_runtime = 0
        try:
            for i in range(repetitions):
                # Set the random number seed deterministically in case
                # the sorting algorithm uses randomness
                random.seed(seed)

                # Run the algorithm and add the runtime to this_runtime
                before = time.perf_counter()
                algorithm(inputs[i])
                this_runtime += time.perf_counter() - before
        finally:
            # Enable garbage collector
            if gcold:
                gc.enable()

        # runtime should hold minimum runtime seen so far
        runtime = min(runtime, this_runtime)

        # If the algorithm took a long time to run, stop immediately
        # to save time
        if repetitions == 1 and runtime >= 30*target:
            break

        # If the runtime meets the target, reduce the number of
        # repetitions left in step 2 of the algorithm
        elif runtime >= target:
            if lives == 0: break
            else: lives -= 1

        else:
            # The runtime was too small, so increase the number of
            # repetitions. Scale up by extrapolating from the actual
            # runtime, but multiply the repetitions by at least 2
            # (to limit the number of scaling steps needed) and at
            # most 5 (to prevent repeating a huge number of times if
            # our guess for the factor is too high)
            if runtime == 0:
                factor = 5
            else:
                factor = int(target / runtime)
                if factor < 2: factor = 2
                if factor > 5: factor = 5
            repetitions *= factor
            runtime = float("inf")
            lives = max_lives

    return runtime / repetitions

def execution_time_report(name, algorithm, **kwargs):
    """Test a sorting algorithm and report the runtime."""

    # Handle keyword arguments.
    real_algorithm = lambda arr: algorithm(arr, **kwargs)

    def column_width(*values):
        """How many characters wide does a column need to be to
        display the given values?"""

        return max(map(len, values))

    def format_row(size, pad, values):
        """Format a table row as a string.

        - size: string to be put in the "Size" column
        - pad: a function (str, width) -> str which pads
          the column to have the given width
        - values: the data stored in the columns, as strings"""

        cells = [size.rjust(size_width)]
        for value in values:
            cells.append(pad(value, header_width))
        return " || ".join(cells)

    def format_data_row(size, times):
        """Format a row of test output as a string.

        size: size of input array
        times: list of times formatted with "format_time_pair"."""

        return format_row(str(size), str.rjust, times)

    def format_total_time(time):
        """Convert total time to a string."""

        return "%6.0f" % time

    def format_time_per_item(time):
        """Convert time per item to a string."""

        return "%3.3f" % time

    def format_time_pair(total_time, time_per_item):
        """Format two time columns as a string."""

        return " | ".join([total_time.rjust(total_time_width),
            time_per_item.rjust(time_per_item_width)])

    def format_time(time, size):
        """Format a single time as a string giving both total time and
        time per item."""

        total = format_total_time(time*1000000)
        per_item = format_time_per_item(time*1000000 / size)
        return format_time_pair(total, per_item)

    def isstring(x):
        """Is a given value a string?"""

        if isinstance(x, str): return True
        if "basestring" in globals():
            if isinstance(x, basestring):
                return True
        return False

    # Various fixed strings that appear in the output
    size_header = "Size"
    randomness_headers = list(map(describe_randomness, randomnesses))
    total_time_header = "Total"
    time_per_item_header = "Per item"
    too_slow_string = "Skipped"
    stack_overflow_string = "Recursion overflow"

    # The width of the "size" column
    size_width = column_width(size_header, *map(str, sample_sizes))
    # The width of the columns containing runtimes
    total_time_width = column_width(total_time_header, format_total_time(9999999))
    time_per_item_width = column_width(time_per_item_header, format_time_per_item(9999.999))
    # The width of the randomness columns
    header_width = \
        column_width(
            format_time_pair("", ""),
            stack_overflow_string,
            *randomness_headers)

    # The total width of the table
    total_width = len(format_data_row("", [""] * len(randomnesses)))

    # The maximum runtime so far for each kind of input data
    max_times = [0] * len(randomnesses)

    # Print the table header
    print("=" * total_width)
    print("  %s (times in microseconds)" % name)
    print("=" * total_width)

    # Check that the sorting algorithm works before going any further.
    try:
        test_algorithm(real_algorithm)
    except NotImplementedError as e:
        print()
        print("NotImplementedError:", e)
        print()
        return

    # Print the rest of the table header
    print(format_row("", str.center, randomness_headers))
    print(format_row("Size", str.rjust,
        [format_time_pair(total_time_header, time_per_item_header)] * len(randomnesses)))
    print("=" * total_width)

    # Each size produces one row of the table.
    for size in sample_sizes:
        # The string for each column gets collected in here.
        times = []
        for i, randomness in enumerate(randomnesses):
            if max_times[i] > time_limit:
                # Don't try running the algorithm if it took >1 s on a
                # smaller input size.
                times.append(too_slow_string.center(header_width))
            else:
                try:
                    time = execute(real_algorithm, generate_sample(size, randomness))
                    max_times[i] = max(max_times[i], time)
                    times.append(format_time(time, size))
                except RecursionError as e:
                    times.append(stack_overflow_string.center(header_width))
                except Exception as e:
                    # Print the exception name in case of an error
                    times.append(type(e).__name__.center(header_width))

        print(format_data_row(size, times))

    print()

if __name__ == '__main__':
    main()
