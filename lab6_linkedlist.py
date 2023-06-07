
# Class LinkedList is an implementation of ADT List that uses a singly-linked
# list as the underlying data structure.

# Some methods in this class were adapted from methods in class LinkedList in
# Lee and Hubbard's "Data Structures and Algorithms with Python", Section 4.10.

__author__ = 'Rama Alkhouli'

class LinkedList:

    class _Node:
        def __init__(self, item: any, next: '_Node' = None) -> None:
            """Initialize this node with the specified data item and link to
            the next node in the linked list.
            """
            self.item = item
            self.next = next

        # Class Node in Section 4.10.1 of the Lee and Hubbard textbook
        # defines accessor and mutator methods for the item and next attributes
        # (getItem, getNext, setItem, setNext). These methods aren't defined
        # here, given that _Node is a simple class that is "private" to class
        # LinkedList. Instead of calling the getter and setter methods,

        # Examples:
        # cursor.getItem() in L&H becomes cursor.item
        # cursor = cursor.getNext() in L&H becomes cursor = cursor.next
        # cursor.setItem(x) in L&H becomes cursor.item = x
        # cursor.setNext(node) in L&H becomes cursor.next = node

        # Code that uses LinkedList shouldn't do this, because a LinkedList's
        # nodes aren't part of its public interface.

    def __init__(self, iterable=[]) -> None:
        """Initialize this LinkedList.

        If no iterable is provided, the new LinkedList is empty.
        Otherwise, initialize the LinkedList by appending the values
        provided by the iterable.

        >>> lst = LinkedList()
        >>> lst
        LinkedList([])

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> lst
        LinkedList([1, 4, 3, 6])
        """
        # A LinkedList always has one "dummy" node that never contains any of
        # the items that are stored in the linked list. This dummy node
        # points to the node at the head of the linked list.

        # _first always points to the dummy node.
        self._first = LinkedList._Node(None)

        # _last always points to the node at the tail of the linked list,
        # or the dummy node when the linked list is empty.
        self._last = self._first
        self._num_items = 0  # of items stored in the LinkedList

        for elem in iterable:
            self.append(elem)
            # append() updates self._num_items.

    def __str__(self) -> str:
        """Return a string representation of this LinkedList.

        >>> lst = LinkedList()
        >>> str(lst)
        '[]'
        >>> lst = LinkedList([1, 4, 3, 6])
        >>> str(lst)
        '[1, 4, 3, 6]'
        """
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "[{0}]".format(", ".join([repr(x) for x in self]))

    def __repr__(self) -> str:
        """Return the canonical string representation of this LinkedList.

        >>> lst = LinkedList()
        >>> repr(lst)
        'LinkedList([])'
        >>> lst = LinkedList([1, 4, 3, 6])
        >>> repr(lst)
        'LinkedList([1, 4, 3, 6])'
        """
        # For an LinkedList object, obj, the expression eval(repr(obj))
        # returns a new LinkedList that is identical to obj.
        return "{0}({1})".format(self.__class__.__name__, str(self))

    def __len__(self) -> int:
        """Return the number of elements in this LinkedList.

        >>> lst = LinkedList()
        >>> len(lst)
        0
        >>> lst = LinkedList([1, 4, 3, 6])
        >>> len(lst)
        4
        """
        return self._num_items

    def __iter__(self):
        """Return an iterator for this LinkedList.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> for x in lst:
        ...     print(x)
        ...
        1
        4
        3
        6
        """
        cursor = self._first.next   # Skip over the dummy node. self._self points to dummy node
        while cursor is not None:
            yield(cursor.item)
            cursor = cursor.next

    def __getitem__(self, i: int) -> any:
        """Return the element stored at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __getitem__() doesn't
        support negative indices.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> lst[0]
        1
        >>> lst[3]
        6
        """
        if 0 <= i < len(self):
            # Traverse the linked list until cursor refers to the
            # node specified by index i.
            cursor = self._first.next   # Skip over the dummy node.
            for _ in range(i):
                cursor = cursor.next
            return cursor.item

        raise IndexError('LinkedList: index out of range')

    def __setitem__(self, i: int, x: any) -> None:
        """Replace the element stored at index i with x.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __setitem__() doesn't
        support negative indices.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> lst[0] = 10
        >>> lst
        LinkedList([10, 4, 3, 6])
        >>> lst[2] = 7
        >>> lst
        LinkedList([10, 4, 7, 6])
        """
        if 0 <= i < len(self):
            # Traverse the linked list until cursor refers to the
            # node specified by index i.
            cursor = self._first.next   # Skip over the dummy node.
            for _ in range(i):
                cursor = cursor.next
            cursor.item = x
            return None

        raise IndexError('LinkedList: assignment index out of range')

    def __add__(self, other: 'LinkedList') -> 'LinkedList':
        """Return a new LinkedList containing the concatenation of this
        LinkedList and other.
        """
        if not isinstance(other, LinkedList):
            raise TypeError('can only concatenate LinkedList to LinkedList')

        newlist = LinkedList()

        cursor = self._first.next  # Skip over the dummy node.
        while cursor is not None:
            newlist.append(cursor.item)
            cursor = cursor.next

        cursor = other._first.next  # Skip over the dummy node.
        while cursor is not None:
            newlist.append(cursor.item)
            cursor = cursor.next

        return newlist

    def append(self, x: any) -> None:
        """Append x to the end of this LinkedList.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> lst.append(2)
        >>> lst
        LinkedList([1, 4, 3, 6, 2])
        >>> len(lst)
        5
        """
        node = LinkedList._Node(x)
        self._last.next = node
        self._last = node
        self._num_items += 1

    def insert(self, i: int, x: any) -> None:
        """Insert x before index i in this LinkedList.
        If i >= len(self), append x to the list.

        Raises IndexError if the index is out of range (i < 0).

        Note: Unlike Python's built-in list type, insert() doesn't
        support negative indices.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> lst.insert(0, 10)
        >>> lst
        LinkedList([10, 1, 4, 3, 6])
        >>> len(lst)
        5

        >>> lst.insert(5, 7)  # append 7 to the list
        >>> lst
        LinkedList([10, 1, 4, 3, 6, 7])
        >>> len(lst)
        6
        """
        if i < 0:
            raise IndexError('LinkedList: assignment index out of range')

        if i < len(self):
            # Traverse the linked list until cursor refers to the
            # node before the node specified by index i.
            cursor = self._first
            for _ in range(i):
                cursor = cursor.next

            node = LinkedList._Node(x, cursor.next)
            cursor.next = node
            self._num_items += 1
        else:
            self.append(x)

    # Exercise 1

    def __contains__(self, x: any) -> bool:
        """Return True if x is in this LinkedList; otherwise False.

        >>> lst = LinkedList([10, 20, 30, 20])
        >>> 10 in lst
        True
        >>> 40 in lst
        False
        """
        
        cursor = self._first.next   # Skip over the dummy node.
        while cursor is not None:
            if cursor.item == x:
                return True
            cursor = cursor.next
        return False
        

    # Exercise 2

    def __eq__(self, other: 'LinkedList') -> bool:
        """Return True if other equals this LinkedList.

        other and self are equal iff:
        (1) other is an LinkedList;
        (2) other and self contain the same number of items;
        (3) other[i] == self[i], for all i, 0 <= i < len(self)

        >>> lst1 = LinkedList([10, 20, 30])
        >>> lst2 = LinkedList([10, 20, 30])
        >>> lst1 == lst2
        True
        >>> tup = (10, 20, 30)  # compare to a tuple with the same elements
        >>> lst1 == tup
        False
        >>> lst2 = LinkedList([10, 20, 30, 20])
        >>> lst1 == lst2
        False
        """
        if not isinstance(other, LinkedList):
            return False

        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self[i] != other[i]:
                return False

        return True

    # Exercise 3

    def __delitem__(self, i: int) -> None:
        """Remove the element at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __delitem__() doesn't
        support negative indices.

        >>> lst = LinkedList([1, 4, 3, 6])
        >>> del lst[0]
        >>> lst
        LinkedList([4, 3, 6])
        >>> len(lst)
        3

        >>> del lst[2]
        >>> lst
        LinkedList([4, 3])
        >>> len(lst)
        2
        """
        if i < 0 or i >= len(self):
            raise IndexError("Index is out of range")  
        if i == 0:
            self._first.next = self._first.next.next
        else:
            # Traverse the linked list until cursor refers to the
            # node before the node specified by index i.
            cursor = self._first
            for _ in range(i):
                cursor = cursor.next

            cursor.next = cursor.next.next

        self._num_items -= 1

    # Exercise 4

    def remove(self, x: any) -> None:
        """Remove the first occurrence of x from this LinkedList.

        Raises ValueError if the list is empty.
        Raises ValueError if x is not in the list.

        >>> lst = LinkedList([3, 1, 2, 3, 4])

        # Remove the first 3.
        >>> lst.remove(3)
        >>> lst
        LinkedList([1, 2, 3, 4])

        # Now remove the second 3.
        >>> lst.remove(3)
        >>> lst
        LinkedList([1, 2, 4])
        """
        
        if self._num_items == 0:
            raise ValueError("the list is empty")

        cursor = self._first.next  
        prev = self._first  # save previous node

        while cursor is not None:
            if cursor.item == x:
                #  remove the element from the list
                prev.next = cursor.next

                if cursor == self._last:
                    # Update the _last if removed the last node 
                    self._last = prev

                self._num_items -= 1
                return
            #increment prev and cursor
            prev = cursor
            cursor = cursor.next    
            
        raise ValueError("x is not in the list")        