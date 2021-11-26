

def mutable_default_value_func(a=[]):
    return a

a_ = mutable_default_value_func()
print(a_)
a_.append(1)
print(mutable_default_value_func()) # default value has changed to [1]


_no_value = object()

def no_value_func(a, b=_no_value):
    # From Python Cookbook:
    # A function that tests to see whether a value (any value) has been supplied to an optional argument or not.
    # The tricky part here is that you can’t use a default value of None , 0 , or False to test for the presence
    # of a user-supplied argument (since all of these are perfectly valid values that a user might
    # supply). Thus, we need something else to test against.
    if b is _no_value:
        print(f'b was not given any value: {b}, setting to empty list')
        b = []
    print(a, b)

no_value_func(1) # goes into if clause
no_value_func(1, None) # None does not behave same as no value


