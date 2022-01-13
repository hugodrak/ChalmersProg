# Lab 3: Plagiarism detection

In this lab your task is to modify a plagiarism detection program so
that it makes better use of data structures. You will also implement a
linear probing hash table and experiment with making a good hash function.

## About the labs

- The lab is part of the examination of the course. Therefore, you must not copy code from or show code to other groups. You are welcome to discuss ideas with one another, but anything you do must be **the work of you and your lab partners**.
- Please read the pages "Doing the lab assignments" and "Running the labs" on Canvas.

## Background

You are head of the Anti-Cheating Department at Palmers University of Mythology, where you are in charge of catching students who copy each others' work.

You recently bought a very expensive *plagiarism detection program*. The program has the following job: it reads in a set of documents, finds similarities between them, and reports all pairs of documents that seem suspiciously similar.

You were very impressed with the program when you saw the salesperson demonstrate it on some small examples. Unfortunately, once you bought the program you realised that *it is extremely slow when given a large number of documents to check*. Reading the source code, you noticed that the program does not use appropriate data structures and therefore its time complexity is poor. (At Palmers University of Mythology, employees are expected to have taken a Data Structures course.)

In this lab, your task is to *speed up the plagiarism detection program* so that it works on much larger document sets. The lab has three parts:

1. Analyse the time complexity of the plagiarism detection program.
2. Speed up the program by modifying it to use appropriate data
   structures - in particular, a Python dictionary (a *map*).
3. Learn more deeply how Python dictionaries work, by implementing
   a *linear probing hash table* and a *hash function*.

## Getting started

Your first task is to make sure that you can run the plagiarism detection program.

The Lab contains Python source files, a directory `documents` containing sample text, and a file `answers.txt` where you will write down answers to questions in the lab. There are four document sets of various sizes called `small`, `medium` and `big`. All the document sets are collections of Wikipedia pages (downloaded automatically by following random links from a starting page).

`lab3.py` contains the main program. It requires a program
argument, which should be the name of a directory containing plain
text files to check.

Now run `lab3.py` on the document set `tiny`, by running the command

```
python3 lab3.py documents/tiny
```

After a few seconds, you should see the following output (probably with different timings):

```
Reading all input files took 0.01 seconds.
Building n-gram index took 0.00 seconds.
Computing similarity scores took 7.80 seconds.
Finding the most similar files took 0.00 seconds.
In total the program took 7.82 seconds.

Hash table statistics:
  files: dictionary, size 5
  index: dictionary, size 0
  similarity: dictionary, size 10

Plagiarism report:
   80 similarity: Find me.txt and Plagiarism.txt
   52 similarity: Find me.txt and Rogeting.txt
   30 similarity: Find me.txt and To be, or not to be.txt
```

The program's main output is the plagiarism report at the bottom. The report lists *pairs* of files which have similar content, together with a number indicating how similar they are (the next section describes how this number is calculated). Here we can see that "Find me.txt" has similar content to several other files. In fact, if you look in these files you will see that "Find me.txt" is heavily plagiarised. "Hamlet.txt" and "To be, or not to be.txt" are also similar, but not plagiarised.

We also see some performance statistics, including timings for the various phases of the program. We see that in total, the program took 7.82 seconds to run, and that almost all the time is in what is reported as "computing similarity scores". Finally, we see statistics about the size of the different hash tables used by the program, which will be useful later.

Now try running the program on the `small` directory, which is about three times as big. You will find that it takes a while. Go on and read the next section while you wait! Once the program is finished, write down how long it took – you will need the answer later.

## How the program measures similarity

One way to measure the similarity of two documents is to count how many words they have in common. However, this approach leads to false positives because the same set of words can be used in two very different documents. A better way is to count n-grams. An n-gram is a sequence of n consecutive words in a document or string. For example, the string "the fat cat sat on the mat" contains the 5-grams "the fat cat sat on", "fat cat sat on the" and "cat sat on the mat".

Given two documents, we will define their similarity score as the number of unique 5-grams that appear in both documents - that is, the size of the intersection of the two documents' sets of 5-grams. For example, "the fat cat's hat sat on the mat" and "the cat's hat sat on the mat" have two 5-grams in common – "cat's hat sat on the" and "hat sat on the mat" – and therefore have a similarity score of 2. A high similarity score means that a lot of content is shared between the documents, and is a possible sign of plagiarism.

## How the program works

The plagiarism detection program consists of the following files:

- `lab3.py`: the main program.
- `ngram.py`: a class for N-grams.
- `hash_table.py`: a hash table implementation. Unfinished; you will complete it later.

