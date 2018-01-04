from sympy.ntheory.primetest import isprime

def mySimulate():
    a = 1
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0


    b=81
    c=b
    if a != 0:
        b=108100
        c=b+17000
    else:
        b=81
        c=b

    while True:
        f=1

        if not isprime(b):
            h+=1

        if c == b:
            return h
        b+= 17


print(mySimulate())
