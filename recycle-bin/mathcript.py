import re
from fractions import Fraction
class Statement(str):
    def __new__(cls):
        self = str.__new__()
        return self
class Expression(str):
    def __new__(cls):
        self = str.__new__()
        return self
class Definition(str):
    def __new__(cls):
        self = str.__new__()
        return self
    

class Letter(str):
    def __new__(cls, text:str):
        match = re.match('(?P<letter>[a-zA-Z])?(?P<name>_([a-zA-Z]+)+)?',text)
        if match:
            self = str.__new__(cls,text)
            d = match.groupdict()
            self.letter = d['letter']
            self.name = d['name'][1:]
            return self


class Rational:
    pass
class Whole:
    pass

class RationalComplex(str):
    real: Rational
    imaginary: Rational
    def __new__(cls, text:str):
        f = '[0-9]+:[+-]?[0-9]+'
        d = '[0-9]+(\.[0-9]*)?'
        r = f'{f}|{d}'
        match_real = re.match(f'^(?P<real>[+-]?({r}))$', text)
        match_imaginary = re.match(f'^(?P<imaginary>[+-]?({r}|)?)i$', text)
        match_complex = re.match(f'^(?P<real>[+-]?({r}))(?P<imaginary>[+-]({r}|)i)$', text)

        if match_real:
            d = match_real.groupdict()
            a, b = Rational(d['real']), Rational('0')
            self = Rational(a)
            self.real = a
            self.imaginary = b
            return self
        
        if match_imaginary:
            d = match_imaginary.groupdict()
            a, b = Rational('0'), d['imaginary']
            if b in ('1', '', '+', '+1'):
                b = '1'
            if b in ('-1','-'):
                b = '-1'

            b = Rational(b)
            if b == '1':
                self = str.__new__(cls,'i')
                self.real = a
                self.imaginary = Rational('1')
                return self
            if b == '-1':
                self = str.__new__(cls,f'-i')
                self.real = a
                self.imaginary = Rational('-1')
                return self
            if b == '0':
                self = str.__new__(cls,'0')
                self.real = a
                self.imaginary = Rational('0')
                return self
        
            self = str.__new__(cls,f'{b}i')
            self.real = a
            self.imaginary = Rational(b)
            return self
        
        if match_complex:
            d = match_complex.groupdict()
            a,b = Rational(d['real']), RationalComplex(d['imaginary'])
            #print(text,d,a)
            if a == '0':
                return RationalComplex(b)
            if b == '0':
                return RationalComplex(a)
            sign = b[0]
            bb = b
            if sign != '-':
                sign = '+'
            else:
                bb = b[1:]
            self = str.__new__(cls,f'{a}{sign}{bb}')
            self.real = a
            self.imaginary = b.imaginary
            return self
    
    def add(z1, z2):
        z1 = RationalComplex(z1)
        z2 = RationalComplex(z2)
        a1, b1 = z1.real, z1.imaginary
        a2, b2 = z2.real, z2.imaginary
        #print(a1,b1,a2,b2,a1.sign,b1.sign,a2.sign,b2.sign)
        a1u, a1d = int('-+'[a1.sign]+a1.numerator), int(a1.denominator)
        b1u, b1d = int('-+'[b1.sign]+b1.numerator), int(b1.denominator)
        a2u, a2d = int('-+'[a2.sign]+a2.numerator), int(a2.denominator)
        b2u, b2d = int('-+'[b2.sign]+b2.numerator), int(b2.denominator)
        #print(a1u,a1d,b1u,b1d,a2u,a2d,b2u,b2d)
        a3 = Rational(f'{a1u*a2d+a2u*a1d}:{a2d*a1d}')
        b3 = Rational(f'{b1u*b2d+b2u*b1d}:{b2d*b1d}')
        #print(f'{a1u*a2d+a2u*a1d}:{a2d*a1d}')
        if b3.sign:
            sign = '+'
        else:
            sign = '-'
            b3 = b3[1:] 
        return RationalComplex(f'{a3}{sign}{b3}i')
    
    def sub(z1, z2):
        z1 = RationalComplex(z1)
        z2 = RationalComplex(z2)
        a1, b1 = z1.real, z1.imaginary
        a2, b2 = z2.real, z2.imaginary
        #print(a1,b1,a2,b2,a1.sign,b1.sign,a2.sign,b2.sign)
        a1u, a1d = int('-+'[a1.sign]+a1.numerator), int(a1.denominator)
        b1u, b1d = int('-+'[b1.sign]+b1.numerator), int(b1.denominator)
        a2u, a2d = int('-+'[a2.sign]+a2.numerator), int(a2.denominator)
        b2u, b2d = int('-+'[b2.sign]+b2.numerator), int(b2.denominator)
        #print(a1u,a1d,b1u,b1d,a2u,a2d,b2u,b2d)
        a3 = Rational(f'{a1u*a2d-a2u*a1d}:{a2d*a1d}')
        b3 = Rational(f'{b1u*b2d-b2u*b1d}:{b2d*b1d}')
        #print(f'{a1u*a2d+a2u*a1d}:{a2d*a1d}')
        if b3.sign:
            sign = '+'
        else:
            sign = '-'
            b3 = b3[1:] 
        return RationalComplex(f'{a3}{sign}{b3}i')

    def mul(z1, z2):
        z1 = RationalComplex(z1)
        z2 = RationalComplex(z2)
        a1, b1 = z1.real, z1.imaginary #(a1+b1i)(a2+b2i)
        a2, b2 = z2.real, z2.imaginary # a1a2 - b1b2 + (a1b2 + b1a2)i
        #print(a1,b1,a2,b2,a1.sign,b1.sign,a2.sign,b2.sign)
        a1u, a1d = int('-+'[a1.sign]+a1.numerator), int(a1.denominator)
        b1u, b1d = int('-+'[b1.sign]+b1.numerator), int(b1.denominator)
        a2u, a2d = int('-+'[a2.sign]+a2.numerator), int(a2.denominator)
        b2u, b2d = int('-+'[b2.sign]+b2.numerator), int(b2.denominator)
        #print(a1u,a1d,b1u,b1d,a2u,a2d,b2u,b2d)
        a1a2 = Rational(f'{a1u*a2u}:{a1d*a2d}')
        b1b2 = Rational(f'{b1u*b2u}:{b1d*b2d}')
        a1b2 = Rational(f'{a1u*b2u}:{a1d*b2d}')
        a2b1 = Rational(f'{a2u*b1u}:{a2d*b1d}')
        a3 = a1a2.sub(b1b2)
        b3 = a1b2.add(a2b1)
        #print(f'{a1u*a2d+a2u*a1d}:{a2d*a1d}')
        if b3.sign:
            sign = '+'
        else:
            sign = '-'
            b3 = b3[1:] 
        return RationalComplex(f'{a3}{sign}{b3}i')
    def reverse(self):
        return RationalComplex('0').sub(self)
    def inverse(self):
        z = RationalComplex(self)
        a, b = z.real, z.imaginary #a2 = a/(a*a + b*b)
        au, ad = int('-+'[a.sign]+a.numerator), int(a.denominator)
        bu, bd = int('-+'[b.sign]+b.numerator), int(b.denominator)
        #print(a1u,a1d,b1u,b1d,a2u,a2d,b2u,b2d)
        a3 = Rational(f'{au*ad*bd*bd}:{au*au*bd*bd+bu*bu*ad*ad}')
        b3 = Rational(f'{-bu*bd*ad*ad}:{au*au*bd*bd+bu*bu*ad*ad}')
        #print(f'{a1u*a2d+a2u*a1d}:{a2d*a1d}')
        if b3.sign:
            sign = '+'
        else:
            sign = '-'
            b3 = b3[1:] 
        return RationalComplex(f'{a3}{sign}{b3}i')
    def div(z1, z2):
        z1 = RationalComplex(z1)
        z2 = RationalComplex(z2)
        return z1.mul(z2.inverse())