There are also some extra files used by the lab code: `type_checking.py`,
`hash_tester.py` and `stopwatch.py`. *You do not need* to look at or
understand these files.

The program uses a simple heuristic to detect plagiarism: *any pair of files with a similarity score of at least 30 is suspicious*. Its basic algorithm is: find all such pairs of files, and print them out, sorted in decreasing order of similarity. In case there are many results, only the top 50 are printed.

In order to implement this algorithm, `lab3.py` builds two main data structures, both of which are maps:

- `files: dict[Path, list[Ngram]]`: a map that contains the contents of all input documents.
  The key is a filename, and the value is a list containing all 5-grams of that file.

  Note that:

  - Filenames are represented using the built-in `Path` class, but you do not have to know anything about this class.
  - n-grams are represented using the `Ngram` class implemented in
    `ngram.py`. You will work with this file later in the lab.

- `similarity: dict[tuple[Path, Path], int]`: a map that contains the similarity scores of all document pairs. The key is a *pair* of filenames (stored as a Python tuple), and the value is the similarity score of those two files.

For example, suppose that we have two files: `A` contains "the fat cat
sat on the mat", and `B` contains "a cute cat sat on the mat". If we
pretend that `Path`s and `Ngrams` are just strings, then the contents
of the maps would be as follows:

```
files =
  {"A": ["the fat cat sat on", "fat cat sat on the", "cat sat on the mat"],
   "B": ["a cute cat sat on", "cute cat sat on the", "cat sat on the mat"]}
similarity = {("A", "B"): 1}
```

Here, the similarity score is 1 because `A` and `B` have one 5-gram in
common.

In the text above, `dict[Path, list[Ngram]]` is a Python type
declaration. If you haven't seen these before, [here is a
cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html#built-in-types).
In this case, it declares that `files` is a dictionary, where the keys
are objects of class `Path`, and the values are lists where each
element is of class `Ngram`. In the other type declaration,
`tuple[Path, Path]` means a tuple `(p1, p2)` where both `p1` and `p2`
are objects of class `Path`.

In more detail, `lab3.py` consists of four functions (plus a main function), each of which is called in turn:

1. `read_paths`: Reads in each document and computes its 5-grams.
   Returns the map `files: dict[Path, list[Ngram]]`.
2. `build_index`: currently does nothing! You will add code to this function later.
3. `find_similarity`: Computes the similarity score of each pair of documents.
   Returns the map `similarity: dict[tuple[Path, Path], int]`.
4. `find_most_similar`: Given the map `similarity`, produces a list of
   all (unordered) pairs of files having similarity at least 30,
   sorted in decreasing order of similarity, and only including the
   top 50 results. Returns a sorted list of pairs: `list[tuple[Path, Path]]`.

The `main` function executes these four functions in turn, then simply
prints out each pair of files returned by `find_most_similar` together
with its similarity (which can be found in the `similarity` map).

**Why is it slow?** In the output above, most of the time was spent in the "Computing similarity scores" step. This corresponds to `find_similarity`, step 3 in the algorithm above. The `find_similarity` function is currently programmed using the following brute-force algorithm:

```
for each document d1:
    for each document d2 ≠ d1:
        for each 5-gram n1 in d1:
            for each 5-gram n2 in d2:
                if n1 = n2:
                    increase the similarity of d1 and d2 by 1
```

Make sure you understand how this algorithm works. Also, read the source code for `find_similarity` and make sure you understand that too. (Ignore the unused `index` parameter to that function for now.)

You can see lots of nested loops here which should be a warning sign for *bad complexity*! As we saw, most of the program's runtime is spent executing this algorithm. If we want to run `lab3.py` on larger document sets, we will have to eliminate this brute force search!

### Task 1: Complexity analysis

Now answer the following questions (write your answers in the answers.txt file provided).

- What is the asymptotic complexity of `find_similarity`?
  Your answer should be in terms of *N*, where *N* is the total number of 5-grams in the document set.

  You may assume that all documents are the same length (have the same
  number of 5-grams). You may also assume that operations on dynamic
  arrays (lists in Python) and hash tables (dictionaries in Python)
  have their usual complexity, and the hash functions used are good
  quality.

  **Hint:** If you get stuck, try analysing it the following way: let *D* be the number of documents and *K* be the number of 5-grams per document. First find an expression for the complexity in terms of both *D* and *K*. Then use the fact that *N = D·K* to find an expression purely in terms of *N*.

