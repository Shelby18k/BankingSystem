import re
from customers import Customer
from customers import RegisteredCustomer
from BankingSystem.customers import cur
from BankingSystem.customers import con
from datetime import date,datetime,timedelta

accountType = {1: 'Saving',
               2: 'Current'}

print("\tWelcome to our bank of trust")
print('\t\tMain Menu')


def validatePin():
    while True:
        try:
            pin = input("Enter your pin code: ")
            if len(pin) == 6:
                pin = int(pin)
                return pin
            else:
                raise ValueError()
        except:
            print('*'*6 + 'Invalid Input' + '*'*6)

def check_user_identity(id,pwd,trigger):
    if trigger == 0:
        stmt = "select case when exists(select 1 from customers where customerid= :1 and password= :2) then 'Y' else 'N' end as rec_exists from dual"
        cur.execute(stmt,{'1':id,'2':pwd})
    elif trigger == 1:
        stmt = "select case when exists(select 1 from customers where customerid= :1) then 'Y' else 'N' end as rec_exists from dual"
        cur.execute(stmt,{'1':id})
    result = cur.fetchall()
    result = str(result[0][0])
    if result == 'N':
        return 0;
    elif result == 'Y':
        return 1;

def checkUserId(id):
    stmt = "select case when exists(select 1 from customers where customerid= :1) then 'Y' else 'N' end as rec_exists from dual"
    cur.execute(stmt,{'1':id})
    result = cur.fetchall()
    result = str(result[0][0])
    if result == 'N':
        return 0;
    elif result == 'Y':
        return 1;
    
def check_account_status(id,pwd):
    stmt = "select blocked from customers where customerid=:1 and password = :2"
    cur.execute(stmt,{'1':id,'2':pwd})
    res = cur.fetchall()
    if str(res[0][0]) == 'yes':
        return 0
    elif str(res[0][0]) == 'no':
        return 1
    
def validityCheck(inp=0):
    while True:
        if inp == 0:
            fname = input("Enter your first name: ")
        elif inp == 1:
            fname = input("Enter your last name: ")
        elif inp == 2:
            fname = input("Enter your city name: ")
        elif inp == 3:
            fname = input("Enter your State name: ")
        if re.match('^[a-zA-Z]+$', fname):
            return fname
        else: 
            print('*'*6+'Invalid input'+'*'*6)
            

def enterAmount():
    while True:
        try:
            amt = float(input("Enter amount: "))
            if amt > 0 and amt >= 5000.0:
                return amt
            else:
                raise ValueError()   
        except:
            print('*'*6+"Please enter a valid amount:"+'*'*6)


def create_customer(id,pwd):
    stmt = "SELECT accounttype,fname,lname,address,city,state,pincode FROM customers where customerid= :1 and password = :2"
    try:
        cur.execute(stmt,{'1':id,'2':pwd})
        res = cur.fetchall()
        accType = str(res[0][0])
        fname = str(res[0][1])
        lname = str(res[0][2])
        address = str(res[0][3])
        city = str(res[0][4])
        state = str(res[0][5])
        pin = int(res[0][6])
        c = RegisteredCustomer(accType,fname,lname,address,city,state,pin,id,pwd)
        return c
    except:
        print("An error occurred")
        return
            
            
def address_change(customer):
    customer.address_change()
    