class Rational(RationalComplex):
    sign: bool
    numerator: Whole
    denominator: Whole
    approximate: float
    def __new__(cls, text:str):
        match_fraction = re.match('^(?P<sign1>[+-])?(?P<a>[0-9]+):(?P<sign2>[+-])?(?P<b>[0-9]+)$',text)
        match_decimal = re.match('^(?P<sign>[+-])?(?P<whole>[0-9]+)(\.(?P<frac>[0-9]*))?$',text)
        if match_decimal:
            d = match_decimal.groupdict()
            w,f = d['whole'], ''
            if d['frac']:
                f = d['frac']
            sign = d["sign"]
            if sign is None:
                sign = '+'
            #print(f'{sign}{w+f}:1{"0"*len(f)}')
            return Rational(f'{sign}{w+f}:1{"0"*len(f)}')
        if match_fraction:
            d = match_fraction.groupdict()
            f = Fraction(int(d['a']), int(d['b']))
            a,b = Whole(f'{f.numerator}'), Whole(f'{f.denominator}')
            sign1,sign2 = d['sign1'], d['sign2']
            if sign1 is None:
                sign1 = '+'
            if sign2 is None:
                sign2 = '+'
            if sign1 == sign2 :
                sign = ''
            else:
                sign = '-'
            if a == '0':
                self = Whole('0')
                self.sign = True
                self.numerator = Whole('0')
                self.denominator = Whole('1')
                self.approximate = 0
                return self
            if b == '1':
                self = Whole(sign + a)
                self.sign = (sign!='-')
                self.numerator = Whole(a)
                self.denominator = Whole('1')
                self.approximate = float(self)
                return self

            self = str.__new__(cls,sign + f'{a}' + (f':{b}','')[b==1])
            self.numerator, self.denominator = a, b
            self.sign = (sign!='-')
            self.approximate = int(a) / int(b)
            self.a, self.b = a,b
            return self
        try:
            return Rational(RationalComplex(text))
        except:
            raise ValueError('')
        

    
    
