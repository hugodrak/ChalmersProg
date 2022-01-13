import random
import array

def insertion_sort(unsorted_array):
    """Sorts array using insertion sort. Not in-place."""

    # sorted_array = []
    sorted_array = array.array('i')

    # Insert each item in turn into sorted_array
    for item in unsorted_array:
        # Optimisation for sorted inputs:
        # First check if the new item should go at the end
        if not sorted_array or item >= sorted_array[-1]:
            sorted_array.append(item)
        else:
            # Otherwise find the insertion point and then insert
            for i in range(len(sorted_array)):
                if item <= sorted_array[i]:
                    # sorted_array.insert(i, x) makes a space at index i by
                    # moving all the following elements up by one,
                    # then sets sorted_array[i]=x
                    sorted_array.insert(i, item)
                    break

    return sorted_array

def merge_sort(array):
    """Sorts array using merge sort."""

    # Base case
    if len(array) <= 1: return array

    mid = len(array) // 2  # // = division rounding down
    # Split array into two roughly equal parts
    first_half = array[:mid]
    second_half = array[mid:]

    # Recursively sort both parts and combine results
    return merge(merge_sort(first_half), merge_sort(second_half))

def merge(array1, array2):
    """Merges two sorted lists into one."""

    # result = []
    result = array.array('i')

    # Copy elements from array1/array2 until we reach the end of one
    # of the arrays
    i = 0
    j = 0
    while i < len(array1) and j < len(array2):
        if array1[i] <= array2[j]:
            result.append(array1[i])
            i += 1
        else:
            result.append(array2[j])
            j += 1

    # One array is already fully copied, so copy any leftover elements
    # from the other array. Note that we don't need an if-statement
    # here, because e.g. if array1 is fully copied then we will have
    # i == len(array1) and so array1[i:] will be empty.
    result.extend(array1[i:])
    result.extend(array2[j:])

    return result

def quick_sort(array, cutoff = 30, use_median_of_three = True, shuffle_array = True):
    """Sorts array using quicksort. Below array size 'cutoff',
    switches to insertion sort. If use_median_of_three is True, uses
    median of three for pivot selection. If shuffle_array is True,
    shuffles the array before sorting."""

    if shuffle_array:
        # TODO: Try using random.shuffle to shuffle the array before sorting
        random.shuffle(array)

    quick_sort_recursive(array, 0, len(array), cutoff, use_median_of_three)

def quick_sort_recursive(array, lo, hi, cutoff, use_median_of_three):
    """Quicksorts the subarray array[lo:hi], i.e. elements
    array[lo] to array[hi-1], switching to insertion sort at the
    specified cutoff, and optionally using median-of-three."""

    # Base case
    if hi <= lo+1: return
    # TODO: check if the size of array[lo:hi] is below the cutoff
    # value, and switch to insertion sort if so. You can write
    # array[lo:hi] to get the relevant part of the list to sort
    # (and in Python, this takes a constant amount of time).
    #
    # Note that insertion_sort is not in-place, so you will need to
    # take the list returned by insertion_sort and store it back in
    # 'array'. Python hint: One way to do this is by using slice
    # assignment, see https://blog.finxter.com/python-slice-assignment/.
    #
    # Afterwards, don't forget to return from the function instead of
    # continuing with the quicksort!
    if len(array[lo:hi]) < cutoff:
        array[lo:hi] = insertion_sort(array[lo:hi])
    else:
    # Partition and then make two recursive calls
        mid = partition(array, lo, hi, use_median_of_three)
        quick_sort_recursive(array, lo, mid, cutoff, use_median_of_three)
        quick_sort_recursive(array, mid+1, hi, cutoff, use_median_of_three)

def partition(array, lo, hi, use_median_of_three):
    """Partition the subarray array[lo:hi]. Returns the final index of
    the pivot. If use_median_of_three is True, uses median-of-three to
    choose the pivot."""

    if use_median_of_three:
        # TODO: try median of three. Find the median of the first, last
        # and middle elements of array[lo:hi], and swap it with array[lo].
        # Hint: use the function median_of_three defined below.
        # Hint: array[lo:hi] selects all elements from array[lo]
        # up to array[hi-1] (not array[hi]).
        # Python hint: x//2 divides x by 2 and rounds down to the
        # nearest integer.
        # print(array, lo, hi, array[lo], array[hi-1])
        median_index = median_of_three(array, lo, (hi-lo)//2 ,hi-1)
        # print(median_index, array[median_index])
        array[lo], array[median_index] = array[median_index], array[lo]
        #raise NotImplementedError('use_median_of_three not implemented')

    # array[lo] is always used as the pivot.
    # Don't change this for median of three but swap the correct pivot
    # with array[lo] instead.
    pivot = array[lo]

    # i moves upwards in the array, j moves downwards.
    # Hence i starts at the first element after the pivot,
    # and j starts at the final element.
    i = lo+1
    j = hi-1

    # Continue until i and j cross
    while i <= j:
        # Find an element in the "less than" partition that should
        # be in the "greater than" partition
        while i <= j and array[i] < pivot:
            i += 1

        # Find an element in the "greater than" partition that should
        # be in the "less than" partition
        while i <= j and array[j] > pivot:
            j -= 1

        # If i and j have crossed now then we should stop without
        # doing a swap.
        if i <= j:
            # Swap the elements and continue.
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1

    # Place the pivot in array[j]
    array[lo], array[j] = array[j], array[lo]

    return j

def median_of_three(array, i, j, k):
    """Return the index of the median element among array[i],
    array[j], and array[k]. (The median of a sequence of numbers
    is the middle that would come in the middle if the numbers were
    sorted.)

    For example, if array[j] <= array[k] <= array[i], then return k."""
    # print("")
    # print(array)
    # print("ijk", i,j,k)
    x = array[i]
    y = array[j]
    z = array[k]
    # print("xyz", x,y,z)
    if x <= y:
        if y <= z: # x <= y <= z
            return j
        else:
            if x <= z: # x <= z <= y
                return k
            else: # z <= x <= y
                return i
    elif x <= z: # y <= x <= z
        return i
    elif y <= z: # y <= z <= x
        return k
    else: # z <= y <= x
        return j