- Here are the approximate number of 5-grams in the four document sets: `tiny` (*N* = 6,000), `small` (*N* = 20,000), `medium` (*N* = 200,000), and `big` (*N* = 2,000,000). How long did the program take to run on the `tiny` and `small` directories? Is the ratio between the runtimes roughly as you would expect, given the complexity? Explain very briefly why.

- How long do you predict the program would take to run on the `big` directory?

## Using the right data structure

The `find_similarity` function is slow because it has to search through
all pairs of 5-grams, even though it only wants the pairs that are equal.
Let's fix this by improving the program's use of data structures.

The data structure you will add is an index that, given a 5-gram,
allows us to figure out which files contain that 5-gram. We can
represent this index as a map (dictionary) where the key is a 5-gram
and the value is a list of all filenames that contain the 5-gram:

```
index: dict[Ngram, list[Path]]
```

In the small example above with files `A` and `B`, the map would look
as follows:
```
index =
  {"the fat cat sat on": ["A"],
   "fat cat sat on the": ["A"],
   "cat sat on the mat": ["A", "B"],
   "a cute cat sat on": ["B"],
   "cute cat sat on the": ["B"]}
```

In fact, `lab3.py` contains a declaration for just such a map. The `build_index` function is supposed to create an index. The index returned by `build_index` is then passed in to `find_similarity`. However, currently `build_index` does not build the index (it returns an empty map) and `find_similarity` does not bother to use it.

### Task 2: Make use of an index

Here is your task:

* Finish the implementation of `build_index`. You have access to the
  parameter `files: dict[Path, list[Ngram]]`, which contains the
  5-grams of each file, as described above. The function should
  return a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
  `index: dict[Ngram, list[Path]]` containing all 5-grams containing
  in all input files; the value associated with a 5-gram should be
  the list of files containing that 5-gram (in any order).

  You do not need to modify any functions except for `build_index` and `find_similarity`. In fact, you do not even need to understand the code of the other functions (although it does not hurt to read them).

To help you catch bugs, `lab3.py` contains some code that checks the
types of your dictionaries at runtime. If there is a type error, you
will get an error message giving the name of the variable, and an
explanation of what is wrong with it.

When you are finished, re-run your program, and make sure it gives the
same results as before. It previously may have taken a minute or two
to run on the `small` directory, but now it should be almost instant.
Run the program on the `medium` and `big` directories too - make sure
that it works, and notice that it runs pretty quickly! Just by using
the right data structures, you have taken a program that would take
*days* to run on the `big` directory, and reduced it to *seconds*.

**Complexity analysis.** Now re-do the complexity analysis that you did earlier by answering the following question:

- What is the time complexity of running `build_index` followed by `find_similarity`? You may make the following assumptions:

  * The document set contains a total of *N* 5-grams.
  * There is not much plagiarised text; specifically, most 5-grams
    occur in one file only. The number of 5-grams that occur in more
    than one file is a *small constant*.
  * Operations on dynamic arrays (lists in Python) and hash tables
    (dictionaries in Python) have their usual complexity, and the hash
    functions used are good quality.

  Your answer should be a single formula representing the total runtime of `build_index` and `find_similarity`.

Here is an **optional extra question**:

- In our complexity analysis, suppose we drop the assumption that there is not much plagiarised text. What is the program's complexity in terms of *N* and *S*, where *S* is the total similarity score across all pairs of files?

## Implementing a hash table and hash function

Now you know that using dictionaries appropriately can have a huge
impact on your program's performance. In this part of the lab, you
will learn how a dictionary can be implemented. You will implement a
hash table using linear program, and your own hash function.

*Note:* Python dictionaries are hash tables - but the code for them is
implemented in C! Your hash table will be implemented in Python, so
will be *quite a lot slower* than the built-in Python dictionaries.
That's OK: the goal for this task is for you to understand hash tables
better, not to make the world's fastest hash table. In a real Python
project, you would use the built-in dictionaries rather than making
your own hash table class.

### Task 3: Implement hash tables with linear probing

In `hash_table.py`, you will find an *unfinished* implementation of a
hash table. Your job is to finish the implementation, and use it in
`lab3.py`. You will make a hash table that uses *linear probing*.

Start by changing `lab3.py` so that it uses the `HashTable` class
rather than the built-in Python dictionaries. To do so, in all the
places where you create a hash table by writing `some_variable = {}`,
change it to read `some_variable = HashTable()`. That might be all you
need to do, since the `HashTable` class supports the same syntax as
Python dictionaries. If `table` is a `HashTable` object, then you can
write:

* `table[x]` to look up the key `x`
* `table[x] = y` to update the key `x`
* `x in table` to check if a key is present
* `for x in table:` to loop through all keys

