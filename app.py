from logging import error
from tkinter import *
import tkinter
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector


def addProductDetails(list):

    try:
        dbDetail = dbInfo()
        
        host = dbDetail['host']
        username = dbDetail['user']
        dbpassword = dbDetail['password']
        db = dbDetail['database']
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=dbpassword,
            database=db
        )
        
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO products (product_code, product_name,product_price) VALUES (%s, %s,%s)"
        val = (list[0],list[1],list[2])
        mycursor.execute(sql, val)


        mydb.commit()

        result=print(mycursor.rowcount, "record inserted.")
        result={'value':'success'}
        return result

    except mysql.connector.Error as err:
        result={'value':'failed',
                'error':'{}'.format(err)}
        return result


def getProductDetails(req):
    try:
        p_code = req['value']
        dbDetail = dbInfo()
        
        host = dbDetail['host']
        username = dbDetail['user']
        dbpassword = dbDetail['password']
        db = dbDetail['database']
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=dbpassword,
            database=db
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM products WHERE product_code = '{}'".format(p_code))
        result = mycursor.fetchall()

        mydb.commit()
        return result

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def getReport():
    try:
        dbDetail = dbInfo()
        
        host = dbDetail['host']
        username = dbDetail['user']
        dbpassword = dbDetail['password']
        db = dbDetail['database']
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=dbpassword,
            database=db
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM report WHERE date BETWEEN '{}' to '{}' ".format())
        result = mycursor.fetchall()

        mydb.commit()
        return result

    except mysql.connector.Error as err: 
        print("Something went wrong: {}".format(err))

def addBillDetails(req):
    try:
        dbDetail = dbInfo()
        
        host = dbDetail['host']
        username = dbDetail['user']
        dbpassword = dbDetail['password']
        db = dbDetail['database']
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=dbpassword,
            database=db
        )
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO report (product_code, product_name,product_price,product_quantity,total_product_amount,total_bill_amount,table_name,date,bill_no) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s)"
        vals = req
        for val in vals:
            mycursor.execute(sql, val)


        mydb.commit()

        success=print(mycursor.rowcount, "record inserted.")
        return success
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def getLatestInsertedId():
    try:
        dbDetail = dbInfo()
        
        host = dbDetail['host']
        username = dbDetail['user']
        dbpassword = dbDetail['password']
        db = dbDetail['database']
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=dbpassword,
            database=db
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("select *from report ORDER BY id DESC LIMIT 1;")
        result = mycursor.fetchall()
        mydb.commit()
        if not result:
            return 0
        else:
            return result[0][9]

    except mysql.connector.Error as err: 
        print("Something went wrong: {}".format(err))





def dbInfo():
    dbInformation = {"host":"localhost","user":"root","password":'',"database":"hotel"}
    return dbInformation