class Whole(Rational):
    value: int
    sign: bool
    def __new__(cls, text:str):
        match = re.match('^[+-]?[0-9]+(\.0*)?$',text)
        if match:
            n = int(float(text))
            self = str.__new__(cls,str(n))
            self.value = n
            self.sign = (n>=0)
            return self
        try:
            return Whole(Rational(text))
        except:
            raise ValueError('')
        

class Context:
    def __init__(self):
        self.definitions = {
            'y': 'x+1'
        }

    def expression(self, expression):
        pass

def match_element(expression,operator = True):
    names = {
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'cot': 'cot',
        'arcsin': 'sin^-1|arcsin',
        'arccos': 'cos^-1|arccos',
        'arctan': 'tan^-1|arctan',
        'arccot': 'cot^-1|arccot',
        'limit': 'lim',
        'converge': '->',
        'integral': 'In',
        'differentiate': 'd_',
        'pi': 'pi',
    }
    fraction = f'[0-9]+:[+-]?[0-9]+'
    decimal = f'[0-9]+(\.[0-9]*)?'
    rational = f'({fraction}|{decimal})'
    rational_complex = f'[+-]?{rational}[+-]{rational}?i|[+-]?{rational}?i|([+-]?{rational})'
    operators = {
        'addition': '\+',
        'substraction': '\-',
        'multiplication': '\*',
        'division': '\/',
        'power': '\^',
        'follow':'\,',
    }
    operatorregx = '|'.join([f'(?P<{name}>{o})' for name, o in operators.items()])
    d = {
        'context':      '\|',
        'equals':       '\=',
        'punc':         '\,',
        'rational complex': rational_complex,
        'letter':       '([a-zA-Z]\'*)(_[a-zA-Z0-9\s]+)?|_[a-zA-Z0-9\s]+', # t'(time) + 1   

        'spacer':       '\s+',

    }
    for name,regx in names.items():
        match = re.match(regx, expression)
        if match:
            return name, match.group()
    if operator:
        match = re.match(operatorregx, expression)
        if match:
            return 'operator', match.group()
    for name,regx in d.items():
        match = re.match(regx, expression)
        if match:
            return name, match.group()
    raise ValueError

class Element(str):
    def __new__(cls, text, index, operator = True):
        d = {
            '(':('\(','\)',')','expression'),
            '>(':('\>\(','\)\<',')<','fine expression'),
            '[':('\[','\]',']','context'),
            '{':('\{','\}','}','set'),
            '>>':('\>\>','\<\<','<<','string'),
            '/*':('\/\*','\*\/','*/','comment'),
        }
        for open in d.keys():
            match = re.match(d[open][0],text)
            if match:
                i = 1
                count = 1
                close_match = re.match(d[open][1],text[i:])
                while (not close_match) or (not count == 0):
                    open_match = re.match(d[open][0],text[i:])
                    close_match = re.match(d[open][1],text[i:])
                    if open_match:
                        count += 1
                    if close_match:
                        count -= 1
                    i += 1
                self = Expression(text[len(open):i-1])
                self.length = i + len(d[open][2]) - 1
                self.name = d[open][3]
                self.index = index
                self.simplest = False
                self.unknown = False
                return self
        name, element = match_element(text,operator=operator)
        self = str.__new__(cls, element)
        self.length = len(self)
        self.name = name
        self.index = index
        self.simplest = True
        if self.name == 'letter':
            self.simplest = False
        self.unknown = False
        return self

class Expression(str):
    pass

RC = RationalComplex


operator = {
    '+': lambda a, b: RC.add(a,b),
    '-': lambda a, b: RC.sub(a,b),
    '*': lambda a, b: RC.mul(a,b),
    '/': lambda a, b: RC.div(a,b),
}

