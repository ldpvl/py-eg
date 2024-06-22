
# Creating a directory or zip file and adding a __main__.py file is one possible way to
# package a larger Python application. It’s a little bit different than a package in that the
# code isn’t meant to be used as a standard library module that’s installed into the Python
# library. Instead, it’s just this bundle of code that you want to hand someone to execute.
# Since directories and zip files are a little different than normal files, you may also want
# to add a supporting shell script to make execution easier. For example, if the code was
# in a file named myapp.zip, you could make a top-level script like this:
# #!/usr/bin/env python3 /usr/local/bin/myapp.zip

# myapplication/
#   spam.py
#   bar.py
#   grok.py
#   __main__.py

# bash % python3 myapplication

# bash % python3 myapp.zip