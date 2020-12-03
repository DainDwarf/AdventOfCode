import math
f='#'
g=open(f).read().split('\n')[:-1]
t=lambda s:len([l for i,l in enumerate(g)if s*i==int(s*i)and l[int(s*i)%len(l)]==f])
print(t(3),math.prod(t(s)for s in(0.5,1,3,5,7)))
