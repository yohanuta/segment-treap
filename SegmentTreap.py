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

from Treap import Treap, pTreap
from Node import Node, pNode
from Interval import n_inf, p_inf, Interval


class pSegmentTreap:
    """An segment treap object that uses rotations for insertion"""
    def __init__(self):
        self.treap = pTreap()
        self.treap.root = pNode(n_inf, n_inf)
    def __eq__(self, other):
    	return self.treap == other.treap
    def display(self):
    	self.treap.display()
    def insert(self, segment, prio1= None, prio2= None):
        self.treap.insert_inner_and_leaf(segment.left, prio1)
        self.treap.insert_inner_and_leaf(segment.right, prio2)
        self.treap.root.add_segment_to_cans(segment, self.treap)


class SegmentTreap:
    """An segment treap object that uses classic zipping for insertion"""
    def __init__(self):
        self.treap = Treap()
        self.treap.root = Node(n_inf, n_inf)
    def display(self):
    	self.treap.display()
    def __eq__(self, other):
    	return self.treap == other.treap
    def insert(self, segment, prio1= None, prio2= None):
        self.treap.insert_inner_and_leaf(segment.left, prio1, segment)
        self.treap.insert_inner_and_leaf(segment.right, prio2, segment)            
        self.treap.root.add_segment_to_cans(segment, self.treap)


class cSegmentTreap:
    """An segment treap object that uses complex zipping for insertion"""
    def __init__(self):
        self.treap = Treap()
        self.treap.root = Node(n_inf, n_inf)
    def display(self):
        self.treap.display()
    def __eq__(self, other):
        return self.treap == other.treap
    def insert(self, segment, prio1= None, prio2= None):
        self.treap.complexinsert_inner_and_leaf(segment.left, prio1, segment)
        self.treap.complexinsert_inner_and_leaf(segment.right, prio2, segment)            
        self.treap.root.add_segment_to_cans(segment, self.treap)
        #print("segment added to cans")
        #self.display()
