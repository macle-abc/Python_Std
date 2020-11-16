def ex1():
    yield 1
    return 2

def ex2():
    a = yield from ex1()
    print("yield from ", a)
    yield None

gen = ex2()
print(gen.send(None))
print(gen.send(None))
print(gen.send(None))