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

# val = {'value':'p01'}

# data = getProductDetails(val)
# print(data[0][1])
# print(data[0][2])
