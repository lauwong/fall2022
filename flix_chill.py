#####################################
##### PLEASE DO NOT MODIFY THIS CODE
#####################################


class BST:
    def __init__(self, item = None, parent = None):
        "Initialize a BST node"
        self.item     = item
        self.parent   = parent
        self.left     = None
        self.right    = None

    def is_empty(self):       return self.item is None
    def is_right_child(self): return self.parent and (self.parent.right == self)
    
    def subtree_min(self):
        "Return node with minimum item key in subtree (assumes nonempty)"
        if self.left:
            return self.left.subtree_min()
        return self

    def subtree_find(self, k):
        "Return node from subtree having item with key k (assumes nonempty)"
        if k == self.item.key:
            return self
        if k < self.item.key and self.left:
            return self.left.subtree_find(k)
        if k > self.item.key and self.right:
            return self.right.subtree_find(k)
        return None

    def subtree_close(self, k): 
        '''
        Return node from (nonempty) subtree having either (assumes nonempty):
            - left-most item with smallest key >  query key k
            - right-most item with largest key <= query key k
        '''
        if k < self.item.key and self.left:
            return self.left.subtree_close(k)
        if k >= self.item.key and self.right:
            return self.right.subtree_close(k)
        return self

    def tree_successor(self):
        "Return next node in an in-order traversal of tree (assumes nonempty)"
        if self.right:
            return self.right.subtree_min()
        node = self
        while node.is_right_child():
            node = node.parent
        return node.parent

    def replace(self, node):
        "Replace self's attributes with node's attributes"
        self.item  = node.item
        self.left  = node.left
        self.right = node.right
        if self.left:   self.left.parent  = self
        if self.right:  self.right.parent = self
       
    def remove(self):
        "Remove self's item from subtree (assumes nonempty)"
        node = self
        if self.left and self.right:                    # has two children
            node = self.right.subtree_min()
            self.item = node.item
        if   node.right:    node.replace(node.right)    # has one child
        elif node.left:     node.replace(node.left)
        else:                                           # has no children
            if node.parent is None:         # root
                node.item = None
                return
            if node.is_right_child():       # right child
                node.parent.right = None
            else:                           # left child
                node.parent.left  = None
            node = node.parent
        node.maintain()

    def maintain(self):
        '''
        Perform maintenance after a dynamic operation
        Called by lowest node with subtree modified by insert or delete
        '''
        pass

    def find_min(self): 
        "Return an item with minimum key, else None"
        if self.is_empty(): return None
        node = self.subtree_min()
        return node.item if node else None

    def find(self, k):
        "Return an item with key k, else None"
        if self.is_empty(): return None
        node = self.subtree_find(k)
        return node.item if node else None

    def find_next(self, k): 
        "Return an item with smallest key greater than k, else None"
        if self.is_empty(): return None
        node = self.subtree_close(k) # guarenteed to have item
        if node.item.key <= k:
            node = node.tree_successor()
        return node.item if node else None

    def insert(self, x):
        "Insert item into self's subtree"
        if self.is_empty():
            self.item = x 
            self.maintain()
        elif x.key < self.item.key:
            if self.left is None:
                self.left  = self.__class__(None, self)
            self.left.insert(x)
        else:
            if self.right is None:
                self.right = self.__class__(None, self)
            self.right.insert(x)

    def delete(self, k):
        "Delete key k from self's subtree"
        if self.is_empty():
            raise IndexError('delete from empty data structure')  
        node = self.subtree_find(k)
        if node is None:
            raise IndexError('key not found in data structure')  
        item = node.item
        node.remove()
        return item

    def iter_recursive(self):
        if self.left:
            yield from self.left.iter_recursive()
        yield self.item
        if self.right:
            yield from self.right.iter_recursive()

    def iter_iterative(self):
        "Return iterator of subtree's nodes in order"
        node = self.subtree_min()
        while node:
            yield node.item
            node = node.tree_successor()

    def item_str(self):
        return str(self.item.key)

    def __str__(self):
        "Return ASCII drawing of the tree"
        if self.is_empty(): return '[Empty tree]'
        s = self.item_str()
        if self.left is None and self.right is None:
            return s
        sl, sr, sep = [''], [''], '_'
        if self.left:
            s = sep + s
            sl = str(self.left).split('\n')
        if self.right:
            s = s + sep
            sr = str(self.right).split('\n')
        wl, cl = len(sl[0]), len(sl[0].lstrip(' _'))
        wr, cr = len(sr[0]), len(sr[0].rstrip(' _'))
        a = [(' ' * (wl - cl)) + ('_' * cl) + s +
             ('_' * cr) + (' ' * (wr - cr))]
        for i in range(max(len(sl), len(sr))):
            ls = sl[i] if i < len(sl) else ' ' * wl
            rs = sr[i] if i < len(sr) else ' ' * wr
            a.append(ls + ' ' * len(s) + rs) 
        return '\n'.join(a)

