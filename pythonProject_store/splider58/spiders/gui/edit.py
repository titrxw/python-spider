import Tkinter 
from Tkinter  import StringVar

class Edit(tkinter.Entry):

    class_text=None
    class_instance=None

    def __init__(self, master=None,default=''):
        Edit.class_text = StringVar()
        Edit.class_text.set(default)
        Edit.class_instance = Tkinter.Entry(master, textvariable=Edit.class_text)


    def getText(self):
        return Edit.class_text.get()

    def getInstance(self):
        return Edit.class_instance
