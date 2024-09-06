from __init__ import NumberBase, Bases

n = NumberBase(222, "01")
n

print(repr(n))
print("bn+1:", n+1)
print("hex:", n.to_base(Bases.HEXADECIMAL))
print("decimal:", n.to_base(Bases.DECIMAL))
print("object:", list(n.to_base([1, "2", type, print])))
print("base 4:", n.to_base(list(range(4))))
print()
print("iter through the digits of the number:")

for x in n:
    print(x, end=", ")

import pickle
d = pickle.dumps(n)
print("From pickle data:")
print(repr(pickle.loads(d)))