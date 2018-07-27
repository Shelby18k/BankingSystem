'''
Created on 24-Jul-2018

@author: TushaR
'''
import os
import cx_Oracle
from datetime import date,datetime,timedelta
from _ast import stmt
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
        
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/id.txt",'w') as f:
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
        
    def enter_amount(self):
        while True:
            amount = float(input("Enter amount: "))
            if amount < 0:
                print('*'*6+'Please enter a positive value')
            else:
                break
        return amount
    
    def insert_in_statement(self,amount,today,trans):
        stmt = "INSERT INTO statementdetails(id,accountid,balance,dt,transtype) values(:1,:2,:3,to_date(:4,'dd-mm-yyyy'),:5)"
        
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/transactionid.txt") as f:
            file_str = f.read()
        file_int = int(file_str)
        file_int += 1
        cur.execute(stmt,{'1':file_int,'2':self.accountNumber,'3':amount,'4':today,'5':trans})
        
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/transactionid.txt",'w') as f:
            f.write(str(file_int))
        
        
    def money_deposit(self):
        amount = self.enter_amount()
        today = date.today()
        today = today.strftime("%d-%m-%Y")
#         print(today)
        stmt = "UPDATE transactions SET balance = balance + :1,dt = to_date(:3,'dd-mm-yyyy') where accountid = :2"
        
        cur.execute(stmt,{'1':amount,'2':self.accountNumber,'3':today})
        print('*'*6+"Your balance has been deposited")
        self.insert_in_statement(amount,today,'Credited')
        con.commit()
        return amount
    
    def money_withdrawal(self,amt):
        today = date.today()
        today = today.strftime("%d-%m-%Y")
#         print("Hello")
        stmt = "UPDATE transactions SET balance = balance - :1,dt = to_date(:3,'dd-mm-yyyy') where accountid = :2"
        try:
            cur.execute(stmt,{'1':amt,'2':self.accountNumber,'3':today})
            print('*'*6+"Your balance has been withdrawn")
            self.insert_in_statement(amt,today,'Debited')
            con.commit()
            return amt
        except:
            print("Error Withdrawing")
    
    
    def deduct_balance(self,amount):
        stmt = "UPDATE transactions SET balance = balance - :1 where accountid = :2"
        cur.execute(stmt,{'1':amount,'2':self.accountNumber})
        
    def add_balance(self,amount,to):
        stmt = "UPDATE transactions SET balance = balance + :1 where accountid = :2"
        cur.execute(stmt,{'1':amount,'2':to})
        
    def transferMoney(self,amount,to):
        self.deduct_balance(amount)
        self.add_balance(amount,to)
        stmt = "INSERT INTO transfermoney(accountid,toaccount,balance) values(:1,:2,:3)"
        cur.execute(stmt,{'1':self.accountNumber,'2':to,'3':amount})
        con.commit()
    
    def  check_available_balance(self,amount,to):
        stmt = "SELECT balance from transactions where accountid = :1"
        cur.execute(stmt,{'1':self.accountNumber})
        res = cur.fetchall()
        a = float(res[0][0])
        withdrawalAmount = a - 5000
        if self.accountType == 'Saving' and a >= amount:
            self.transferMoney(amount, to)
            stmt = "UPDATE transactioncount set transcount = transcount+1 where accountid = :1"
            cur.execute(stmt,{'1':self.accountNumber})
            con.commit()
            return 1
        elif self.accountType == 'Current' and withdrawalAmount >= amount:
            self.transferMoney(amount, to)
            return 1
        else:
            print('*'*8+"Balance is not sufficient")
            return 0
        
    
    def account_close(self):
        stmt = "INSERT INTO accountclosed(accountid) values(:1)"
        try:
            cur.execute(stmt,{'1':self.accountNumber})
            con.commit()
            return 1
        except:
            print("Error in closing account\n")
        
        
            
           
        
class Admin:
    def __init__(self,adminid,password):
        self.adminid = adminid
        self.password = password
    
    def closed_accounts(self):
        stmt = "select * from accountclosed"
        cur.execute(stmt)
        res = cur.fetchall()
        if len(res) == 0:
            print("*"*10+"No account has been closed")
        else:
            print("AccountID\t\tDate")
            for r in res:
                print("{a}\t\t{d}".format(a = r[0],d = str(r[1])[0:10]))
            print("\n")
