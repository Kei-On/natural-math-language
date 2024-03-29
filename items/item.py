import re
import math
from icecream import ic
class Item(str):
    _child = None
    _left = None
    _right = None
    _parent = None


    def regex(tags = None):
        regex = '|'.join([f'({sub.regex(None)})' for sub in Item.__subclasses__()])
        return f'({regex})'

    def __new__(cls, seed, left = None, right = None, parent = None, child = None):
        match = re.fullmatch(Item.regex(),seed)
        if match:
            for sub in cls.__subclasses__():
                try:
                    self = sub.__new__(sub,seed)
                    return self
                except:
                    pass
            raise ValueError(seed)
        raise ValueError(seed)
    
    def __init__(self, seed, left = None, right = None, parent = None, child = None):
        self._left = left
        self._right = right
        self._parent = parent
        self._child = child
    
    @classmethod
    def get_subclass(cls, name: str):
        for sub in cls.__subclasses__():
            if sub.__name__ == name:
                return sub
            sub_get_subclass = sub.get_subclass(name)
            if sub_get_subclass:
                return sub_get_subclass
        return None

    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self, new):
        if self._left:
            self._left._right = None
        if new:
            new._right = self
        self._left = new

    @property
    def right(self):
        return self._right
    
    @right.setter
    def right(self, new):
        if self._right:
            self._right._left = None
        if new:
            new._left = self
        self._right = new

    def _search_left(self):
        if self._parent:
            return self._parent
        if self.left:
            return self.left._search_left()
        return None
    
    def _search_right(self):
        if self._parent:
            return self._parent
        if self.right:
            return self.right._search_right()
        return None

    @property
    def parent(self):
        L, R = self._search_left(), self._search_right()
        if L: return L
        if R: return R
        return None
        
    @parent.setter
    def parent(self, new):
        if self._parent:
            self._parent._child = None
        if new:
            new._child = self
        self._parent = new

    @property
    def child(self):
        return self._child
    
    @child.setter
    def child(self, new):
        if self._child:
            self._child._parent = None
        if new:
            new._parent = self
        self._child = new

    @property
    def next(self):
        if self.right is None:
            return None
        if self.right is self:
            raise Exception('circle chain')
        if not re.match('\s+',self.right):
            return self.right
        return self.right.next
    
    @property
    def last(self):
        if self.left is None:
            return None
        if self.left is self:
            raise Exception('circle chain')
        if not re.match('\s+',self.left):
            return self.left
        return self.left.last
    
    @property
    def head(self):
        if self.left is None:
            return self
        if self.left is self:
            raise Exception('circle chain')
        return self.left.head
    
    @property
    def tail(self):
        if self.right is None:
            return self
        if self.right is self:
            raise Exception('circle chain')
        return self.right.head
    
    @property
    def tree(self):
        now = self
        queue = []
        while now:
            queue += [now]
            now = now.right
        while queue:
            now = queue[0]
            queue = queue[1:]
            i = 0
            if not now.left:
                p = now.parent
                if p:
                    while p.left:
                        if p.left.__class__.__name__ == 'PlaceHolder':
                            break
                        i += len(p.left.__str__())
                        p = p.left
            if now.__class__.__name__ == 'Parenthesis':
                print(' '*i+' ',end='')
            else:
                print(' '*i+now.__str__(),end='')
            if now.child:
                new = now.child
                while new:
                    queue += [new]
                    new = new.right
            if not now.right:
                p = now
                while p.parent:
                    p = p.parent
                if not p.right:
                    print()
        print()

    
    def get(self, index):
        now = self
        for i in range(index):
            now = self.right
        return now
    
    def lookfor(self, item):
        now = self.right
        while now:
            if now == item:
                return now
            now = now.right
        return None

    @property
    def global_dist(self):
        if self.left is None and self.parent is None:
            return 0
        if self.left is None:
            return self.parent.global_dist
        return self.left.global_dist + len(self.left.__str__())
    @property
    def short(self):
        return self
    