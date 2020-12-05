s=set(int(l.translate({66:49,70:48,82:49,76:48}),2)for l in open("i"))
print(max(s),set(range(min(s),max(s)))-s)
