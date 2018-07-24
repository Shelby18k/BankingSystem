print("\tWelcome to our bank of trust")
print('\t\tMain Menu')


def validate(accountType):
    pass

def SignUp():
    print('*'*6 + 'Welcome user' + '*'*6)
    accountType = input("Enter your Account Type(Saving/Current)")
    validate(accountType)


def SignIn():
    pass

def AdminSignIn():
    pass

options = {1 : SignUp,
           2: SignIn,
           3: AdminSignIn,
           4: 'Quit',
}

def selectOption():
    while True:
        choice  = int(input("Choice?"))
        a = options.get(choice,'Invalid Choice')
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