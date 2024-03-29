from items.item import *

class PlaceHolder(Item):
    def regex(tags = None):
        D = Item.get_subclass('Parenthesis').dict
        opens = [d['regex'] for k, d in D.items() if 'open' in d['name']]
        closes =  [d['regex'] for k, d in D.items() if 'close' in d['name']]
        left = '|'.join(opens)
        right = '|'.join(closes)
        regex = f'({left})\.+({right})'
        if tags:
            return f'(?P<placeholder>{regex})'
        return f'({regex})'
    
    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            for sub in cls.__subclasses__():
                try:
                    return sub(seed)
                except:
                    pass
            return str.__new__(cls, seed)
        raise ValueError(seed)
    
    def __str__(self):
        l = 0
        now = self.child.right
        while now.right is not None:
            l += len(now.__str__())
            now = now.right
        return re.sub('\.+','.'*l,self)

    @property
    def short(self):
        return self
        #return re.sub('\.+','...',self)
    
    @property    
    def expression(self):
        now = self.child
        text = ''
        while now:
            if isinstance(now, PlaceHolder):
                text += now.expression
            else:
                text += now
            now = now.right
        return Item.get_subclass('Expression')(text)
    
class Priority(PlaceHolder):

    def regex(tags = None):
        return '\(\.+\)'

    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)
    


    def evaluate(self,dic = {}):
        pass
        
        

    
class Context(PlaceHolder):

    def regex(tags = None):
        return '\[\.+\]'
    
    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)
    
    def statements(self):
        now = self.child.right
        statements = [[]]
        while now.right:
            if now == '|':
                statements += [[]]
            else:
                statements[-1] += [now]
            now = now.right
        return statements
    
    def dict(self):
        dic = {}
        statements = self.statements()
        for statement in statements:
            pair = ['', '']
            switch = 0
            for item in statement:
                if item == '=':
                    switch = 1
                    continue
                pair[switch] += item
            dic[pair[0]] = pair[1]
        return dic