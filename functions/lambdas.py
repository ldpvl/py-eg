funcs = [lambda x, y=_: x * y for _ in range(5)]

for func in funcs:
    print(func(2))