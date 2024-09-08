class PicturesqueException(Exception):
   def __init__(self, msg=""):
      self.value = msg
   def __str__(self):
      return self.value
class PicturesqueUnreconizedCommandException(PicturesqueException): pass
class PicturesqueUnreconizedEventException(PicturesqueException): pass
class PicturesqueCommandNotInNamespaceException(PicturesqueException): pass
class PicturesqueWindowNotFoundException(PicturesqueException): pass
class PicturesqueInvalidWidgetException(PicturesqueException): pass
class PicturesqueInvalidOSException(PicturesqueException): pass
class PicturesqueInvalidURLException(PicturesqueException): pass
class PicturesqueTooManyArgumentsException(PicturesqueException): pass
class PicturesqueTooLittleArgumentsException(PicturesqueException): pass
class PicturesqueNotANamespaceException(PicturesqueException): pass