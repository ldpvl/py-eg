
# You want precise control over the symbols that are exported from a module or package
# when a user uses the from module import * statement.

def spam():
    pass

def grok():
    pass

blah = 42

# Only export 'spam' and 'grok'
__all__ = ['spam', 'grok']