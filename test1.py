class B:
    b: str

class A(B):
    a: str


a = A()

a.a = "1"
a.b = "2"

atrr = getattr(a, 'a')

setattr(a, 'a', "5")

print(isinstance(atrr, str))

print(isinstance(a, B))

print(a.a)
