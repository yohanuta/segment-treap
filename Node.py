# Copyright (C) 2020  Johannes Wolf

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random

from Interval import Interval, n_inf, p_inf


def generate_priority():
    return random.random()

# def display_priority(priority):
#     if priority == n_inf:
#         return "-inf"
#     else:
#         return str(round(self.priority * 10) % 10)

class Node():
    """A class for nodes of segment treaps without parent pointers,
    i.e. for insertions using zipping.
    """
    def __init__(self, key, priority, left = None, right = None, associated_interval = None, can = None, belonging_segment = None):
        """Initialize a class object, i.e. a segment tree node.
        
        Parameters:
            key (int): The key of the node

            priority (int): The priority of the node
            
            left (Node): The left child of the node or None
            
            right (Node): The right child of the node or None
            
            associated_interval (Interval): The associated interval of the node

            can ({Interval}): The canonical subset of the node

            belonging_segment (Interval): The segment that belongs to the node

        Returns:
            A segment tree node without parent pointer
        """
        self.key = key
        self.left = left
        self.right = right
        self.belonging_segment = belonging_segment
        if associated_interval is None:
            self.associated_interval = Interval()
        else:
            self.associated_interval = associated_interval
        if can is None:
            self.can = set()
        else:
            self.can = can
        if priority == None:
            self.priority = generate_priority()
        else:
            self.priority = priority

    def __lt__(self, other):
        return self.key < other.key



    def __gt__(self, other):
        return self.key > other.key

    def __eq__(self, other):
        if other == None:
            return False
        if self.key == other.key and self.left == other.left and self.right \
        == other.right and self.priority == other.priority and \
        self.associated_interval.left == other.associated_interval.left and \
        self.associated_interval.right == other.associated_interval.right and \
        self.can == other.can: 
            return True 
        else:
            return False
    def __le__(self, other):
        return self < other or self == other     
    def __ge__(self, other):
        return self > other or self == other 
    def __repr__(self):
        if self.can == set():
            return str(self.key) + "," + str(self.associated_interval)
        return str(self.key) + "," + str(self.associated_interval) + "," + str(self.can)

    def is_leaf(self):
        return self.left == None and self.right == None

    def display_priority(self):
        if self.priority == n_inf:
            return "-inf"
        else:
            return str(round(self.priority * 10) % 10)

    def traverse(self):
        if self.is_leaf():
            if self.belonging_segment is None:
                ## We are at the dummy node
                return set()
            else:
                return {self.belonging_segment}
        else:
            return self.left.traverse().union(self.right.traverse())

    def update_can(self, parent):
        segments = list(self.can)
        #print("Update", self, "with parent", parent, ". Segments in Question:", segments)
        self.can = set()
        int_self = self.associated_interval
        int_par = parent.associated_interval
        for segment in segments: 
            if segment.covers(int_self) and not segment.covers(int_par):
                self.can.add(segment)
        #print(self.can)
        # print("Appropriate segments:", self.can)

    def find_can(self, parent, segments):
        # print("Update", self, "with parent", parent, ". Segments in Question:", segments)
        self.can = set()
        int_self = self.associated_interval
        int_par = parent.associated_interval
        for segment in segments: 
            if segment.covers(int_self) and not segment.covers(int_par):
                self.can.add(segment)
        # print("Appropriate segments:", self.can)

    def pull_segments_from_child(self, child, parent):
        #print("pull: before:", self, child, parent)
        if child == None:
            return
        segments = list(child.can)
        for segment in segments:
            if segment.covers(self.associated_interval):
                child.can.remove(segment)
                if not segment.covers(parent.associated_interval):
                    self.can.add(segment)

        #print("pull: after:", self, child, parent)

    # def update_corner_node(self, parent):
    #     int_self = self.associated_interval
    #     int_par = parent.associated_interval
    #     can = list(self.can)
    #     ##step 1:
    #     for segment in can:    
    #         if segment.covers(int_par):
    #             self.can.remove(segment)
    #     ##step 2 works together with non-corner cases seperately

    #     ##step 3
    #     empty collection 

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root. 
        This was copied from 
        https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python."""
        # No child.
        if self.right is None and self.left is None:
            line = str(self)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle
        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = str(self)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2
        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = str(self)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = str(self)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def is_covered_by(self, segment):
        return segment.covers(self.associated_interval)

    def add_segment_to_cans(self, segment, debug_treap=None):
        # print("check: ",self, segment)
        if self.is_covered_by(segment):
            # print("add")
            self.can.add(segment)
            # print("Add segment", segment, "to can of", self)
            #debug_treap.display()
        else:
            if self.left is not None and self.left.associated_interval.intersects(segment):
                self.left.add_segment_to_cans(segment, debug_treap)
            if self.right is not None and self.right.associated_interval.intersects(segment):
                self.right.add_segment_to_cans(segment, debug_treap)

    def union_of_children_intervals(self):
        if self.left is None and self.right is None:
            return Interval()
        elif self.left is None:
            return self.right.associated_interval
        elif self.right is None:
            return self.left.associated_interval
        else:
            return self.left.associated_interval.union(self.right.associated_interval)

class pNode(Node):
    """A class for nodes of segment treaps with parent pointers,
     i.e. for insertions using rotations.
     """
    def __init__(self, key, priority, parent = None, left = None, right = None, associated_interval = Interval(), can = set()):
        """Initialize a class object, i.e. a segment tree node with parent pointer.
        
        Parameters:
            key (int): The key of the node

            priority (int): The priority of the node
            
            parent (Node): The node's parent

            left (Node): The left child of the node or None
            
            right (Node): The right child of the node or None
            
            associated_interval (Interval): The associated interval of the node

            can ({Interval}): The canonical subset of the node

            belonging_segment (Interval): The segment that belongs to the node

        Returns:
            A segment tree node with parent pointer
        """
        super().__init__(key, priority, left = None, right = None, associated_interval = Interval(), can = set())
        self.parent = parent

