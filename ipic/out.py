import ipic.errors

DEFAULT_LAMBDA = lambda *a: None

class PicturesqueOutputHandler:
    _listeners = {
       "_output": DEFAULT_LAMBDA,
       "_error": DEFAULT_LAMBDA,
       "_output_sameline": DEFAULT_LAMBDA,
       "_error_string": DEFAULT_LAMBDA,
       "_handle_flush": DEFAULT_LAMBDA,
       "_input": DEFAULT_LAMBDA
    }
    _output = []
    _errors = []
    def bind(self, evt, func):
       if evt == "output":
          self._listeners["_output"] = func
       elif evt == "error":
          self._listeners["_error"] = func
       elif evt == "output_sameline":
          self._listeners["_output_sameline"] = func
       elif evt == "error_string":
          self._listeners["_error_string"] = func
       elif evt == "flush":
          self._listeners["_handle_flush"] = func
       elif evt == "reqinput":
          self._listeners["_input"] = func
       else:
          raise ipic.errors.PicturesqueUnreconizedEventException(repr(evt))
    def output(self, text):
       self._output.append(text)
       self._listeners["_output"](text)
    def output_sameline(self, text):
       self._output.append(text)
       self._listeners["_output_sameline"](text)
    def error(self, err, lineno, line, filename, proc):
       self._errors.append(err)
       self._listeners["_error"](err, lineno, line, filename, proc)
    def strerror(self, err):
       self._errors.append(err)
       self._listeners["_error_string"](err)
    def flush(self):
       self._listeners["_handle_flush"]()
    def getoutput(self):
       return self._output
    def geterrors(self):
       return self._errors
    def reqinput(self):
       return self._listeners["_input"]()
    def __str__(self):
       return "\n".join(self._output)