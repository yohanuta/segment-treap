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

import time

from Node import Node, pNode
from Interval import Interval, n_inf, p_inf


class Treap:
    """A class for treaps as the base data structure for segment treaps 
    using zipping.
    """
    def __init__(self):
        """Return an empty Treap."""
        self.root = None

    def __eq__(self, other):
        return self.root == other.root

    def is_empty(self):
        """Return True iff the Treap object is empty"""
        return self.root is None

    def find_node_to_be_replaced(self, key, priority):
        """For an insetrion using zipping: Return the node that will be 
        replaced with x_inner and its parent.
        """
        curr = self.root
        parent = None
        while  not curr is None and curr.priority > priority:
            if key < curr.key:
                curr, parent = curr.left, curr
            else:
                curr, parent = curr.right, curr
        return curr, parent

    def insert_inner_and_leaf(self, key, priority=None, belonging_segment = None):
        """Insert a segment's endpoint to self using (simple) classic zipping
        twice, once as an inner node and once as a leaf.
        """
        # print("insert: ", key)
        x = Node(key, priority, belonging_segment = belonging_segment)
        x_leaf = Node(key, n_inf, associated_interval=Interval(key, p_inf), belonging_segment = belonging_segment)
        priority = x.priority
        to_be_replaced, parent = self.find_node_to_be_replaced(key, priority)
        segments_in_subtree = to_be_replaced.traverse()
        # print("Segments in Subtree:", segments_in_subtree )

        if parent is None:
            self.root = x
        #hänge x an seinen neuen Elternknoten
        elif x < parent:
            parent.left = x
        else:
            parent.right = x
        x.associated_interval = to_be_replaced.associated_interval.deepcopy()
        # print("A0")
        # self.display()
        x.can = to_be_replaced.can
        to_be_replaced.can = set()
        #hänge to_be_replaced an x
        if to_be_replaced < x:
            x.left = to_be_replaced
        else:
            x.right = to_be_replaced
        parent = x
        curr = to_be_replaced
        fix = parent
        # self.display()
        while curr is not None:
            if curr < x: 
                ## curr is red
                while curr is not None and curr < x:
                    curr.associated_interval.right = key
                    curr.find_can(parent, segments_in_subtree)
                    if curr.left is not None:
                        curr.left.find_can(curr, segments_in_subtree)
                    curr, parent = curr.right, curr
            else: 
                ## curr is green
                while curr is not None and curr > x:
                    curr.associated_interval.left = key
                    curr.find_can(parent, segments_in_subtree)
                    if curr.right is not None:
                        curr.right.find_can(curr, segments_in_subtree)
                    curr, parent = curr.left, curr
            if curr is not None:
                if curr < fix:
                    fix.left = curr 
                else: 
                    fix.right = curr
                fix, parent = parent, fix
        ###Find the end of the green spine.
        if fix.key == key:
            ## The end of the green spline is still to_be_replaced.
            fix.right = x_leaf
            x_leaf.associated_interval.right = fix.associated_interval.right
            x_leaf.find_can(fix, segments_in_subtree)
        elif fix.key > key:
            ### fix is the end of the green spline
            fix.left = x_leaf
            x_leaf.associated_interval.right = fix.key
            x_leaf.find_can(fix, segments_in_subtree)
        else:
            raise
            #par is the end of the green spline:
            parent.left = x_leaf            
            x_leaf.associated_interval.right = fix.key
            x_leaf.find_can(parent, segments_in_subtree)
        # print("insert", key, "done!")
        # self.display()

    def complexinsert_inner_and_leaf(self, key, priority=None, belonging_segment = None):
        """Insert a segment's endpoint to self using complex zipping
        twice, once as an inner node and once as a leaf.
        """
        #print("insert: ", key)
        x = Node(key, priority, belonging_segment = belonging_segment)
        x_leaf = Node(key, n_inf, associated_interval=Interval(key, p_inf), belonging_segment = belonging_segment)
        priority = x.priority
        to_be_replaced, parent = self.find_node_to_be_replaced(key, priority)
        collection = set()
        # print("Segments in Subtree:", segments_in_subtree )

        if parent is None:
            self.root = x
        #hänge x an seinen neuen Elternknoten
        elif x < parent:
            parent.left = x
        else:
            parent.right = x
        x.associated_interval = to_be_replaced.associated_interval.deepcopy()
        # print("A0")
        # self.display()
        x.can = to_be_replaced.can
        to_be_replaced.can = set()
        #hänge to_be_replaced an x
        if to_be_replaced < x:
            x.left = to_be_replaced
        else:
            x.right = to_be_replaced
        parent = x
        curr = to_be_replaced
        fix = parent
        collection |= curr.can
        # self.display()
        while curr is not None:
            #print("curr", curr)
            if curr < x: 
                ## curr is red
                if parent <= x:
                    ## curr is non-corner node
                    curr.associated_interval.right = key
                    collection |= curr.can
                    curr.pull_segments_from_child(curr.left, parent)
                    curr, parent = curr.right, curr
                else:
                    curr.associated_interval.right = key
                    if fix == x:
                        fix.left = curr
                    else:
                        fix.right = curr
                    collection, curr.can = curr.can, collection # step 3, 4
                    curr.can |= collection # step 1
                    curr.update_can(fix)
                    curr.pull_segments_from_child(curr.left, fix) # step 2
                    fix = parent
                    curr, parent = curr.right, curr
            else: 
                ## curr is green
                if parent >= x:
                    ## curr is non-corner node
                    curr.associated_interval.left = key
                    collection |= curr.can
                    curr.pull_segments_from_child(curr.right, parent)
                    curr, parent = curr.left, curr
                else:
                    #curr is corner node
                    curr.associated_interval.left = key
                    if fix == x:
                        fix.right = curr
                    else:
                        fix.left = curr
                    collection, curr.can = curr.can, collection # step 3, 4
                    curr.can |= collection # step 1
                    curr.update_can(fix)
                    curr.pull_segments_from_child(curr.right, fix) # step 2
                    fix = parent
                    curr, parent = curr.left, curr

        ## We have reached the end of the tree
        if fix == x:
            ## The end of the green spline is still to_be_replaced.
            fix.right = x_leaf
            x_leaf.associated_interval.right = fix.associated_interval.right
            #x_leaf.update_can(fix, segments_in_subtree)
        elif fix.key > key:
            ### fix is the end of the green spline
            fix.left = x_leaf
            x_leaf.associated_interval.right = fix.key
            #x_leaf.update_can(fix, segments_in_subtree)
        else:
            #print(curr, fix)
            raise
            #par is the end of the green spline:
            parent.left = x_leaf            
            x_leaf.associated_interval.right = fix.key
            x_leaf.update_can(parent, segments_in_subtree)
        x_leaf.can = collection
        x_leaf.update_can(fix)
        #print("insert", key, "done!")
        self.display()

    def find_leaf(self, key):
        """Return the leaf whose associated interval contains key."""
        parent = None
        node = self.root
        if self.is_empty():
            return node, parent
        while True:
            if node.is_leaf():
                return node, parent
            elif key < node.key:
                node, parent = node.left, node
            else:
                node, parent = node.right, node

    def display(self):
        return
        lines, _, _, _ = self.root._display_aux() 
        for line in lines: 
            print(line) 
        print((20 -  len(lines)) * "\n")


