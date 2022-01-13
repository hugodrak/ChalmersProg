
# Lab 2: Autocomplete

In this lab your task is to implement autocomplete for a given set of terms, where a term consists of a string and an associated non-negative weight. That is, given a prefix, find all queries that start with the given prefix, in descending order of weight.

## About the labs

- The lab is part of the examination of the course. Therefore, you must not copy code from or show code to other groups. You are welcome to discuss ideas with one another, but anything you do must be **the work of you and your lab partners**.
- Please read the pages "Doing the lab assignments" and "Running the labs" on Canvas.

## Getting started

To run the labs, you will need **Python 3**. Make sure that the
command `python3` works. Note that just runing `python` might give you
Python 2 instead!

The lab directory contains the following Python files:

- **term.py**: autocompletion terms
- **range\_binary\_search.py**: two different binary search algorithms
- **autocompleter.py**: the autocompletion engine
- **autocomplete_cli.py**: a command-line interface to the autocompleter (should not be changed)

as well as a directory of **dictionaries**, and a file **answers.txt** where you will write down answers to questions in the lab.

The main file is **autocomplete_cli.py**, but if you try to run it you will get a runtime error:

```
$ python3 autocomplete_cli.py dictionaries/romaner.txt 5
Traceback (most recent call last):
  (...)
NotImplementedError
```

## Background

In this lab your task is to implement autocomplete for a given set of terms, where a term consists of a string and an associated non-negative weight. That is, given a prefix, find all queries that start with the given prefix, in descending order of weight.

Autocomplete is pervasive in modern applications. As the user types, the program predicts the complete query (typically a word or phrase) that the user intends to type. Autocomplete is most effective when there are a limited number of likely queries. For example, Wikipedia uses it to display matching page titles as the user types; search engines use it to display suggestions; cell phones use it to speed up text input.

| Wikipedia search | Web search | SMS suggestions |
|------------------|------------|-----------------|
| ![Wikipedia autocomplete](img/autoc-wikipedia.png) | ![DuckDuckGo autocomplete](img/autoc-duckduck.png) | ![SMS autocomplete](img/autoc-sms.png) |

In these examples, the application predicts how likely it is that the user is typing each query and presents to the user a list of the top-matching queries, in descending order of weight. These weights are determined by historical data, such as box office revenue for movies, frequencies of search queries from other Google users, or the typing history of a cell phone user. For the purposes of this assignment, you will have access to a set of all possible queries and associated weights (and these queries and weights will not change).

The performance of autocomplete functionality is critical in many systems. For example, consider a search engine which runs an autocomplete application on a server farm. According to one study, the application has only about 50ms to return a list of suggestions for it to be useful to the user. Moreover, in principle, it must perform this computation for every keystroke typed into the search bar and for every user!

In this assignment, you will implement autocomplete by (1) sorting the terms alphabetically; (2) binary searching to find all query strings that start with a given prefix; and (3) sorting the matching terms by weight.

## Part 1: The autocompletion term

The class `Term` in **term.py** represents an autocompletion term: a string and an associated integer weight. Extend it with the following static methods, which support comparing terms by three different orders:

