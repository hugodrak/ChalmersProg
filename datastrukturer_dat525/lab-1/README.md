# Lab 1: Sorting, Complexity

In this lab, you will explore how different sorting algorithms perform in practice. There are two main tasks:

- Measuring the runtime of various sorting algorithms on different degrees of sortedness of input data and empirically determining their complexity
- Taking a simple implementation of quicksort and speeding it up by adding important optimisations

## About the labs

- The lab is part of the examination of the course. Therefore, you must not copy code from or show code to other groups. You are welcome to discuss ideas with one another, but anything you do must be **the work of you and your lab partners**.
<<<<<<< HEAD
- Please read [the general instructions for doing the labs assigments](https://chalmers.instructure.com/courses/15943/pages/doing-the-lab-assignments).
=======
- Please read the pages "Doing the lab assignments" and "Running the labs" on Canvas.
>>>>>>> 7ed50260a2bc9613c0a6c92301ad4b98b39a6e71

## Getting started

To run the labs, you will need **Python 3**. Make sure that the
command `python3` works. Note that just runing `python` might give you
Python 2 instead!

The file `sorting.py` contains implementations of three sorting algorithms:

- **insertion_sort** - insertion sort
- **merge_sort** - top-down merge sort
- **quick_sort** - quicksort, using the first element as the pivot

There is also a useful for you to run:

- **bench.py** - a benchmark and testing program;
  prints performance reports for the sorting algorithms
  and tests that they work correctly.

and a file **answers.txt** where you will write down answers to questions in the lab.

Now run **python3 bench.py**. It will measure the performance of each of the algorithms above and print out a timing report for each one. (If you get a `NameError` exception, you are running under Python 2 by mistake!) The timing report will look something like this:

```
========================================================================
  merge_sort (times in microseconds)
========================================================================
       ||       Random       ||     95% sorted     ||       Sorted
  Size ||   Total | Per item ||   Total | Per item ||   Total | Per item
========================================================================
    10 ||      21 |    2.057 ||      19 |    1.884 ||      17 |    1.667
    30 ||      69 |    2.311 ||      57 |    1.909 ||      61 |    2.047
   100 ||     308 |    3.080 ||     262 |    2.620 ||     234 |    2.342
   300 ||    1036 |    3.453 ||     836 |    2.787 ||     747 |    2.489
  1000 ||    3771 |    3.771 ||    2899 |    2.899 ||    2514 |    2.514
  3000 ||   12714 |    4.238 ||    9543 |    3.181 ||    8263 |    2.754
 10000 ||   48537 |    4.854 ||   37008 |    3.701 ||   30610 |    3.061
 30000 ||  161503 |    5.383 ||  121741 |    4.058 ||   98933 |    3.298
100000 ||  603911 |    6.039 ||  450782 |    4.508 ||  377205 |    3.772
```

At the top of the table you see which sorting algorithm was tested. The table shows how the algorithm's runtime (given in microseconds) varies with the size of the input array (shown in the leftmost column) for three degrees of sortedness:

- Completely random arrays
- Arrays where 95% of elements are in the right order, but the rest are chosen at random
- Arrays that are already in the right order

The time is presented in two columns:

- _Total:_ This shows the total time for sorting that array.
- _Per item:_ This is the total time divided by the size of the array.

For example, the table above shows that mergesort took 604ms on an array of 100000 random integers, and 377ms on a sorted array of 100000 integers.

In the tables for insertion sort and quicksort, you will see error
messages in some table cells, instead of runtimes:

- _Skipped_: This means that the test was predicted to take more than
  1 second to run, and was skipped to save time.
- _Recursion overflow_: This means that when running the test, the
  sorting algorithm recursed too deeply. Python limits code to 1000
  levels of recursive calls.

## Task 1: figuring out the complexity

Look at the timing reports for the different algorithms.

You will notice that some of the algorithms are more efficient than others. In fact, the algorithms have different *complexities*:

- Some take quadratic time (the runtime is proportional to *n*<sup>2</sup>, where *n* is the size of the input array).
- Others take linearithmic time (the runtime is proportional to *n* log *n*).
- Others take linear time (the runtime is proportional to *n*).
- Often the complexity even depends on the degree of sortedness of the input array (random, 95% sorted, or sorted).

We will learn more about complexity later in the course.
For now, we take the above as defining complexity.
Since complexity ignores a factor of proportionality, it is not a direct measure of speed.
Rather, it tracks changes in a program's runtime as its input becomes larger.

Your first task is to answer the following question:

- For each of the three sorting algorithms, and each kind of array
  (random, 95% sorted, sorted), what is the algorithm's complexity?

You should answer this question _only looking at the timing data_, not
thinking about how the algorithms work.

*Hint:* The "time per item" column is useful for finding the
complexity. For an array of size *n*, this column gives the runtime
divided by *n*. So:

- If the runtime is proportional to *n*<sup>2</sup>,
  the time per item will be proportional to *n*.
- If the runtime is proportional to *n* log *n*,
  the time per item will be proportional to log *n*.
- If the runtime is proportional to *n*,
  the time per item will be roughly a constant regardless of the array size.

Write your answers in the file **answers.txt** provided. One answer is filled in for you already.

## Task 2: improving quicksort

You will have noticed that the quicksort implementation in **sort.py** performs badly on sorted input arrays. This is because it always chooses the pivot to be the first element of the input array, which in a sorted array means that one of the partitions is always empty. In this task you will make several improvements to the quicksort implementation and see how well they work in practice.

If you look at the **quick_sort** function, you will find three comments starting with `# TODO: [...]` which indicate an improvement you should make. **Before running your modified code, read the next section, "Choosing which improvements get used"!** Here are the three improvements:

1. **Before sorting the array, shuffle it** (rearrange it into a random order). You should only do this immediately at the beginning of quicksort, and not inside any of the recursive calls. To shuffle the input array, you can call `random.shuffle(array)`.

  The goal of shuffling the input is to avoid having bad performance on sorted arrays, by turning every input array into a randomly-ordered array. With the array shuffled, it should be OK to always use the first element as the pivot.

2. **Use the median-of-three for the pivot selection**. By default, the first element is used as pivot in the subarray we are currently sorting. Instead, look at the first element, the last element and the middle element of the subarray, and use the median value of those three as the pivot.

  In **sort.py**, you will find a function:

  ```
  def median_of_three(array, i, j, k):
  ```
  which looks at `array[i]`, `array[j]` and `array[k]` and return the index (`i`, `j` or `k`) containing the median element.

  Change the partitioning function so that it first finds the median-of-three and then *swaps* it with the first element in the subarray. To swap two array elements `i` and `j`, you can write:

  ```
  array[i], array[j] = array[j], array[i]
  ```

  The goal of median-of-three is twofold: 1) ensure that if the subarray is sorted, the middle value is chosen as the pivot; 2) by choosing between three pivot candidates, try to improve the distribution of elements between the two partitions.

