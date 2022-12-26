from datetime import datetime
import copy


class Number:
    def __init__(self, hexnumb):
        self.coef = []
        self.r = 0
        hexnumb=(1024-len(hexnumb))*'0'+hexnumb
        for i in range(256):
            self.coef.append(int(hexnumb[1020-4*i:1024-4*i],16))

    def __add__(self, snumb):
        carry = 0
        c = Number('0')
        for i in range(256):
                t = self.coef[i] + snumb.coef[i] + carry
                c.coef[i] = t & (65535)
                carry = t >> 16
        return c

    def __sub__(self, snumb):
            borrow = 0
            c = Number('0')
            for i in range(256):
                t = self.coef[i] - snumb.coef[i] - borrow
                if t >= 0:
                    c.coef[i] = t
                    borrow = 0
                else:
                    c.coef[i] = (65535) + t
                    borrow = 1
            if borrow != 0:
                print('Negative number')
            return c

    def __eq__(self, snumb):
            i = 255
            while(self.coef[i] == snumb.coef[i]):
                i = i - 1
                if(i == -1):
                    return 0
                else:
                    if (self.coef[i] >= snumb.coef[i]):
                        return 1
                    else:
                        return -1

    def LongMulOneDigit(self, snumb):
            carry = 0
            c = Number('0')
            for i in range(256):
                t = self.coef[i] * snumb + carry
                c.coef[i] = t & (65535)
                carry = t >> 16
            c.coef.append(carry)
            return c

    def LongShiftDigitsToHigh(self, snumb):
            k = copy.deepcopy(self)
            for i in range(snumb):
                self.coef.insert(0, 0)
                self.coef.pop()
            return k

    def __mul__(self, snumb):
            c = Number('0')
            for i in range(256):
                t = self.LongMulOneDigit(snumb.coef[i])
                t.LongShiftDigitsToHigh(i)
                c = c + t
            return c

    def __floordiv__(self, snumb):
        t1 = list(self.coef)
        t2 = list(snumb.coef)
        self.coef=list(self.convert2bin())
        snumb.coef=list(snumb.convert2bin())

        for i in range(len(self.coef)):
            self.coef[i]=int(self.coef[i])

        for i in range(len(snumb.coef)):
            snumb.coef[i]=int(snumb.coef[i])

        k = snumb.BitLength()
        R = copy.deepcopy(self)
        Q = Number('0')
        Q.coef = list(Q.convert2bin())

        for i in range(len(Q.coef)):
            Q.coef[i] = int(Q.coef[i])
        while not R >= snumb:
            n = R.BitLength()
            c = snumb.LongShiftDigitsToHigh(n-k)
            if c>=R-Number('1'):
                n = n-1
                c = snumb.LongShiftDigitsToHigh(n-k)
            R = R-c
            Q.coef[n-k]=1
        self.coef = t1
        snumb.coef = t2
        Q = Q.convert2hex()
        Q.r = R.coef[0]
        return Q, R
    __truediv__=__floordiv__

    def convert2bin(self):
        i=255
        res=""
        while i!=-1:
            t=bin(self.coef[i])[2:]
            if len(t)==16:
                res = res + t
            else:
                t = bin(self.coef[i])[2:]
                while len(t)!=16:
                    t = '0'+ t
                res = res + t
            i-=1
        return res

    def __pow__(self,snumb):
        c = Number('1')
        t = snumb.convert2bin()[::-1]
        for i in range(BitLength_str(t),-1,-1):
            if t[i]=='1':
                c=c*self
            if i!=0:
                c=c*c
        return c

    def convert(self):
        i = 255
        result = ""
        while i != -1:
            t = hex(self.coef[i])[2:]
            if len(t) == 4:
                result = result + t
            else:
                t = hex(self.coef[i])[2:]
                while len(t) != 4:
                    t = '0' + t
                result = result + t
            i -= 1
        return result

    def bin_convert(self):
            i=255
            result = ""
            while i!=-1:
                list = bin(self.coef[i])[2:]
                if len(t)==16:
                    result = result + t
                else:
                    t = bin(self.coef[i])[2:]
                    while len(t)!=16:
                        t = '0' + t
                    result = result+t
                i-=1
            return result



    def convert2hex(self):
        for i in range(len(self.coef)):
            self.coef[i] = str(self.coef[i])
        return Number(hex(int(''.join(self.coef)[::-1],2))[2:])

    def BitLength(self):
        for i in range(255,-1,-1):
            if self.coef[i]!=0:
                return i

def BitLength_str(arg):
    for i in range(len(arg)-1,-1,-1):
        if arg[i]!='0':
            return i



start_time = datetime.now()



a = Number('DAF1ABDA4AD4D9FE3E36A529210C2AE99B905922FC0519798A26E351FE23AF375AD6BA288EE030B70DF0CE1CDF1E8B75BA56494DC6ED36B181814CD5783E6C81')
b = Number('3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7')
#b = Number('10')
print((a+b).convert().lstrip("0"))
print((a-b).convert().lstrip("0"))

print((a*b).convert().lstrip("0"))
#print((a/b).convert())
print((b*b).convert().lstrip("0"))
print(pow(b, a).convert().lstrip("0"))

#print((a*b).bin_convert())
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))











