# SYSC 2100 Winter 2023 Lab 3

# An implementation of ADT Bag that uses a fixed-capacity array as the
# underlying data structure.

import ctypes
import random

__author__ = 'Rama Alkhouli'
__student_number__ = '101198025'


class ArrayBag:

    class _ArrayBagIterator:
        """Supports iteration over ArrayBag objects.

        See: https://docs.python.org/3/library/stdtypes.html#iterator-types
        """

        def __init__(self, bag: 'ArrayBag') -> None:
            """Initialize the iterator for the bag.
            """
            # The iterator accesses the bag's backing array directly.
            self.backing_array = bag._elems
            self.num_items = bag._num_items
            self.index = 0

        # Iterator objects must support the iterator protocol (methods
        # __next__ and __iter__.)

        def __next__(self) -> any:
            """Return the next item from this iterator.

            Raises StopIteration if there are no further items to return.
            """
            if self.index < self.num_items:
                item = self.backing_array[self.index]
                self.index += 1
                return item

            raise StopIteration

        def __iter__(self) -> '_ArrayBagIterator':
            """Return the iterator object itself."""
            return self

    def __init__(self, iterable=[]) -> None:
        """Initialize this ArrayBag.

        If no iterable is provided, the new ArrayBag is empty.
        Otherwise, initialize the ArrayBag by adding the values
        provided by the iterable.

        >>> bag = ArrayBag()
        >>> bag
        ArrayBag([])
        >>> bag = ArrayBag([1, 4, 3, 6, 3])
        >>> bag
        ArrayBag([1, 4, 3, 6, 3])
        """
        self._num_items = 0  # of elements stored in the ArrayBag
        self._elems = _new_array(1)  # backing array

        # Note: len(self._elems) is the capacity of the backing array,
        # and not the number of items in the ArrayBag.
        # The capacity of the backing array is always >= the number of items
        # in the ArrayBag.

        for elem in iterable:
            self.add(elem)
            # add() updates self._num_items and increases the capacity of
            # the backing array, as required.

    def __str__(self) -> str:
        """Return a string representation of this ArrayBag.

        >>> bag = ArrayBag()
        >>> str(bag)
        '{}'
        >>> bag = ArrayBag([1, 4, 3, 6, 3])
        >>> str(bag)
        '{1, 4, 3, 6, 3}'

        Note: Depending on how __str__ is implemented, the order of the
        elements in the returned string may different.
        """
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "{{{0}}}".format(", ".join([repr(x) for x in self]))

    def __repr__(self) -> str:
        """Return the canonical string representation of this ArrayBag.

        >>> bag = ArrayBag()
        >>> repr(bag)
        'ArrayBag([])'
        >>> bag = ArrayBag([3, 1, 2, 3, 4])
        >>> repr(bag)
        'ArrayBag([3, 1, 2, 3, 4])'

        Note: Depending on how __repr__ is implemented, the order of the
        elements in the returned string may be in a different.
        """

        # For a ArrayBag object, obj, the expression eval(repr(obj))
        # returns a new ArrayBag that is equal to obj.

        return "{0}([{1}])".format(self.__class__.__name__,
                                   ", ".join([repr(x) for x in self]))

    def __len__(self) -> int:
        """Return the number of items in this ArrayBag.

        >>> bag = ArrayBag()
        >>> len(bag)
        0
        >>> bag = ArrayBag([1, 4, 3, 6])
        >>> len(bag)
        4
        """
        return self._num_items

    def __iter__(self) -> '_ArrayBagIterator':
        """Return an iterator for this ArrayBag.

        >>> bag = ArrayBag([3, 6, 3])
        >>> for x in bag:
        ...     print(x)
        ...
        3
        6
        3
        """
        return ArrayBag._ArrayBagIterator(self)

    def __contains__(self, item: any) -> bool:
        """Return True if item is in this ArrayBag; otherwise False.

        >>> bag = ArrayBag()
        >>> 2 in bag
        False
        >>> bag = ArrayBag([1, 4, 3, 6])
        >>> 4 in bag
        True
        >>> 7 in bag
        False
        """
        for i in range(len(self)):
            if self._elems[i] == item:
                return True
        return False

    def add(self, item: any) -> None:
        """Add item to this ArrayBag.

        >>> bag = ArrayBag([1, 4, 3, 6])
        >>> bag.add(3)
        >>> len(bag)
        5
        >>> str(bag)
        '{1, 4, 3, 6, 3}'
        """
        if len(self) == len(self._elems):
            # The backing array is full, so replace it with one that
            # has more capacity.
            self._resize()

        self._elems[self._num_items] = item
        self._num_items += 1

    def count(self, item: any) -> int:
        """Return the total number of occurrences of item in this bag.

        >>> bag = ArrayBag([3, 1, 2, 3, 4])
        >>> bag.count(3)
        2
        >>> bag.count(7)
        0
        """
        counter = 0
        for i in range(len(self)):
            if self._elems[i] == item:
                counter +=1
        return counter

    def remove(self, item: any) -> any:
        """Remove and return one instance of item from this ArrayBag.

        Raises ValueError if the bag is empty.
        Raises ValueError if item is not in the bag.

        >>> bag = ArrayBag([3, 1, 2, 3, 4])

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

        if self._num_items == 0:
            raise ValueError("bag.remove(item): remove from empty bag")
        if item not in self._elems:
             raise ValueError("bag.remove(item): item is not in bag")
        
        # find index of item 
        i = 0
        for x in range(len(self)):
            if self._elems[x] == item:
                break
            i += 1
            
        # store the item to be removed
        removed_item = self._elems[i]

        # remove item
        self._elems[i:self._num_items - 1] = self._elems[i + 1:self._num_items]
        self._num_items -= 1
        if len(self._elems) >= 3 * len(self):
            self._resize()
        
        return removed_item
               


    def grab(self) -> any:
        """Remove and return a randomly selected item from this bag.

        Raises ValueError if the bag is empty.

        >>> bag = ArrayBag([3, 1, 2, 3, 4])
        >>> len(bag)
        5

        >>> ArrayBag.grab()
        # grab will randomly select one of items stored in the bag,
        # and remove and return that value. The value displayed in the shell
        # will be one of 1, 2, 3 or 4, depending on which item was removed.

        >>> len(bag)
        4
        """
        if self._num_items == 0:
            raise ValueError("bag.grab(): grab from empty bag")
        random_item = random.randint(0, len(self)-1)
        self.remove(random_item)
        

    def __add__(self, other: 'ArrayBag') -> 'ArrayBag':
        """Return a new ArrayBag containing the concatenation of self and other.

        Raises TypeError if other is not a ArrayBag.

        >>> bag1 = ArrayBag([1, 3, 5])
        >>> bag2 = ArrayBag([2, 4, 6])
        >>> bag3 = bag1 + bag2
        >>> repr(bag3)
        'ArrayBag([1, 3, 5, 2, 4, 6])'

        Note: Depending on how __add__ and __repr__ are implemented, the
        order of the elements in the string returned by repr may be different.
        """
        if not isinstance(other, ArrayBag):
            raise ValueError("can only concatenate ArrayBag to ArrayBag")
        
        # newBag = ArrayBag()
        # n = len(self) + len(other)
        # newBag._elems = _new_array(n)
        # newBag._elems[0:len(self)] = self._elems[0:len(self)]
        # newBag._elems[len(self):n] = other._elems[0:len(other)]
        # newBag._num_items = n
        # return newBag
        # create arraybag with copying elemnts from arraBag self
        newBag = ArrayBag(self)
        # loop through other + add items to newBag
        for item in other:
            newBag.add(item)

        return newBag

    def __eq__(self, other: 'ArrayBag') -> bool:
        """Return True if self is equal to the ArrayBag referred to by other;
        otherwise return False.

        >>> bag1 = ArrayBag([1, 2, 3])
        >>> bag2 = ArrayBag([3, 2, 1])
        >>> bag1 == bag2
        True

        >>> bag1 = ArrayBag([1, 2, 3])
        >>> bag2 = ArrayBag([4, 5, 6])
        >>> bag1 == bag2
        False
        """
        if not isinstance(other, ArrayBag):
            return False
        if len(other) != len(self):
            return False
        for i in range(len(self)):
            for j in range(len(other)):
                if self._elems[i] != other._elems[j]:
                    j += 1     
            return False
            i +=1
            
        return True

        # lst1 = list(self)
        # lst2 = list(other)
        
        # if sorted(lst1) == sorted(lst2):
        #     return True
        # else:
        #     return False
        
        

    def _resize(self) -> None:
        """Change this ArrayBag's capacity to 2 * n, where n is the number of
        elements in the bag. If the bag is empty, change its capacity to 1.
        """
        # Allocate a new array with the required capacity.
        arr = _new_array(max(1, 2 * self._num_items))

        # Copy the _num_items elements in the current backing array to the
        # new array.
        arr[0:self._num_items] = self._elems[0:self._num_items]

        # Replace the current backing array.
        self._elems = arr


def _new_array(capacity: int) -> 'py_object_Array_<capacity>':
    """Return a new array with the specified capacity that stores
    references to Python objects. All elements are initialized to None.

    >>> arr = _new_array(10)
    >>> len(arr)
    10

    >>> for i in range(10):
    ...      a[i] = 2 * i
    ...

    >>> arr[0]
    0
    >>> arr[9]
    18

    >>> 4 in arr
    True
    >>> 3 in arr
    False
    """
    if capacity <= 0:
        raise ValueError('new_array: capacity must be > 0')

    PyCArrayType = ctypes.py_object * capacity
    a = PyCArrayType()
    for i in range(len(a)):
        a[i] = None

    return a
