class PicturesqueException(Exception):
   def __init__(self, msg=""):
      self.value = msg
   def __str__(self):
      return self.value
class PicturesqueUnreconizedCommandException(PicturesqueException): pass
class PicturesqueUnreconizedEventException(PicturesqueException): pass
class PicturesqueCommandAlreadyInNamespaceException(PicturesqueException): pass
class PicturesqueWindowNotFoundException(PicturesqueException): pass
class PicturesqueInvalidWidgetException(PicturesqueException): pass