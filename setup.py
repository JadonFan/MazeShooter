import sys, os
from cx_Freeze import setup, Executable

## os.environ["TCL_LIBRARY"] = ...

base = None
if sys.platform == "win32":
    base = "Win32GUI"

extra_packages = ["pygame", "numpy"]
extra_modules = ["numpy.core._methods", "numpy.lib.format"]
extra_files = ["arrowup.png", "arrowright.png", "arrowleft.png", "arrowdown.png", "person.png", "audiosign.jpg", "mazegamemusic.wav", "uwlogo.png"]

setup(name = "mazeshooter" ,
	  author = "Jadon Fan",
      version = "1.0" ,
      description = "Maze Shooting Game" ,
      options = {"build_exe": {"includes": extra_modules, "include_files": extra_files}},
      executables = [Executable("mazeshooter.py")])