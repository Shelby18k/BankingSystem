'''
Created on 24-Jul-2018

@author: TushaR
'''
import os
import cx_Oracle
from datetime import date,datetime,timedelta
os.chdir("C:\instantclient-basic-nt-12.2.0.1.0\instantclient_12_2")

con = cx_Oracle.connect('system/tushar@localhost')
cur  = con.cursor()

class Customer:
    def __init__(self,accountType,fname,lname,address,city,state,pincode):
        self.accountType = accountType
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
    
    def generateAccountNumber(self):
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/id.txt") as f:
            file_str = f.read()
            
        file_int = int(file_str)
        file_int += 1
        self.accountNumber = self.accountType[0] + self.fname[0] + str(self.pincode) + self.lname[0] + str(file_int)
        with open("C:/Users/TushaR/eclipse-workspace/Python Course/src/Pydev/hello.txt",'w') as f:
            f.write(str(file_int))
        return self.accountNumber
    
    def enterPassword(self):
        print('*'*6 + " Your account number is " + self.generateAccountNumber())
        while True:
            password = input("Enter your password...?(min.8 length)")
            if len(password) >= 8:
                self.password = password
                print("Your password set successfully..!!")
                return
            else:
                print('*'*6 + 'Invalid Input' + '*'*6)
    
    def registerUser(self):
        stmt = """INSERT INTO customers(customerid,accountno,password,accounttype,fname,
        lname,address,city,state,pincode) values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)"""
        try:
            cur.execute(stmt,{'1':self.accountNumber,'2':self.accountNumber,'3':self.password,'4':self.accountType,'5':self.fname,
                              '6':self.lname,'7':self.address,'8':self.city,'9':self.state,'10':self.pincode})
            con.commit()
            return self.accountNumber
        except:
            print("An error occurred while registering, please contact admin")
            return None






class RegisteredCustomer(Customer):
    def __init__(self,accountType,fname, lname, address, city, state, pincode,accountNumber,password):
        super(RegisteredCustomer,self).__init__(accountType, fname, lname, address, city, state, pincode)
        self.accountNumber = accountNumber
        self.password = password
    
    def address_change(self):
        address = input("Enter your new address, Line 1: ")
        address += " " + input("Line 2: ")
        stmt = "UPDATE customers set address = :1 where customerid = :2 and password = :3"
        cur.execute(stmt,{'1':address,'2':self.accountNumber,'3':self.password})
        con.commit()
        print("Address Changed Successfully\n")
        
    def money_deposit(self):
        while True:
            amount = float(input("Enter deposit amount: "))
            if amount < 0:
                print('*'*6+'Please enter a positive value')
            else:
                break
        today = date.today()
        today = datetime.strptime(str(today)[0:10],'%Y-%m-%d')
        stmt = "UPDATE transactions SET balance = balance + :1,dt = to_date(:3,'dd-mm-yyyy') where accountid = :2"
        try:
            cur.execute(stmt,{'1':amount,'2':self.accountNumber,'3':today})
            con.commit()
            print('*'*6+"Your balance has been deposited")
            stmt = "INSERT INTO statementdetails(accountid,balance,dt,transtype) values(:1,:2,to_date(:3,'dd-mm-yyyy'),:4)"
            cur.execute(stmt,{'1':self.accountNumber,'2':amount,'3':today,'4':'Credited'})
            return amount
        except:
            print("Error Depositing")
        
        
    
   
# rdate = date.today() + timedelta(days=30)
# rdate = rdate.strftime("%d-%m-%Y")
# print(str(rdate))

# stmt = "SELECT transcount,dt,renewaldate from transactioncount where accountid = :1"
# cur.execute(stmt,{'1':'ST248179K1'})
# res = cur.fetchall()
# print(res)
# count = int(res[0][0])
# d1 = res[0][1]
# d2 = res[0][2]
# print(d1)
# print(d2)
# print(type(d2))
# d1 = datetime.strptime(str(d1)[0:10],'%Y-%m-%d')
# d2 = datetime.strptime(str(d1)[0:10],'%Y-%m-%d')
# print(d2)
# print(d1)
# print(type(d2))
# if d1== d2:
#     print("Equeal")
# if d1 > d2:
#     print("Hello")
# if d2 > d1:
#     print("Hello1") 
# print(d2-d1)