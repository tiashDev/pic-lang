import tkinter
import tkinter.messagebox
import tkinter.simpledialog
from pygments import lex
from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Generic
from pygments.lexer import bygroups
from pygments.styles import get_style_by_name
from pygments.token import *
import ipic.lang
ipic.lang.turtle.title("Artist")
ipic.lang.turtle.bye()
import tkinter.filedialog
import tkinter.scrolledtext
import traceback

CTRL = {
   "display": "Ctrl",
   "tkinter": "Control"
}

SEPS = {
   "display": "+",
   "tkinter": "-"
}

gfont = "Courier"
gfsize = 10
filename = None
unsaved = False
title = "Artist - untitled"

def update_title():
   title = f"Artist - {'*' if unsaved else ''}{filename if filename else 'untitled'}"
   root.title(title)

class Lexer(RegexLexer):
    name = 'Picturesque'
    aliases = ['pic']
    filenames = ['*.draw']

    tokens = {
        'root': [
            (r'~.*', Comment.Multiline, 'blockcomment'),
            (r'(forward|backward|right|left|end|begin|start|reset|print|color|home|title|fill|wait|setx|sety|stamp|hide|show|logln|image|clear|closeonclick|mode|setworldcoordinates|goto|help|include|dot|plot|closeturtle|bar|barh|pie|hist|path.start|path.end|pen.up|pen.down|fillcolor.start|fillcolor.end|fillcolor.begin|stamps.clear|input|forever|eval)',Name.Builtin), # M or G commands
            (r'[^gGmM][+-]?\d*[.]?\d+', Keyword),
            (r'\s', Text.Whitespace),
            (r'.*\n', Text),
        ],
        'blockcomment': [
            (r'.*;.*$', Comment.Multiline, '#pop'),
            (r'^.*\n', Comment.Multiline),
            (r'.', Comment.Multiline),
        ]
    }

def load_style(stylename):
    style = get_style_by_name(stylename)
    syntax_highlighting_tags = []
    for token, opts in style.list_styles():
        kwargs = {}
        fg = opts['color']
        bg = opts['bgcolor']
        if fg:
            kwargs['foreground'] = '#' + fg
        if bg:
            kwargs['background'] = '#' + bg
        font = (gfont, gfsize) + tuple(key for key in ('bold', 'italic') if opts[key])
        kwargs['font'] = font
        kwargs['underline'] = opts['underline']
        editor.tag_configure(str(token), **kwargs)
        syntax_highlighting_tags.append(str(token))
    try:
       editor.configure(bg=style.background_color,
                     fg=editor.tag_cget("Token.Text", "foreground"),
                     selectbackground=style.highlight_color)
    except:
       pass
    editor.tag_configure(str(Generic.StrongEmph), font=(gfont, gfsize, 'bold', 'italic'))
    syntax_highlighting_tags.append(str(Generic.StrongEmph))
    return syntax_highlighting_tags    

def check_markdown(start='1.0', end='end', saved=False):
    global unsaved
    if not saved:
       unsaved = True
    update_title()
    data = editor.get(start, end)
    while data and data[0] == '\n':
        start = editor.index('%s+1c' % start)
        data = data[1:]
    editor.mark_set('range_start', start)
    # clear tags
    for t in syntax_highlighting_tags:
        editor.tag_remove(t, start, "range_start +%ic" % len(data))
    # parse text
    for token, content in lex(data, lexer):
        editor.mark_set("range_end", "range_start + %ic" % len(content))
        for t in token.split():
            editor.tag_add(str(t), "range_start", "range_end")
        editor.mark_set("range_start", "range_end")
    

root = tkinter.Tk()
root.title(title)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
editor = tkinter.scrolledtext.ScrolledText(root, font=f"{gfont} {gfsize}")
editor.grid(row=0, column=0, sticky="NSEW")

lexer = Lexer()
syntax_highlighting_tags = load_style("lovelace")
check_markdown(saved=True)

# bind each key Release to the markdown checker function
editor.bind("<KeyRelease>", lambda event: check_markdown())

