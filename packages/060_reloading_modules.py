
# >>> import spam
# >>> import imp
# >>> imp.reload(spam)
# <module 'spam' from './spam.py'>
# >>>

# Reloading a module is something that is often useful during debugging and develop‐
# ment, but which is generally never safe in production code due to the fact that it doesn’t
# always work as you expect.
# Under the covers, the reload() operation wipes out the contents of a module’s under‐
# lying dictionary and refreshes it by re-executing the module’s source code. The identity
# of the module object itself remains unchanged. Thus, this operation updates the module
# everywhere that it has been imported in a program.
# However, reload() does not update definitions that have been imported using state‐
# ments such as from module import name.

# # spam.py
# def bar():
#   print('bar')
#
# def grok():
#   print('grok')
#
# Now start an interactive session:
# >>> import spam
# >>> from spam import grok
# >>> spam.bar()
# bar

# >>> grok()
# grok
# >>>

# Without quitting Python, go edit the source code to spam.py so that the function grok()
# looks like this:
# def grok():
#   print('New grok')

# >>> import imp
# >>> imp.reload(spam)
# <module 'spam' from './spam.py'>
# >>> spam.bar()
# bar
# >>> grok() # Notice old output
# grok
# >>> spam.grok() # Notice new output
# New grok
# >>>

# In this example, you’ll observe that there are two versions of the grok() function loaded.
# Generally, this is not what you want, and is just the sort of thing that eventually leads
# to massive headaches.
# For this reason, reloading of modules is probably something to be avoided in production
# code. Save it for debugging or for interactive sessions where you’re experimenting with
# the interpreter and trying things out.