from config_defaults import *
try:
    from config import *
except ImportError:
    # then just use defaults
    pass
