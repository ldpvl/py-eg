TEXT = """\
Line 1
Line 2
Line 3
DONE
Line 4
Line 5
...
"""

lines = (_ for _ in TEXT.splitlines())

for line in iter(lambda: next(lines), 'DONE'):
    print(line)
