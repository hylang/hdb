import urwid
from hdb.lazyedit import LineWalker
from hdb.codegen import codegen
# hack so we can use ctrl s, ctrl q and ctrl c
ui = urwid.raw_display.RealTerminal()
ui.tty_signal_keys('undefined', 'undefined', 'undefined', 'undefined',
'undefined')



class WidgetHandler():
    palette = [('header', 'white', 'black'),
               ('reveal focus', 'dark cyan', 'black'),
               ('edit', 'dark cyan', 'default')]

    def __init__(self, file):
        self.items = []
        self.views = {}

        self.linewalker = LineWalker(file)

        self.code_view = urwid.ListBox(self.linewalker)
        self.init_view = [("weight",500, self.code_view),]

        # Apply the right scheme for the edit region and append as its
        # the default view for hdb
        #self.items.append(urwid.AttrMap(self.content, None, 'edit'))

        self.content_list = urwid.SimpleListWalker(self.init_view)

        self.pile = urwid.Pile(self.content_list)

        # Because i am an untidy motherfucker
        self.content = self.pile.contents

        # Debug purposes
        self.tmp = ""
        self.show_value = urwid.Text("bam", wrap="clip")
        head = urwid.AttrMap(self.show_value, 'header')

        self.frame = urwid.Frame(self.pile)

        self.divs = []

        self.code = None
        self.ast = None


    def set_value(self):
        self.show_value.set_text(self.tmp)

    def test_ast(self):
        self.tmp = self.linewalker.get_code()
        self.ast, self.code = codegen(self.tmp)
        if "code" in self.views.keys():
            view = self.views["code"]
            view.set_text(self.code)
        if "ast" in self.views.keys():
            view = self.views["ast"]
            view.set_text(self.ast)


    def input(self, input, raw):
        return input


    def input_unhandled(self, input):
        """Main input handler"""
        if isinstance(input, tuple):
            return
        if input == "ctrl w":
            self.test_ast()
            self.set_value()
        if input == "ctrl a":
            self.add_view("ast")
        if input == "ctrl v":
            self.add_view("code")
        if input in ("ctrl c"):
            raise urwid.ExitMainLoop()


    def start(self):
        loop = urwid.MainLoop(self.frame, self.palette,
                              input_filter=self.input,
                              unhandled_input=self.input_unhandled,
                              pop_ups=True)
        loop.run()


    def insert_view(self, view):
        self.div = urwid.Divider(div_char="-")
        self.divs.append(self.div)
        self.content.append((self.div, ("pack", None)))
        self.content.append((view, ("pack", None)))


    def add_view(self, name):
        if name in self.views.keys():
            self.remove_view(name)
            return
        if self.ast == None and self.code == None:
            ret = "Nuthing"
        if name == "ast" and self.ast != None:
            ret = self.ast
        if name == "code" and self.code != None:
            ret = self.code
        view = urwid.Text(ret)
        self.views[name] = view
        self.insert_view(view)

    def remove_view(self, name):
        view = self.views[name]

        # Wierd hack so we always get the last inserted div
        div = self.divs.pop()
        self.content.remove((view, ("pack", None)))
        self.content.remove((div, ("pack", None)))

        # So we can insert the view again later on
        del self.views[name]

        #self.divs.remove(div)

    def get_view(self, name):
        # API stuff later on
        return self.views[name]


