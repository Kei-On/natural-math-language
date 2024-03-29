from items.item import *
class Parenthesis(Item):
    dict = {
        '(':{
            'name': 'round-open',
            'regex': '\(',
        },
        ')':{
            'name': 'round-close',
            'regex': '\)',
        },
        '[':{
            'name': 'block-open',
            'regex': '\[',
        },
        ']':{
            'name': 'block-close',
            'regex': '\]',
        },
        '{':{
            'name': 'sharp-open',
            'regex': '\{',
        },
        '}':{
            'name': 'sharp-close',
            'regex': '\}',
        },

    }

    def regex(tags = None):
        if tags:
            a = '|'.join([f"(?P<{d['name']}>{d['regex']})" for d in Parenthesis.dict.values()])
            return f'{a}'
        a = '|'.join([d['regex'] for d in Parenthesis.dict.values()])
        return f'{a}'
    
    def isopen(p):
        if p in Parenthesis.dict.keys():
            if 'open' in Parenthesis.dict[p]['name']:
                return True
        return False

    
    def isclose(p):
        if p in Parenthesis.dict.keys():
            if 'close' in Parenthesis.dict[p]['name']:
                return True
        return False
    
    def __new__(cls, seed):
        if seed in Parenthesis.dict.keys():
            self = str.__new__(cls, seed)
            return self
        raise ValueError(seed)
        