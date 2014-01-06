import urwid


class WidgetHandler():
    palette = [('header', 'white', 'black'),
               ('reveal focus', 'dark cyan', 'black'),
               ('edit', 'dark cyan', 'default')]

    def __init__(self, file):
        self.items = []

        self.code_view = urwid.Edit(edit_text=file, multiline=True)

        # Apply the right scheme for the edit region and append as its
        # the default view for hdb
        self.items.append(urwid.AttrMap(self.code_view, None, 'edit'))


        self.content = urwid.SimpleListWalker(self.items)

        self.listbox = urwid.ListBox(self.content)

        self.frame = urwid.Frame(self.listbox)

    def input_filter(self, input, raw):
        return input


    def input_unhandled(self, input):
        pass


    def start(self):
        loop = urwid.MainLoop(self.frame, self.palette,
                              input_filter=self.input_filter,
                              unhandled_input=self.input_unhandled)
        loop.run()

    def insert_view(self, view):
        self.div = urwid.Divider(div_char="-")

        self.items.append(div)
        self.items.append(urwid.AttrMap(view, None, 'reveal focus'))