def check_transaction_count(customer):
    stmt = "SELECT transcount,dt,renewaldate from transactioncount where accountid = :1"
    cur.execute(stmt,{'1':customer.accountNumber})
    res = cur.fetchall()
    count = int(res[0][0])
    d1 = res[0][1]
    d2 = res[0][2]
    d1 = datetime.strptime(str(d1)[0:10],'%Y-%m-%d')
    d2 = datetime.strptime(str(d2)[0:10],'%Y-%m-%d')
    today = date.today()
    today = datetime.strptime(str(today)[0:10],'%Y-%m-%d')
    rdate = date.today() + timedelta(days=30)
    rdate = rdate.strftime("%d-%m-%Y")
    
    if today > d2:
        stmt = """UPDATE transactioncount set transcount = :1,dt = to_date(:2,'dd-mm-yyyy'),
                renewaldate = to_date(:3,'dd-mm-yyyy') where accountid = :4"""
        cur.execute(stmt,{'4':customer.accountNumber,'2':today,'3':rdate,'1':0})
        con.commit()
        stmt = "SELECT transcount from transactioncount where accountid= :1"
        cur.execute(stmt,{'1':customer.accountNumber})
        res = cur.fetchall()
        count = int(res[0][0])
    if count > 9:
        print('*'*6 + "Sorry you have exhausted this month transaction limit")
        print("\tYou cannot deposit more, this month return next month")
        return 0

def money_deposit(customer):
    if customer.accountType == accountType.get(1):
        transaction_count = check_transaction_count(customer)
        if transaction_count == 0:
            return
        amt = customer.money_deposit()
        if amt:
            stmt = "UPDATE transactioncount set transcount = transcount+1 where accountid = :1"
            cur.execute(stmt,{'1':customer.accountNumber})
            con.commit()
            print("You have deposited: " + str(amt))
    elif customer.accountType == accountType.get(2):
        amt = customer.money_deposit()
        if amt:
            stmt = "UPDATE transactioncount set transcount = transcount+1 where accountid = :1"
            cur.execute(stmt,{'1':customer.accountNumber})
            con.commit()
            print("You have deposited: " + str(amt))
    

def money_withdrawal(customer):
    transaction_count = check_transaction_count(customer)
    if transaction_count == 0:
        return
    amount = customer.enter_amount()
    stmt = "SELECT balance from transactions where accountid = :1"
    cur.execute(stmt,{'1':customer.accountNumber})
    res = cur.fetchall()
    a = float(res[0][0])
    if a >= amount:
        withdrawalAmount = a - 5000
        if customer.accountType == accountType.get(2) and withdrawalAmount >= amount:
            amt = customer.money_withdrawal(amount)
            if amt:
                print("Successfully Withdrawal: " + str(amt))
        else:
            print('*'*6 + "No sufficient funds in your account, please deposit first\n")
            return 
        if customer.accountType == accountType.get(1):
            amt = customer.money_withdrawal(amount)
            if amt:
                print("Successfully Withdrawal: " + str(amt))
        if customer.accountType == accountType.get(1):
            stmt = "UPDATE transactioncount set transcount = transcount+1 where accountid = :1" 
            cur.execute(stmt,{'1':customer.accountNumber})
            con.commit()
    else:
        print('*'*6 + "No sufficient funds in your account, please deposit first\n")
        return
    

def print_statement():
    print('Print')
    pass

def transfer_money(customer):
    transaction_count = check_transaction_count(customer)
    if transaction_count == 0:
        return
    amount = customer.enter_amount()
    custAcct = input("Enter account no. of the person, you need to transfer: \n")
    exist = check_user_identity(custAcct,'HellNo',1)
    if exist == 0:
        print('*'*6 + "Such user doesn't exist, Please try again!")
        return
    elif exist == 1:
        checker = customer.check_available_balance(amount,custAcct)
        if checker == 1:
            print("\tMoney Transferred Successfully.")
        else:
            print("\tPlease Check your balance!")
    else:
        return
        

def account_closure():
    print('Close')
    pass
            

submenuOptions = {1: address_change,
                  2: money_deposit,
                  3: money_withdrawal,
                  4: print_statement,
                  5: transfer_money,
                  6: account_closure,
                  7: 'customer_logout'}

def subMenu(customer):
    while True:
        print("\t1. Address Change")
        print("\t2. Money Deposit")
        print("\t3. Money Withdrawal")
        print("\t4. Print Statement")
        print("\t5. Transfer Money")
        print("\t6. Account Closure")
        print("\t7. Customer Logout")
        opt = selectOption(submenuOptions)
        if opt == 'customer_logout':
            return
        else:
            opt(customer)
        

