import turtle as iturtle, time, string, matplotlib.pyplot, numpy, plotly.express, sys, ipic.errors, ipic.out, tkinter, json, tkinter.ttk, tkinter.messagebox, tkinter.colorchooser, tkinter.scrolledtext, shlex, tkinter.filedialog
stamps = list()
out = ipic.out.PicturesqueOutputHandler()
turtle_gone = False
iturtle.title("Picturesque")
def initturtle(turtle_screen):
   global iturtle
   iturtle = iturtle.RawTurtle(turtle_screen)
tkinter_win_ids = {}
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
  - pie <..l> * <..n>: Plots a pie with labelss <..l> and values <..n>.
    Overloads -
      - pie <..l> * <..n> : <..c>: Plots a pie with labels <..l> and values <..n>. <..c> is a list of the colour of the slices.
  - hist <..v>: Plots a histogram with values <..v>.
    Overloads -
      - hist random: Plots a histogram with random values.
      - hist random <me> <md> <mo>: Plots a histogram with random values. The mean of the values is <me>, the median <md> and the mode <mo>.
  - eval <..c>: Executes the code <..c>.
  - forever <..c>: Executes the code <..c> forever.
  - wininit <n>: Initializes a window with the name <n>.
  - wintitle <n> <..t>: Gives the window with name <n> the title <..t>.
  - input <..t> | <..b>: Asks the user for input in the GUI. The window which appears has the title <..t> and body <..b>
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
def interpret(do, val, lineno, line, is_console, filename, is_artist):
   global stamps
   global turtle_gone
   global tkinter_win_ids
   if do == "FORWARD":
      iturtle.forward(int(val))
   elif do == "BACKWARD":
      iturtle.backward(int(val))
   elif do == "RIGHT":
      iturtle.right(int(val))
   elif do == "LEFT":
      iturtle.left(int(val))
   elif do == "PATH.END" or do == "PEN.UP":
      iturtle.penup()
   elif do == "PATH.BEGIN" or do == "PATH.START" or do == "PEN.DOWN":
      iturtle.pendown()
   elif do == "RESET":
      iturtle.reset()
   elif do == "CLEAR":
      iturtle.clearscreen()
   elif do == "COLOR":
      iturtle.color(val)
   elif do == "FILL":
      iturtle.fillcolor(val)
   elif do == "HOME":
      iturtle.home()
   elif do == "FILLCOLOR.START" or do == "FILLCOLOR.BEGIN":
      iturtle.begin_fill()
   elif do == "FILLCOLOR.END":
      iturtle.end_fill()
   elif do == "WAIT":
      time.sleep(float(val))
   elif do == "SETX":
      iturtle.setx(int(val))
   elif do == "SETY":
      iturtle.sety(int(val))
   elif do == "STAMP":
      stamps.append(iturtle.stamp())
   elif do == "STAMPS.CLEAR":
      iturtle.clearstamps()
   elif do == "SPEED":
      iturtle.speed(int(val))
   elif do == "SIZE":
      iturtle.pensize(int(val))
   elif do == "LOGLN":
      out.output(val)
   elif do == "CIRCLE":
      iturtle.circle(int(val))
   elif do == "OUTLINE":
      iturtle.pencolor(val)
   elif do == "HIDE":
      iturtle.hideturtle()
   elif do == "SHOW":
      iturtle.showturtle()
   elif do == "SCREEN.COLOR":
      iturtle.getscreen().bgcolor(val)
   elif do == "SCREEN.IMAGE":
      iturtle.getscreen().bgpic(val)
   elif do == "CLOSEONCLICK":
      iturtle.getscreen().exitonclick()
      turtle_gone = True
   elif do == "MODE":
      iturtle.mode(val)
   elif do == "SETWORLDCOORDINATES":
      iturtle.getscreen().setworldcoordinates(tuple(map(int, val.split(' '))))
   elif do == "CLOSETURTLE":
      iturtle.bye()
      turtle_gone = True
   elif do == "DOT":
      args = val.split(' ')
      iturtle.dot(args[0], args[1])
   elif do == "GOTO":
      iturtle.setpos(tuple(map(int, val.split(' '))))
   elif do == "SHAPE":
      iturtle.shape(val.lower())
   elif do == "HELP":
      out.output(helpme)
   elif do == "EXIT":
      if val != "":
         sys.exit(int(val))
      else:
         sys.exit(0)
   elif do == "INCLUDE":
      lexer(open(val, "r").read())
   # elif do == "VAR":
      # args = val.split(" ")
      # if args[1] == "=":
         # varnames.append(args[0])
         # varvals.append(args[2])
      # else:
         # file = ""
         # if len(sys.argv) > 1:
            # file = sys.argv[1]
         # else:
            # file = "<console>"
         # print("Error: Invalid syntax at line", str(lineno), "in", file, file=sys.stderr)
   elif do == "PLOT":
      matplotlib.pyplot.figure(num = "Picturesque")
      xpoints = numpy.array([int(x) for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") > -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.plot(xpoints, ypoints, val[val.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.plot(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "BAR":
      matplotlib.pyplot.figure(num = "Picturesque")
      xpoints = numpy.array([x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") > -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.bar(xpoints, ypoints, color = val[val.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.bar(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "BARH":
      matplotlib.pyplot.figure(num = "Picturesque")
      xpoints = numpy.array([x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))])
      if val.find(" : ") > -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.barh(xpoints, ypoints, color = val[val.find(" : ")+len(" : "):].lower())
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.barh(xpoints, ypoints)
      matplotlib.pyplot.show()
   elif do == "PIE":
      matplotlib.pyplot.figure(num = "Picturesque")
      mylabels = [x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))]
      if (val.find(" : ") > -1):
         y = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" : ")].split(" "))])
         matplotlib.pyplot.pie(y, labels = mylabels, colors = list(val[val.find(" : ")+len(" : "):].lower().split(" ")))
      else:
         y = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         matplotlib.pyplot.pie(y, labels = mylabels)
      matplotlib.pyplot.legend(title = "Legend")
      matplotlib.pyplot.show()
   elif do == "HIST":
      matplotlib.pyplot.figure(num = "Picturesque")
      if not val.startswith("RANDOM"):
         x = numpy.array([float(i) for i in list(val.split(" "))]);
         matplotlib.pyplot.hist(x)
      else:
         args = val.split(" ")[1:]
         if len(args) > 1:
            x = numpy.random.normal(int(args[0]), int(args[1]), int(args[2]))
            matplotlib.pyplot.hist(x)
         else:
            x = numpy.random.normal(170, 10, 250)
            matplotlib.pyplot.hist(x)
      matplotlib.pyplot.show()
   elif do == "BBAR":
      xpoints = [x.replace("\\S", " ").replace("\\(S)", "\\S") for x in list(val[:val.find(" * ")].split(" "))]
      if val.find(" | ") > -1:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):val.find(" | ")].split(" "))])
         plotly.express.bar(x=xpoints, y=ypoints).write_html(val[val.find(" | ")+len(" | "):])
      else:
         ypoints = numpy.array([int(x) for x in list(val[val.find(" * ")+len(" * "):].split(" "))])
         plotly.express.bar(x=xpoints, y=ypoints).show()
   elif do == "EVAL":
      lexer(val)
   elif do == "FOREVER":
      while True:
         try:
            lexer(val.replace(",", ";").replace("'", ","))
         except KeyboardInterrupt:
            break
   elif do == "WININIT":
      tkinter_win_ids[val] = tkinter.Tk()
      tkinter_win_ids[val].title("Picturesque")
   elif do == "WINTITLE":
      args = shlex.split(val)
      try:
         tkinter_win_ids[args[0]].title(args[1])
      except KeyError:
         raise ipic.errors.PicturesqueWindowNotFoundException(f"The window {shlex.quote(args[0])} does not exist. (line {lineno}, file {filename if filename != None else '<console>'})")
   elif do == "LOOPWIN":
      try:
         tkinter_win_ids[val].mainloop()
      except KeyboardInterrupt:
         pass
   elif do == "CLOSEWIN":
      tkinter_win_ids[val].destroy()
   elif do == "BTN":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Button(tkinter_win_ids[args["PARENT"]], text=args["TEXT"], command=lambda *a: lexer(args["ONCLICK"].replace(",", ";").replace("'", ",")))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SBTN":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Button(tkinter_win_ids[args["PARENT"]], text=args["TEXT"], command=lambda *a: lexer(args["ONCLICK"].replace(",", ";").replace("'", ",")))
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "LBL":
      args = json.loads(val)
      tkinter.Label(tkinter_win_ids[args["PARENT"]], text=args["TEXT"]).pack()
   elif do == "TXT":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Text(tkinter_win_ids[args["PARENT"]], width=args["WIDTH"], height=args["HEIGHT"])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "ENTRY":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.Entry(tkinter_win_ids[args["PARENT"]])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SENTRY":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Entry(tkinter_win_ids[args["PARENT"]])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "SCROLLTXT":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.scrolledtext.ScrolledText(tkinter_win_ids[args["PARENT"]], width=args["WIDTH"], height=args["HEIGHT"])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "MODIFY":
      args = json.loads(val)
      if args["CMD"] == "INSERT":
         if tkinter_win_ids[args["NAME"]].__class__.__name__ == "ScrolledText" or tkinter_win_ids[args["NAME"]].__class__.__name__ == "Text" or tkinter_win_ids[args["NAME"]].__class__.__name__ == "Entry":
            tkinter_win_ids[args["NAME"]].insert(args["ARGS"][0].lower(), args["ARGS"][1])
         else:
            raise PicturesqueInvalidWidgetException(f"Invalid widget for command {shlex.quote(args['CMD'])}. (line {lineno}, file {filename if filename != None else '<console>'})")
      elif args["CMD"] == "INVOKE":
         if tkinter_win_ids[args["NAME"]].__class__.__name__ == "Button":
            tkinter_win_ids[args["NAME"]].invoke()
         else:
            raise PicturesqueInvalidWidgetException(f"Invalid widget for command {shlex.quote(args['CMD'])}. (line {lineno}, file {filename if filename != None else '<console>'})")
      else:
         raise ipic.errors.PicturesqueUnreconizedCommandException(f"""Error: Unrecognized command {shlex.quote(args['CMD'])} at line {lineno} in {filename if filename != None else "<console>"}.""")
   elif do == "FRM":
      args = json.loads(val)
      tkinter_win_ids[args["NAME"]] = tkinter.ttk.Frame(tkinter_win_ids[args["PARENT"]])
      tkinter_win_ids[args["NAME"]].pack()
   elif do == "INFO":
      tkinter.messagebox.showinfo(val[:val.find(" | ")], val[val.find(" | ")+3:])
   elif do == "ASKCOLOR":
      color = tkinter.colorchooser.askcolor()
      out.output(str(color) if color != (None, None) else "(input canceled by user)")
   elif do == "INPUT":
      if turtle_gone:
         iturtle.Turtle._screen = None  # force recreation of singleton Screen object
         iturtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
      inputtxt = iturtle.getscreen().textinput(val[:val.find(" | ")], val[val.find(" | ")+3:])
      if turtle_gone:
         iturtle.bye()
      out.output(inputtxt if inputtxt is not None else "(input canceled by user)")
   elif do == "NUMINPUT":
      if turtle_gone:
         iturtle.Turtle._screen = None  # force recreation of singleton Screen object
         iturtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
      inputtxt = iturtle.getscreen().numinput(val[:val.find(" | ")], val[val.find(" | ")+3:])
      if turtle_gone:
         iturtle.bye()
      out.output(inputtxt if inputtxt is not None else "(input canceled by user)")
   elif do == "WRITE":
      iturtle.write(val)
   elif do == "ASKOPENFILE":
      out.output(tkinter.filedialog.askopenfilename())
   elif do == "ASKOPENFILES":
      out.output("\n".join(tkinter.filedialog.askopenfilenames()))
   elif do == "ASKDIR":
      out.output(tkinter.filedialog.askdirectory())
   elif do == "TCLINIT":
      tkinter_win_ids[val] = tkinter.Tcl()
   elif do == "TKINIT":
      if tkinter_win_ids[val].__class__.__name__ == "Tcl":
         tkinter_win_ids[val].loadtk()
      else:
         f"Invalid widget for command {shlex.quote(args['CMD'])}. (line {lineno}, file {filename if filename != None else '<console>'})"
   else:
      file = ""
      if filename != None:
         file = filename
      else:
         file = "<console>"
      markers = ""
      for x in range(len(do)):
         markers += "^"
      for x in line:
         if x in string.whitespace:
             markers = x + markers
         else: 
             break
      raise ipic.errors.PicturesqueUnreconizedCommandException(f"""Error: Unrecognized command at line {lineno} in {file}.
  {line[1:-1] if line.startswith("\n") else line}
  {markers[1:-1] if markers.startswith("\n") else markers}""")