class AVL(BST):
    def __init__(self, item = None, parent = None):
        "Augment BST with height and skew"
        super().__init__(item, parent)
        self.new_node = AVL
        self.height   = 0
        self.skew     = 0

    def update(self):
        "Update height and skew"
        left_height  = self.left.height  if self.left  else -1
        right_height = self.right.height if self.right else -1
        self.height  = max(left_height, right_height) + 1
        self.skew    = right_height - left_height

    def rotate_right(self):
        '''
        Rotate left to right, assuming left is not None
         __s__      __n__
        _n_  c  =>  a  _s_
        a b            b c
        Self and node swap contents so that subtree root does not change
        '''
        node, c = self.left, self.right
        a, b    = node.left, node.right 
        self.item, node.item = node.item, self.item
        if a:   a.parent = self
        if c:   c.parent = node
        self.left, self.right = a, node
        node.left, node.right = b, c
        node.update()
        self.update()

    def rotate_left(self):
        '''
        Rotate right to left, assuming right is not None
        __s__        __n__
        a  _n_  =>  _s_  c
           b c      a b   
        Self and node swap contents so that subtree root does not change
        '''
        a, node = self.left, self.right
        b, c    = node.left, node.right
        self.item, node.item = node.item, self.item
        if a:   a.parent = node
        if c:   c.parent = self
        self.left, self.right = node, c
        node.left, node.right = a, b
        node.update()
        self.update()

    def maintain(self):
        "Update height and skew and rebalance up the tree"
        self.update()
        if self.skew == 2:      # must have right child
            if self.right.skew == -1:
                self.right.rotate_right() 
            self.rotate_left()
        elif self.skew == -2:   # must have left child
            if self.left.skew == 1:
                self.left.rotate_left() 
            self.rotate_right()
        if self.parent:
            self.parent.maintain()

    def item_str(self):
        return str(self.item.key) + (
            '<' if 0 < self.skew else
            '>' if 0 > self.skew else '=')

class Movie:


    def __init__(self, id, date, rank):
        """
        Instantiates a Movie object with id, date, rank, as well as augmented values:
        """
        self.key, self.id, self.rank = date, id, rank

        # Add and initialize your augmentations

        self.max_rank = (self.rank, self.id)

"""
AVL Tree structure keyed by s (date) that handles insert(m, s, r) and finding highest(s). 
Note that additional data structures may be needed for part a) to implement delete/earliest, 
but these are not required for the coding portion.
"""
class FlixChillManager(AVL):
    def __init__(self, item = None, parent = None): 
        super().__init__(item, parent)

    def insert(self, m, s, r):
        """
        Input: m | an integer representing a movie ID
        Input: s | an integer representing a movie starting date
        Input: r | an integer representing a movie ranking
        """

        if self.is_empty():
            self.item = Movie(m, s, r)
            self.maintain()
        elif s < self.item.key:
            if self.left is None:
                self.left  = self.__class__(None, self)
            self.left.insert(m, s, r)
        else:
            if self.right is None:
                self.right = self.__class__(None, self)
            self.right.insert(m, s, r)
    
    def maintain(self):
        super().maintain()

        # Maintain augmentations
        
        if self.left:
            if self.left.item.max_rank > self.item.max_rank:
                self.item.max_rank = self.left.item.max_rank
        if self.right:
            if self.right.item.max_rank > self.item.max_rank:
                self.item.max_rank = self.right.item.max_rank

        if self.parent:
            self.parent.maintain()
        
    def delete(self, m):
        """
        Input: m | an integer representing a movie ID
        
        Deletes movie with ID m (no return value)
        """

        pass # not required for coding portion of PSet 
        
    def earliest(self, s):
        """
        Input: s | an integer representing a date
        
        Return the ID of the movie with the lowest date greater than or equal to s
        """
        # Don't modify this function

        if self.is_empty(): return None
        if self.subtree_find(s) != None:
            return self.subtree_find(s)
        node = self.subtree_close(s) # guarenteed to have item
        if node.item.key < s:
            node = node.tree_successor()
        return node if node else None

    def highest(self, s):
        """
        Input: s | an integer representing a date
        
        Return the ID of the movie with the highest ranking that starts on or after date s
        """
        highest_node = self.highest_helper(s)

        return highest_node[1]
    
    def highest_helper(self, s):

        if self.is_empty():
            return (-float('inf'), -1)

        if self.item.key == s:
            if self.right:
                return max((self.item.rank, self.item.id), self.right.item.max_rank)
            return self.item.max_rank
        elif self.item.key > s:
            if self.right and self.left:
                return max((self.item.rank, self.item.id), self.right.item.max_rank, self.left.highest_helper(s))
            elif self.left:
                return max((self.item.rank, self.item.id), self.left.highest(s))
            return self.item.max_rank
        else:
            if self.right:
                return self.right.highest_helper(s)
            return (-float('inf'), -1)

# Do not modify
def testDB(ops):
    f = FlixChillManager()
    for op in ops:
        if op[0] == 'i':
            f.insert(op[1], op[2], op[3])
        else:
            return f.highest(op[1])