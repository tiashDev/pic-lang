import sys, string, os
turtle_gone = False
helpme = """Commands:
  - forward <px>: Moves the turtle (the pen) forward by <px> pixels.
  - backward <px>: Moves it backward by <px> pixels.
  - right <deg>: Turns the pen right by <deg> degrees.
  - left <deg>: Turns it left by <deg> degrees.
  - path.begin = path.start = pen.down: Starts drawing a line.
  - path.end = pen.up: Ends a line.
  - reset: Resets the program.
  - clear: Clears the screen.
  - color <color>: Sets the color of the current line to <color>.
  - fill <color>: Fills the turtle with the color <color>.
  - fillcolor.start = fillcolor.begin: Starts filling the turtle with the color specified by fill (see [fill] above).
  - fillcolor.end: Stops filling the turtle with the color specified by fill (see [fill] above).
  - wait <secs>: Waits for <secs> seconds.
  - setx <x>: Sets the X coordinate of the turtle to <x>.
  - sety <y>: Sets the Y coordinate of the turtle to <y>.
  - stamp: Stamps a copy of the turtle onto the canvas.
  - stamps.clear: Clears all the stamps.
  - speed <s>: Sets the speed of the turtle to <s>.
  - size <s>: Sets the width of the line to <s>.
  - logln <v>: Logs a value (<v>) to the console on a new line.
  - circle <r>: Makes the turtle go around in a circle with radius <r>.
  - outline <c>: Sets the colour of the outline of the turtle to <c>.
  - hide: Hides the turtle.
  - show: Shows the turtle.
  - screen.color <c>: Sets the colour of the screen to <c>.
  - screen.image <i>: Sets the background image of the screen to <i>.
  - closeonclick: Makes it so that if you click the turtle window, it will close.
  - mode <m>: Sets the header mode to <m>.
    <m> can be -
      - "standard": The default turtle heading is to the east
      - "world": The default turtle heading is specified using user-defined world coordinates (using setworldcoordinates)
      - "logo": The default turtle heading is to the north
  - goto <x> <y>: Makes the turtle go to x <x> and y <y>.
  - exit <c=0>: Exits the program with code <c>.
  - include <f>: Executes file <f>.
  - dot <r> <c>: Draws a dot with radius <r> and colour <c>.
  - shape <s>: Sets the shape of the turtle to <s>.
    <s> can be -
      - arrow 
      - turtle 
      - circle 
      - square 
      - triangle 
      - classic
  - plot <..x> * <..y>: Plots a plot with x-axis <..x> and y-axis <..y>.
    Overloads -
      - plot <..x> * <..y> : <s>: Plots a plot with x-axis <..x> and y-axis <..y>. <s> is a Matplotlib format string for styling the plot.
  - bar <..l> * <..n>: Plots a vertical bar plot with labels <..l> and values <..n>.
    Overloads -
      - bar <..l> * <..n> : <c>: Plots a vertical bar plot with labels <..l> and values <..n>. <c> is the colour of all the bars.
  - barh <..l> * <..n>: Plots a horizontal bar plot with labels <..l> and values <..n>.
    Overloads -
      - barh <..l> * <..n> : <c>: Plots a horizontal bar plot with labels <..l> and values <..n>. <c> is the colour of all the bars.
  - pie <..l> * <..n>: Plots a pie with values <..l> and values <..n>.
    Overloads -
      - pie <..l> * <..n> : <..c>: Plots a pie with values <..l> and values <..n>. <..c> is a list of the colour of the slices.
  - hist <..v>: Plots a histogram with values <..v>.
    Overloads -
      - hist random: Plots a histogram with random values.
      - hist random <me> <md> <mo>: Plots a histogram with random values. The mean of the values is <me>, the median <md> and the mode <mo>.
Default variables:
  - $pos: Gets the position of the turtle in format "(<x>,<y>)".
  - $x: Gets the x coordinate (horizontal position) of the turtle.
  - $y: Gets the y coordinate (vertical position) of the turtle
  - $down: A boolean. True if the turtle is down, otherwise false.
    Toggleable using -
      - path.start = path.begin = pen.down
      - path.end = pen.up
  - $outline: Gets the color of the current outline of the turtle
  - $fill: Gets the color of the current filling of the turtle
  - $color: Gets the current color of the lines drawn by the turtle
  - $visible: Another boolean. True if the turtle is visible, otherwise false.
    Toggleable using -
      - hide
      - show
  - $turtle_shape_polygonal_points: The turtle's current shape polygon as a list of coordinate pairs
  - $winwidth: The width of the window, in pixels
  - $winheight: The height of the window, in pixels
  - $bgimage: The current background image of the screen
  - $mode: The turtle heading mode of the drawing
    Values -
      - "standard": The default turtle heading is to the east
      - "world": The default turtle heading is specified using user-defined world coordinates (using setworldcoordinates)
      - "logo": The default turtle heading is to the north
    Toggleable using -
      - mode
  - $shape: Gets the current shape of the turtle."""
