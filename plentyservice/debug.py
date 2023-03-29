#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains utilities for service endpoint debugging.
"""

import traceback
from functools import wraps


class Debugger:
    def __init__(self, raise_on_err=False):
        self.raise_on_err = raise_on_err

    def handle_exceptions(self):
        """Creates a decorator to return exceptions as response obj.
        Args:
            raise_on_err (bool): whether or not to raise the exception.
        Returns:
            (Response): the traceback and exception as a response object
        """

        def real_decorator(f):
            """Wraps a function with aan exception handler.
            Args:
                f (func): The function to wrap with an exception handler.
            Returns:
                (func): The wrapped function.
            """

            @wraps(f)
            def wrapper(*args, **kwargs):
                """Attempts to run f. On failure will format the exception
                and return it
                Returns:
                    (str): A fail message, or the result of calling f.
                """
                try:
                    return f(*args, **kwargs)
                except:
                    if self.raise_on_err:
                        raise
                    return self.format_error_msg()

            return wrapper

        return real_decorator

    def format_error_msg(self):
        return traceback.format_exc(), 500
