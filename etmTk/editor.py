from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename
import tkFont
# if platform.python_version() >= '3':
#     import tkinter
#     from tkinter import Tk, Entry, INSERT, END, Label, Toplevel, Button, Frame, LEFT, Text, PanedWindow, OptionMenu, StringVar
#     from tkinter import messagebox as tkMessageBox
#     from tkinter import ttk
#     from tkinter import font as tkFont
#     from tkinter import simpledialog as tkSimpleDialog
#     # import tkFont
# else:
#     import Tkinter as tkinter
#     from Tkinter import Tk, Entry, INSERT, END, Label, Toplevel, Button, Frame, LEFT, Text, PanedWindow, OptionMenu, StringVar
#     import tkMessageBox
#     import ttk
#     import tkFont
#     import tkSimpleDialog


from tkMessageBox import askokcancel

class ScrolledText(Frame):

    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.text_value = StringVar(self)
        self.settext(text, file)

    def makewidgets(self):
        # sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, font=tkFont.Font(family="Lucida Sans Typewriter"), undo=True)

        # sbar.config(command=text.yview)
        # text.config(yscrollcommand=sbar.set)
        # sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END+'-1c')


class SimpleEditor(ScrolledText):

    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        btnwdth = 5
        Button(frm, text='Save', width=btnwdth, command=self.onSave).pack(side=LEFT)
        Button(frm, text='Repeat', width=btnwdth, command=self.onCut).pack(side=LEFT)
        Button(frm, text='Review', width=btnwdth, command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find', width=btnwdth, command=self.onFind).pack(side=LEFT)
        self.find_text = StringVar(frm)
        # self.find_text.set('Find?')
        # self.find_text.trace('w', self.onFind)
        e = Entry(frm, textvariable=self.find_text)
        e.pack(side=LEFT, fill=X, expand=1)
        e.bind("<Return>", self.onFind)
        e.bind("<Escape>", self.clearFind)
        Button(frm, text='Quit', width=btnwdth, command=self.quit).pack(side=LEFT)
        self.st = ScrolledText.__init__(self, parent, file=file)

    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()
            open(filename, 'w').write(alltext)

    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def clearFind(self, *args):
        self.find_text.set("")

    def onFind(self, *args):
        target = self.find_text.get()
        print('onFind')
        # target = askstring('SimpleEditor', 'Search String?')
        print('target', target)
        if target:
            where = self.text.search(target, INSERT, END)
            if not where:
                where = self.text.search(target, "0.0", INSERT)
            if where:
                print(where)
                pastit = where + ('+%dc' % len(target))
                # self.text.tag_remove(SEL, '1.0', END)
                self.text.tag_add(SEL, where, pastit)
                self.text.mark_set(INSERT, pastit)
                self.text.see(INSERT)
                self.text.focus()

    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans:
            Frame.quit(self)


if __name__ == '__main__':
    try:
        SimpleEditor(file=sys.argv[1]).mainloop()
    except IndexError:
        SimpleEditor().mainloop()