menubar = tkinter.Menu(root, tearoff=False)
root.config(menu=menubar)
def run():
   turtle_gone = False
   outwin = tkinter.Toplevel()
   outwin.title("Artist (Output)")
   outwin.rowconfigure(0, weight=True)
   outwin.columnconfigure(0, weight=True)
   outwin.columnconfigure(1, weight=True)
   def on_close(*args):
       try:
          ipic.lang.turtle.bye()
       except:
          pass
       outwin.destroy()
   outwin.protocol("WM_DELETE_WINDOW", on_close)
   out = tkinter.scrolledtext.ScrolledText(outwin)
   out.bind("<Key>", lambda e: "break")
   out.grid(row=0, column=0, sticky="nsew")
   cnv = tkinter.Canvas(outwin)
   cnv.grid(row=0, column=1, sticky="nsew")
   scr = ipic.lang.turtle.TurtleScreen(cnv)
   ipic.lang.turtle.Turtle._screen = None  # force recreation of singleton Screen object
   ipic.lang.turtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
   ipic.lang.iturtle = ipic.lang.turtle.RawTurtle(scr)
   ipic.lang.turtle.bye()
   def on_output(text):
      start = len(out.get('1.0', 'end-1c').split("\n"))
      out.insert("end", f"\n{text}" if not len(out.get('1.0', 'end-1c')) == 0 else text)
      out.tag_config("text", foreground="blue")
      out.tag_add("text", f"{start}.0", "end")
   def on_error(err, *a):
      ipic.lang.iturtle.bye()
      start = len(out.get('1.0', 'end-1c').split("\n"))+1 if not len(out.get('1.0', 'end-1c')) == 0 else len(out.get('1.0', 'end-1c').split("\n"))
      if not err.__class__.__name__.startswith("Picturesque"):
         out.insert("end", "\nError in internal Python distribution" if not len(out.get('1.0', 'end-1c')) == 0 else "Error in internal Python distribution")
         fexc = ""
         for x in traceback.format_exception(err):
            fexc += x
         out.insert("end", f"\n{fexc}" if not len(out.get('1.0', 'end-1c')) == 0 else fexc)
      else:
         out.insert("end", f"\n{str(err)}" if not len(out.get('1.0', 'end-1c')) == 0 else str(err))
      out.tag_config("err", foreground="red")
      out.tag_add("err", f"{start}.0", "end")
   def on_input():
      return tkinter.simpledialog.askstring("Artist", "This program wants to ask you a question!")
   ipic.lang.out.bind("output", on_output)
   ipic.lang.out.bind("error", on_error)
   ipic.lang.out.bind("reqinput", on_input)

   ipic.lang.lexer("".join(editor.get('1.0', 'end-1c')))
   
def openfile():
   global filename, unsaved
   try:
      filename = tkinter.filedialog.askopenfilename(filetypes = (("Picturesque Code File", "*.draw"), ("All files", "*.*")))
      x = open(filename).read()
      editor.delete("1.0", "end")
      editor.insert("end", x)
   except:
      pass
   unsaved = False
   check_markdown(saved=True)

def savefile(save_as=False):
   global unsaved, filename
   if not filename or save_as:
       filename = tkinter.filedialog.asksaveasfilename(filetypes = (("Picturesque Code File", "*.draw"), ("All files", "*.*")))
   if filename:
      file = open(filename, "w")
      file.write(editor.get('1.0', 'end-1c'))
      unsaved = False
      update_title()

def add_cmd(menu, lbl, cmd, kbd):
    def transform_kbd(type_):
        nonlocal kbd
        global SEPS
        transformed = []
        for x in kbd:
            if isinstance(x, dict):
                transformed.append(x[type_])
            else:
                transformed.append(x)
        return SEPS[type_].join(transformed)
    menu.add_command(label=lbl, command=cmd, accelerator=transform_kbd("display"))
    root.bind_all(f"<{transform_kbd('tkinter')}>", lambda *_: cmd)

menubar_items = {
   "debug": tkinter.Menu(menubar, tearoff=False),
   "file": tkinter.Menu(menubar, tearoff=False)
}

add_cmd(menubar_items["debug"], "Run", run, ["F5"])
add_cmd(menubar_items["file"], "Open", openfile, [CTRL, "O"])
add_cmd(menubar_items["file"], "Save", savefile, [CTRL, "S"])
add_cmd(menubar_items["file"], "Save as..", lambda: savefile(True), [CTRL, "Alt", "S"])
menubar.add_cascade(label="File", menu=menubar_items["file"])
menubar.add_cascade(label="Debug", menu=menubar_items["debug"])

root.mainloop()