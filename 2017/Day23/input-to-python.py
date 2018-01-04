def mySimulate():
    a = 0
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

        d=2
        while True:

            e=2
            while True:
                if d*e == b:
                    f=0
                e+=1
                if b == e:
                    break

            d+=1
            if d == b:
                break

        if f == 0:
            h+=1

        if c == b:
            return h
        b+= 17


print(mySimulate())
