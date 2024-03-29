from items.item import *

class Whole : pass

class RaComplexRoll(str):
    def regex(tags = None) -> str:
        regex = RaComplex.regex(None)
        if tags:
            return f'(?P<RaComplexRoll>({regex})(\s*[+-]\s*({regex}))*)'
        return f'({regex})(\s*[+-]\s*({regex}))*'

    def __new__(cls, seed):
        text = str(seed)
        match = re.fullmatch(cls.regex(), text)
        if not match:
            raise ValueError(f'{seed}')
        sum = RaComplex('0')
        text = re.sub('\s','',text)
        while text:
            match = re.match(RaComplex.regex(),text)
            if match is None:
                raise ValueError(text)
            text = text[len(match.group()):]
            sum = sum.add(match.group())
        return sum


class RaComplex(str):
    def regex(tags = ['Re','Im','r','i']) -> str:
        a = Rational.regex(None)
        b = RaImaginary.regex(None)
        if tags is None:
            return f'({b})|({a})|({a}\s*[+-]\s*{b})'
        return f'(?P<{tags[1]}>{b})|(?P<{tags[0]}>{a})|(?P<{tags[2]}>{a})\s*(?P<{tags[3]}>[+-]\s*({b}))'
    
    @property
    def vector(self):
        match = match = re.fullmatch(RaComplex.regex(), self)
        d = match.groupdict()
        Re, Im, r, i = d['Re'], d['Im'], d['r'], d['i']
        if r and i:
            r = Rational(r)
            i = RaImaginary(i).coefficient
            return r,i
        if Re:
            return Rational(Re), Rational('0')
        if Im:
            return Rational('0'), RaImaginary(Im).coefficient
        
    @property
    def re(self):
        return self.vector[0]
    
    @property
    def im(self):
        return self.vector[1]

    def __new__(cls, seed):
        text = str(seed)
        match = re.fullmatch(cls.regex(), text)
        if not match:
            raise ValueError(f'{seed}')
        d = match.groupdict()
        Re, Im, r, i = d['Re'], d['Im'], d['r'], d['i']
        if r and i:
            r = Rational(r)
            i = RaImaginary(i)
            si = SignedRaImaginary(i)
            if r == '0' and i == '0i':
                return str.__new__(cls, '0')
            if r == '0':
                return str.__new__(cls, i)
            if i == '0i':
                return str.__new__(cls, r)
            return str.__new__(cls, r + si)
        if Re:
            return str.__new__(cls, Rational(Re))
        if Im:
            if RaImaginary(Im) in ['0i', '+0i', '-0i']:
                return RaComplex('0')
            return str.__new__(cls, RaImaginary(Im))
        
    def coefficients_of(u, v = None):
        u = RaComplex(u)
        ur, ui = u.vector
        a, b, c, d = ur.vector + ui.vector
        if v is None:
            return a,b,c,d
        
        v = RaComplex(v)
        vr, vi = v.vector
        e, f, g, h = vr.vector + vi.vector
        return a,b,c,d,e,f,g,h
    
    def add(u, v):
        a,b,c,d,e,f,g,h = RaComplex.coefficients_of(u,v)
        x, y = int(a)*int(f)+int(b)*int(e), int(b)*int(f)
        z, w = int(c)*int(h)+int(d)*int(g), int(d)*int(h)
        real = Rational(f'{x}/{y}')
        imag = SignedRaImaginary(f'{z}/{w}i')
        return RaComplex(f'{real}{imag}')
    
    def sub(u, v):
        a,b,c,d,e,f,g,h = RaComplex.coefficients_of(u,v)
        x, y = int(a)*int(f)-int(b)*int(e), int(b)*int(f)
        z, w = int(c)*int(h)-int(d)*int(g), int(d)*int(h)
        real = Rational(f'{x}/{y}')
        imag = SignedRaImaginary(f'{z}/{w}i')
        return RaComplex(f'{real}{imag}')
    
    @property
    def rev(u):
        return RaComplex('0').sub(RaComplex(u))
    
    def mul(u, v):
        a,b,c,d,e,f,g,h = RaComplex.coefficients_of(u,v)
        mul = lambda a,b,c,d: int(a)*int(b)*int(c)*int(d)
        x, y = mul(a,e,d,h) - mul(b,f,c,g), mul(b,f,d,h)
        z, w = mul(a,g,d,f) + mul(b,h,c,e), mul(b,h,d,f)
        real = Rational(f'{x}/{y}')
        imag = SignedRaImaginary(f'{z}/{w}i')
        return RaComplex(f'{real}{imag}')

    @property
    def inv(u):
        a,b,c,d = RaComplex.coefficients_of(u)
        mul = lambda a,b,c,d: int(a)*int(b)*int(c)*int(d)
        x, y = mul(a,b,d,d), mul(a,a,d,d) + mul(b,b,c,c)
        z, w = -mul(c,d,b,b), mul(a,a,d,d)+ mul(b,b,c,c)
        real = Rational(f'{x}/{y}')
        imag = SignedRaImaginary(f'{z}/{w}i')
        return RaComplex(f'{real}{imag}')
    
    def div(u, v):
        return RaComplex(u).mul(RaComplex(v).inv)
    
        