so you may not need to change anything else in the code. However, the
program will crash because the `HashTable` class is not yet fully
implemented. The next task is to finish implementing it!

`HashTable` is a class with three fields:

* `_keys` and `_values` are the hash table itself (the array).
  `self._keys[i]` stores either a key, or `None` if there is no key
  at that position. `self._values[i]` stores the associated value.
* `_size` is the number of keys currently stored in the hash table.

Looking at `hash_table.py`, you will find that most of the code is
done, but two methods are not implemented (rather, they raise a
`NotImplementedError`). Your job is to implement these two methods!
Here are the two methods you need to implement:

- `_probe(self, key)` takes a key, and returns the index where the key
  should be stored in the hash table, using linear probing.
  There are two cases:

  - If the key is present, it returns the position where it is
    currently stored.
  - Otherwise, it returns the position where the key *would*
    be stored if we now added it to the hash table.

  Some tips for implementing `_probe`:
  - `hash(key)` gives the hash code for `key`.
  - `len(self._keys)` gives the size of the array, and `%` is the
    modulo operator in Python.
  - If there is no key stored at index `i`, then `self._keys[i]` will
    be `None`.

- `put(self, key, value)` adds a key-value pair to the hash table,
  If `key` is already present in the hash table, it updates the
  corresponding value to `value`. Here are some tips:

  - Use `_probe` to find out the correct index.
  - Read the code for `get` for inspiration.
  - Make sure to increment `_size` when you add a new key.
  - You will need to grow the array if the load factor gets too high.
    To help you do this, there is a method `self._resize()` which grows the
    array (without checking the load factor), and a method
    `self._load_factor()` which calculates the load factor.
    Use `self._max_load_factor` (without parentheses) to get the
    maximum load factor.

As mentioned above, expect your hash table implementation to be much
slower than Python's built-in dictionaries - for example 10x slower is
normal. After you are finished implementing the hash table, check that
`lab3.py` still works on at least the `medium` document set.

#### Testing your implementation

You will probably make some mistakes when implementing the hash table
class! To help you find them, there is a testing script,
`hash_tester.py`. To use it, just run:

```
python3 hash_tester.py
```

The script will try calling your `get` and `put` functions in
different combinations, and will also check the hash table invariant
(e.g. that every key is stored in the correct location). If it finds a
bug, it will print out a piece of code that demonstrates the problem.

Even if your hash table seems to work, make sure to run
`hash_tester.py` before you submit the lab.

#### Looking at the number of collisions

When you run `lab3.py` you will see some statistics about the hash
tables, for example:

```
Hash table statistics:
  files: Hash table, size 953, capacity 3072, load factor 0.31, average distance 0.23, max distance 7
  index: Hash table, size 2061519, capacity 6291456, load factor 0.33, average distance 0.24, max distance 16
  similarity: Hash table, size 27084, capacity 98304, load factor 0.28, average distance 0.19, max distance 10
```

This shows:

* *size*: the number of keys in the hash table
* *capacity*: the capacity of the underlying array
* *load factor*: the current load factor
* *average distance*: the difference *on average* that a key is stored
  from its ideal position (if a key is stored in its ideal position,
  the distance is 0)
* *max distance*: the difference from the ideal position for the
  *worst-placed* key, i.e. the one further from its ideal position

Run `lab3.py` on the `big` document set and, with the help of the
statistics it prints out, answer this question:

- Assume that we call `index.get` on a random key which is present in
  the hash table. How many array accesses are needed on average to
  find the key? And how many in the worst case? Explain how you got
  your answer.

  Include the hash table statistics from `lab3.py documents/big` in
  your answer. Answer with a number calculated for that document set.

### Task 4: Improve a hash function

In `ngram.py`, you will find the implementation of the n-gram class.
An n-gram is represented as an n-tuple of strings, stored in the
`self.words` variable. The method that computes the hash code is
`__hash__`; currently it calls `hash(self.words)`, which just invokes
Python's built-in hash function for tuples.

Now you will see the effect of a *bad* hash function. Delete the line
`return hash(self.words)` and uncomment the code directly below,
marked "Bad hash function". This code computes a hash by adding the
character codes of all characters in the n-gram. Re-run the program on
the `tiny` dataset - it's really slow! Look at the "Hash table
statistics" section of the output and figure out why.

Your final task is to improve this hash function! How you do this is
up to you, except that you may not call Python's built-in `hash`. Note
that *the program will still run slowly, because the hash function is
implemented in Python instead of C as it was before*. Your goal is not
to improve the runtime of the program, but to *reduce the number of
hash collisions*.

