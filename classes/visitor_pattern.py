# You need to write code that processes or navigates through a complicated data structure
# consisting of many different kinds of objects, each of which needs to be handled in a
# different way. For example, walking through a tree structure and performing different
# actions depending on what kind of tree nodes are encountered.

# One weakness of the visitor pattern is its heavy reliance on recursion. If you try to apply
# it to a deeply nested structure, it’s possible that you will hit Python’s recursion depth
# limit (see sys.getrecursionlimit()). To avoid this problem, you can make certain
# choices in your data structures. For example, you can use normal Python lists instead
# of linked lists or try to aggregate more data in each node to make the data more shallow.

# Use of the visitor pattern is extremely common in programs related to parsing and
# compiling. One notable implementation can be found in Python’s own ast module. In
# addition to allowing traversal of tree structures, it provides a variation that allows a data
# structure to be rewritten or transformed as it is traversed (e.g., nodes added or removed).

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value


# Representation of a nested data structure 1 + 2 * (3 - 4) / 5
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

# The first idea is a design strategy where code
# that manipulates a complicated data structure is decoupled from the data structure itself.
# That is, in this recipe, none of the various Node classes provide any implementation that
# does anything with the data. Instead, all of the data manipulation is carried out by
# specific implementations of the separate NodeVisitor class. This separation makes the
# code extremely general purpose.

class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)

        if meth is None:
            meth = self.generic_visit

        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

# The second major idea of this recipe is in the implementation of the visitor class itself.
# In the visitor, you want to dispatch to a different handling method based on some value
# such as the node type.

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand


if __name__ == '__main__':
    e = Evaluator()
    print(e.visit(t4)) # 0.6