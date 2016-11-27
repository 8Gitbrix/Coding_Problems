class BSTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val   = val
            self.left  = left
            self.right = right

        def __repr__(self):
            t = BSTree()
            t.root = self
            return repr(t)

    def __init__(self):
        self.root = None

    @staticmethod
    def rotate_right(t):
        """Returns the root of the tree resulting from a right rotation about `t`.
        Assumes that `t` and `t`'s left subtree are not empty"""
        x = t.left
        y = t
        x_p = BSTree.Node(x.val, left=x.left)
        y_p = BSTree.Node(y.val, left=x.right, right=y.right)
        x_p.right = y_p
        return x_p

    @staticmethod
    def rotate_left(t):
        """Returns the root of the tree resulting from a left rotation about `t`.
        Assumes that `t` and `t`'s right subtree are not empty"""
        x = t
        y = t.right
        x_p = BSTree.Node(x.val, left=x.left, right=y.left)
        y_p = BSTree.Node(y.val, left=x_p, right=y.right)
        return y_p

    @staticmethod
    def height(t):
        if not t:
            return 0
        else:
            return 1 + max(BSTree.height(t.left), BSTree.height(t.right))

    @staticmethod
    def rebalance(t):
        """Fixes the given tree, which is assumed to have one subtree that is precisely
        2 nodes "taller" than the other."""
        if BSTree.height(t.left) > BSTree.height(t.right):
            if BSTree.height(t.left.left) > BSTree.height(t.left.right):
                print("Fixing LL")
                return BSTree.rotate_right(t)
            else:
                print("Fixing LR")
                t.left = BSTree.rotate_left(t.left)
                return BSTree.rotate_right(t)
        return t

    def add(self, x):
        """Adds element x to the binary search tree."""
        def add_rec(t):
            if not t:
                node = BSTree.Node(x)
            elif x < t.val:
                t.left = add_rec(t.left)
                node = t
            else:
                t.right = add_rec(t.right)
                node = t

            if abs(BSTree.height(node.left) - BSTree.height(node.right)) >= 2:
                node = BSTree.rebalance(node)
            return node

        self.root = add_rec(self.root)

    def clear(self):
        self.root = None

    def contains(self, x):
        """Returns True if x is found in the tree; otherwise, returns False."""
        def contain_rec(t):
            if x == t.val:
                return True
            elif x < t.val:
                contain_rec(t.left)
            elif x > t.val:
                contain_rec(t.right)
            return False

        return contain_rec(self.root)

    def hasChildren(self):
        "A 0 value means no children, -1 means a only a left child, 1 means a right child, 2 means 2 children"
        if not self.left and not self.right:
            return 0
        elif self.left and not self.right:
            return -1
        elif not self.left and self.right:
            return 1
        else:
            return 2

    def remove(self, x):
        """Removes the first instance of x located in the tree."""
        def remove_rec(t, x):
            if not t:
                raise KeyError('Error value not found')
            if t.val < x:
                remove_rec(t.left)
            elif t.val > x:
                remove_rec(t.right)
            elif t.val == x:
                if hasChildren(t)==0:
                    t = None
                elif hasChildren(t.left)!=0 and hasChildren(t.right)!=0:
                    t.val = t.left.val
                    t.left= None
                #if both the children of node you are removing also have children
                elif hasChildren(t.left)!=0 or hasChildren(t.right)!=0:
                    t.val = t.left.val
                    #save right node of left value as a separate tree
                    addTree = t.left.right
                    t.left = t.left.left
                    #add every element from the saved right tree back into this new tree
                    for y in addTree:
                        add(t,y)

        self.root = remove(self.root)

    def __iter__(self):
        def iter_rec(t):
            if t:
                yield from iter_rec(t.left)
                yield t.val
                yield from iter_rec(t.right)
        yield from iter_rec(self.root)

    def __repr__(self):
        # return repr(list(self))
        return self._tree_repr()

    def _tree_repr(self, width=64):
        height = BSTree.height(self.root)
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        return repr_str
