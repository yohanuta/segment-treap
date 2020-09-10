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
import random
import matplotlib.pyplot as plt

from SegmentTreap import pSegmentTreap, SegmentTreap, cSegmentTreap
from Interval import Interval, n_inf, p_inf
from Treap import Treap, pTreap
from Node import Node, pNode, generate_priority

class double_feature():
    """A double_feature object contains a SegmentTreap and and a pSegmentTreap. 
    The former uses zipping, the latter rotations for insertion.
    """
    def __init__(self):
        self.conventional = pSegmentTreap()
        self.zipper = SegmentTreap()
    def insert(self, segment):
        """Insert a segment to both trees with the same priorities."""
        priority1 = generate_priority()
        priority2 = generate_priority()
        self.conventional.insert(segment, priority1, priority2)
        self.zipper.insert(segment, priority1, priority2)

    def compare(self):
        """Check whether the two trees have the same structure."""
        return self.conventional == self.zipper
    def display(self):
        """Display both trees."""
        self.conventional.display()
        self.zipper.display()

def random_test_double(num_segments, num_iterations):
    """Generate random segments, insert them to both trees using double_feature.
    Finally check whether they turn out the same. 
    
    Parameters:

        num_segments (int): The number of segments that will be added to empty trees per iteration.

        num_iterations (int): The number of repetitions.

    Result: 

        Nothing, if the trees are the same. An error, if at any time, they are not.
    """
    for i in range(num_iterations):
        # time.sleep(.001)
        double = double_feature()
        # print("new SegmentTreap")
        a= [i for i in range(2 * num_segments)]
        random.shuffle(a)
        for i in range(num_segments):
            first = a[2*i]
            second = a[2*i + 1]
            if second < first:
                first, second = second, first
            segment = Interval(first, second)
            double.insert(segment)
            if double.conventional != double.zipper:
                double.display()
                raise
        double.display()



def test(num_segments=100, num_iterations=1000, method = "Rotations"):
    """Generate random segments. Measure the time to insert them to one of three different kinds of segment treaps.

    Parameters:

        num_segments (int): The number of segments that will be 
        added to empty trees per iteration.

        num_iterations (int): The number of repetitions.

        method (str): "Rotations", "Zipping" or "ComplexZipping", 
        depending on which insertion algorithm shall be used

        Returns: 

            Time it took to build the trees.
    """
    print("Number of Iterations:", num_iterations)
    print("Number of Segments per Iteration:", num_segments)
    print("Method:", method)
    # with progressbar.ProgressBar(max_value=num_iterations) as bar:

    start = time.time()
    for iteration in range(num_iterations):
        if method == "Rotations":
            Tree = pSegmentTreap()
        elif method == "Zipping":
            Tree = SegmentTreap()
        elif method == "ComplexZipping":
            Tree = cSegmentTreap()
        segments = [i for i in range(2 * num_segments)]
        random.shuffle(segments)
        for i in range(num_segments):
            first = segments[2*i]
            second = segments[2*i + 1]
            if second < first:
                first, second = second, first
            segment = Interval(first, second)
            Tree.insert(segment)
        # bar.update(iteration)
    end = time.time()
    return end - start


def plot_results(max_num_segments = 1000, step = 50, segments_per_iteration = 100000, Rotations = True, classic_zipping = True, complex_zipping = True, filename = 'test.png'):
    """plot the results of the test() function for different kinds of segment treaps
    
    Parameters:
        
        max_num_segments (int): We increment the number of segments
        added to an empty segment treap per iteration up to this number.

        step (int): The size of the incrementation step for the number
        of segments that will be added to the empty treap.
        For steps = 50, only 50, 100, 150, 200, ... segments
        will be added to each segment treap.
        
        segments_per_iteration (int): The number of segments that will
        be added in total (throughout all iterations) for a fixed
        number of segments that will be added per iteration.

        Rotations (bool): If True, a segment Treap using rotations
        will be included in the graph.

        classic_zipping (bool): If True, a segment Treap using classic 
        zipping will be included in the graph.

        complex_zipping (bool): If True, a segment Treap using complex
        zipping will be included in the graph.

    Returns:
        A graph will be returned:
        x-axis: number of inserted segments per iteration
        y-axis: average time of generating Segment Treap per iteration.
    """
    start = time.time()

    data_rotations = []
    data_classiczipping = []
    data_complexzipping = []
    x_axis = range(step, max_num_segments+1, step)
    for num_segments in x_axis:
        num_iterations = int(segments_per_iteration / num_segments)
        if Rotations == True:
            data_rotations.append(test(num_segments, num_iterations, method = "Rotations")/num_iterations)
        if classic_zipping == True:
            data_classiczipping.append(test(num_segments, num_iterations, method = "Zipping")/num_iterations)
        if complex_zipping == True:
            data_complexzipping.append(test(num_segments, num_iterations, method = "ComplexZipping")/num_iterations)
        ###

    if classic_zipping == True:
        plt.plot(x_axis, data_classiczipping, 'r', label="Zipping")
    if complex_zipping == True:
        plt.plot(x_axis, data_complexzipping, 'g', label="complex Zipping")
    if Rotations == True:
        plt.plot(x_axis, data_rotations, 'b', label="Rotations")
    plt.xlabel('number of inserted segments')
    plt.ylabel('average time of generating Segment Treap')
    plt.legend()
    # plt.show()
    plt.savefig(filename)
    plt.close()



    end = time.time()
    seconds = int(end - start)
    minutes = seconds // 60
    seconds = seconds % 60
    print("Making this graph took", minutes, "minutes and ", seconds, "seconds.")

plot_results(1000, 10, 100000, complex_zipping=True, filename="three.png")
plot_results(1000, 10, 100000, complex_zipping=False, filename="two.png")
# random_test_double(100,100)

