import ast
from pprint import pprint

ex = ast.parse('2 + 3*4 + x', mode='eval')
print(ex)

pprint(ast.dump(ex))

# Analyzing the source tree requires a bit of study on your part, but it consists of a col‐
# lection of AST nodes. The easiest way to work with these nodes is to define a visitor
# class that implements various visit_NodeName() methods where NodeName() matches
# the node of interest.

# Here is an example of a decorator that lowers globally
# accessed names into the body of a function by reparsing the function body’s source code,
# rewriting the AST, and recreating the function’s code object:


import ast
import inspect


# Node visitor that lowers globally accessed names into
# the function body as local variables.
class NameLower(ast.NodeVisitor):
    def __init__(self, lowered_names):
        self.lowered_names = lowered_names

    def visit_FunctionDef(self, node):
        # Compile some assignments to lower the constants
        code = '__globals = globals()\n'
        code += '\n'.join("{0} = __globals['{0}']".format(name)
                          for name in self.lowered_names)
        code_ast = ast.parse(code, mode='exec')
        # Inject new statements into the function body
        node.body[:0] = code_ast.body
        # Save the function object
        self.func = node


# Decorator that turns global names into locals
def lower_names(*namelist):
    def lower(func):
        srclines = inspect.getsource(func).splitlines()
        # Skip source lines prior to the @lower_names decorator
        for n, line in enumerate(srclines):
            if '@lower_names' in line:
                break

        src = '\n'.join(srclines[n + 1:])

        # Hack to deal with indented code
        if src.startswith((' ', '\t')):
            src = 'if 1:\n' + src
        top = ast.parse(src, mode='exec')

        # Transform the AST
        cl = NameLower(namelist)
        cl.visit(top)

        # Execute the modified AST
        temp = {}
        exec(compile(top, '', 'exec'), temp, temp)

        # Pull out the modified code object
        func.__code__ = temp[func.__name__].__code__
        return func
    return lower


# To use this code, you would write code such as the following:
INCR = 1

@lower_names('INCR')
def countdown(n):
    while n > 0:
        n -= INCR

# The decorator rewrites the source code of the countdown() function to look like this:

# def countdown(n):
#     __globals = globals()
#         INCR = __globals['INCR']
#         while n > 0:
#             n -= INCR

# In a performance test, it makes the function run about 20% faster.
# Now, should you go applying this decorator to all of your functions? Probably not.
# However, it’s a good illustration of some very advanced things that might be possible
# through AST manipulation, source code manipulation, and other techniques.


countdown(1000000)