class RaImaginary(Item):
    def regex(tags = ['coefficient']) -> str:
        regex = Rational.regex(None)
        if tags is None:
            return f'({regex})\s*i|([+-]\s*)*i'
        return f'(?P<{tags[0]}>{regex})\s*i|(?P<i>([+-]\s*)*i)'
    
    @property
    def sign(self):
        return '+-'[self[0]=='-']
    
    @property
    def coefficient(self):
        if self == 'i':
            return Rational('1')
        if self == '-i':
            return Rational('-1')
        return Rational(re.sub('i','',self))
    
    def __new__(cls, seed):
        text = str(seed)
        match = re.fullmatch(cls.regex(['co']), text)
        if not match:
            raise ValueError(f'{seed}')
        co,i = match.groupdict()['co'], match.groupdict()['i']
        if co:
            co = Rational(co)
            if co == '1':
                return str.__new__(cls, f'i')
            if co == '-1':
                return str.__new__(cls, f'-i')
            self = str.__new__(cls, f'{co}i')
            return self
        if i:
            i = re.sub('i','1',i)
            i = Rational(i)
            i = re.sub('1','i',i)
            self = str.__new__(cls, i)
            return self
        raise ValueError(seed)
    
class SignedRaImaginary(RaImaginary):
    def __new__(cls, seed):
        a = RaImaginary(seed)
        if a.sign == '+':
            return str.__new__(cls, f'+{a}')
        return a

class Rational(RaComplex,Item):
    @property
    def sign(self) -> str:
        return ('+','-')[self[0]=='-']
    
    @property
    def vector(self):
        if not '/' in self:
            return Whole(self), Whole('1')
        regx = Rational.regex(['a','b','c','d']).split('|')[0]
        match = re.fullmatch(regx,self)
        if match:
            d = match.groupdict()
            return Whole(d['a']), Whole(d['b'])
    
    @property
    def numerator(self):
        return self.vector[0]
    @property
    def denominator(self) -> Whole:
        return self.vector[1]
    
    def regex(tags = ['a','b','whole','fraction']) -> str:
        regex = Whole.regex(None)
        if tags is None:
            return f'({regex})\/({regex})|({regex})(\.\d+)?'
        a, b, c, d = tags
        return f'(?P<{a}>({regex}))\/(?P<{b}>({regex}))|(?P<{c}>({regex}))(\.(?P<{d}>\d+))?'

    def __new__(cls, seed):
        text = str(seed)
        match = re.fullmatch(cls.regex(['a','b','c','d']), text)
        if not match:
            raise ValueError(f'{seed}')
        
        dic = match.groupdict()
        a, b, whole, fraction = dic['a'], dic['b'], dic['c'], dic['d']

        if a and b:
            sa, sb = SignedWhole(a), SignedWhole(b)
            ua, ub = UnsignedWhole(a), UnsignedWhole(b)
            sign = ['+','-'][sa.sign != sb.sign]
            ia, ib = int(ua), int(ub)
            ic = math.gcd(ia,ib)
            ua, ub = int(ia/ic), int(ib/ic)
            shown_sign = ['','-'][sa.sign != sb.sign]
            self = str.__new__(cls, f'{shown_sign}{ua}/{ub}')
            if self.denominator == '0':
                if self.numerator.int > 0:
                    return str.__new__(cls, '1:0')
                if self.numerator.int < 0:
                    return str.__new__(cls, '-1:0')
                return str.__new__(cls, '0:0')
            if self.denominator == '1':
                return self.numerator
            return self
        
        elif whole and fraction:
            sign = '+-'[whole.count('-') % 2]

            whole = UnsignedWhole(whole)
            fraction = re.sub('0+$','',fraction)
            a = int(f'{whole}{fraction}')
            b = pow(10,len(fraction))
            for c in (2,5):
                while (a/c) == int(a/c) and (b/c) == int(b/c):
                    a, b = a/c, b/c
            return Rational(f'{sign}{int(a)}/{int(b)}')
        
        try:
            return Whole(seed)
        except:
            raise ValueError(f'{seed}')
    
class SignedRational(Rational):
    def __new__(cls, seed):
        a = Rational(seed)
        if a.sign == '+':
            return str.__new__(cls, f'+{a}')
        return a
    
class Whole(Rational):
    def regex(tags = None):
        return '([+-]\s*)*\d+'
    
    def __new__(cls, seed):
        text = cls.simplify(str(seed))
        text = str(int(text))
        match = re.fullmatch(cls.regex(), text)
        if not match:
            raise ValueError(f'{seed}')
        self = str.__new__(cls, cls.simplify(text))
        return self


    @property
    def int(self):
        return int(self)
    
    def simplify(text):
        minus = text.count('-') % 2
        return re.sub('([+-]\s*)+',('','-')[minus],text)

class SignedWhole(Whole):
    def simplify(text):
        minus = text.count('-') % 2
        return re.sub('([+-]\s*)+',('+','-')[minus],text)

class UnsignedWhole(Whole):
    def simplify(text):
        minus = text.count('-') % 2
        return re.sub('([+-]\s*)+',('','')[minus],text)