3. **Switch to insertion sort for small subarrays**. Quicksort recurses all the way down until it reaches a subarray of size 1, which results in very many recursive calls. You should change the recursion's base case so that small subarrays are sorted with insertion sort. (What in the timing data suggests that this is a good idea?)

  To sort the subarray `array[lo..hi]`, you can call `insertion_sort(array, lo, hi)`. **You do not need to implement insertion sort yourself.**

  You will need to choose an appropriate cutoff size for switching to insertion sort. You should **do this in a systematic way**, rather than guessing. For example, here is one approach you could take:

  - From the timing data, figure out an initial estimate for the cutoff value.
  - To refine your estimate, try some nearby values and measure their performance.

  But you may find a good cutoff value in whatever way you like. Also, you do not need to find an exact value, as this will differ from computer to computer - rounding the cutoff value to the nearest 10 would be reasonable.

  Whatever approach you use, make sure that your answer is reasonable, by
  checking that when you change the cutoff value by some amount in either direction,
  the performance starts to gets worse.

### Choosing which improvements get used

When you benchmark quicksort, you will want to sometimes switch
different improvements on or off. The **quick_sort** function
therefore allows its caller to customise what improvements get used.
To do so, it takes several keyword arguments:

```
def quick_sort(array, cutoff = 0, use_median_of_three = False, shuffle_array = False):
  ...
```

The meaning of these arguments is as follows:

* `cutoff` determines the size at which recursive subcalls in quicksort switches to insertion sort.
* If `shuffle_array` is true, the array should be shuffled before sorting.
* If `use_median_of_three` is true, the median-of-three strategy should be used for pivot selection.

When you implement your improvements, make sure to take these
arguments into account. The code you were given already contains
if-statements that check `shuffle_array` and `use_median_of_three`,
which should help you to do this.

Looking at the default values of the arguments, you can see that **all
improvements are switched off by default**! To switch them on, you
need to modify the benchmark program, **bench.py**. In the `main`
function at the top of **bench.py**, you will see a commented-out
statement:

```
execution_time_report("quick_sort, cutoff=5, shuffle, median of three",
    sort.quick_sort, cutoff = 5, shuffle_array = True, use_median_of_three = True)
```

