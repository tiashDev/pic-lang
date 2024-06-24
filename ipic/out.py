import ipic.errors

class PicturesqueOutputHandler:
    _listeners = {
       "_output": lambda e: "break",
       "_error": lambda e: "break",
       "_clear": lambda e: "break"
    }
    _output = []
    _errors = []
    def bind(self, evt, func):
       if evt == "output":
          self._listeners["_output"] = func
       elif evt == "error":
          self._listeners["_error"] = func
       elif evt == "onrequestclearscreen":
          self._listeners["_clear"] = func
       else:
          raise ipic.errors.PicturesqueUnreconizedEventException(f"\"{evt}\"")
    def output(self, text):
       self._output.append(text)
       self._listeners["_output"](text)
    def error(self, err):
       self._errors.append(err)
       self._listeners["_error"](err)
    def requestclearscreen(self):
       self._listeners["_clear"]()
    def getoutput(self):
       return self._output
    def geterrors(self):
       return self._errors
    def __str__(self):
       return "\n".join(self._output)