"""The module for any errors from a request."""


class RequestError(RuntimeError):
    def __init__(self, message, err_code):
        super(RuntimeError, self).__init__(message)
        self.message = message
        self.err_code = err_code

    def __str__(self):
        return str(self.err_code) + ": " + str(self.message)
