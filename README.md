# SegmentTreap

SegmentTreap is a python program for Segment Treaps, a data structure for one-dimensional intersection search.

## Usage

Running main.py will for an increasing number (in steps of 50) of random segments add them to an empty segment treap. 
For each step 10000 segments will be added in total. This will be repeated three times for insertions using rotation, 
zipping and a second more complex zipping algorithm.


## Files

### main.py
Run tests and generate graphs.

### SegmentTreap.py
Define the classes SegmentTreap, pSegmentTreap and cSegmentTreap that use rotations, 
zipping and complex zipping for insertion respectively.

### Treap.py
Define the classes Treap and pTreap that are treaps without and with parent pointers. 
They allow to insert segments endpoints twice, once as an inner node and once as a leaf. 

### Node.py
Define the classes Node and pNode for Segment Tree nodes without and with a parent pointer.

### Interval.py
Define the interval class that is both used for segments and intervals.

## License
[GPLv3] <https://www.gnu.org/licenses/>