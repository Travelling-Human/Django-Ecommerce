# monkey_patch.py
from django.core.files import locks

# Override lock and unlock with dummy functions
def dummy_lock(*args, **kwargs):
    return True

def dummy_unlock(*args, **kwargs):
    return True

# Apply monkey patch
locks.lock = dummy_lock
locks.unlock = dummy_unlock