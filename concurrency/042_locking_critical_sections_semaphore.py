# Semaphore object is a synchronization primitive based on a shared counter. If the
# counter is nonzero, the with statement decrements the count and a thread is allowed to
# proceed. The counter is incremented upon the conclusion of the with block. If the
# counter is zero, progress is blocked until the counter is incremented by another thread.
# Although a semaphore can be used in the same manner as a standard Lock, the added
# complexity in implementation negatively impacts performance. Instead of simple lock‐
# ing, Semaphore objects are more useful for applications involving signaling between
# threads or throttling. For example, if you want to limit the amount of concurrency in a
# part of code, you might use a semaphore, as follows:

from threading import Semaphore
import urllib.request

# At most, five threads allowed to run at once
_fetch_url_sema = Semaphore(5)

def fetch_url(url):
    with _fetch_url_sema:
        return urllib.request.urlopen(url)