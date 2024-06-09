import ipic.errors

class PicturesqueOutputHandler:
    _listeners = {
       "_output": lambda e: "break",
       "_error": lambda e: "break"
    }
    _output = ""
    _errors = []
    def bind(self, evt, func):
       if evt == "output":
          self._listeners["_output"] = func
       elif evt == "error":
          self._listeners["_error"] = func
       else:
          raise ipic.errors.PicturesqueUnreconizedEventException(f"\"{evt}\"")
    def output(self, text):
       self._output += f"{text}\n"
       self._output = self._output[:-1]
       self._listeners["_output"](text)
    def error(self, err):
       self._errors.append(err)
       self._listeners["_error"](err)
    def getoutput(self):
       return self._output
    def geterrors(self):
       return self._errors
    def __str__(self):
       return self._output