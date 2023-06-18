# SYSC 2100 Winter 2023 Lab 4

# Class ArrayList is an implementation of ADT List that uses an array as the
# underlying data structure. The iterator is implemented by a generator.

import ctypes  # To create the backing array.

__author__ = 'Rama Alkhouli'
__student_number__ = '101198025'


class ArrayList:

    def __init__(self, iterable=[]) -> None:
        """Initialize this ArrayList.

        If no iterable is provided, the new ArrayList is empty.
        Otherwise, initialize the ArrayList by appending the values
        provided by the iterable.

        >>> lst = ArrayList()
        >>> lst
        ArrayList([])
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst
        ArrayList([1, 4, 3, 6])
        """
        self._num_items = 0  # of elements stored in the ArrayList
        self._elems = _new_array(1)  # backing array

        # Note: len(self._elems) is the capacity of the backing array,
        # and not the number of items in the ArrayList.
        # The capacity of the backing array is always >= the number of items
        # in the ArrayList.

        for elem in iterable:
            self.append(elem)
            # append() updates self._num_items and increases the capacity of
            # the backing array, as required.

    def __str__(self) -> str:
        """Return a string representation of this ArrayList.

        >>> lst = ArrayList()
        >>> str(lst)
        '[]'
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> str(lst)
        '[1, 4, 3, 6]'
        """
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "[{0}]".format(", ".join([repr(x) for x in self]))

        # The above statement is equivalent to this code:
        #
        # Form a list containing the repr string representations of all the
        # elements in the ArrayList:
        #
        # tmp = []
        # for x in self:
        #     tmp.append(repr(x))
        #
        # Concatenate all the strings in tmp into a single string, with ", "
        # between each one:
        #
        # s = ''
        # for i in range(len(tmp)):
        #    s += tmp[i]
        #    #  Append a trailing comma-space after all but the last element.
        #    if i < len(tmp) - 1:
        #        s += ', '
        #
        # Create and return the string with the format:
        # '[elem1, elem2, elem3, ...]'
        #
        # return "[{0}]".format(s)

    def __repr__(self) -> str:
        """Return the canonical string representation of this ArrayList.

        >>> lst = ArrayList()
        >>> repr(lst)
        'ArrayList([])'
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> repr(lst)
        'ArrayList([1, 4, 3, 6])'
        """
        # For an ArrayList object, obj, the expression eval(repr(obj))
        # returns a new ArrayList that is identical to obj.
        return "{0}({1})".format(self.__class__.__name__, str(self))

    def __len__(self) -> int:
        """Return the number of elements in this ArrayList.

        >>> lst = ArrayList()
        >>> len(lst)
        0
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> len(lst)
        4
        """
        return self._num_items

    def __iter__(self):
        """Return an iterator for this ArrayList.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> for x in lst:
        ...     print(x)
        ...
        1
        4
        3
        6
        """
        for i in range(len(self)):
            yield self[i]   # equivalent to self.__getitem__(i)

            # We could instead access the backing array directly; i.e,
            # yield self._elems[i]

    def __getitem__(self, i: int) -> any:
        """Return the element at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __getitem__() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst[0]
        1
        >>> lst[3]
        6
        """
        if 0 <= i < len(self):
            return self._elems[i]

        raise IndexError('ArrayList: index out of range')

    def __setitem__(self, i: int, x: any) -> None:
        """Replace the element at index i with x.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __setitem__() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst[0] = 10
        >>> lst
        ArrayList([10, 4, 3, 6])
        >>> lst[2] = 7
        >>> lst
        ArrayList([10, 4, 7, 6])
        """
        if 0 <= i < len(self):
            self._elems[i] = x
            return None

        raise IndexError('ArrayList: assignment index out of range')

    def __delitem__(self, i: int) -> None:
        """Remove the element at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __delitem__() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> del lst[0]
        >>> lst
        ArrayList([4, 3, 6])
        >>> len(lst)
        3

        >>> del lst[2]
        >>> lst
        ArrayList([4, 3])
        >>> len(lst)
        2
        """
        if 0 <= i < len(self):
            # Shift any subsequent elements one position to the left, to close
            # the gap let when x is removed.
            self._elems[i:self._num_items - 1] = \
                self._elems[i + 1:self._num_items]
            self._num_items -= 1

            # Reduce the list's capacity when two-thirds or more of the
            # array is unused.
            if len(self._elems) >= 3 * len(self):
                self._resize()

            return None

        raise IndexError('ArrayList: assignment index out of range')

    def __contains__(self, x: any) -> bool:
        """Return True if x is in this ArrayList; otherwise False.

        >>> lst = ArrayList([10, 20, 30, 20])
        >>> 10 in lst
        True
        >>> 40 in lst
        False
        """
        # for elem in self:
        #     if elem == x:
        #         return True
        # return False

        for i in range(len(self)):   # IMPORTANT: for in range(len(self._elems)) IS WRONG!
            if self._elems[i] == x:
                return True
        return False

    def __add__(self, other: 'ArrayList') -> 'ArrayList':
        """Return a new ArrayList containing the concatenation of this ArrayList
        and other.

        Raises TypeError if other is not an ArrayList.

        >>> list1 = ArrayList([1, 3, 5])
        >>> list2 = ArrayList([2, 4, 6])
        >>> list3 = list1 + list2
        >>> list3
        ArrayList([1, 3, 5, 2, 4, 6])
        """
        if not isinstance(other, ArrayList):
            raise TypeError("can only concatenate ArrayList to ArrayList")

        # Create a new, empty, ArrayList, then replace its backing array with
        # one that has sufficient capacity to hold all the elements from the
        # lists we're concatenating.
        #
        # This eliminates the multiple calls to _resize() that could occur
        # if the new list was constructed by appending elements one-by-one
        # to an ArrayList; for example,
        #
        #    newlist = ArrayList(self)
        #    for elem in other:
        #        newlist.append(elem)
        #    return newlist

        newlist = ArrayList()
        n = len(self) + len(other)
        newlist._elems = _new_array(n)
        newlist._elems[0:len(self)] = self._elems[0:len(self)]
        newlist._elems[len(self):n] = other._elems[0:len(other)]
        newlist._num_items = n
        return newlist

    def __eq__(self, other: 'ArrayList') -> bool:
        """Return True if other equals this ArrayList.

        other and self are equal iff:
        (1) other is an ArrayList;
        (2) other and self contain the same number of items;
        (3) other[i] == self[i], for all i, 0 <= i < len(self)

        >>> lst1 = ArrayList([10, 20, 30])
        >>> lst2 = ArrayList([10, 20, 30])
        >>> lst1 == lst2
        True

        >>> tup = (10, 20, 30)  # compare to a tuple with the same elements
        >>> lst1 == tup
        False

        >>> lst2 = ArrayList([10, 20, 30, 20])
        >>> lst1 == lst2
        False
        """
        if not isinstance(other, ArrayList):
            return False

        if len(other) != len(self):
            return False

        for i in range(len(self)):
            if self._elems[i] != other._elems[i]:
                # Instead of accessing the backing arrays directly,
                # we could call __getitem__ on the two ArrayLists; i.e.,
                #    if self[i] != other[i]:
                return False
        return True

    def append(self, x: any) -> None:
        """Append x to the end of this ArrayList.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.append(2)
        >>> lst
        ArrayList([1, 4, 3, 6, 2])
        >>> len(lst)
        5
        """
        if len(self) == len(self._elems):
            # The backing array is full, so replace it with one that
            # has more capacity.
            self._resize()

        self._elems[self._num_items] = x
        self._num_items += 1

    def insert(self, i: int, x: any) -> None:
        """Insert x before index i in this ArrayList.
        If i >= len(self), append x to the list.

        Raises IndexError if the index is out of range (i < 0).

        Note: Unlike Python's built-in list type, insert() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.insert(0, 10)
        >>> lst
        ArrayList([10, 1, 4, 3, 6])
        >>> len(lst)
        5

        >>> lst.insert(5, 7)  # append 7 to the list
        >>> lst
        ArrayList([10, 1, 4, 3, 6, 7])
        >>> len(lst)
        6
        """
        if self._num_items == len(self._elems):
            # The backing array is full, so replace it with one that
            # has more capacity.
            self._resize()

        if i < 0:
            raise IndexError('ArrayList: assignment index out of range')

        if i < len(self):
            # Elements in the list are stored at indices 0 .. num_items - 1,
            # inclusive.
            # Shift the element currently at index i and any subsequent
            # elements one position to the right, to make room for x.

            self._elems[i + 1:self._num_items + 1] = \
                self._elems[i:self._num_items]
            self._elems[i] = x
            self._num_items += 1
        else:
            self.append(x)

    # Exercise 1

    def extend(self, iterable) -> None:
        """Extend this ArrayList with the elements from the iterable.

        >>> list1 = ArrayList([1, 3, 5])
        >>> list2 = ArrayList([2, 4, 6])
        >>> list1.extend(list2)
        >>> list1
        ArrayList([1, 3, 5, 2, 4 6])

        >>> list1 = ArrayList([10, 20, 30])
        >>> tup = (60, 50, 40)
        >>> list1.extend(tup)
        >>> list1
        ArrayList([10, 20, 30, 60, 50, 40])
        """

        for item in iterable:
            self.append(item)
        # return self._elems

    # Exercise 2

    def index(self, x: any) -> int:
        """Return the index of the first occurrence of x in this ArrayList.

        Raises ValueError if x is not in the list.

        >>> lst = ArrayList([10, 20, 30])
        >>> lst.index(10)
        0
        >>> lst.index(20)
        1
        """
        
        counter = 0
        if x not in self:
            raise ValueError ("Item is not in the ArrayList")
        for i in self:
            if i == x:
                break
            counter +=1
        return counter
        
                

    # Exercise 3

    def pop(self, i: int = -1) -> any:
        """Remove and return the element at index i. By default, the last element is removed.

        Raises IndexError if the index is out of range.

        Note: Like Python's built-in list type, pop() supports negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.pop()  # equivalent to lst.pop(-1)
        6
        >>> lst
        ArrayList([1, 4, 3])

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.pop(0)
        1
        >>> lst
        ArrayList([4, 3, 6])
        """

        if i < -self._num_items or i >= self._num_items:
            raise IndexError("pop index is out of range")

        if i < 0:
            i += self._num_items

        deletedItem = self[i]
        self.__delitem__(i)
        return deletedItem
        

    # Exercise 4

    def __reversed__(self):
        """Return a reverse iterator for this ArrayList.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> for x in lst.__reversed__():
        ...     print(x)
        ...
        6
        3
        4
        1
        """
        if self._num_items == 0:
            return ArrayList()
        return iter(self._elems[self._num_items - 1::-1])



    def _resize(self) -> None:
        """Change this ArrayList's capacity to 2 * n, where n is the number of
        elements in the list. If the list is empty, change its capacity to 1.
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
