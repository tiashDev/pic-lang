import tkinter
import tkinter.messagebox
from pygments import lex
from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Generic
from pygments.lexer import bygroups
from pygments.styles import get_style_by_name
from pygments.token import *
import ipic.lang
ipic.lang.iturtle.title("Artist")
ipic.lang.iturtle.bye()
import tkinter.filedialog
import tkinter.scrolledtext
import traceback

gfont = "Courier"
gfsize = 10
filename = None

class PicturesqueLexer(RegexLexer):
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

# add markup for bold-italic
class Lexer(PicturesqueLexer):
    pass
    
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

def check_markdown(start='1.0', end='end'):
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
root.title("Artist")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
editor = tkinter.scrolledtext.ScrolledText(root, font=f"{gfont} {gfsize}")
editor.grid(row=0, column=0, sticky="NSEW")

lexer = Lexer()
syntax_highlighting_tags = load_style("lovelace")
check_markdown()

# bind each key Release to the markdown checker function
editor.bind("<KeyRelease>", lambda event: check_markdown())

menubar = tkinter.Menu(root, tearoff=False)
root.config(menu=menubar)
def run():
   turtle_gone = False
   outwin = tkinter.Tk()
   outwin.title("Artist (Output)")
   outwin.rowconfigure(0, weight=True)
   outwin.columnconfigure(0, weight=True)
   def on_close(*args):
       try:
          ipic.lang.iturtle.bye()
       except:
          pass
       outwin.destroy()
   outwin.protocol("WM_DELETE_WINDOW", on_close)
   out = tkinter.scrolledtext.ScrolledText(outwin)
   out.bind("<Key>", lambda e: "break")
   out.grid(row=0, column=0, sticky="nsew")
   def on_output(text):
      start = len(out.get('1.0', 'end-1c').split("\n"))
      out.insert("end", f"\n{text}" if not len(out.get('1.0', 'end-1c')) == 0 else text)
      out.tag_config("text", foreground="blue")
      out.tag_add("text", f"{start}.0", "end")
   def on_error(err):
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
   ipic.lang.out.bind("output", on_output)
   ipic.lang.out.bind("error", on_error)
   ipic.lang.iturtle.Turtle._screen = None  # force recreation of singleton Screen object
   ipic.lang.iturtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
   ipic.lang.lexer("".join(editor.get('1.0', 'end-1c')), is_artist=True)
def openfile():
   global filename
   try:
      filename = tkinter.filedialog.askopenfilename(filetypes = (("Picturesque Code File", "*.draw"), ("All files", "*.*")))
      x = open(filename).read()
      editor.delete("1.0", "end")
      editor.insert("end", x)
   except:
      pass
   check_markdown()
menubar_items = {
   "debug": tkinter.Menu(menubar, tearoff=False),
   "file": tkinter.Menu(menubar, tearoff=False)
}
menubar_items["debug"].add_command(label="Run", command=run)
menubar_items["file"].add_command(label="Open", command=openfile)
menubar_items["file"].add_command(label="Save")
menubar_items["file"].add_command(label="Save as..")
menubar.add_cascade(label="File", menu=menubar_items["file"])
menubar.add_cascade(label="Debug", menu=menubar_items["debug"])

root.mainloop()