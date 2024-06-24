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
try:
   if confirm("Do you want to build picturesque.exe?"):
      print("--------------------- Building picturesque.exe ---------------------")
      os.system("env\\Scripts\\pyinstaller -F picturesque.py -p env\\Lib\\site-packages -p ipic -i ..\\logo\\picturesque.ico --hidden-import turtle --specpath ./specs/ --distpath path")
      print("-------------------------- End of output ---------------------------")
      has_build = True
   if confirm("Do you want to build pic.exe?"):
      print("----------------------- Building pic.exe ---------------------------")
      os.system("env\\Scripts\\pyinstaller -F picturesque.py -p env\\Lib\\site-packages -p ipic -n pic -i ..\\logo\\picturesque.ico --hidden-import turtle --specpath ./specs/ --distpath path")
      print("-------------------------- End of output ---------------------------")
      has_build = True
   if confirm("Do you want to build artist.exe?"):
      print("--------------------- Building artist.exe ---------------------")
      os.system("env\\Scripts\\pyinstaller -F artist.py -p env\\Lib\\site-packages -p ipic -i ..\\logo\\artist.ico --windowed --hidden-import turtle --specpath ./specs/ --distpath path")
      print("-------------------------- End of output ---------------------------")
      has_build = True
   if confirm("Do you want to build paintshop.exe?"):
      print("--------------------- Building paintshop.exe -----------------------")
      os.system("env\\Scripts\\pyinstaller -F paintshop_windows.py -p env\\Lib\\site-packages -n paintshop --specpath ./specs/ --distpath path")
      print("-------------------------- End of output ---------------------------")
      has_build = True
   if confirm("Do you want to build pspm.exe?"):
      print("------------------------ Building pspm.exe -------------------------")
      os.system("env\\Scripts\\pyinstaller -F paintshop_windows.py -p env\\Lib\\site-packages -n pspm --specpath ./specs/ --distpath path")
      print("-------------------------- End of output ---------------------------")
      has_build = True
   if has_build and confirm("Do you want to delete the \"build\" folder?"):
      shutil.rmtree("build")
   os.system("pause")
except KeyboardInterrupt:
   pass