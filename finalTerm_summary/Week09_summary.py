# 딕셔너리 생성, PUT, GET, SIZE, CONTAIN, DELETE
'''
dic = {}
dic['a'] = 1

print(dic['a'])
print(len(dic))

print(list(dic.keys()))
print(list(dic.values()))
print(list(dic.items()))

print('a' in dic)
print('b' in dic)

del dic['a']
print('a' in dic)
'''


# word Counter
'''
def frequencyCounter(sentence, minFreq):
    counter = {}

    segments = list(sentence.split())

    for seg in segments:
        if not seg in counter:
            counter[seg] = 1
        else:
            counter[seg] += 1

    sorted_items = sorted(counter.items(), key= lambda x : x[1])
    
    result = []

    for item in sorted_items:
        if item[1] >= minFreq:
            result.append(item)

    return result

sentence = "a a a a a a b b b b b  c c c c d d d "
print(frequencyCounter(sentence, 4))
'''

'''
# BST 구현

class BST:
    class Node:
        def __init__(self, key, value):
            self.key, self.value = key, value
            self.left = self.right = None
            self.count = 1 

    def __init__(self):
        self.root = None

    def get(self, key):
        pointer = self.root

        while pointer != None:
            if pointer.key == key:
                return pointer.value
            elif key < pointer.key:
                pointer = pointer.left
            elif pointer.key < key:
                pointer = pointer.right

        return None

    def put(self, key, value):
        def putOnNode(x, key, value):
            if x == None:
                return self.Node(key, value)
            
            if key < x.key:
                x.left = putOnNode(x.left, key, value)
            elif key == x.key:
                x.value = value
            elif x.key < key:
                x.right = putOnNode(x.right, key, value)

            x.count = self.sizeOnNode(x.left) + 1 + self.sizeOnNode(x.right)
                
            return x
        
        self.root = putOnNode(self.root, key, value)

    def sizeOnNode(self, x):
        if x == None:
            return 0
        else:
            return x.count
        
    def size(self):
        return self.sizeOnNode(self.root)

    def min(self):
        if self.root == None:
            return None
        
        pointer = self.root

        while pointer != None:
            if pointer.left != None:
                pointer = pointer.left
            else:
                break

        return pointer.key
    
    def max(self):
        if self.root == None:
            return None
        
        pointer = self.root

        while pointer != None:
            if pointer.right != None:
                pointer = pointer.right
            else:
                break

        return pointer.key
                

    def floor(self, k):
        def floorOnNode(x, k):
            if x == None: return None
            
            if k < x.key:
                r = floorOnNode(x.left, k)

                if r != None:
                    return r
                else:
                    return None
                
            elif x.key < k:
                r = floorOnNode(x.right, k)

                if r != None:
                    return r
                else:
                    return x.key
                
            else:
                return x.key
        
        return_value = floorOnNode(self.root, k)

        if return_value != None:
            return return_value
        else:
            return None
        
    def ceiling(self, k):
        def ceilingOnNode(x, k):
            if x == None:
                return None
            
            if k < x.key:
                r = ceilingOnNode(x.left, k)

                if r != None:
                    return r
                else:
                    return x.key
                
            elif x.key < k:
                r = ceilingOnNode(x.right, k)

                if r != None:
                    return r
                else:
                    return None
                
            else:
                return x.key


        r = ceilingOnNode(self.root, k)

        if r != None:
            return r
        else:
            return None
        
    def rank(self, k):
        def rankOnNode(x, k):
            if x == None:
                return 0
            
            if k < x.key:
                return rankOnNode(x.left, k)
            elif x.key < k:
                return self.sizeOnNode(x.left) + 1 + rankOnNode(x.right, k)
            else:
                return self.sizeOnNode(x.left)

        return rankOnNode(self.root, k)
    
    
    def inorder(self):
        def inorderOnNode(x):
            if x == None:
                return
            
            inorderOnNode(x.left)
            result.append(x.key)
            inorderOnNode(x.right)
        
        result = []
        inorderOnNode(self.root)

        return result
            



bst = BST() 

bst.put("a",1)
bst.put("c",2)
bst.put("e",3)
bst.put("b",4)
bst.put("c",5)
#print(bst.size())

print(bst.get("a"))
print(bst.get("b"))
print(bst.get("c"))
print(bst.get("d"))
print(bst.get("e"))

print(bst.min())
print(bst.max())
print(bst.floor('f'))
print(bst.ceiling('d'))

print(bst.size())

print(bst.rank("a"))
print(bst.rank("b"))
print(bst.rank("c"))
print(bst.rank("d"))
print(bst.rank("e"))
print(bst.inorder())
'''



# 1-D range Search 구현

from queue import PriorityQueue


