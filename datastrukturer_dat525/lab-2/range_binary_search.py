from term import Term


def first_index_of(array, term, ordering):
    """Returns the index of the *first* element in `array` that equals the search term,
    according to the given ordering, or -1 if there is no matching element.
    Precondition: `array` is sorted according to the given ordering.
    Complexity: O(log N) comparisons where N is the length of `array`.
    """

    #Procedure for finding the leftmost element in the tree, using binary search tree

    L = 0
    R = len(array)
    max_index = R
    while L < R:
        m = (L+R)//2 #set m (pos of middle element) to the floor of the equation; which is the greatest int < or = to the euqation
        if ordering(array[m]) < ordering(term): 
            L = m + 1
        else:
            R = m
            
    if L < max_index and ordering(array[L]) == ordering(term):
        return L
    else:
        return -1
        

def last_index_of(array, term, ordering):
    """Returns the index of the *last* element in `array` that equals the search term,
    according to the given ordering, or -1 if there are is matching element.
    Precondition: `array` is sorted according to the given ordering.
    Complexity: O(log N) comparisons where N is the length of `array`.
    """
    #Procedure for finding the rightmost element in the tree, using binary search tree
    L = 0
    R = len(array)
    max_index = R
    while L < R:
        m = (L+R)//2
        if ordering(array[m]) > ordering(term):
            R = m
        else:
            L = m + 1

    if (R-1) < max_index and ordering(array[R-1]) == ordering(term):
        return R-1
    else:
        return -1
    


if __name__ == '__main__':
    # Here you can write some tests if you want.
    test_a = [Term('ab', 90),Term('ab', 85),Term('ab', 85),Term('adbd', 100),
              Term('ABC', 80), Term('AAA', 70)]
    print(first_index_of(test_a, Term('ab', 12), Term.lexicographic_order))
    print(last_index_of(test_a, Term('AB', 12), Term.lexicographic_order))
