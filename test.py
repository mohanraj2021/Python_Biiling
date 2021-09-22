import tkinter

root = tkinter.Tk()
myvar = tkinter.StringVar()
myvar.set('')
mywidget = tkinter.Entry(root,textvariable=myvar,width=10)
mywidget.pack()

def oddblue(a,b,c):
    if len(myvar.get())%2 == 0:
        mywidget.config(bg='red')
    else:
        mywidget.config(bg='blue')
    mywidget.update_idletasks()

myvar.trace('w',oddblue)

root.mainloop()