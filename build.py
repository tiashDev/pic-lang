import os, shutil
def confirm(prompt):
   def do_confirm(prompt):
      confirm_val = input(f"{prompt} (y/n) ")
      if confirm_val == "y":
         return True
      elif confirm_val == "n":
         return False
      else:
         return do_confirm(prompt)
   return do_confirm(prompt)
has_build = False
hidden_import = ""
for x in os.listdir("./ipic/ns/builtins/"):
   y = x.removesuffix(".py")
   if not x.startswith("_"):
      hidden_import += f" --hidden-import ipic.ns.builtins.{y}"
try:
   if confirm("Do you want to build Picturesque?"):
      print("--------------------- Building Picturesque ---------------------")
      os.system(f"env\\Scripts\\pyinstaller -F picturesque.py -p ipic{hidden_import} -i ..\\logo\\picturesque.ico --specpath ./specs/")
      print("------------------------ End of output -------------------------")
      print("Creating hard links ... ", end="")
      os.link("./dist/picturesque.exe", "./path/picturesque.exe")
      os.link("./dist/picturesque.exe", "./path/pic.exe")
      print("done")
      has_build = True
   if confirm("Do you want to build Paintshop?"):
      print("--------------------- Building Paintshop -----------------------")
      os.system("env\\Scripts\\pyinstaller -F paintshop_windows.py -n paintshop --specpath ./specs/")
      print("------------------------ End of output -------------------------")
      print("Creating hard links ... ", end="")
      os.link("./dist/paintshop.exe", "./path/paintshop.exe")
      os.link("./dist/paintshop.exe", "./path/pspm.exe")
      print("done")
      has_build = True
   if confirm("Do you want to build PicPack?"):
      print("----------------------- Building picpack.exe -----------------------")
      os.system(f"env\\Scripts\\pyinstaller -F picpack.py -p ipic -p picpack_internals{hidden_import} -n picpack --specpath ./specs/")
      print("-------------------------- End of output ---------------------------")
      print("Creating hard links ... ", end="")
      os.link("./dist/picpack.exe", "./path/picpack.exe")
      print("done")
      has_build = True
   if has_build and confirm("Do you want to delete the \"build\" folder?"):
      shutil.rmtree("build")
   os.system("pause")
except KeyboardInterrupt:
   pass