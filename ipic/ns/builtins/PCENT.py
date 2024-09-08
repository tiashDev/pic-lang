"""A way of calculating percentages via the Unitary Method."""
import ipic.ns
from ipic.errors import PicturesqueException
__author__ = "Ridwan bin Mohammad (Tiash)"

class main(ipic.ns.ShlexNamespace):
   """The namespace class."""
   def _of(self, apcent, anum):
      pcent = int(apcent); num = int(anum)
      if pcent > 100:
         raise PicturesqueException(f"Percentage cannot exceed 100%")
      return (num / 100) * pcent
   def do_of(self, pcent, num):
      self.out.output(self._of(pcent, num))
   def do_rof(self, pcent, num, var):
      self.var_dict[var] = self._of(pcent, num)