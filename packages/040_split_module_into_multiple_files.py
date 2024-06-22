# Often, it’s just easier to unify things and allow a single import like this:
# from mymodule import A, B
# For this latter case, it’s most common to think of mymodule as being one large source
# file. However, this recipe shows how to stitch multiple files together into a single logical
# namespace. The key to doing this is to create a package directory and to use the
# __init__.py file to glue the parts together.

# mymodule.py
# class A:
#     def spam(self):
#         print('A.spam')
#
# class B(A):
#     def bar(self):
#         print('B.bar')


# mymodule/
#   __init__.py
#   a.py # contains class A
#   b.py # contains class B

# __init__.py
# from .a import A
# from .b import B


# >>> import mymodule
# >>> a = mymodule.A()
# >>> a.spam()