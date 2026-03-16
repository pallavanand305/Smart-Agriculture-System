"""
AADS Module — Red-Black Tree
Indexes sensor readings by timestamp for O(log n) range queries.
Properties (CLRS): root=BLACK, no adjacent RED nodes,
equal black-height on all root-to-null paths.
"""

RED, BLACK = "RED", "BLACK"


class RBTNode:
    def __init__(self, key, data=None):
        self.key    = key          # timestamp (float/int)
        self.data   = data         # SensorReading dict
        self.color  = RED
        self.left   = None
        self.right  = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        # Sentinel NIL node
        self.NIL        = RBTNode(key=None)
        self.NIL.color  = BLACK
        self.root       = self.NIL

    # ── Public API ──────────────────────────────────────────────────────────

    def insert(self, key, data=None):
        z        = RBTNode(key, data)
        z.left   = self.NIL
        z.right  = self.NIL
        self._bst_insert(z)
        self._fix_insert(z)

    def range_query(self, lo, hi):
        """Return all readings with lo <= key <= hi (in-order)."""
        result = []
        self._range(self.root, lo, hi, result)
        return result

    def size(self):
        return self._count(self.root)

    # ── Internal helpers ────────────────────────────────────────────────────

    def _bst_insert(self, z):
        y, x = self.NIL, self.root
        while x != self.NIL:
            y = x
            x = x.left if z.key < x.key else x.right
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    def _fix_insert(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right          # uncle
                if y.color == RED:                 # Case 1
                    z.parent.color         = BLACK
                    y.color                = BLACK
                    z.parent.parent.color  = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:        # Case 2
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color        = BLACK  # Case 3
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color         = BLACK
                    y.color                = BLACK
                    z.parent.parent.color  = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color        = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _left_rotate(self, x):
        y         = x.right
        x.right   = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left  = y
        else:
            x.parent.right = y
        y.left   = x
        x.parent = y

    def _right_rotate(self, x):
        y        = x.left
        x.left   = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left  = y
        y.right  = x
        x.parent = y

    def _range(self, node, lo, hi, result):
        if node == self.NIL:
            return
        if lo < node.key:
            self._range(node.left, lo, hi, result)
        if lo <= node.key <= hi:
            result.append(node.data)
        if node.key < hi:
            self._range(node.right, lo, hi, result)

    def _count(self, node):
        if node == self.NIL:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)


# ── Quick demo ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import time
    rbt = RedBlackTree()
    base = int(time.time())
    for i in range(10):
        rbt.insert(base + i*60, {"moisture": 40 + i, "temp": 25})

    results = rbt.range_query(base + 120, base + 480)
    print(f"Range query returned {len(results)} records:")
    for r in results:
        print(" ", r)
