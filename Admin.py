from tkinter import *
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
from logging import error
from datetime import date



def loginUser(req):
    try:
        Unum = req['number']
        Upassword = req['password']
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
        results =mycursor.execute("SELECT * FROM user WHERE number = '{}' and password = '{}'".format(Unum,Upassword))
        query = mycursor.fetchall()
        mydb.commit()
        if query:
            result={}
            result['success'] = True
            return result 
        else:
            result={}
            result['success'] = False
            return result

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def reportData(dateRange):
    try:
        fromDate = dateRange['fromDate']
        toDate = dateRange['toDate']     
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
        mycursor.execute("SELECT * FROM report WHERE date BETWEEN '{}' and '{}'".format(fromDate,toDate))
        results = mycursor.fetchall()
        mydb.commit()
        if results:
            result={}
            result['result'] = results
            result['success'] = True
            return result 
        else:
            result={}
            result['success'] = False
            return result

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def UserRegistration(userData):
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
        
        sql = "INSERT INTO user (username, number,password) VALUES (%s, %s,%s)"
        val = (userData['username'],userData['number'],userData['password'])
        mycursor.execute(sql, val)


        mydb.commit()

        result=print(mycursor.rowcount, "record inserted.")
        result={'value':'success'}
        return result

    except mysql.connector.Error as err:
        if err.errno == 1062:
            result={'value':'failed',
                'error':'{}'.format(err.errno)}
            return result
        else:    
            result={'value':'failed',
                    'error':'{}'.format(err)}
            return result


def dbInfo():
    dbInformation = {"host":"localhost","user":"root","password":'',"database":"hotel"}
    return dbInformation


