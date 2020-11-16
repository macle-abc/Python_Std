def ex2():
    yield 1
    yield 2
    return 3


def ex3():
    a = yield from ex2()
    print("yield from", a)
    b = yield from ex2()
    print("yield from b", b)


for i in ex3():
    print(i)