def SignUp():
    print('*'*6 + 'Welcome user' + '*'*6)
    print("Choose your account type")
    print("1. Saving")
    print("2. Current")
    accType = selectOption(accountType)  #To call for check in accountType dictionary
    fname = validityCheck(0)
    lname = validityCheck(1)
    address = input("Enter your address, Line 1: ")
    address += " "+ input("Line 2: ")
    city = validityCheck(inp=2)
    state = validityCheck(inp=3)
    pincode = validatePin()
    c = Customer(accType,fname,lname,address,city,state,pincode)
    c.enterPassword()
    acctNo = c.registerUser()
    if accType == 'Saving':
        rdate = date.today() + timedelta(days=30)
        rdate = rdate.strftime("%d-%m-%Y")
        stmt = "INSERT INTO transactioncount(accountid,renewaldate) values(:1,to_date(:2,'dd-mm-yyyy'))"
        cur.execute(stmt,{'1':acctNo,'2':rdate})
        stamt = "INSERT INTO transactions(accountid) values(:1)"
        cur.execute(stamt,{'1':acctNo})
        con.commit()
    elif accType == 'Current':
        print("You need to deposit min. amount of Rs. 5000")
        amt = enterAmount()
        stmt = "INSERT INTO transactions(accountid,balance) values(:1,:2)"
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/transactionid.txt") as f:
            file_str = f.read()
        file_int = int(file_str)
        
        cur.execute(stmt,{'1':acctNo,'2':amt})
        stamt = "INSERT INTO statementdetails(id,accountid,balance,transtype) values(:1,:2,:3,:4)"
        cur.execute(stamt,{'1':file_int,'2':acctNo,'3':amt,'4':'Credited'})
        con.commit()
        file_int += 1
        with open("C:/Users/TushaR/eclipse-workspace/BankingSystem/src/BankingSystem/transactionid.txt",'w') as f:
            f.write(str(file_int))
    if acctNo:
        print("*"*6 + "You are successfully registered with our bank, you must login now..!\n")
    else:
        print("*"*6 + "Error registering")


def SignIn():
    userid = -1
    totalAttempts = 0
    while totalAttempts < 3:
        customerid = input("Enter your customer id: ")
        password = input("Enter your password: ")
        userid = check_user_identity(customerid,password,0)
        if userid == 0:
            print("*"*6 + "Invalid UserID or password\n" + "*"*6)
        elif userid == 1:
            status = check_account_status(customerid,password)
            if status == 0:
                print("Your account has been blocked, contact admin")
                break
            elif status == 1:
                c = create_customer(customerid,password)
                subMenu(c)
                break
        if totalAttempts == 2:
            result = checkUserId(customerid)
            if result == 1:
                stmt = 'UPDATE customers SET blocked = :1 where customerid = :2'
                try:
                    cur.execute(stmt,{'1':'yes','2':customerid})
                    con.commit()
                    print("You have exceeded the number of login attempts")
                    print("*"*6 + " Account has been blocked " + "*"*6)
                    print("Contact Admin: ")
                except:
                    print("Some error occurred")   
        totalAttempts += 1
    

def AdminSignIn():
    pass

options = {1 : SignUp,
           2: SignIn,
           3: AdminSignIn,
           4: 'Quit',
}

def selectOption(opt):
    while True:
        choice  = int(input("Choice?"))
        a = opt.get(choice,'Invalid Choice')
        if a == 'Invalid Choice':
            print(a)
            continue
        else:
            return a
quit = 0
while quit != 4:
    print('1. Sign Up (New Customer)')
    print('2. Sign In (Existing Customer)')
    print('3. Admin Sign In')
    print('4. Quit')
    c = None
    opt = selectOption(options)
    if opt == 'Quit':
        print('*'*5 + 'Thanks for coming!' + '*'*5)
        quit = 4
    else:
        opt()