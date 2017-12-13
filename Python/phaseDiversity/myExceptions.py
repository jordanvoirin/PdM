class PSFssizeError(ValueError):
   '''Raise when the size of the PSFs are not correct'''
   def __init__(self, message, foo, *args):
       self.message = message
       self.foo = foo
       super(PSFssizeError, self).__init__(message, foo, *args)

class NyquistError(ValueError):
   '''Raise when the PSFs properties do not respect the nyquist criterion'''
   def __init__(self, message, foo, *args):
       self.message = message
       self.foo = foo
       super(NyquistError, self).__init__(message, foo, *args)

class PupilSizeError(ValueError):
    '''Raise when Npupil is bigger than the size of the PSF N'''
    def __init__(self, message, foo, *args):
        self.message = message
        self.foo = foo
        super(PupilSizeError, self).__init__(message, foo, *args)
