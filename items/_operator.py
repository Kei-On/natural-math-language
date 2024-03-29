from items.item import *
class Operator(Item):
    dict = {

            '+':{
                'name': 'plus',
                'regex': '\+',
            },
            '-':{
                'name': 'minus',
                'regex': '\-',
            },
            '*':{
                'name': 'times',
                'regex': '\*',
            },
            '/':{
                'name': 'over',
                'regex': '\/',
            },
            '=':{
                'name': 'equals',
                'regex': '\=',
            },            
            ',':{
                'name': 'punctuation',
                'regex': '\,',
            },
            '|':{
                'name': 'splitter',
                'regex': '\|',
            }
        }
    def regex(tags = None):
        if tags:
            a = '|'.join([f"(?P<{d['name']}>{d['regex']})" for d in Operator.dict.values()])
            return f'{a}'
        a = '|'.join([d['regex'] for d in Operator.dict.values()])
        return f'{a}'
    

    def __new__(cls, seed):
        if re.match(cls.regex(),seed):
            return str.__new__(cls, seed)
        raise ValueError(seed)