class BillApp:
    def __init__(self,root):
        self.root=root
        self.root.geometry('1350x700')
        self.root.title("Powered by DeCode")
        p1 = PhotoImage(file = 'decode.png')
        self.root.iconphoto(False, p1)
        
        
        # image = PhotoImage(file='decode.png')
        # titleFrame = Frame(self.root, bg='white',width=1350, height=60,image=image)
        # titleFrame.place(y=1)
        
        top_left = Frame(self.root, bg='white', width=1350, height=60)
        top_left.place(y=0)
        image = Image.open("decode.png")
        photo = ImageTk.PhotoImage(image.resize((150,70), Image.ANTIALIAS))
        logolabel = Label(top_left, image=photo, )
        logolabel.image = photo
        logolabel.place(y=0)
        title =Label(top_left,text="Hotel Swagat" ,bd=12,bg='white',font=('Arial',25,'bold'))
        title.place(x=550)

        title1 =Label(top_left,text="info@d-code.co.in" ,bd=10,bg='white',font=('Arial',12,'bold'))
        title1.place(x=152,y=0)
        


        title2 =Label(top_left,text="Helpline: +91 9373417227" ,bd=10,bg='white',font=('Arial',12,'bold'))
        title2.place(x=152,y=30)
        getEntryValue1 = tkinter.StringVar()
        getEntryValue1.set('')
        entry2StrVal = tkinter.StringVar()
        entry3StrVal = tkinter.StringVar()
        entry4StrVal = tkinter.StringVar()
        entry5StrVal = tkinter.StringVar()
        style = ttk.Style()
        #=============== Entry Area ==============# 
        label = Label(self.root, text="Product Code :")
        label.place(x=10,y=80)
        entry = Entry(self.root, width=10, textvariable=getEntryValue1)
        entry.place(x=120, y=80)
        
        label2 = Label(self.root, text="Product Name :")
        label2.place(x=200, y=80)
        entry2 = Entry(self.root,width=30,textvariable=entry2StrVal)
        entry2.place(x=300, y=80)
        
        label3 = Label(self.root, text="Product Amount :",)
        label3.place(x=10,y=120)
        entry3 = Entry(self.root,width=10,textvariable=entry3StrVal)
        entry3.place(x=120, y=120)
        
        label4 = Label(self.root, text="Quantity :")
        label4.place(x=210, y=120)  
        entry4 = Spinbox(self.root,width=10,from_=1, to=100, increment=1, textvariable=entry4StrVal)
        entry4.place(x=300, y=120)
        
        label5 = Label(self.root, text="Amount :",)
        label5.place(x=10, y=160)
        entry5 = Entry(self.root,width=10,textvariable=entry5StrVal)
        entry5.place(x=120, y=160)
        
        #Method to Clear product entries
        def clear_text():
            entry.delete(0, 'end')
            entry2.delete(0, 'end')
            entry3.delete(0, 'end')
            entry4.delete(0, 'end')
            entry5.delete(0, 'end')

        #=============== Table Area ==============#



        tableLabel = Label(self.root, text='Entry Table')
        tableLabel.place(x=10,y=275)

        frame = Frame(self.root,).place()
        self.tv = ttk.Treeview(frame,columns=(1,2,3,4,5),show='headings',height='15',)
        self.tv.place(x=10,y=300)
        
        
        self.tv.heading(1,text="Product Code",anchor='center')
        self.tv.heading(2,text="Product Name")
        self.tv.heading(3,text="Product Price")
        self.tv.heading(4,text="Product Quantity")
        self.tv.heading(5,text="Amount")
        self.tv.column(1,anchor='center',width=100)
        self.tv.column(2,anchor='center',width=100)
        self.tv.column(3,anchor='center',width=100)
        self.tv.column(4,anchor='center',width=110)
        self.tv.column(5,anchor='center',width=90)
        style.theme_use("clam")
        style.configure('Treeview.Heading',  background="#E1ECF4")


        frame1 = Frame(self.root).place()
        tv1 = ttk.Treeview(frame1,columns=(1,2,3),show='',height='16')
        tv1.place(x=600,y=301)

        tv1.heading(1,text="Product Name",anchor='center',)
        tv1.heading(2,text="Amount",anchor='center')
        tv1.heading(3,text="Quantity",anchor='center')
        tv1.column(1,anchor='center',width=70)
        tv1.column(2,anchor='center',width=70)
        tv1.column(3,anchor='center',width=70)
        

        F3 = Label(self.root,bd = 1,relief = GROOVE)
        F3.place(x = 600,y = 301,width = 325,height = 330)
        #===========
        bill_title = Label(F3,text = "Bill",font = ("Lucida",13,"bold"),bd= 3,relief = GROOVE)
        bill_title.pack(fill = X)

        #============
        scroll_y = Scrollbar(F3,orient = VERTICAL)
        self.txt = Text(F3,yscrollcommand = scroll_y.set)
        scroll_y.pack(side = RIGHT,fill = Y)
        scroll_y.config(command = self.txt.yview)
        self.txt.pack(fill = BOTH,expand = 1)
        

        
        #=============== Hall Frame Section ===============#
        parentFrame = Frame(self.root,bg='#fff').pack(expand=1, fill=X,)
        

        framelabel = Label(parentFrame, text="Tables",font=12)
        framelabel.place(x=900,y=70)
        hallFrame = Frame(parentFrame, width=500, height=400, bg='#E1ECF4')
        hallFrame.place(x=530,y=100)

        iframe1 = Frame(hallFrame,  relief=SUNKEN,bg='#E1ECF4')

        v=StringVar()
        

        Radiobutton(iframe1, text='T-1', variable=v,indicatoron=0,value="table1",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W ,padx=15,)
        Radiobutton(iframe1, text='T-2', variable=v,indicatoron=0,value="table2",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-3', variable=v,indicatoron=0,value="table3",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-4', variable=v,indicatoron=0,value="table4",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-5', variable=v,indicatoron=0,value="table5",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-6', variable=v,indicatoron=0,value="table6",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-7', variable=v,indicatoron=0,value="table7",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-8', variable=v,indicatoron=0,value="table8",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)

        Radiobutton(iframe1, text='T-9', variable=v,indicatoron=0,value="table9",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe1, text='T-10', variable=v,indicatoron=0,value="table10",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)

        Radiobutton(iframe1, text='T-11', variable=v,indicatoron=0,value="table11",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)


        iframe2 = Frame(hallFrame,  relief=SUNKEN,bg='#E1ECF4')
        iframe3 = Frame(hallFrame,height=50,  relief=SUNKEN,bg='#E1ECF4')
        
        

        Radiobutton(iframe2, text='T-12', variable=v,indicatoron=0,value="table12",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W ,padx=15,)
        Radiobutton(iframe2, text='T-13', variable=v,indicatoron=0,value="table13",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-14', variable=v,indicatoron=0,value="table14",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-15', variable=v,indicatoron=0,value="table15",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-16', variable=v,indicatoron=0,value="table16",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-17', variable=v,indicatoron=0,value="table17",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-18', variable=v,indicatoron=0,value="table18",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)

        Radiobutton(iframe2, text='T-19', variable=v,indicatoron=0,value="table19",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-20', variable=v,indicatoron=0,value="table20",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)

        Radiobutton(iframe2, text='T-21', variable=v,indicatoron=0,value="table21",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        Radiobutton(iframe2, text='T-22', variable=v,indicatoron=0,value="table22",height='2',width='5',borderwidth=1,activebackground="#E1ECF4").pack(side=LEFT, anchor=W,padx=15)
        iframe1.pack(expand=1,pady=10, padx=5)
        iframe3.pack()
        iframe2.pack(expand=1,pady=10, padx=5)


        #=============== Hall Frame Section ===============#

        #method for auto field fill of Productname & Productprice 
        def updateAmount(a,b,c):
            try:    
                x = getEntryValue1.get()
                y={'value':x}
                data = getProductDetails(y) #Gets the product details 
                if data:
                    
                    entry2Value = data[0][2]
                    entry3Value = data[0][3]
                   #sets tuple value product of data into entry field of Product name & product price
                    entry2StrVal.set(entry2Value)
                    entry3StrVal.set(entry3Value)
                    
                else:
                    #If invalid product code entered the enrty field of Productname & ProductPrice will be blank
                    entry2StrVal.set('')
                    entry3StrVal.set('')
                    entry4StrVal.set('1')
                    return "Invalid data"
                entry2.update_idletasks() 
            except error as err:
                return err
        getEntryValue1.trace('w',updateAmount)

        #Method for updating the amount according to quantity
        def updateTotalamout(a,b,c):
            try:
                p=entry4StrVal.get()
                q =entry3StrVal.get()
                if p and q:
                    p = int(p)
                    q = int(q)
                    r = (p * q)
                    entry5StrVal.set(r)
                else:
                   entry5StrVal.set('') 
            except Exception as err:
                return err
        
        entry4StrVal.trace('w',updateTotalamout)
        entry3StrVal.trace('w',updateTotalamout)

        #Method to add the bill details in table
        def addToTable():
            a = getEntryValue1.get()
            b = entry2StrVal.get()
            c = entry3StrVal.get()
            d = entry4StrVal.get()
            e = entry5StrVal.get()
            tableList = []
            tableList.extend([a,b,c,d,e])
            if a and b and c and d and e:
                self.tv.insert('',END, values=tableList)  
            clear_text()

        #Methods for updating the Table records
        def updateTable():
            
            selected=self.tv.focus()
            valueslist=self.tv.item(selected,'values')
          
            getEntryValue1.set(valueslist[0])
            entry2StrVal.set(valueslist[1])
            entry3StrVal.set(valueslist[2])
            entry4StrVal.set(valueslist[3])
            entry5StrVal.set(valueslist[4])
            delitem = self.tv.item(selected)
            delTvitem()
        #Method for to Delete item from Entry table
        def delTvitem():
            selectedItem = self.tv.selection()
            self.tv.delete(selectedItem)  
        

        #Method for Print bill and insert Table records to DB
        def bill():
            global bill_num
            items = []
            bill_amt =[]
            tablenum = v.get()
            bill_num = int(getLatestInsertedId())
            bill_num +=1
            tableData =[]
            now = datetime.now()
            created_at = now.strftime("%d/%m/%Y %H:%M:%S")
            if tablenum and tablenum !='0':
                for lines in self.tv.get_children():
                    bill_amt.append(self.tv.item(lines)['values'][4])
                    items.append(self.tv.item(lines)['values'])            
                total_bill_amount=sum(bill_amt) 
                appendItems =[total_bill_amount,tablenum,created_at,bill_num]
                for item in items:
                    lists = list(item)
                    lists.extend(appendItems)
                    tableDatavalues =tuple(lists)
                    tableData.append(tableDatavalues)
                v.set(0)
                if tableData:
                    addBillDetails(tableData)
                    self.tv.delete(*self.tv.get_children())
                    self.clear()
                    messagebox.showinfo("Success", "Data Added to Database")
                    self.Info()
                else:
                    messagebox.showerror("Error", "Add Products")
            else:
                messagebox.showerror("Error", "Select Table")

        #Buttons to Add & Del the items in table  
        # <--Start-->
        addButton = Button(self.root,text='Add',command=addToTable,width=10)
        addButton.place(x=20, y=220)
        
        delButton = Button(self.root,text='Delete',command=delTvitem,width=10)
        delButton.place(x=150, y=220)

        clearButton = Button(self.root,text='Clear',command=clear_text,width=10)
        clearButton.place(x=280, y=220)

        updateButton = Button(self.root,text='Update',command=updateTable,width=10)
        updateButton.place(x=410, y=220)

        billButton = Button(self.root,text='Bill',command=self.bill_area,width=20)
        billButton.place(x=1000, y=540)

        
        # printButton = Button(self.root,text='Print',command=self.Info)
        # printButton.place(x=400, y=200)

        saveButton = Button(self.root,text='Print',command=bill,width=20)
        saveButton.place(x=1000, y=440)

        addProButton = Button(self.root,text='Add Product',command=self.openNewWindow,width=20)
        addProButton.place(x=1000, y=340)
        #<--End-->

    #Method for Printing bill details in bill text frame
    def welcome_soft(self):
        bill_num = int(getLatestInsertedId())
        bill_num +=1
        self.txt.insert(END,"             Hotel Swagat\n")
        self.txt.insert(END,f"\nBill No. : {str(bill_num)}")
        self.txt.insert(END,"\n===================================")
        self.txt.insert(END,"\nProduct          Qty         Price")
        self.txt.insert(END,"\n===================================")

    #Method for deleting & clear the all data form txt frame. 
    def clear(self):
        self.txt.delete('1.0',END)

    #Method for creating bill by the records from treeview.
    def bill_area(self):
        self.clear()
        self.welcome_soft()
        items = []
        d = []
        for lines in self.tv.get_children():
            items.append(self.tv.item(lines)['values'])
            
        for item in items:
            a = item[1]
            b = item[3]
            c = item[4]
            
            tableList = []
            tableList.clear()
            tableList.extend([a,b,c])
            
            d.append(c)
            
            if a and b and c:
                space = ' '*(18 -len(a))
                proPrice = str(b)
                space1 = ' '*(14-len(proPrice))
                self.txt.insert(END,"\n")                       
                self.txt.insert(END,f"\n{a}{space}{b}{space1}{c}" )       
        s = sum(d)
        space3 =" "*(26-len(proPrice))
        self.txt.insert(END,"\n===================================")
        self.txt.insert(END,f"\n{space3}Total :{s} ")
        
        self.txt.insert(END,f"\n==========Powered By Dcode=========",)

        
        #Buttons to Add & Del the items in table  
        # <--Start-->
    

    

    def Info(self):
        printText = self.txt.get("1.0", END)
        print(printText)
        
        
    def openNewWindow(self):

        productCode = StringVar()
        productName = StringVar()
        productPrice = StringVar()

        newWindow = Toplevel(self.root)
        newWindow.title("Powered by Decode")
        newWindow.geometry("700x200")
        p2 = PhotoImage(file = 'decode.png')
        newWindow.iconphoto(False, p2)
        Label(newWindow,text ="Add Products").pack()

        label = Label(newWindow, text="Product Code :",)
        label.place(x=10,y=80)
        entry = Entry(newWindow, width=10,textvariable=productCode )
        entry.place(x=100, y=80)
        
        label2 = Label(newWindow, text="Product Name :",)
        label2.place(x=200, y=80)
        entry2 = Entry(newWindow,width=30,textvariable=productName)
        entry2.place(x=295, y=80)
        
        label3 = Label(newWindow, text="Product Amount :", )
        label3.place(x=500,y=80)
        entry3 = Entry(newWindow,width=10,textvariable=productPrice)
        entry3.place(x=605, y=80)

        def addProductToDb():
            prCode = productCode.get()
            prName = productName.get()
            prPrice = productPrice.get()
            if prCode and prName and prPrice:
                productDetails=[prCode,prName,prPrice]
                result=addProductDetails(productDetails)
                if result['value'] == 'success':
                    messagebox.showinfo('Success','Product Added Successfully')
                
                else:
                    messagebox.showerror('Error','Product Code or Product Name Already Exist')
            else:
                messagebox.showerror('Error','Enter Product Details')


        newWindowsaveButton = Button(newWindow,text='save',command=addProductToDb)
        newWindowsaveButton.place(x=350, y=150)





root = tkinter.Tk()
obj = BillApp(root)
root.resizable(width=False, height=False)
root.mainloop() 