This line specifies that the array should be shuffled, that
median-of-three should be used for the pivot, and that a cutoff to
insertion sort of 5 should be used. To try it out, just uncomment the
line.

When benchmarking your code, you will want to try out different
combinations of improvements, and different cutoffs to insertion sort.
To do so, just have several calls to `execution_time_report`. You can
copy the line above, changing the arguments to adjust the settings,
and changing the string so that you can tell each version apart.

To help the person grading your assignment, please also keep the call
`execution_time_report("quick_sort", sort.quick_sort)` that tests
`quick_sort` with no improvements.

### Finding bugs

**bench.py** not only measures the performance of your code, it also
checks that it sorts correctly. If you introduce a bug when improving
quicksort, you will get an error message that looks something like
this:

```
Test failed! There is a bug in the sorting algorithm.
Input array: [2, 4]
Expected answer: [2, 4]
Actual answer: [4, 2]
```

This shows that we tried to sort the array `[2, 4]`, which should give
the result `[2, 4]`. However, quicksort mistakenly gave the answer `[4, 2]`.

Once you have this test case, you can add `print` statements to your
code to trace what is going on, or alternatively try out the Python
debugger `pdb` (https://dbwebb.se/kunskap/python-debugger).

### Your task

Your task is as follows:

- Make the improvements above, one at a time. After you have made an improvement, test it with **bench.py** and check: did the performance improve? Did the complexity change?
- Figure out which *combination* of improvements works best. That is, it may not be a good idea to add all three! Try different combinations to find the best one.

When you have done that, fill in **answers.txt** with the following information:

- Which of the three improvements above affect the complexity of quicksort, and in what way?
- What cutoff works best for insertion sort? You will also need to explain, in a few sentences, how you found the cutoff value.
- What did you find to be the best combination of improvements?

## Your submission

Your repository on GitLab Chalmers should contain the following changes:

- Your improved version of **sort.py**
- A file **output.txt** with the output from running **bench.py** on the three different sorting algorithms with the improvements you have chosen for quicksort
- The file **answers.txt**, with all answers filled in

When you are finished, create a Git tag `submission0` (for the commit you wish to submit).
For re-submissions, use `submission1`, `submission2`, etc.
The tag serves as your proof of submission.
You cannot change or delete it afterwards.
We will then grade your submission and post our feedback as issues in your project.
<<<<<<< HEAD
For more information on how to submit, see: https://chalmers.instructure.com/courses/15943/pages/doing-the-lab-assignments
=======
For more information on how to submit, see "Doing the lab assignments" on Canvas.
>>>>>>> 7ed50260a2bc9613c0a6c92301ad4b98b39a6e71

## Optional tasks

If you would like an extra challenge, here are some suggestions for things you could do:

- Since Python is not the fastest programming language, all the
  sorting algorithms are much slower than they could be. To speed them
  up, try running your code under [PyPy](https://www.pypy.org/), a
  version of the Python interpreter which compiles Python code to
  machine code.

  Having done that, you can speed up the code further by making it use
  Python `array` objects rather than lists. To do so:

  - In `insertion_sort`, change the line `sorted_array = []`
    to `sorted_array = array.array('i')`.
  - Similarly, in `merge`, change the line `result = []`
    to `result = array.array('i')`.
  - Finally, go into `bench.py`, find the function `generate_sample`,
    and at the bottom of that function, uncomment the commented-out
    line `#return array.array('i', sample)`. This will make the
    benchmark program use arrays as input instead of lists.

  Now you have done this, compare your code against Python's built-in
  sorting algorithm `list.sort`, by uncommenting the line in
  **bench.py**.
- Modify **quick_sort** to choose a random element as pivot. You may think that this would have the same effect as shuffling the array. It doesn't! Try it out and see what happens, then figure out what causes the difference. (Hint: the time taken by partitioning depends on the order of the input array.)
- Implement [Dual-pivot quicksort](https://web.archive.org/web/20151002230717/http://iaroslavski.narod.ru/quicksort/DualPivotQuicksort.pdf), which is the main algorithm used by Java to sort arrays of ints.
- (Very hard!) Implement [Timsort](https://en.wikipedia.org/wiki/Timsort), the sorting algorithm used by Python. It is basically run-based mergesort plus lots and lots of clever tricks to make it faster.
- Make a sorting function that dynamically chooses between different algorithms depending on the input array. For example, the Java sorting algorithm does this: it usually uses dual-pivot quicksort, but switches to a run-based mergesort for input arrays having few runs (and does this check in the recursive calls too).
