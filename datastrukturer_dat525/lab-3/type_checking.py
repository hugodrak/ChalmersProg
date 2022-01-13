"""Functions to help with type checking.

You do not need to read or understand this code!"""

from pathlib import Path
from ngram import Ngram
from hash_table import HashTable

class TypeError(Exception):
    pass

def error(where, *msgs):
    raise TypeError("\n".join(["", "Type error in '%s'" % where, *msgs]))

    if result is not None:
        raise TypeError("Type checking failed for variable '%s'!\n\n%s" % (name, result))

def check_dict(name, it, key_type, value_type, key_strict=False):
    if not isinstance(it, dict) and not isinstance(it, HashTable):
        error(name,
              "It should be a dict or HashTable",
              "But instead it has type %s" % type(it).__name__)

    for key in it:
        if not isinstance(key, key_type) or (key_strict and type(key) != key_type):
            error(name,
                  "It should contain keys of type %s" % key_type.__name__,
                  "But it contains a key of type %s" % type(key).__name__,
                  "Key: %r" % (key,))

        value = it[key]
        if not isinstance(value, value_type):
            error(name,
                  "It should contain values of type %s" % value_type.__name__,
                  "But it contains a value of type %s" % type(value).__name__,
                  "Key: %r" % (key,),
                  "Value: %r" % (value,))

def check_value(name, it, item_type):
    for key in it:
        value = it[key]

        for item in value:
            if not isinstance(item, item_type):
                error(name,
                      "It should contain values of type list[%s]" % item_type.__name__,
                      "But one of the items in the list has type %s" % type(item).__name__,
                      "Key: %r" % (key,),
                      "Value: %r" % (value,),
                      "Item: %r" % (item,))

def check_key_pair(name, it, item_type):
    for tup in it:
        if len(tup) != 2:
            error(name,
                  "It should contain keys of type tuple[%s, %s]" % (item_type.__name__, item_type.__name__),
                  "But one of the keys is a tuple of length %d" % len(tup),
                  "Key: %r" % (tup,))

        key1, key2 = tup

        if not isinstance(key1, item_type) or not isinstance(key2, item_type):
            error(name,
                  "It should contain keys of type tuple[%s, %s]" % (item_type.__name__, item_type.__name__),
                  "But one of the items in the list has type tuple[%s, %s]" % (type(key1).__name__, type(key2).__name__),
                  "Key: %r" % (tup,))

def check_files(files):
    check_dict("files", files, Path, list)
    check_value("files", files, Ngram)

def check_index(index):
    check_dict("index", index, Ngram, list)
    check_value("index", index, Path)

def check_similarity(similarity):
    check_dict("similarity", similarity, tuple, int, key_strict=True)
    check_key_pair("similarity", similarity, Path)

def check_most_similar(most_similar):
    if not isinstance(most_similar, list):
        error("most_similar",
              "It should be a list",
              "But instead it has type %s" % type(most_similar).__name__)

    for item in most_similar:
        if not isinstance(item, tuple):
            error("most_similar",
                  "It should contain items of type tuple[Path, Path]",
                  "But it contains an item of type %s" % type(key).__name__,
                  "Item: %r" % (item,))

        if len(item) != 2:
            error("most_similar",
                  "It should contain items of type tuple[Path, Path]"
                  "But one of the items is a tuple of length %d" % len(item),
                  "Item: %r" % (item,))

        item1, item2 = item

        if not isinstance(item1, Path) or not isinstance(item2, Path):
            error(name,
                  "It should contain items of type tuple[Path, Path]",
                  "But one of the items in the list has type tuple[%s, %s]" % (type(item1).__name__, type(item2).__name__),
                  "Item: %r" % (item,))
