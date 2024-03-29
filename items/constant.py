from items.item import *
class Constant(Item):
    def regex(tags = None):
        return '|'.join(Constant.list())
    
    def items():
        return [Item(const) for const in Constant.list()]
    
    def list():
        return [
            'pi',
            'e',
        ]
    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)
