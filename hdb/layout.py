import urwid


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

        self.code_view = urwid.Edit(edit_text=file, multiline=True)

        # Apply the right scheme for the edit region and append as its
        # the default view for hdb
        self.items.append(urwid.AttrMap(self.code_view, None, 'edit'))


        self.content = urwid.SimpleListWalker(self.items)

        self.listbox = urwid.ListBox(self.content)

        self.frame = urwid.Frame(self.listbox)


    def input(self, input, raw):
        return input


    def input_unhandled(self, input):
        if input == "ctrl v":
            self.add_ast_view()
        if input in ("ctrl v", "ctrl c"):
            raise urwid.ExitMainLoop()


    def start(self):
        loop = urwid.MainLoop(self.frame, self.palette,
                              input_filter=self.input,
                              unhandled_input=self.input_unhandled,
                              pop_ups=True)
        loop.run()


    def insert_view(self, view):
        self.div = urwid.Divider(div_char="-")

        self.content.append(self.div)
        self.content.append(urwid.AttrMap(view, None, 'reveal focus'))


    def add_ast_view(self, name=None):
        if "ast" in self.views.keys():
            return
        view = urwid.Text("ast view")
        self.insert_view(view)
        self.views["ast"] = view


    def add_code_view(self, name=None):
        view = urwid.Text("code view")
        self.views["code"] = view


    def get_view(self, name):
        return self.views[name]


