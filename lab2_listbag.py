# SYSC 2100 Winter 2023 Lab 2

# An implementation of ADT Bag that uses an instance of Python's built-in
# list type as the underlying data structure.

import random
from typing import Any

__author__ = 'Rama'
__student_number__ = '101198025'


class ListBag:

    def __init__(self, iterable=[]) -> None:
        """Initialize this ListBag.

        If no iterable is provided, the new ListBag is empty.
        Otherwise, initialize the ListBag by adding the values
        provided by the iterable.

        >>> bag = ListBag()
        >>> bag
        ListBag([])
        >>> bag = ListBag([1, 4, 3, 6, 3])
        >>> bag
        ListBag([1, 4, 3, 6, 3])
        """
        self._elems = []
        for item in iterable:
            self._elems.append(item)
            # or, self.add(item)

    def __str__(self) -> str:
        """Return a string representation of this ListBag.

        >>> bag = ListBag()
        >>> str(bag)
        '{}'
        >>> bag = ListBag([1, 4, 3, 6, 3])
        >>> str(bag)
        '{1, 4, 3, 6, 3}'

        Note: Depending on how __str__ is implemented, the order of the
        elements in the returned string may be different.
        """
        # Use the string representation of the bag's underlying list,
        # with the enclosing '[]' replaced by '{}'.
        s = str(self._elems)
        return '{' + s[1:len(s) - 1] + '}'

    def __repr__(self) -> str:
        """Return the canonical string representation of this ListBag.

        >>> bag = ListBag()
        >>> repr(bag)
        'ListBag([])'
        >>> bag = ListBag([3, 1, 2, 3, 4])
        >>> repr(bag)
        'ListBag([3, 1, 2, 3, 4])'

        Note: Depending on how __repr__ is implemented, the order of the
        list elements in the returned string may be in a different.
        """

        # For a ListBag object, obj, the expression eval(repr(obj))
        # returns a new ListBag that is equal to obj.

        return "{0}({1})".format(self.__class__.__name__, self._elems)
        # or, return self.__class__.__name__ + '(' + str(self._elems) + ')'

    def __len__(self) -> int:
        """Return the number of items in this ListBag.

        >>> bag = ListBag()
        >>> len(bag)
        0
        >>> bag = ListBag([1, 4, 3, 6])
        >>> len(bag)
        4
        """
        return len(self._elems)

    def __iter__(self) -> 'list_iterator':
        """Return an iterator for this ListBag.

        >>> bag = ListBag([3, 6, 3])
        >>> for x in bag:
        ...     print(x)
        ...
        3
        6
        3
        """
        return iter(self._elems)

    def __contains__(self, item: any) -> bool:
        """Return True if item is in this ListBag; otherwise False.

        >>> bag = ListBag()
        >>> 2 in bag
        False
        >>> bag = ListBag([1, 4, 3, 6])
        >>> 4 in bag
        True
        >>> 7 in bag
        False
        """
        return item in self._elems
    
    def add(self, item: any) -> None:
        """Add item to this ListBag.

        >>> bag = ListBag([1, 4, 3, 6])
        >>> bag.add(3)
        >>> len(bag)
        5
        >>> str(bag)
        '{1, 4, 3, 6, 3}'
        """
        self._elems.append(item)

    def count(self, item: any) -> int:
        """Return the total number of occurrences of item in this bag.

        >>> bag = ListBag([3, 1, 2, 3, 4])
        >>> bag.count(3)
        2
        >>> bag.count(7)
        0
        """
        return self._elems.count(item)

    def remove(self, item: any) -> any:
        """Remove and return one instance of item from this ListBag.

        Raises ValueError if the bag is empty.
        Raises ValueError if item is not in the bag.

        >>> bag = ListBag([3, 1, 2, 3, 4])

        # The bag has 5 elements, including two 3's.
        >>>len(bag)
        5
        >>> bag.count(3)
        2

        # Now remove one 3.
        >>> bag.remove(3)
        3
        >>> bag.count(3)
        1
        >>> len(bag)
        4
        """

        if (self._elems == []):
            raise ValueError ("bag.remove(x): remove from empty bag") 
        elif (self.count(item) == 0):
            raise ValueError ("bag.remove(x): x not in bag")
        self._elems.remove(item)
        return item
        

    def grab(self) -> any:
        """Remove and return a randomly selected item from this bag.

        Raises ValueError if the bag is empty.

        >>> bag = ListBag([3, 1, 2, 3, 4])
        >>> len(bag)
        5

        >>> ListBag.grab()
        # grab will randomly select one of items stored in the bag,
        # and remove and return that value. The value displayed in the shell
        # will be one of 1, 2, 3 or 4, depending on which item was removed.

        >>> len(bag)
        4
        """

        if (self._elems == 0 ):
            raise ValueError ("bag.grab(): grab from empty bag")
        return self._elems.pop(random.randrange(len(self._elems)))

    def __add__(self, other: 'ListBag') -> 'ListBag':
        """Return a new ListBag containing the concatenation of self and other.

        Raises TypeError if other is not a ListBag.

        >>> bag1 = ListBag([1, 3, 5])
        >>> bag2 = ListBag([2, 4, 6])
        >>> bag3 = bag1 + bag2
        >>> repr(bag3)
        'ListBag([1, 3, 5, 2, 4, 6])'

        Note: Depending on how __add__ and __repr__ are implemented, the
        order of the elements in the string returned by repr may be different.
        """
        if not isinstance(other, ListBag):
            raise TypeError('other must be a ListBag')
        elems2 = self._elems.copy()
        elems2.extend(other._elems)
        return ListBag(elems2)


    def __eq__(self, other: 'ListBag') -> bool:
        """Return True if self is equal to the ListBag referred to by other;
        otherwise return False.

        >>> bag1 = ListBag([1, 2, 3])
        >>> bag2 = ListBag([3, 2, 1])
        >>> bag1 == bag2
        True

        >>> bag1 = ListBag([1, 2, 3])
        >>> bag2 = ListBag([4, 5, 6])
        >>> bag1 == bag2
        False
        """
        if not isinstance(other, ListBag):
            return False
        return sorted(list(self)) == sorted(list(other))
