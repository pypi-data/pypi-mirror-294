# This code is from Expert Python Programming.

# The basic pattern here seems to be like currying, in that the args and function are separated.


def mydecorator(function):
    def _mydecorator(*args, **kw):
        # do some stuff before the real function gets called
        res = function(*args, **kw)
        # do some stuff after
        return res

    # returns the sub-function
    return _mydecorator


def mydecorator_with_args(arg1, arg2):
    def _mydecorator_with_args(function):
        def __mydecorator_with_args(*args, **kw):
            # do some stuff before the real function gets called
            res = function(*args, **kw)
            # do some stuff after
            return res

        # returns the sub-function
        return __mydecorator_with_args

    return _mydecorator_with_args
