import re
from customers import Customer
from BankingSystem.customers import cur
from BankingSystem.customers import con

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

def check_user_identity(id,pwd):
    stmt = "select case when exists(select 1 from customers where customerid= :1 and password= :2) then 'Y' else 'N' end as rec_exists from dual"
    cur.execute(stmt,{'1':id,'2':pwd})
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
            
            
def address_change():
    print('Address')
    pass

def money_deposit():
    print('Deposit')
    pass

def money_withdrawal():
    print('Withdraw')
    pass

def print_statement():
    print('Print')
    pass

def transfer_money():
    print('Transfer')
    pass

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

def subMenu():
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
        opt()
        

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
    success = c.registerUser()
    if success == 1:
        print("*"*6 + "You are successfully registered with our bank, you must login now..!\n")
    


def SignIn():
    userid = -1
    totalAttempts = 0
    while totalAttempts < 3:
        customerid = input("Enter your customer id: ")
        password = input("Enter your password: ")
        userid = check_user_identity(customerid,password)
        if userid == 0:
            print("*"*6 + "Invalid UserID or password\n" + "*"*6)
        elif userid == 1:
            status = check_account_status(customerid,password)
            if status == 0:
                print("Your account has been blocked, contact admin")
                break
            elif status == 1:
                subMenu()
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
    
    opt = selectOption(options)
    if opt == 'Quit':
        print('*'*5 + 'Thanks for coming!' + '*'*5)
        quit = 4
    else:
        opt()