class LLRB:      
    class Node:                
        def __init__(self, key, val): # Constructor
            self.key, self.val = key, val
            self.left = self.right = None
            self.count = 1 # Number of nodes itself and below            
            self.red = True # Color of parent link

    def __init__(self): # Constructor
        self.root = None

    @staticmethod
    def getOnNode(h, key):
        while h != None:
            if key < h.key: h = h.left
            elif key > h.key: h = h.right
            else: return h.val # key == x.key
        return None # The key was NOT found

    def get(self, key):
        return LLRB.getOnNode(self.root, key)

    def contains(self, key):
        return self.get(key) != None

    @staticmethod    
    def isRed(x):
            if x == None: return False
            return x.red

    @staticmethod 
    def fixUp(h): # Fix the tree such that it conforms to the LLRB representation
        if h == None: return None
        if LLRB.isRed(h.right) and not LLRB.isRed(h.left): h = LLRB.rotateLeft(h)  # Lean right -> lean left
        if LLRB.isRed(h.left) and LLRB.isRed(h.left.left): h = LLRB.rotateRight(h) # 4-node all leaning left -> 4-node leaning left and right
        if LLRB.isRed(h.left) and LLRB.isRed(h.right): LLRB.flipColors(h) # Split a 4-node into two 2-nodes
        return h
    
    @staticmethod 
    def rotateLeft(h):
        assert(LLRB.isRed(h.right))
        x = h.right
        h.right = x.left
        x.left = h
        x.red = h.red
        h.red = True
        return x

    @staticmethod
    def rotateRight(h):
        assert(LLRB.isRed(h.left))
        x = h.left
        h.left = x.right
        x.right = h
        x.red = h.red
        h.red = True
        return x

    @staticmethod
    def moveRedLeft(h):
        LLRB.flipColors(h)
        if LLRB.isRed(h.right.left):
            h.right = LLRB.rotateRight(h.right)
            h = LLRB.rotateLeft(h)
            LLRB.flipColors(h)
        return h
    
    @staticmethod
    def moveRedRight(h):
        LLRB.flipColors(h)
        if LLRB.isRed(h.left.left):
            h = LLRB.rotateRight(h)
            LLRB.flipColors(h)
        return h

    @staticmethod
    def flipColors(h):
        #assert((not LLRB.isRed(h) and LLRB.isRed(h.left) and LLRB.isRed(h.right)) or\
        #    (LLRB.isRed(h) and not LLRB.isRed(h.left) and not LLRB.isRed(h.right)))        
        h.red = not h.red
        h.left.red = not h.left.red
        h.right.red = not h.right.red

    @staticmethod
    def deleteMin(h):
        if h.left == None: return None
        if not LLRB.isRed(h.left) and not LLRB.isRed(h.left.left):
            h = LLRB.moveRedLeft(h)
        h.left = LLRB.deleteMin(h.left)
        h = LLRB.fixUp(h)
        h.count = LLRB.sizeOnNode(h.left) + 1 + LLRB.sizeOnNode(h.right)
        return h

    def delete(self, key):
        def deleteOnNode(h, key):
            if h == None: return None
            if key < h.key:
                if h.left != None and not LLRB.isRed(h.left) and not LLRB.isRed(h.left.left):
                    h = LLRB.moveRedLeft(h)
                h.left = deleteOnNode(h.left, key)
            else:
                if LLRB.isRed(h.left): h = LLRB.rotateRight(h)
                if key == h.key and h.right == None: return None
                if h.right != None and not LLRB.isRed(h.right) and not LLRB.isRed(h.right.left):
                    h = LLRB.moveRedRight(h)
                if key == h.key: # Hibbard deletion: place the min in the right subtree on the deleted spot 
                    h.key = LLRB.minOnNode(h.right)
                    h.value = LLRB.getOnNode(h.right, h.key)
                    h.right = LLRB.deleteMin(h.right)
                else:
                    h.right = deleteOnNode(h.right, key)
            h = LLRB.fixUp(h)
            h.count = LLRB.sizeOnNode(h.left) + 1 + LLRB.sizeOnNode(h.right)        
            return h
        self.root = deleteOnNode(self.root, key)
        if self.root != None:
            self.root.red = False # To not violate the assertion in flipColors(h), where the root splits

    def put(self, key, val):
        def putOnNode(x, key, val):
            if x == None: return self.Node(key, val)
            if key < x.key: x.left = putOnNode(x.left, key, val)
            elif key > x.key: x.right = putOnNode(x.right, key, val)
            else: x.val = val # key == x.key
            x = LLRB.fixUp(x)
            x.count = LLRB.sizeOnNode(x.left) + 1 + LLRB.sizeOnNode(x.right)
            return x     
        self.root = putOnNode(self.root, key, val)
        self.root.red = False # To not violate the assertion in flipColors(h), where the root splits

    @staticmethod
    def minOnNode(h):
        if h == None: return None
        else:
            while h.left != None:
                h = h.left
        return h.key

    def min(self):
        return LLRB.minOnNode(self.root)
        
    def max(self):
        if self.root == None: return None
        else:            
            x = self.root
            while x.right != None:
                x = x.right
            return x.key

    def floor(self, key):
        def floorOnNode(x, key):
            if x == None: return None
            if key == x.key: return x
            elif key < x.key: return floorOnNode(x.left, key)

            t = floorOnNode(x.right, key)
            if t != None: return t
            else: return x
        x = floorOnNode(self.root, key)
        if x == None: return None
        else: return x.key

    def ceiling(self, key):
        def ceilingOnNode(x, key):
            if x == None: return None
            if key == x.key: return x
            elif x.key < key: return ceilingOnNode(x.right, key)

            t = ceilingOnNode(x.left, key)
            if t != None: return t
            else: return x
        x = ceilingOnNode(self.root, key)
        if x == None: return None
        else: return x.key

    @staticmethod
    def sizeOnNode(x):
            if x == None: return 0
            else: return x.count

    def size(self):        
        return LLRB.sizeOnNode(self.root)    

    def rank(self, key): # How many keys < key?
        def rankOnNode(x, key):
            if x == None:
                return 0
            
            if key < x.key:
                return rankOnNode(x.left)
            elif x.key < key:
                return self.sizeOnNode(x.left) + 1 + rankOnNode(x.right, key)
            else:
                return self.sizeOnNode(x.left)

        return rankOnNode(self.root, key)

    def select(self, idx):
        def selectOnNode(x, idx): # idx-th element on the subtree rooted at x
            if x == None: return None # idx-th element does not exist
            if idx < LLRB.sizeOnNode(x.left): return selectOnNode(x.left, idx)
            elif idx > LLRB.sizeOnNode(x.left): return selectOnNode(x.right, idx-LLRB.sizeOnNode(x.left)-1)
            else: return x.key # idx == LLRB.sizeOnNode(x.left)
        return selectOnNode(self.root, idx)        

    def inorder(self):        
        def inorderOnNode(x, q):
            if x == None: return
            inorderOnNode(x.left, q)
            q.append(x.key)
            inorderOnNode(x.right, q)
        q = []
        inorderOnNode(self.root, q)
        return q

    def levelorder(self):
        qNode, qKey, idx = [], [], 0
        if self.root == None: return qNode
        else: qNode.append(self.root)        
        while idx < len(qNode):
            x = qNode[idx]
            if x.left != None: qNode.append(x.left)
            if x.right != None: qNode.append(x.right)
            qKey.append(x.key)
            idx += 1
        return qKey

    def rangeCount(self, lo, hi): # Number of keys between lo and hi, both inclusive
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)

    def rangeSearch(self, lo, hi): # Return all keys between lo and hi, both inclusive
        def rangeSearchOnNode(x, lo, hi):
            if x == None:
                return
            
            if lo < x.key:
                rangeSearchOnNode(x.left, lo, hi)
            if lo <= x.key and x.key <= hi:
                result.append(x.key)
            if x.key < hi:
                rangeSearchOnNode(x.right, lo, hi)
        
        result = []
        rangeSearchOnNode(self.root, lo, hi)

        return result



