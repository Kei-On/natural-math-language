from items.item import *

class Unown(Item):
    def regex(tags = None):
        l = '[abcdfghj-zA-Z]'
        L = '[a-zA-Z]'
        return f'({l}(_{L})*|{L}?(_{L})+)'
    
    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)

class UnownPart(Item):
    def regex(tag):
        return '(1{100000})'
    
    def __new__(cls, seed):
        self = Item.get_subclass('Expression')
        return self
        raise ValueError(seed)
    