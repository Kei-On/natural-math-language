from items.item import *

class Marker(Item):
    def regex(tag):
        return '(1{100000})'
    def __new__(cls, seed):
        if seed in ('start','end'):
            return str.__new__(cls, seed)
        raise ValueError(seed)
    
class Expression(Item):

    def regex(tag):
        return '(1{100000})'
    def __new__(cls, seed):
        return str.__new__(cls, seed)
    
    @property
    def split_first_item(self):
        regex = Item.regex()
        match = re.match(regex, self)
        if not match:
            return (Marker('end'), '')
        seed = match.group()
        return (Item(seed), Expression(self[len(seed):]))

    @property
    def entry(self):
        first, rest = self.split_first_item
        #print(entry,rest)
        start = Marker('start')
        first.left = start
        now = first
        next = first
        while next != 'end':
            #start.tree
            next, rest = rest.split_first_item

            if Item.get_subclass('Parenthesis').isopen(now):
                now.child = next
                now = next
            elif Item.get_subclass('Parenthesis').isclose(now):
                head = now.head
                open = head.parent
                left = open.left
                close = now
                placeholder = Item.get_subclass('PlaceHolder')(f'{open}{"..."}{close}')
                open.parent = placeholder
                open.child = None
                left.right = placeholder
                open.right = head
                placeholder.right = next

                now = next
            else:
                now.right = next
                now = next
        next.left = None
        entry = start.right
        entry.left = None
        return entry
    
    @property
    def items(self):
        items = []
        now = self.entry
        while not now is None:
            items += [now]
            now = now.next
        return items
    
    def evaluate(self,dic = {}):
        Priority = Item.get_subclass('Priority')
        entry = self.entry
        now = entry
        while now:
            if isinstance(now, Priority):
                result = now.expression.evaluate()
                result.left = now.left
                result.right = now.right
                now = result
            now = now.right
        
        now = entry
        while now:
            next = now.next
            result = now.bind(next)
            if result:
                result.left = now.left
                result.right = next.right
            now = next
        
        
        pass




    
#if __name__ == '__main__':
#    ipt = input()

