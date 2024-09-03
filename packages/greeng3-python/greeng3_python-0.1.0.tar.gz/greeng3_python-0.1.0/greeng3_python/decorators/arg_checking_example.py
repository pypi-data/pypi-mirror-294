# This code is from Expert Python Programming.

from itertools import izip

rpc_info = {}


def xmlrpc(in_=(), out_=(type(None),)):
    def _xmlrpc(function):
        # registering the signature
        func_name = function.func_name
        rpc_info[func_name] = (in_, out_)

        def _check_types(elements, types):
            """Subfunction that checks the types."""
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            types = enumerate(izip(elements, types))
            for index, couple in types:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError(f'arg #{index} should be {of_the_right_type}')

        # wrapped function
        def __xmlrpc(*args):  # no keywords allowed
            # checking what goes in
            checkable_args = args[1:]  # removing self
            _check_types(checkable_args, in_)

            # running the function
            res = function(*args)

            # checking what comes out
            if not type(res) in (tuple, list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res, out_)

            # the function and the type checking succeeded
            return res

        return __xmlrpc

    return _xmlrpc


class RPCView(object):
    @xmlrpc((int, int))
    def method1(self, int1, int2):
        print(f'received {int1} and {int2}')

    @xmlrpc((str,), (int,))
    def method2(self, phrase):
        print(f'received {phrase}')
        return 12