# Sweep Line Algorithm 구현

class Segment:
    def __init__(self, x1, y1, x2, y2):
        assert(x1==x2 or y1==y2) # Accept either a horizontal or vertical segment  
        assert(not (x1==x2 and y1==y2)) # Two end points cannot be equal              

        # Put smaller values in (x1,y1) and larger values in (x2,y2)
        if x1==x2:            
            if y1<y2: self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            else: self.x1, self.y1, self.x2, self.y2 = x1, y2, x2, y1
        elif y1==y2:
            if x1<x2: self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            else: self.x1, self.y1, self.x2, self.y2 = x2, y1, x1, y2
    
    def isHorizontal(self):
        return self.y1 == self.y2

    def isVertical(self):
        return self.x1 == self.x2

    # Create a human-readable string representation
    def __str__(self):
        return f"({self.x1},{self.y1})--({self.x2},{self.y2})"

    def __repr__(self): # Called when a Segment is printed as an element of a list
        return self.__str__()

    # Defines behavior for the equality operator, ==
    # This operator is required for grading
    def __eq__(self, other):
        if other == None: return False
        if not isinstance(other, Segment): return False        
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2
    


def sweepLine(segments):
    pq = PriorityQueue()
    llrb = LLRB()

    result = []

    for seg in segments:
        if seg.isHorizontal():
            pq.put((seg.x1, seg))
            pq.put((seg.x2, seg))
        else:
            pq.put((seg.x1, seg))

    while not pq.empty():
        x, seg = pq.get()

        if seg.isHorizontal():
            if llrb.contains(seg.y1):
                llrb.delete(seg.y1)
            else:
                llrb.put(seg.y1, seg)

        else:
            r = llrb.rangeSearch(seg.y1, seg.y2)

            for i in r:
                result.append((llrb.get(i), seg))

    return result