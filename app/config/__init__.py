import os
import sys

import app.config.settings


# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(sys.modules['app.config.settings'], '{0}Config'.format(APP_ENV))()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not '__' in f]:
   # environment can override anything
   val = os.environ.get(atr, getattr(_current, atr))
   setattr(sys.modules[__name__], atr, val)


def as_dict():
   res = {}
   for atr in [f for f in dir(app.config) if not '__' in f]:
       val = getattr(app.config, atr)
       res[atr] = val
   return res