class BillApp:
    def __init__(self,root):
        self.root=root
        self.root.geometry('1350x700')
        self.root.title("Powered by DeCode")
        style = ttk.Style()
        number = StringVar()
        password = StringVar()
        

        top_left = Frame(self.root, bg='white', width=290, height=350)
        top_left.place(x=500,y=150)

        label = Label(top_left, text="Mobile Number:",bg='#E1ECF4')
        label.place(x=110,y=50)
        entry = Entry(top_left, width=30,textvariable=number,bd=2)
        entry.place(x=60, y=100)
        
        label2 = Label(top_left, text="Password :",bg='#E1ECF4')
        label2.place(x=120, y=150)
        entry2 = Entry(top_left,width=30,textvariable=password,bd=2,show='*')
        entry2.place(x=60, y=200)


        frame = Frame(self.root,width=1000).place()
        self.tv = ttk.Treeview(frame,columns=(1,2,3,4),show='headings',height='20',)
        self.tv.place_forget()
        
        

        self.tv.heading(1,text="Product Name",anchor='center')
        self.tv.heading(2,text="Total Amount",anchor='center')
        self.tv.heading(3,text="Table",anchor='center')
        self.tv.heading(4,text="Bill No",anchor='center')
        self.tv.column(1,anchor='center',width=900)
        self.tv.column(2,anchor='center',width=100)
        self.tv.column(3,anchor='center',width=100)
        self.tv.column(4,anchor='center',width=100)
        style.theme_use("clam")
        style.configure('Treeview.Heading',  background="#E1ECF4")

        def removeSpace(string):
            product = []
            for j in string:
                s =str(j).replace(' ','')
                product.append(s)
            return product

        def logout():
            top_left.place(x=500,y=150)
            registerButton.place(x=550, y=530)
            self.tv.place_forget()
            logoutButton.place_forget()
            entry.delete(0,'end')
            entry2.delete(0,'end')
            self.tv.delete(*self.tv.get_children())
        
        def report():
            try:
                date1 = date.today()
                date2 = date.today()
                dateRange ={
                    'fromDate': date1,
                    'toDate':date2
                }
                modellists = [[]]
                items = reportData(dateRange)
                i=0
                billNum = items['result'][0][9]
                productlist=[]
                tablelist =[]
                for item in items['result']:
                    
                    if item[9] != billNum:
                        billNum = item[9]
                        product = removeSpace(productlist)
                        modellists[i].append(product)
                        modellists[i].extend(tablelist) 
                        modellists.append([])
                        i+=1
                        productlist=[]
                        product =[]
                    if item[9] == billNum:
                        productlist.append(item[2])
                        tablelist =[]
                        tablelist.extend([item[6],item[7],item[9]])   
                product = removeSpace(productlist)
                modellists[i].append(product)
                modellists[i].extend(tablelist)    

                return modellists
            except error as err:
                return err   

        def login():
            Unumber = number.get()
            Upassword = password.get()
            uData ={'number':Unumber,
                    'password':Upassword}
            if Unumber and Upassword:
                if len(Unumber) == 10:
                    result=loginUser(uData)
                    if result['success'] == True:
                        top_left.place_forget()
                        registerButton.place_forget()
                        self.tv.place(x=70, y=150)
                        logoutButton.place(x=1150,y=70)
                        modellists = report()
                        for modelList in modellists:
                            self.tv.insert('',END,values=modelList,)
                    else:
                        messagebox.showerror('Error', 'Provide Valid Credentials')

                else:
                        messagebox.showerror('Error', 'Provide Valid Mobile Number')

            else:
                if not (Unumber or Upassword):
                    messagebox.showerror('Error', 'Fill The Credentials Field') 

                elif not Unumber:
                    messagebox.showerror('Error', 'Fill The User Number Field')

                elif not Upassword:
                    messagebox.showerror('Error', 'Fill The User Password Field')

            

        loginButton = Button(top_left,text='Login',width=11,command=login)
        loginButton.place(x=100, y=280)

        logoutButton = Button(self.root,text='Logout',width=15,height=3,command=logout)
        logoutButton.place_forget()
        
        

        registerButton = Button(self.root,text='Register User',command=self.registerWindow,width=25)
        registerButton.place(x=550, y=530)

    
    def registerWindow(self):
        newWindow = Toplevel(self.root)
        newWindow.title("Powered by Decode")
        newWindow.geometry("350x400")
        newWindow.resizable(width=False, height=False)
        newWindow.transient(self.root)
        newWindow.grab_set()
        userData ={}
        username = StringVar()
        number = StringVar()
        password = StringVar()

         

        def UserRegister():
            Uname = username.get()
            Unumber = number.get()
            Upassword = password.get()
            userData['username'],userData['number'],userData['password'] = Uname,Unumber,Upassword
            if Uname and Unumber and Upassword:

                if len(Unumber) == 10:
                    result =UserRegistration(userData)
                    
                    if result['value'] == 'success':
                        messagebox.showinfo('Success', 'User Created Successfully')

                    elif result['error'] == '1062':

                        messagebox.showerror('Error','Username or Mobile number Already Exist')

                    else:
                        messagebox.showerror('Error','User Creation Failed Please Try Again.!')

                else:
                    messagebox.showerror('Error','Provide Valid Mobile Number')
            else:
                if not (Uname or Unumber or Upassword):
                    messagebox.showerror('Error','Please Enter User Details')
                elif not Uname:
                    messagebox.showerror('Error','Please Enter Username')
            
                elif not Unumber:
                    messagebox.showerror('Error','Please Enter Mobile Number')

                elif not Upassword:
                    messagebox.showerror('Error','Please Enter Password')

        top_right = Frame(newWindow, bg='white', width=290, height=350)
        top_right.place(x=30,y=23)

        label = Label(top_right, text="User Name :",)
        label.place(x=110,y=30)
        entry = Entry(top_right, width=30,textvariable=username,bd=2)
        entry.place(x=60, y=80)
        
        label2 = Label(top_right, text="Phone :",)
        label2.place(x=120, y=130)
        entry2 = Entry(top_right,width=30,textvariable=number,bd=2)
        entry2.place(x=60, y=180)

        label3 = Label(top_right, text="Password :",)
        label3.place(x=118, y=230)
        entry3 = Entry(top_right,width=30,textvariable=password,bd=2)
        entry3.place(x=60, y=280)

        

        register1Button = Button(top_right,text='Register',command=UserRegister,width=13)
        register1Button.place(x=100, y=320)

        

        
            
root = tkinter.Tk()
obj = BillApp(root)
root.resizable(width=False, height=False)
root.mainloop()