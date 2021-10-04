from tkinter import *
from tkinter import Tk, Text, BOTH, W, N, E, S, filedialog
from tkinter import ttk
from tkinter.ttk import Frame, Button, Label, Style
from audit_parser import parse_audit_file



class Audit_Find_Tool(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        
        self.master.title("Audit Find Tool")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        


        searchLabel = Label(self, text="Search:", font = "24", background="gray", foreground="white")
        searchLabel.grid(sticky=E, pady=4, padx=5, row = 0, column = 0)

        self.searchEntry = Entry(self) 
        self.searchEntry.grid(sticky=E+W+S+N, pady=4, padx=5, row = 0, column =1)

        self.searchEntry.focus_set() 
        findButton = Button(self, text='Find', command = self.find ) 
        findButton.grid(sticky=W, pady=4, padx=5, row = 0, column = 2)

        openButton = Button(self, text="Open .audit file", command=self.openFile)
        openButton.grid(sticky=S, row=5, column=0, pady=4, padx=50)

        saveButton = Button(self, text="Save .audit file", command=self.saveFile)
        saveButton.grid(sticky=S, row=5, column=2, pady=4, padx=50)

        self.textBox = Text(self)
        self.textBox.grid(row=1, column=0, columnspan=3, rowspan=4,
            padx=5, sticky=E+W+S+N)

        self.scrollbar = Scrollbar(self)
        self.textBox.config(yscrollcommand= self.scrollbar.set)
        self.scrollbar.config(command= self.textBox.yview)
        self.scrollbar.grid(column=3, row=1, rowspan=4,  sticky=N+S+W)


    def openFile(self):  
        file = filedialog.askopenfile(mode="r", defaultextension=".audit",  filetypes = [("Audit files", "*.audit")])

        if not file:
            return
        
        f = open(file.name, "r")

        structure = parse_audit_file(f.read())


        self.textBox.config(state=NORMAL) 
    
        structure = [cols[2:] for cols in structure]
         
        structure = [item for s in structure for item in s] 

        self.checkbuttons = []
        self.vars = []
         
        for i in range(len(structure)):
            var = IntVar(value=0)
            cb = Checkbutton(self.textBox, text = structure[i], variable=var, onvalue=1, offvalue=0, 
                bg = 'white', cursor='hand2', wraplength=900, justify=LEFT)
            self.textBox.window_create("end", window=cb)
            self.textBox.insert("end", "\n")
            self.checkbuttons.append(cb)
            self.vars.append(var)        

        self.textBox.config(state=DISABLED) 


    def saveFile(self): 
        file = filedialog.asksaveasfile(mode="w", defaultextension=".audit")
        f = open(file.name, "w")
        
        for cb, var in zip(self.checkbuttons, self.vars):
            text = cb.cget("text")
            value = var.get()
            if value == 1:
                f.write("%s\n" % (text))
        f.close()  


    def find(self): 
        self.textBox.tag_remove('found', '1.0', END) 
        s = self.searchEntry.get() 
        
        if s: 
            idx = '1.0'
            while 1: 
                idx = self.textBox.search(s, idx, nocase=1, 
                            stopindex=END) 
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(s)) 
                self.textBox.tag_add('found', idx, lastidx) 
                idx = lastidx 
            
            self.textBox.tag_config('found', foreground='red') 
        self.searchEntry.focus_set() 

def main():

    root = Tk()
    root.geometry("1000x1000")
    app = Audit_Find_Tool()
    root.mainloop()


if __name__ == '__main__':
    main()