import urwid
import astor
from hy.lex import tokenize
from hy.lex.exceptions import PrematureEndOfInput
from hy.compiler import hy_compile


palette = [('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout')]

ast_text = urwid.Text("press ctrl f")

python_text = urwid.Text("waaiiittttt for it")

edit_object = urwid.Edit(edit_text='(print "hello world!")', multiline=True)

items = [edit_object,
         urwid.Divider(div_char="-"),
         ast_text,
         urwid.Divider(div_char="-"),
         python_text]

content = urwid.SimpleListWalker([
    urwid.AttrMap(w, None, 'reveal focus') for w in items])

listbox = urwid.ListBox(content)

show_key = urwid.Text("Press any key", wrap='clip')
head = urwid.AttrMap(show_key, 'header')
top = urwid.Frame(listbox, head)

def getAST():
    code = edit_object.edit_text
    try:
        a = tokenize(code)
        b = hy_compile(a, "hdb")
        ret = astor.dump(b)
    except PrematureEndOfInput:
        ret = "missing a paren"
    return ret

def getPython():
    code = edit_object.edit_text
    try:
        a = tokenize(code)
        b = hy_compile(a, "hdb")
        ret =  astor.codegen.to_source(b)
    except PrematureEndOfInput:
        ret = "missing a paren"
    return ret

def show_all_input(input, raw):
    show_key.set_text("Pressed: " + str(input))
    return input


def exit_on_cr(input):
    if input in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    if input == "ctrl f":
        ret_text = getAST()
        ast_text.set_text(ret_text)
        py_text = getPython()
        python_text.set_text(py_text)
    #elif input == 'up':
    #    focus_widget, idx = listbox.get_focus()
    #    if idx > 0:
    #        idx = idx-1
    #        listbox.set_focus(idx)
    #elif input == 'down':
    #    focus_widget, idx = listbox.get_focus()
    #    idx = idx+1
    #    listbox.set_focus(idx)

def out(s):
    show_key.set_text(str(s))


loop = urwid.MainLoop(top, palette,
    input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.run()