- [case-insensitive lexicographic order](https://docs.python.org/3/library/stdtypes.html#str.casefold);
- in descending order by weight; and
- case-insensitive lexicographic order, but using only the first *k* characters – this order may seem a bit odd, but you will use it in Part 3 to find all words that start with a given prefix (of length *k*)

```python
class Term:
    (...)

    @staticmethod
    def lexicographic_order(term):
        """Case-insensitive lexicographic order."""

    @staticmethod
    def reverse_weight_order(term):
        """Descending order by weight."""

    @staticmethod
    def prefix_order(k):
        """Case-insensitive lexicographic order, but using only the first k characters of the word."""
```

To get case-insensitive lexicographic order, you should use the string method `.casefold(…)`.

### Testing the Term class

There are some tests at the end of the file. When you have implemented your comparison functions, you should be able to run the file from the command line. However, note that these tests do not prove that your implementation is correct!

### Performance requirements

- The string comparison functions should have linear complexity in the number of characters needed to resolve the comparison.

## Part 2: Binary search for a range

When binary searching a sorted array that contains more than one key equal to the search key, the client may want to know the index of either the first or the last such key. Accordingly, implement modified versions of binary search in the file **range\_binary\_search.py**:

```python
def first_index_of(array, term, ordering):
    """Returns the index of the *first* element in `array` that equals the search term,
    according to the given ordering, or -1 if there is no matching element.
    Precondition: `array` is sorted according to the given ordering.
    Complexity: O(log N) comparisons where N is the length of `array`.
    """

def last_index_of(array, term, ordering):
    """Returns the index of the *last* element in `array` that equals the search term,
    according to the given ordering, or -1 if there are is matching element.
    Precondition: `array` is sorted according to the given ordering.
    Complexity: O(log N) comparisons where N is the length of `array`.
    """
```
These functions are *generic* in the type of the array elements.
As long as the ordering returns something that Python can compare,
the arrays can contain numbers, strings, tuples or arbitrary objects.

***Important***: When comparing elements, don't forget to apply the ordering! I.e., if you want to compare `a` with `b`, you should actually compare `ordering(a)` with `ordering(b)`.

### Testing your implementation

We suggest that you come up with some tests that you can run on your binary search functions, and test them before moving on to the next part. You can e.g. put them at the end of the file (under `if __name__=='__main__':`), and then you can run the program from the command line.

### Performance requirements

- The functions `first_index_of(…)` and `last_index_of(…)` should have logarithmic comparison complexity in the array length.
- In this context, a comparison is one usage of any comparison operator, `==`, `<`, `>=`, etc.

## Part 3: Autocompletion

In this part, you will implement a data type that provides autocomplete functionality for a given set of string and weights, using the class `Term` and the functions `first_index_of(…)` and `last_index_of(…)`. To do so, (i) sort the terms in lexicographic order; (ii) use binary search to find all terms that start with a given prefix; and (iii) sort the matching terms in descending order by weight. Organize your program by implementing the following API in the class `Autocompleter`:

```python
class Autocompleter:
    def __init__(self, dictionary):
        """Initializes the dictionary from the given list of terms."""
        self.dictionary = dictionary
        self.sort_dictionary()

    def sort_dictionary(self):
        """Sorts the dictionary in *case-insensitive* lexicographic order.
        Complexity: O(N log N) where N is the number of dictionary terms."""

    def number_of_matches(self, prefix):
        """Returns the number of terms that start with the given prefix.
        Precondition: the internal dictionary is in lexicographic order.
        Complexity: O(log N) where N is the number of dictionary terms."""

    def all_matches(self, prefix):
        """Returns all terms that start with the given prefix, in descending order of weight.
        Precondition: the internal dictionary is in lexicographic order.
        Complexity: O(log N + M log M) where M is the number of matching terms."""
```

### Performance requirements

- The method `.sort_dictionary()` should make proportional to *N* log(*N*) comparisons (or better) in the worst case, where *N* is the number of terms.
- The method `.all_matches(…)` should make proportional to log *N* + *M* log(*M*) comparisons (or better) in the worst case, where *M* is the number of matching terms.
- The method `.number_of_matches(…)` should make proportional to log(*N*) comparisons (or better) in the worst case. It should not depend on *M*.
- In this context, a comparison is one usage of any comparison operator, `==`, `<`, `>=`, etc.

***Note***: You may use Python's builtin method `list.sort` — you don't have to implement sorting by yourself. You may assume that this method performs O(N log(N)) comparisons in the length N of the input array.

## Input format

We provide a number of sample input files for testing. Each file consists of a number of pairs of strings and non-negative weights. There is one pair per line, with the weight and string separated by whitespace. A weight can be any integer between 0 and 2<sup>63</sup>−1. The string can be an arbitrary sequence of Unicode characters, including spaces (but not newlines, and no spaces at the end).

- **wiktionary.txt** contains the 10,000 most common words in Project Gutenberg, with weights proportional to their frequencies.

  ```
    5627187200  the
    3395006400  of
    2994418400  and
    2595609600  to
                ...
    392402      wench
    392323      calves
  ```

- **cities.txt** contains 93,827 cities, with weights equal to their populations.

  ```
      14608512  Shanghai, China
      13076300  Buenos Aires, Argentina
      12691836  Mumbai, India
      12294193  Mexico City, Distrito Federal, Mexico
                ...
      2         Grytviken, South Georgia and The South Sandwich Islands
      2         Al Khāniq, Yemen
  ```

- **romaner.txt** contains all 83,334 [non-hapax](https://en.wikipedia.org/wiki/Hapax_legomenon) words from a selection of [69 Swedish novels](https://spraakbanken.gu.se/eng/resource/romi), with weights proportional to their frequencies.

  ```
       190569  och
       128893  att
       107002  det
       104153  i
               ...
       2       020
       2       00vad
  ```

- **gp2011.txt** contains all 261,201 non-hapax words from [Göteborgsposten 2011](https://spraakbanken.gu.se/eng/resource/gp2011), with weights proportional to their frequencies.

  ```
       476575  och
       476240  i
       414059  att
       292398  är
               ...
       2       074
       2       0565
  ```

- **nordsamiska.txt** contains 41,530 common words in [Northern Sami](https://repo.clarino.uib.no/xmlui/handle/11509/106), with weights proportional to their frequencies.

  ```
      17       soabadanráđđi
      12       láigoboađđu
      211      ovddemus
      11       tastatuvra
               ...
      12       observeret
      19       čohkiidus
  ```

## Wrapping up: The command-line client

You can test that your code works by running the command-line client **autocomplete\_cli.py**.

The client takes the name of an input file and an integer `max_matches` as arguments. It reads the data from the file; then it repeatedly reads autocomplete queries from standard input, and prints out the top `max_matches` matching terms in descending order of weight. Like this:

<pre>
$ python3 autocomplete_cli.py dictionaries/romaner.txt 5
Loaded dictionary dictionaries/romaner.txt containing 83334 words
Maximum number of matches to display: 5

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>and</i></b>
Number of matches for prefix and: 104
        7659    andra
         699    Anders
         625    Andro
         371    andre
         295    andan

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>flaggstångsknopp</i></b>
Number of matches for prefix flaggstångsknopp: 0

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>c</i></b>
Number of matches for prefix c: 929
        1032    Charles
         563    Caesar
         397    chans
         286    cigarrett
         253    Claudia

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>jav</i></b>
Number of matches for prefix jav: 7
         287    Javisst
          57    javisst
          12    Java
          10    Javisstja
           3    Javäl
</pre>

The command-line client exits when there is no more input (Windows: Ctrl-Z followed by Enter, Unix: Ctrl-D).
You may also terminate it by pressing Ctrl-C.

<pre>
$ python3 autocomplete_cli.py dictionaries/cities.txt 7
Loaded dictionary dictionaries/cities.txt containing 93827 words
Maximum number of matches to display: 7

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>gö</i></b>
Number of matches for prefix Gö: 64
      504084    Göteborg, Sweden
      122149    Göttingen, Germany
       58040    Göppingen, Germany
       57751    Görlitz, Germany
       40763    Gönen, Turkey
       34243    Göksun, Turkey
       32374    Gödöllő, Hungary

Enter search prefix (CTRL-C/D/Z to quit)
<b><i>Al M</i></b>
Number of matches for prefix Al M: 39
      431052    Al Maḩallah al Kubrá, Egypt
      420195    Al Manşūrah, Egypt
      290802    Al Mubarraz, Saudi Arabia
      258132    Al Mukallā, Yemen
      227150    Al Minyā, Egypt
      128297    Al Manāqil, Sudan
       99357    Al Maţarīyah, Egypt
</pre>

***Important***: You should get results similar to the ones above! Make sure you're returning the same number of matches, and that you use case-insensitive comparisons.

## Testing your program

We suggest that you test your program with corner cases in order to iron out bugs.
Using the dictionary `dictionaries/wiktionary.txt`, search for:
- a key that comes before all words ("!!!") or after all words ("ööööööö"),
- a key that matches only the first word ("'cause") or only the last word ("zone"),
- a key that doesn't exist, but whose prefix matches a word ("wholelotofnothing"),
- the empty key ("").

You can write these tests directly in the file you want to test, by adding something like this at the end of the file:

```python
if __name__ == '__main__':
    # run some tests...
    # if you want to use command-line arguments, you can use this:
    arguments = sys.argv[1:]
```

There are already some tests in `term.py` that you can be inspired by. 


## Your submission

Important: You may not import any library, not even standard libraries.

Push your updates of the following files to your repository on GitLab Chalmers:
  - **term.py**
  - **range\_binary\_search.py**
  - **autocompleter.py**
  - **answers.txt**, with all questions answered

When you are finished, create a tag `submission0` (for the commit you wish to submit).
For re-submissions, use `submission1`, `submission2`, etc.
The tag serves as your proof of submission.
You cannot change or delete it afterwards.
We will then grade your submission and post our feedback as issues in your project.
For more information on how to submit, see "Doing the lab assignments" on Canvas.


## Optional tasks

If you would like an extra challenge, here are some suggestions for things you could do:

- Use locales when doing the comparisons, instead of the simple lexicographic order, so that e.g. *a*, *á* and *A* are all treated as equal, but *a* and *ä* are not. Unfortunately Python does not have decent locale support, the PyICU library can handle all those things: https://pypi.org/project/PyICU/

- Calculate a frequency distribution of your own from a corpus. Corpora can e.g. be downloaded from [Språkbanken Text](https://spraakbanken.gu.se/resurser) or the [Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download).

- (advanced) Fuzzy autocomplete. This should be possible in the following (sketchy) way:
  - Create a new list ("1-deleted") with all possible results from deleting one character from the original dictionary.
      - you need to decide about a cost for deleting a character, which should be used to reduce the original term weight
  - When looking up a prefix:
      - lookup the prefix in the original dictionary
      - lookup the prefix in the list of 1-deleted terms
      - delete one character from the prefix and lookup in (1) the original dictionary, and (2) in the 1-deleted terms
  - You can do the same for 2-deleted terms, and 3-deleted terms, but notice that the number of terms will explode.

## Acknowledgements

This assignment was conceived by Matthew Drabick and Kevin Wayne (©2014), with some changes to fit this course.
