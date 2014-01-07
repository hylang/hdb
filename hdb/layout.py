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
        self.divs = []

    def input(self, input, raw):
        return input


    def input_unhandled(self, input):
        """Main input handler"""
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
        self.content.append(self.div)
        self.content.append(view)


    def add_view(self, name):
        if name in self.views.keys():
            self.remove_view(name)
            return
        view = urwid.Text(name + " view")
        self.views[name] = view
        self.insert_view(view)

    def remove_view(self, name):
        view = self.views[name]

        # Wierd hack so we always get the last inserted div
        div = list(reversed(self.divs)).pop()
        self.content.remove(view)
        self.content.remove(div)

        # So we can insert the view again later on
        del self.views[name]

        self.divs.remove(div)

    def get_view(self, name):
        # API stuff later on
        return self.views[name]


