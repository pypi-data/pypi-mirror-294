sdfg = []
def andgate(a,b,c,d):
    if(d=="triple"):
        if(a==b):
            x=c
        else:
            x=0
        return x
    if(d=="double"):   
        if(a==b):
            aa=1
        else:
            aa=0
        return aa

def xorgate(a,b):
    if(a+b<2):
        if(a+b==0):
            c=0
        else:
            c=1
    else:
        c=0
    return c

def orgate(a,b):
    if(a+b<2):
        if(a+b==0):
            c=0
        else:
            c=1
    else:
        if(a+b<=2):
            c=1
    return c
def notgate(a):
    if(a==1):
        c=0
    else:
        c=1
    return c
def fullbinadder(in1,in2,b):
    xor1 = xorgate(in1,in2)
    xor2 = xorgate(xor1,b)
    and1 = andgate(b,xor1)
    and2 = andgate(in1,in2)
    or1 = orgate(and1,and2)
    return xor2, or1
