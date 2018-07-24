'''
Created on 24-Jul-2018

@author: TushaR
'''
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
        with open("id.txt") as f:
            file_str = f.read()
            
        file_int = int(file_str)
        file_int += 1
        self.accountNumber = self.accountType[0] + self.fname[0] + str(self.pincode) + self.lname[0] + str(file_int)
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
    
    
# c = Customer('Saving','Tushar','Kansal','Char Dukan Landour Cantt.','Mussoorie', 'Uttarakhand', '248179')
# c.generateAccountNumber()