def evaluate(elements, context):
    #a = input()
    if len(elements) == 1:
        element = elements[0]
        if element.name in ('expression'):
            return Expression(element).evaluate(context)
        if element.name in ('fine expression', 'rational complex'):
            return element
        if element.name == 'letter':
            if element in context.keys():
                return Element(context[element],operator=False)
            else:
                element.name = 'fine expression'
                return element
        raise ValueError
            
        
    if len(elements) == 2:
        e1, e2 = elements

        
        e1 = Expression(e1).evaluate(context)
        e2 = Expression(e2).evaluate(context)
        
        if 'fine expression' in (e1.name,e2.name):
            element = str.__new__(Element,f'(({e1})({e2}))')
            element.name = 'fine expression'
            return element

        return operator['call'](e1,e2)
    
    e1, e2, e3, *E = elements

    if e2.name == 'operator':

        e1 = Expression(e1).evaluate(context)
     
        e3 = Expression(e3).evaluate(context)
        
        if 'fine expression' in (e1.name,e3.name):
            element = str.__new__(Element,f'(({e1}){e2}({e3}))')
            element.name = 'fine expression'
            return evaluate([element]+E, context)
        
        e4 = Element(operator[e2](e1,e3),operator = False)

        return evaluate([e4]+E, context)
    
    e1 = Expression(e1).evaluate(context)
    e2 = Expression(e2).evaluate(context)
    if 'fine expression' in (e1.name,e2.name):
        element = str.__new__(Element,f'(({e1})({e2}))')
        element.name = 'fine expression'
        return evaluate([element,e3]+E, context)
    
    e4 = Element(operator['call'](e1,e2))
    return evaluate([e4,e3] + E, context)

    

class Expression(str):
    def __new__(cls, expression, context = {}):
        self = str.__new__(cls, expression)
        self.context = context
        self.init_elements()
        return self
    
    def init_elements(self):
        expression = self
        self.elements = []
        element = Element(expression,0)
        expression = expression[element.length:]
        self.elements.append(element)
        while expression:
            last = self.elements[len(self.elements)-1]
            element = Element(expression,last.index + last.length)
            expression = expression[element.length:]
            self.elements.append(element)

    def tree(self):
        print(self.elements)
        for element in self.elements:
            try:
                print(f'{element}: {element.elements}')
            except:
                pass
    def evaluate(self, context = {}):
        #self.init_elements()
        levels = [
            '^',
            '*/',
            '+-',
            ','
        ]
        if len(self.elements) == 1:
            element = self.elements[0]
            if element.simplest or element.unknown:
                return element
            if element.name in ('expression'):
                return Expression(element).evaluate(context)
            if element.name == 'letter':
                if element in context.keys():
                    return Element(context[element],0,operator=False)
                else:
                    element.unknown = True
                    element.simplest = True
                    return element
            raise ValueError
        

        for i in range(len(self.elements)-1):
            a = Expression(self.elements[i]).evaluate(context)
            b = Expression(self.elements[i+1]).evaluate(context)
            if not 'operator' in (a.name, b.name):
                c = a.call(b)
                
                return Expression(self[:a.index] + c + self[b.index + b.length:]).evaluate(context)

        for operators in levels:
            for i, element in enumerate(self.elements):
                if element in operators:
                    o = element
                    a = self.elements[i-1]
                    b = self.elements[i+1]
                    l,r = a.index, b.index + b.length
                    a = Expression(a).evaluate(context)
                    b = Expression(b).evaluate(context)
                    if a.unknown or b.unknown:
                        c = str.__new__(Element,self[l:r])
                        c.name = 'expression'
                        c.length = r-l
                        c.index = l
                        c.simplest = True
                        c.unknown = True
                        self.elements = self.elements[:i-1]+[c]+self.elements[i+2:]
                        print(self,[ele.unknown for ele in self.elements])
                        return self.evaluate(context)
                    else:
                        c = operator[o](a, b)
                    print(self)
                    return Expression(self[:l] + c + self[r:]).evaluate(context)
                

'''        
        self.sub = ('','')
        self.operation = ''
        if len(self.elements) == 1:
            return self
        if len(self.elements) == 2:
            a,b = self.elements
            self.sub = (Expression(a[1]),Expression(b[1]))
            self.operation = 'call'
            return self
        else:
            a,b,*_ = self.elements
            self.sub = (Expression(a[1]),Expression(b[1]))
            self.operation = ''
            return self

        return self'''





if __name__ == '__main__':
    
    
    pass



'''
y := 1/x    #Definition
y | x=2   #Expression
>>1/2

y | x->inf
>>exists A, for any eps exists N, for any n>N, ||(y | x=n) - A|| < eps
A | 


{x|y=1}
>>{1,-1}

A = {y|x in {1,2,3,4}}
sum(A)
>>10
product(A)
>>24
min(A)
>>1
max(A)
>>4


f := x >> y  #function definition
f := x >> 2x
f(x) := 2x
x := f(x)/2
f(2) #expression to call function
>>4

lim(f(x)|x->0)
f' := lim((f(x+dx)-f(x))/dx|dx->0)

'''