# - var <n> = <v>: Creates a variable with name <n> and value <v>.
    # Then you can access it (the variable you created) using %<n>. 
    # Example -
       # var x = 10;
       # logln %x; ~ Logs "10" to the console;
    # NOTE - Variables are "immutable". That means you cannot change the value of the variable, once you have defined it.
def compiler(do, val, lineno, line, showerr=True):
   global turtle_gone
   if do == "FORWARD":
      return f"turtle.forward({val})"
   elif do == "BACKWARD":
      return f"turtle.backward({val})"
   elif do == "RIGHT":
      return f"turtle.right({val})"
   elif do == "LEFT":
      return f"turtle.left({val})"
   elif do == "PATH.END" or do == "PEN.UP":
      return "turtle.penup()"
   elif do == "PATH.BEGIN" or do == "PATH.START" or do == "PEN.DOWN":
      return "turtle.pendown()"
   elif do == "RESET":
      return "turtle.reset()"
   elif do == "CLEAR":
      return "turtle.clearscreen()"
   elif do == "CLOSETURTLE":
      turtle_gone = True
      return "turtle.bye()"
   else:
      file = ""
      markers = ""
      if len(sys.argv) > 1:
         file = sys.argv[1]
      else:
         file = "<console>"
      for x in range(len(do)):
         markers += "^"
      for x in line:
         if x in string.whitespace:
             markers = x + markers
         else: 
             break
      if showerr:
         print("Error: Unrecognized command at line", lineno, "in", file, "-", file=sys.stderr)
         print(" ", line[1:] if line.startswith("\n") else line, file=sys.stderr)
         print(" ", markers[1:] if markers.startswith("\n") else markers, file=sys.stderr)
      return f"""# Compiler: Error - Unrecognized command at line {lineno} in {file}:
#   {line[1:] if line.startswith("\n") else line}
#   {markers[1:] if markers.startswith("\n") else markers}"""
def lexer(program):
   global stamps
   if program.endswith(";"):
      program = program[0:-1]
   cmd_list = program.split(";")
   compiled_file = open(f"{sys.argv[1]}.py" , "wt")
   compiled_file.write(f"""# Picturesque: Copyright (c) 2024.
# Python: Copyright (c) 2001-2024. Python Software Foundation
# To run this file, run the following command:
#   picipy {sys.argv[1]}.py
import sys, turtle, time, string, matplotlib.pyplot, numpy, plotly.express
turtle.title("Picturesque")
""")
   for x in range(len(cmd_list)):
      cmd = cmd_list[x]
      line = cmd
      cmd = cmd.strip()
      cmd = cmd.upper()
      cmd_len = len(cmd.split(" "))
      if cmd_len == 0 or len(cmd) == 0 or cmd[0] == "~":
         continue
      cmd_type = cmd
      num = ""
      if cmd_len > 1:
         num = cmd[cmd.find(" ")+1:]
         cmd_type = cmd[:cmd.find(" ")]
      def defsysvar(nm, val, num):
          return num.replace(f"${nm.upper()}", val)
      num = defsysvar("POS", "turtle.position()", num)
      num = defsysvar("X", "turtle.xcor()", num)
      num = defsysvar("Y", "turtle.ycor()", num)
      num = defsysvar("DOWN", "turtle.isdown()", num)
      num = defsysvar("OUTLINE", "turtle.pencolor()", num)
      num = defsysvar("FILL", "turtle.fillcolor()", num)
      num = defsysvar("COLOR", "turtle.color()", num)
      num = defsysvar("VISIBLE", "turtle.isvisible()", num)
      num = defsysvar("TURTLE_SHAPE_POLYGONAL_POINTS", "turtle.get_shapepoly()", num)
      num = defsysvar("BGCOLOR", "turtle.getscreen().bgcolor()", num)
      num = defsysvar("BGIMAGE", "turtle.getscreen().bgpic()", num)
      num = defsysvar("WINHEIGHT", "turtle.getscreen().window_height()", num)
      num = defsysvar("WINWIDTH", "turtle.getscreen().window_width()", num)
      num = defsysvar("MODE", "turtle.mode()", num)
      num = defsysvar("shape", "turtle.shape()", num)
      # for x in range(len(varnames)):
         # num = num.replace(f"%{varnames[x]}", varvals[x])
      compiled_file.write(f"{compiler(cmd_type, num, x + 1, line)}\n")
      if compiler(cmd_type, num, x + 1, line, showerr = False).startswith("# Compiler: Error - "):
         break
   if not turtle_gone:
      compiled_file.write("turtle.mainloop()")
if len(sys.argv) > 1:
   lexer(open(sys.argv[1], "r").read())