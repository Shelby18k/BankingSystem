import re
from customers import Customer
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
        

def SignUp():
    print('*'*6 + 'Welcome user' + '*'*6)
    print("Choose your account type")
    print("1. Saving")
    print("2. Current")
    accountType = selectOption(1)  #To call for check in accountType dictionary
    fname = validityCheck(0)
    lname = validityCheck(1)
    address = input("Enter your address, Line 1: ")
    address += " "+ input("Line 2: ")
    city = validityCheck(inp=2)
    state = validityCheck(inp=3)
    pincode = validatePin()
    c = Customer(accountType,fname,lname,address,city,state,pincode)
    print("Registered Successfully..!\n")
    


def SignIn():
    pass

def AdminSignIn():
    pass

options = {1 : SignUp,
           2: SignIn,
           3: AdminSignIn,
           4: 'Quit',
}

def selectOption(inp=0):
    while True:
        choice  = int(input("Choice?"))
        if inp == 0:
            a = options.get(choice,'Invalid Choice')
        elif inp == 1:
            a = accountType.get(choice,'Invalid Choice')
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
    
    opt = selectOption()
    if opt == 'Quit':
        print('*'*5 + 'Thanks for coming!' + '*'*5)
        quit = 4
    else:
        opt()