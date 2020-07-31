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
# positive infinity
p_inf = float("inf")
# negative infinity
n_inf = - float("inf")



class Interval:
    """An interval object that is used for both segments and intervals"""
    def __init__(self, left=n_inf, right=p_inf):
        if left > right:
            print(left, right)
            raise
        else:
            self.left = left
            self.right = right

    def __repr__(self):
        l = str(self.left)
        if self.left == n_inf:
            l = ""
        r = str(self.right)
        if self.right == p_inf:
            r = ""
        return l +":"+ r

    def __hash__(self):
        return hash((self.left, self.right))

    def covers(self, other):
        """Return True iff self covers other."""
        if other is None:
            return False
        #print(self, " covers ", other, " : ", self.left <= other.left and self.right >= other.right)
        return self.left <= other.left and self.right >= other.right

    def intersects(self, other):
        """Return True iff self intersects other."""
        #print(self, " intersects ", other, " : ", self.right > other.left and self.left < other.right)
        return self.right > other.left and self.left < other.right

    def union(self,other):
        """Given two touching intervals, return the union of the two."""
        if other == None:
            return self
        if not self.right == other.left:
            raise
        return Interval(self.left, other.right)

    def is_in(self, point):
        """Return True iff point is in interval self."""
        return self.left <= point and point <= self.right
        
    def deepcopy(self):
        return Interval(self.left, self.right)

    def split_at(self, point):
        """Return two intervals that together make up the old one splitted at point."""
        if not self.is_in(point):
            # print("interval: ", self.left, self.right)
            # print("point: ", point)
            raise
        return Interval(self.left, point), Interval(point, self.right)


