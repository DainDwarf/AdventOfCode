s=set(int(l.translate(l.maketrans('BFRL','1010')),2)for l in open("i"))
print(max(s),set(range(min(s),max(s)))-s)
