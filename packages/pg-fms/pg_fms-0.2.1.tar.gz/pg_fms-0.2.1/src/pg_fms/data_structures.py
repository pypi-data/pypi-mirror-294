from typing import List, Any


class TrieNode:
    """
    A node in a Trie data structure.
    """

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

    def insert(self, word):
        """
        Insert a word into the Trie.
        """
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """
        Search for a word in the Trie.
        """
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def delete(self, word):
        """
        Delete a word from the Trie.
        """
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        node.is_end_of_word = False
        return True

    def traverse(self, node, prefix):
        """
        Traverse the Trie and print all words.
        """
        if node.is_end_of_word:
            print(prefix)
        for char, child in node.children.items():
            self.traverse(child, prefix + char)

    def get_all_words(self):
        """
        Get all words in the Trie.
        """
        words = []
        self.traverse(self, "")
        return words


class Node:
    """
    A node in a linked list.
    """

    def __init__(self, item):
        self.item = item
        self.next = None


class LinkedList:
    """
    A linked list.
    """

    def __init__(self):
        self.head = None

    def print_list(self):
        """
        Print the linked list.
        """
        cur_node = self.head
        while cur_node:
            print(cur_node.item)
            cur_node = cur_node.next

    def append(self, item):
        """
        Append an item to the linked list.
        """
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def prepend(self, item):
        """
        Prepend an item to the linked list.
        """
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def insert_after_node(self, prev_node, item):
        """
        Insert an item after a given node.
        """
        if not prev_node:
            print("Previous node is not in the list")
            return
        new_node = Node(item)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key):
        """
        Delete a node by key.
        """
        cur_node = self.head
        if cur_node and cur_node.item == key:
            self.head = cur_node.next
            cur_node = None
            return
        prev = None
        while cur_node and cur_node.item != key:
            prev = cur_node
            cur_node = cur_node.next
        if cur_node is None:
            return
        prev.next = cur_node.next
        cur_node = None

    def delete_node_at_pos(self, pos):
        """
        Delete a node by position.
        """
        cur_node = self.head
        if pos == 0:
            self.head = cur_node.next
            cur_node = None
            return
        prev = None
        count = 1
        while cur_node and count != pos:
            prev = cur_node
            cur_node = cur_node.next
            count += 1
        if cur_node is None:
            return
        prev.next = cur_node.next
        cur_node = None

    def len_iterative(self):
        """
        Get the length of the linked list iteratively.
        """
        count = 0
        cur_node = self.head
        while cur_node:
            count += 1
            cur_node = cur_node.next
        return count

    def len_recursive(self, node):
        """
        Get the length of the linked list recursively.
        """
        if node is None:
            return 0
        return 1 + self.len_recursive(node.next)

    def swap_nodes(self, key1, key2):
        """
        Swap two nodes by key.
        """
        if key1 == key2:
            return
        prev1 = None
        cur1 = self.head
        while cur1 and cur1.item != key1:
            prev1 = cur1
            cur1 = cur1.next
        prev2 = None
        cur2 = self.head
        while cur2 and cur2.item != key2:
            prev2 = cur2
            cur2 = cur2.next
        if not cur1 or not cur2:
            return
        if prev1:
            prev1.next = cur2
        else:
            self.head = cur2
        if prev2:
            prev2.next = cur1
        else:
            self.head = cur1
        cur1.next, cur2.next = cur2.next, cur1.next

    def reverse_iterative(self):
        """
        Reverse the linked list iteratively.
        """
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def reverse_recursive(self):
        """
        Reverse the linked list recursively.
        """

        def _reverse_recursive(cur, prev):
            if not cur:
                return prev
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
            return _reverse_recursive(cur, prev)

        self.head = _reverse_recursive(cur=self.head, prev=None)

    def merge_sorted(self, llist):
        """
        Merge two sorted linked lists.
        """
        p = self.head
        q = llist.head
        s = None
        if not p:
            return q
        if not q:
            return p
        if p and q:
            if p.item <= q.item:
                s = p
                p = s.next
            else:
                s = q
                q = s.next
            new_head = s
        while p and q:
            if p.item <= q.item:
                s.next = p
                s = p
                p = s.next
            else:
                s.next = q
                s = q
                q = s.next
        if not p:
            s.next = q
        if not q:
            s.next = p
        return new_head

    def remove_duplicates(self):
        """
        Remove duplicates from the linked list.
        """
        cur = self.head
        prev = None
        dup_values = dict()
        while cur:
            if cur.item in dup_values:
                prev.next = cur.next
                cur = None
            else:
                dup_values[cur.item] = 1
                prev = cur
            cur = prev.next

    def print_nth_from_last(self, n):
        """
        Print the nth node from the last.
        """
        total_len = self.len_iterative()
        cur = self.head
        while cur:
            if total_len == n:
                print(cur.item)
                return cur.item
            total_len -= 1
            cur = cur.next
        if cur is None:
            return

    def rotate(self, k):
        """
        Rotate the linked list to the right by k nodes.
        """
        p = self.head
        q = self.head
        prev = None
        count = 0
        while p and count < k:
            prev = p
            p = p.next
            q = q.next
            count += 1
        p = prev
        while q:
            prev = q
            q = q.next
        q = prev
        q.next = self.head
        self.head = p.next
        p.next = None

    def is_palindrome(self):
        """
        Check if the linked list is a palindrome.
        """
        s = ""
        p = self.head
        while p:
            s += p.item
            p = p.next
        return s == s[::-1]

    def move_tail_to_head(self):
        """
        Move the tail node to the head of the linked list.
        """
        last = self.head
        second_to_last = None
        while last.next:
            second_to_last = last
            last = last.next
        last.next = self.head
        second_to_last.next = None
        self.head = last

    def sum_two_lists(self, llist):
        """
        Sum two linked lists.
        """
        p = self.head
        q = llist.head
        sum_llist = LinkedList()
        carry = 0
        while p or q:
            if not p:
                i = 0
            else:
                i = p.item
            if not q:
                j = 0
            else:
                j = q.item
            s = i + j + carry
            if s >= 10:
                carry = 1
                remainder = s % 10
                sum_llist.append(remainder)
            else:
                carry = 0
                sum_llist.append(s)
            if p:
                p = p.next
            if q:
                q = q.next
        sum_llist.print_list()

    def is_circular_linked_list(self, input_list):
        """
        Check if the linked list is circular.
        """
        cur = input_list.head
        while cur:
            cur = cur.next
            if cur == input_list.head:
                return True
        return False

    def to_list(self):
        """
        Convert the linked list to a list.
        """
        cur = self.head
        while cur:
            yield cur.item
            cur = cur.next

    def is_empty(self):
        """
        Check if the linked list is empty.
        """
        return self.head is None