class pTreap(Treap):
    """A class for treaps as the base data structure for segment treaps
    using rotations.
    """
    def __init__(self):
        super().__init__()

    def insert_inner_and_leaf(self, key, priority = None):
        """Insert a segment's endpoint to self using rotations
        twice, once as an inner node and once as a leaf.
        """
        leaf_old, parent = self.find_leaf(key)
        inner_new = pNode(key, priority)
        leaf_new = pNode(key, n_inf)
        if parent is not None:
            if inner_new < parent:
                parent.left = inner_new
       	    else:
                parent.right = inner_new
        else:
            self.root = inner_new
        inner_new.parent = parent
        inner_new.left = leaf_old
        inner_new.right = leaf_new
        leaf_new.parent = inner_new
        leaf_old.parent = inner_new
        inner_new.associated_interval = leaf_old.associated_interval
        leaf_old.associated_interval, leaf_new.associated_interval = inner_new.associated_interval.split_at(key)
        inner_new.can = leaf_old.can
        leaf_old.can = set()
        leaf_new.can = set()
        while self.root != inner_new and inner_new.priority > inner_new.parent.priority:
            self.rotate_up(inner_new)

    def rotate_up(self, node):
        """Rotate the inserted node up like this:
          X            Y 
         / \          / \
        A   Y   ->   X   C      
           / \      / \     
          B   C    A   B  
        """
        ##single rotation:
        if node is None:
            # self.display()
            raise
        parent = node.parent
        if parent is None:
            raise 
        rotate_right = parent.left == node
        if rotate_right:
            #print("rotate right")
            #rotate right
            node.right, parent.left = parent, node.right
            if parent.left: 
                parent.left.parent = parent
        else:
            #rotate left
            #print("rotate left")
            node.left, parent.right = parent, node.left
            if parent.right:
                parent.right.parent = parent
        grandparent = parent.parent
        node.parent, parent.parent = grandparent, node
        if grandparent:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        else:
            self.root = node
        #change associated intervals
        node.associated_interval = parent.associated_interval
        parent.associated_interval = parent.union_of_children_intervals()
        # change canonical subsets
        #   X            Y 
        #  / \          / \
        # A   Y   ->   X   C      
        #    / \      / \     
        #   B   C    A   B  
        X = parent
        Y = node
        if rotate_right:
            A = Y.left
            B = X.left
            C = X.right
            A.can |= Y.can
            B.can |= Y.can
            Y.can = X.can
            X.can = B.can & C.can 
            C.can -= X.can
            B.can -= X.can
        else:
            A = X.left
            B = X.right
            C = Y.right
            C.can |= Y.can
            B.can |= Y.can            
            Y.can = X.can
            X.can = B.can & A.can
            A.can -= X.can
            B.can -= X.can


