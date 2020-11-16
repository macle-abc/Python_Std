def ex():
    print("yield 1")
    yield 1
    print("yield 2")
    yield 2


gen = ex()
print("启动")
a = gen.send(None)
print("get", a)
b = gen.send(None)
print("get", b)