class Stack:
    """
    A stack data structure.
    """

    def __init__(self):
        self.stack = []

    def create_stack(self):
        """
        Create a stack.
        """
        stack = []
        return stack

    def check_empty(self):
        """
        Check if the stack is empty.
        """
        return len(self.stack) == 0

    def push(self, item):
        """
        Push an item onto the stack.
        """
        self.stack.append(item)
        print("pushed item: " + item)

    def pop(self):
        """
        Pop an item from the stack.
        """
        if self.check_empty():
            return "stack is empty"
        return self.stack.pop()

    def is_empty(self):
        """
        Check if the stack is empty.
        """
        return len(self.stack) == 0

    def peek(self):
        """
        Peek at the top item of the stack.
        """
        return self.stack[-1]


class Queue:
    """
    A queue data structure.
    """

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """
        Add an element to the queue.
        """
        self.queue.append(item)

    def dequeue(self):
        """
        Remove an element from the queue.
        """
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    def display(self):
        """
        Display the queue.
        """
        print(self.queue)

    def size(self):
        """
        Get the size of the queue.
        """
        return len(self.queue)

    def to_list(self):
        """
        Convert the queue to a list.
        """
        return self.queue

    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return len(self.queue) == 0


class PriorityQueue(Queue):
    """
    A priority queue data structure.
    """

    @staticmethod
    def heapify(arr: List[Any], n: int, i: int):
        """
        Heapify the tree.
        """
        # Find the largest among root, left child and right child
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        # Swap and continue heapifying if root is not largest
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            PriorityQueue.heapify(arr, n, largest)

    @staticmethod
    def insert(array: List[Any], newNum: int):
        """
        Insert a new number into the priority queue.
        """
        size = len(array)
        if size == 0:
            array.append(newNum)
        else:
            array.append(newNum)
            for i in range((size // 2) - 1, -1, -1):
                PriorityQueue.heapify(array, size, i)

    @staticmethod
    def deleteNode(array: List[Any], num: int):  # pylint: disable=C0103
        """
        Delete a number from the priority queue.
        """
        size = len(array)
        i = 0
        for i in range(0, size):
            if num == array[i]:
                break
        array[i], array[size - 1] = array[size - 1], array[i]
        array.remove(size - 1)

        for i in range((len(array) // 2) - 1, -1, -1):
            PriorityQueue.heapify(array, len(array), i)

    def is_empty(self):
        """
        Check if the priority queue is empty.
        """
        return len(self.queue) == 0

    def to_sorted_list(self):
        """
        Convert the priority queue to a sorted list.
        """
        sorted_list = []
        while not self.is_empty():
            sorted_list.append(self.dequeue())
        return sorted_list


class Deque:
    """
    A double-ended queue (deque) data structure.
    """

    def __init__(self):
        """
        Initialize the deque.
        """
        self.items = []

    def isEmpty(self):  # pylint: disable=C0103
        """
        Check if the deque is empty.
        """
        return self.items == []

    def addRear(self, item):  # pylint: disable=C0103
        """
        Add an element from rear.
        """
        self.items.append(item)

    def addFront(self, item):  # pylint: disable=C0103
        """
        Add an element from front.
        """
        self.items.insert(0, item)

    def removeFront(self):  # pylint: disable=C0103
        """
        Remove an element from front.
        """
        return self.items.pop(0)

    def removeRear(self):  # pylint: disable=C0103
        """
        Remove an element from rear.
        """
        return self.items.pop()

    def size(self):
        """
        Get the size of the deque.
        """
        return len(self.items)


class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element.
    """

    def __init__(self) -> None:
        """
        Initialize the min stack.
        """
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        """
        Push a value onto the stack.
        """
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        """
        Pop a value from the stack.
        """
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        """
        Get the top value from the stack.
        """
        return self.stack[-1]

    def getMin(self) -> int:  # pylint: disable=C0103
        """
        Get the minimum value from the stack.
        """
        return self.min_stack[-1]