def lexer(program, is_console=False, filename=None, is_artist=False):
   global stamps
   if program.endswith(";"):
      program = program[0:-1]
   cmd_list = program.split(";")
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
          return num.replace(f"${nm.upper()}", str(val))
      if not turtle_gone:
          num = defsysvar("POS", iturtle.position(), num)
          num = defsysvar("X", iturtle.xcor(), num)
          num = defsysvar("Y", iturtle.ycor(), num)
          num = defsysvar("DOWN", iturtle.isdown(), num)
          num = defsysvar("OUTLINE", iturtle.pencolor(), num)
          num = defsysvar("FILL", iturtle.fillcolor(), num)
          num = defsysvar("COLOR", iturtle.color(), num)
          num = defsysvar("VISIBLE", iturtle.isvisible(), num)
          num = defsysvar("TURTLE_SHAPE_POLYGONAL_POINTS", iturtle.get_shapepoly(), num)
          num = defsysvar("BGCOLOR", iturtle.getscreen().bgcolor(), num)
          num = defsysvar("BGIMAGE", iturtle.getscreen().bgpic(), num)
          num = defsysvar("WINHEIGHT", iturtle.getscreen().window_height(), num)
          num = defsysvar("WINWIDTH", iturtle.getscreen().window_width(), num)
          num = defsysvar("STAMPS", stamps, num)
          num = defsysvar("MODE", iturtle.mode(), num)
          num = defsysvar("shape", iturtle.shape(), num)
      num = num.replace("($)", "$")
      # for x in range(len(varnames)):
         # num = num.replace(f"%{varnames[x]}", varvals[x])=
      try:
         interpret(cmd_type, num, x + 1, line, is_console, filename, is_artist)
      except Exception as err:
         out.error(err)