Your goal is to get an average distance of *less than 2* when running
your code on the `small` document set. (You may need to start testing
on `tiny`, until the hash function is reasonably good.) If the hash
function is good enough, it should also work on `medium`, but this is
not compulsory.

Tips:

- Design it so that when you swap two words of the n-gram, the hash
  value usually changes. Also when you swap two letters of a word.
- Make sure that the hash function can return relatively large
  numbers. This is important when the array is large, so that larger
  indexes in the array can be used.
  (This is one reason why just adding the character codes is so bad!)
- Rather than only looking at the character codes, one idea would be
  to also look at the position where each character occurs in the
  n-gram. If you want to do this, the
  [`enumerate` function](https://book.pythontips.com/en/latest/enumerate.html)
  could be useful.
- Look at the lectures for ideas!

Now answer the following question (write your answers in the answers.txt file provided).

- How did you improve the hash function?
  Briefly explain why your design gives a better distribution than the
  bad hash function.

## Looking back on what you have done

By introducing an extra data structure (an index from n-grams to files), you managed to speed up the execution of the plagiarism detection program enormously. You can check a document set in seconds that would have taken hours before, just by introducing one index. These are the kind of gains you get by basing your program on suitable data structures.

With some patience, you could now check a much larger set of documents – say 1GB. This might take an hour or so – but in the version of the program you started with, it would have taken about *5 years*!

We also saw that almost all of the program's runtime was spent in one small subtask. Seeing that our program was slow, it would have been a total waste of time to optimise the part that reads in the files, or that ranks the similarity scores. On the other hand, by focusing on the right part of the program, huge gains were possible. Try to remember Knuth's famous quote:

- "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%."

You also implemented linear probing hash tables, and saw that they
perform well - at 50% load factor, an item can be looked up with on
average 1-2 array accesses. But it requires a good hash function!
In reality, you should use Python's dictionaries rather than making
your own - they've been carefully tuned and optimised! When
programming, make sure you know your programming language's standard
library of data structures.

(Python dictionaries use linear probing, but with a twist. In most
linear probing implementations, when there is a collision, we go
forward by 1 position in the array (we say that the *probing constant*
is 1). However, in Python, the probing constant is calculated from the
item's hash code. This reduces collisions when the hash function is
lower-quality. If you're interested you can read the full details
[here](https://github.com/python/cpython/blob/main/Objects/dictobject.c#L139).)

Of course, a real plagiarism detection program should have many more features, and some possible feature ideas are listed below - but when processing text on this scale, behind every fancy detection feature there needs to be a smart data structure!

## Your submission

Push your updates of the following files to your repository on GitLab Chalmers:
- `lab3.py`
- `hash_table.py`
- `ngram.py`
- `answers.txt`, with all (non-optional) questions answered

When you are finished, create a tag `submission0` (for the commit you wish to submit).
For re-submissions, use `submission1`, `submission2`, etc.
The tag serves as your proof of submission. You cannot change or delete it afterwards. We will then grade your submission and post our feedback as issues in your project. For more information on how to submit, see "Doing the lab assignments" on Canvas.

## Lots of optional tasks

Here are a few ideas for things to do if you want to learn more. These are just a few possible starting points – robust plagiarism detection is a difficult and open-ended problem!

- Implement a different probing method, such as
  [Robin Hood hashing](https://programming.guide/robin-hood-hashing.html) or
  [quadratic probing](https://en.wikipedia.org/wiki/Quadratic_probing#Alternating_signs).
  See how they compare to linear probing when the load factor is high
  (> 90%).

- Calculate what n-grams are most common and least common. When scoring similarity, weight less common shared n-grams higher. Or weight n-grams using [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).

- Rather than just counting how many 5-grams two documents have in common, count n-grams for lots of different values of n simultaneously. Harder: measure similarity by the *longest* n-gram that two documents have in common. (I'm not sure how to do this efficiently! Perhaps there is some clever way using a suffix tree?)

- Make the similarity score more robust. For example, figure out how to catch plagiarists who use a thesaurus to replace words by synonyms (is there a way for the program to normalise texts, e.g., replacing each word by its "best" synonym?) Similarly, deleting or inserting words from the text reduces the number of matching n-grams – can we fix that?

- Can this method be used to find plagiarised code? One problem is that many files often contain the same standard boilerplate (e.g. licence text, standard loop structures, ...), which leads to high plagiarism scores - can this be fixed?

## Acknowledgements

This lab is inspired by the "Catching Plagiarists" lab by Baker Franke.
