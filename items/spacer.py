from items.item import *
class Spacer(Item):
    def regex(tags = None):
        if tags:
            return f'(?P<spacer>\s+)'
        return f'(\s+)'
    
    
    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)
    
    @property
    def short(self):
        return ' '
    
